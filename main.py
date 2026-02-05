import asyncio
import glob
import json
import os
import re
import sqlite3
from contextlib import asynccontextmanager
from typing import Dict, List, Optional

import dotenv
import fitz  # PyMuPDF
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse

# New Google GenAI SDK
# We transitioned to this SDK to support 'thinking_config' for Gemini 3
from google import genai
from google.genai import types
from pydantic import BaseModel

dotenv.load_dotenv()

DB_PATH = "audit.db"
POLICIES_DIR = "policies"

# Initialize Global Client
# This client handles all interactions with the Gemini API
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes the SQLite database with FTS5 support."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Enable FTS5 Extension (Full Text Search)
    try:
        cursor.execute("SELECT load_extension('fts5');")
    except:
        pass

    # Schema Migration: Check if 'total_pages' column exists
    # If not, drop and recreate the table (simple migration strategy)
    try:
        cursor.execute("SELECT total_pages FROM policies_fts LIMIT 1")
    except sqlite3.OperationalError:
        print("Migrating DB: Dropping old policies_fts table...")
        cursor.execute("DROP TABLE IF EXISTS policies_fts")
        conn.commit()

    # Create the virtual table for policy searching
    # We use FTS5 for efficient text matching on title, summary, and full_text
    cursor.execute(
        """
    CREATE VIRTUAL TABLE IF NOT EXISTS policies_fts USING fts5(
        file_id UNINDEXED,
        policy_number,
        title,
        summary,
        total_pages UNINDEXED,
        full_text,
        tokenize='porter'
    );
    """
    )
    conn.commit()
    conn.close()


async def extract_metadata(text_chunk: str, filename: str) -> Dict:
    """
    Uses Gemini (Fast Model) to extract a clean Title and Summary from the policy header.
    We use the fast model here because this is a simple extraction task.
    """
    prompt = f"""
    Analyze the following text (first few pages of a policy document).
    Extract the official POLICY TITLE and a 1-sentence SUMMARY.

    Filename: {filename}
    Text: {text_chunk[:5000]}

    Return strictly JSON: {{"title": "...", "summary": "..."}}
    """

    retries = 0
    max_retries = 5
    base_delay = 2

    while retries < max_retries:
        try:
            # FAST MODEL: gemini-2.0-flash
            # Efficient for metadata extraction
            response = await client.aio.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                ),
            )
            data = json.loads(response.text)
            if isinstance(data, list):
                if len(data) > 0:
                    return data[0]
                else:
                    return {
                        "title": filename,
                        "summary": "Empty metadata list returned.",
                    }
            return data
        except Exception as e:
            if "429" in str(e) or "Resource exhausted" in str(e):
                wait = base_delay * (2**retries)
                print(f"Rate limit hit for {filename}. Retrying in {wait}s...")
                await asyncio.sleep(wait)
                retries += 1
            else:
                print(f"Metadata extraction failed for {filename}: {e}")
                return {"title": filename, "summary": "Metadata extraction failed."}

    return {"title": filename, "summary": "Rate limit exceeded."}


async def process_pdf(
    pdf_path: str, sem: asyncio.Semaphore, cursor_queue: asyncio.Queue
):
    """
    Reads PDF, extracts metadata, and prepares data for DB insertion.
    Uses a semaphore to limit concurrent processing.
    """
    async with sem:
        try:
            doc = fitz.open(pdf_path)
            full_text = ""
            # Extract full text with explicit Page Markers
            # This allows the LLM to cite specific pages later (e.g., "Page 3")
            for i, page in enumerate(doc):
                page_text = page.get_text()
                full_text += f"\n--- Page {i+1} ---\n{page_text}"

            if not full_text.strip():
                print(
                    f"Skipping {filename}: No text extracted. (Is this a scanned image?)"
                )
                return

            # Heuristic for Policy ID (e.g., "GA.7110" from "GA.7110 Street Medicine.pdf")
            filename = os.path.basename(pdf_path)
            policy_number = filename.split(" ")[0].strip()

            # Extract Metadata (Title/Summary) using first few pages
            # We use the LLM for this to get high quality data for identifying documents
            metadata = await extract_metadata(full_text[:5000], filename)
            total_pages = len(doc)

            # Put result in queue for the main thread to write
            # (SQLite writes must be serialized, hence the queue)
            await cursor_queue.put(
                (
                    filename,
                    policy_number,
                    metadata.get("title", filename),
                    metadata.get("summary", ""),
                    total_pages,
                    full_text,
                )
            )

            print(f"Processed: {filename} -> {metadata.get('title')}")

        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")


