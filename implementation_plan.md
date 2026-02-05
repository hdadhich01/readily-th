# Healthcare Compliance RAG Backend Implementation Plan

## Goal

Build a FastAPI backend that serves as a RAG (Retrieval-Augmented Generation) system for healthcare policy compliance audits.
The system will ingest PDF policies, index them using SQLite FTS5, and provide endpoints to extract questions from audit PDFs and evaluate them against the indexed policies using Google's Gemini model.

## User Review Required

> [!NOTE]
> **Frontend Exclusion**: The original Perplexity plan included HTML templates in `main.py`. Per your request to "leave frontend alone" and use "bolt.new" later, this plan **excludes** all HTML/CSS serving. `main.py` will be a pure JSON REST API.

> [!IMPORTANT]
> **API Keys**: You will need to provide a `GEMINI_API_KEY` in a `.env` file in the `backend/` directory.

## Proposed Changes

### Backend Structure

The backend will be contained within `backend/`.

#### [MODIFY] [requirements.txt](file:///home/hdadhich/readily-TH/backend/requirements.txt)

- Add dependencies: `fastapi`, `uvicorn[standard]`, `python-multipart`, `pymupdf` (fitz), `google-generativeai`, `python-dotenv`.
- **Note**: Dependencies will not be pinned to specific versions to avoid conflicts/staleness, as requested.

### Backend Structure

#### [MODIFY] [main.py](file:///home/hdadhich/readily-TH/backend/main.py)

**Refactoring for Document-Level RAG:**

1.  **Database Setup (`init_db`)**:
    - **New Table**: `policies_fts` (Document-Level).
    - **Schema**: `(file_id, policy_number, title, summary, full_text)`.
    - _Note_: We will drop/replace the old `pages_fts` table.

2.  **Policy Ingestion (`index_policies_document_level`)**:
    - Scan `policies/` recursively.
    - For each PDF:
      - **Page-Aware Text Extraction**: Concatenate text with `--- Page {n} ---` delimiters.
      - **Metadata**: Extract Title, Summary, and **Total Pages**.
      - Insert into `policies_fts`.

3.  **LLM Router & Evaluation (`evaluate_single`)**:
    - **Step 1: Topic Extraction**: Identify search terms.
    - **Step 2: Document Routing**: Search `policies_fts`.
    - **Step 3: Long-Context Eval**:
      - **Prompt Update**:
        - Enforce strict "Evidence" formatting for YES/NO/UNCERTAIN.
        - For "NO": Require contradictory text OR "Not found" statement in code block.
        - Reduce Variance: Add "Chain of Thought" requirement (hidden) or stricter rules for "Uncertain".

4.  **API Endpoints**:
    - Retain existing endpoints but update logic to use the new pipeline.

### Directory Structure

- `backend/policies/`: Directory to place PDF files. (User needs to populate this).
- `backend/audit.db`: SQLite database (auto-generated).

## Verification Plan

### Automated Tests

We will use `curl` or a simple python script to test the endpoints.

1.  **Startup**: Run the server and ensure `audit.db` is created and populated (requires at least one PDF in `policies/`).
2.  **Health Check**: `curl http://localhost:8000/health` should return `{"status": "ok", "pages_indexed": N}`.
3.  **Extraction**: Upload a dummy PDF to `/extract_questions` and check JSON structure.
4.  **Evaluation**: Send a sample question to `/evaluate` and check if it finds evidence (requires a relevant PDF policy).

### Manual Verification

- User will need to drop their provided PDFs into `backend/policies/`.
- We will verify the FTS5 search manually by querying the DB if needed.

## Frontend Implementation (Added)

### [NEW] [templates/index.html](file:///home/hdadhich/readily-TH/backend/templates/index.html)

- Simple HTML5 page with Tailwind CDN (for basic styling).
- **Features**:
  - File input for PDF upload.
  - "Process" button to call `/upload_questionnaire`.
  - Dynamic table to show extracted questions.
  - "Evaluate All" button to call `/batch_evaluate`.
  - Status badges (Green/Red/Yellow) for compliance results.

### [MODIFY] [main.py](file:///home/hdadhich/readily-TH/backend/main.py)

- Import `HTMLResponse`.
- Add route `GET /` that reads and returns `templates/index.html`.