async def db_writer(queue: asyncio.Queue, total_files: int):
    """Background task that consumes processed PDFs from queue and writes to SQLite."""
    conn = get_db_connection()
    cursor = conn.cursor()
    processed_count = 0

    while processed_count < total_files:
        item = await queue.get()
        cursor.execute(
            "INSERT INTO policies_fts (file_id, policy_number, title, summary, total_pages, full_text) VALUES (?, ?, ?, ?, ?, ?)",
            item,
        )
        conn.commit()
        processed_count += 1
        if processed_count % 10 == 0:
            print(f"Committed {processed_count}/{total_files} policies.")

    conn.close()


async def index_policies():
    """Main ingestion function. Scans directory and starts processing."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if DB is already populated to avoid re-indexing on every restart
    try:
        cursor.execute("SELECT count(*) FROM policies_fts")
        if cursor.fetchone()[0] > 0:
            print("DB already populated. Skipping ingestion.")
            conn.close()
            return
    except:
        pass

    print("Starting Document-Level Ingestion...")
    pdf_files = glob.glob(os.path.join(POLICIES_DIR, "**", "*.pdf"), recursive=True)
    if not pdf_files:
        print("No PDFs found in policies directory.")
        conn.close()
        return

    print(f"Found {len(pdf_files)} PDFs.")

    # Limit concurrency to avoid overloading system/API
    sem = asyncio.Semaphore(20)
    queue = asyncio.Queue()

    writer_task = asyncio.create_task(db_writer(queue, len(pdf_files)))
    await asyncio.gather(*[process_pdf(f, sem, queue) for f in pdf_files])
    await writer_task
    print("Ingestion Complete.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager: Runs ingestion on startup."""
    init_db()
    # Run ingestion content in background/startup
    await index_policies()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health_check():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT count(*) FROM policies_fts")
        count = cursor.fetchone()[0]
    except:
        count = 0
    conn.close()
    return {"status": "ok", "policies_indexed": count}


@app.get("/", response_class=HTMLResponse)
async def read_root():
    if os.path.exists("templates/index.html"):
        with open("templates/index.html", "r") as f:
            return f.read()
    return "<h1>Readily-TH Backend Running</h1>"


class EvaluationRequest(BaseModel):
    question: str
    section: Optional[str] = None


class BatchEvaluationRequest(BaseModel):
    questions: List[EvaluationRequest]


async def evaluate_single(req: EvaluationRequest) -> Dict:
    """
    Core RAG Function:
    1. Identify search terms (Routing)
    2. Retrieve documents (FTS)
    3. Evaluate compliance (Thinking Model)
    """

    # ---------------------------------------------------------
    # STEP 1: Identify Topic (Routing) - FAST MODEL
    # ---------------------------------------------------------
    topic_prompt = f"""
    Based on this audit question, what are the specific 3 search terms I should use to find the relevant policy document?
    Focus on specific policy NAMES (e.g. "Hospice", "Claims Payment", "Grievances") and UNIQUE IDS if implied.

    Question: {req.question}

    Return strictly JSON: ["Term 1", "Term 2", "Term 3"]
    """

    try:
        # We use Gemini 2.0 Flash for this simple reasoning task to save latency
        topic_res = await client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents=topic_prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )
        search_terms = json.loads(topic_res.text)
        print(f"Router Terms: {search_terms}")
    except Exception as e:
        print(f"Router Error: {e}")
        search_terms = [req.question]

    # ---------------------------------------------------------
    # STEP 2: Route to Documents (FTS Retrieval)
    # ---------------------------------------------------------
    conn = get_db_connection()
    cursor = conn.cursor()
    matched_policies = []

    for term in search_terms:
        # Sanitize term for FTS: remove non-alphanumeric chars (except spaces)
        safe_term = re.sub(r"[^a-zA-Z0-9 ]", "", term)
        try:
            # Matches against title, summary, policy_number, and full_text
            cursor.execute(
                """
                SELECT file_id, policy_number, title, total_pages, full_text
                FROM policies_fts
                WHERE policies_fts MATCH ?
                ORDER BY rank
                LIMIT 2
            """,
                (safe_term,),
            )
            matched_policies.extend([dict(row) for row in cursor.fetchall()])
        except Exception as e:
            print(f"Search Error for '{term}': {e}")

    conn.close()

    # Deduplicate results found by multiple terms
    unique_policies = {}
    for p in matched_policies:
        unique_policies[p["file_id"]] = p

    # If no documents found, return early to avoid hallucination
    if not unique_policies:
        return {
            "question": req.question,
            "met": "uncertain",
            "evidence": {
                "chunk": "No relevant policy documents found.",
                "doc": "N/A",
                "page": 0,
                "reason": "No policies matched the search topics.",
            },
        }

    # ---------------------------------------------------------
    # STEP 3: Long Context Evaluation - COMPLIANCE MODEL (Reasoning)
    # ---------------------------------------------------------
    context_text = ""
    for p in list(unique_policies.values())[:2]:
        t_pages = p.get("total_pages")
        if t_pages is None:
            t_pages = "?"
        context_text += f"\n\n=== POLICY: {p['policy_number']} - {p['title']} (File: {p['file_id']}, Total Pages: {t_pages}) ===\n{p['full_text']}"

    eval_prompt = f"""
    You are a STRICT healthcare compliance auditor.

    REQUIREMENT: "{req.question}"
    SECTION: {req.section}

    CONTEXT:
    {context_text}

    TASK:
    Determine if the Requirement is MET (YES), NOT MET (NO), or UNCERTAIN.

    GUIDELINES:
    1. **Decisiveness**:
       - YES: Found explicit evidence.
       - NO: Silent or contradictory.
       - UNCERTAIN: Missing referenced appendix only.

    2. **Evidence**:
       - **YES**: Provide VERBATIM quotes.
       - **NO**: Provide a "Gap Statement" explaining what is missing.

    OUTPUT JSON:
    {{
        "met": "YES" | "NO" | "UNCERTAIN",
        "evidence": {{
            "sources": [
                {{
                    "doc": "Policy Title / Filename",
                    "page": "Page #",
                    "total_pages": "Total Pages from header",
                    "doc_title": "Just the Title (no filename)"
                }}
            ],
            "excerpt": "Verbatim Quote (YES) or Gap Statement (NO)",
            "reason": "Detailed explanation."
        }}
    }}
    - If UNCERTAIN: Explain in 'reason'.
    """

    # Retry logic for Rate Limits (429)
    retries = 0
    max_retries = 3
    base_delay = 5

    while retries <= max_retries:
        try:
            # COMPLIANCE MODEL: gemini-3-flash-preview
            # CONFIG: "Thinking High" ->  Models detailed thought process before answering.
            # This is crucial for complex compliance logic.
            response = await client.aio.models.generate_content(
                model="gemini-3-flash-preview",
                contents=eval_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    thinking_config=types.ThinkingConfig(thinking_level="high"),
                ),
            )
            result = json.loads(response.text)

            if isinstance(result, list):
                if len(result) > 0:
                    result = result[0]
                else:
                    return {
                        "met": "uncertain",
                        "evidence": {"reason": "LLM returned empty list"},
                        "question": req.question,
                    }

            result["question"] = req.question
            return result

        except Exception as e:
            if "429" in str(e) or "Resource exhausted" in str(e):
                if retries == max_retries:
                    print(f"Eval Failed after retries: {e}")
                    return {
                        "question": req.question,
                        "met": "uncertain",
                        "evidence": {
                            "reason": "Rate limit exceeded. Try batch evaluation with fewer items."
                        },
                    }
                wait = base_delay * (2**retries)
                print(f"Rate limit hit for evaluation. Retrying in {wait}s...")
                await asyncio.sleep(wait)
                retries += 1
            else:
                print(f"Eval Error: {e}")
                return {
                    "question": req.question,
                    "met": "uncertain",
                    "evidence": {"reason": f"LLM Error: {e}"},
                }


@app.post("/upload_questionnaire")
async def upload_questionnaire(file: UploadFile = File(...)):
    """
    Endpoint to process an uploaded PDF questionnaire.
    Extracts questions using Gemini 2.0 Flash (Fast).
    """
    # Save temp file
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        # Extract text from PDF
        text = ""
        doc = fitz.open(temp_path)
        for page in doc:
            text += page.get_text()
        doc.close()

        # Extract questions via Gemini
        prompt = f"""
        Extract all audit requirements/questions from the text below.
        Return strictly a JSON array of objects: [{{"section": "...", "question": "..."}}]

        RULES:
        - Exclude headers like "Review Findings", "Criteria", "Metric" from the question text.
        - Text should be the actual requirement question only.

        TEXT:
        {text}
        """

        # FAST MODEL: gemini-2.0-flash
        # We use the fast model here because extraction is a simple pattern matching task.
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )
        questions = json.loads(response.text)
        return questions

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


@app.post("/process_question")
async def process_question_endpoint(req: EvaluationRequest):
    return await evaluate_single(req)


@app.post("/evaluate")
async def evaluate_endpoint(req: EvaluationRequest):
    return await evaluate_single(req)


@app.post("/batch_evaluate")
async def batch_evaluate_endpoint(req: BatchEvaluationRequest):
    sem = asyncio.Semaphore(10)

    async def bound_evaluate(q):
        async with sem:
            return await evaluate_single(q)

    results = await asyncio.gather(*[bound_evaluate(q) for q in req.questions])
    return results


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
