# Readily Take-Home: Compliance Audit System

## 1. Goal

Build a robust RAG (Retrieval-Augmented Generation) system for healthcare policy compliance audits. The system ingests PDF policies, extracts requirements from questionnaires, and uses advanced LLM reasoning to determine compliance with precise evidence.

## 2. System Architecture

### A. Technology Stack

- **Backend**: FastAPI (Python), Uvicorn
- **Database**: SQLite with **FTS5 extension** (Full-Text Search)
- **LLM Provider**: **Google Gemini (GenAI SDK)**
- **Frontend**: HTML5 + Tailwind CSS (Vanilla JS)
- **PDF Processing**: PyMuPDF (`fitz`)

### B. Core Components

#### 1. Gemini Model Strategy

To balance performance and reasoning depth, the system uses two distinct model configurations:

- **`gemini-2.0-flash`**: Used for **Fast Tasks**.
  - _Use Case_: Metadata extraction, Search term generation (Routing), and Questionnaire parsing.
  - _Benefit_: Low latency and high throughput.
- **`gemini-3-flash-preview`**: Used for **Deep Reasoning**.
  - _Configuration_: `thinking_config: { thinking_level: "high" }`
  - _Use Case_: Compliance evaluation. This model "thinks" before answering, effectively simulating an auditor's chain of thought to reduce hallucinations and improve precision.

#### 2. RAG Pipeline (`evaluate_single`)

The evaluation flow matches "Document-Level" retrieval concepts:

1.  **Topic Extraction**: The question is sent to `gemini-2.0-flash` to generate 3 specific search keywords (e.g., "Hospice Election Form").
2.  **Document Retrieval**: We query the `policies_fts` table using FTS5 to find the top 2 most relevant _full documents_.
3.  **Context Assembly**: Full text of relevant policies (with page markers) is injected into the context window.
4.  **Reasoning**: `gemini-3-flash-preview` evaluates the requirement against the policies. It is instructed to be **Strict** (Evidence Required) and categorize as **YES**, **NO**, or **UNCERTAIN**.

#### 3. Data Ingestion

- **Folder Scanning**: Recursively reads all `.pdf` files in the `policies/` directory.
- **Page-Aware Extraction**: Text is extracted with `--- Page X ---` delimiters to enable page-level citations.
- **Indexing**: Metadata (Title, Summary, Total Pages) is extracted via LLM and stored in SQLite `policies_fts`.

## 3. Directory Structure

```
/
├── main.py              # Single-file FastAPI application
├── requirements.txt     # Python dependencies
├── audit.db             # Generated SQLite database (FTS5)
├── policies/            # [Input] Folder for Policy PDFs
└── templates/
    └── index.html       # Frontend UI
```

## 4. Frontend Features

- **Clean UI**: Tailwind CSS based interface.
- **Questionnaire Upload**: Parses unstructured PDF questionnaires into a structured table of requirements.
- **Batch Processing**: Evaluates requirements in parallel (browser-managed concurrency).
- **Results Validation**:
  - **Green/Red/Yellow badges** for Met/Not Met/Uncertain.
  - **Citations**: Lists Policy Name and **Page Number**.
  - **Evidence**: Displays the verbatim excerpt or a gap statement.

## 5. Deployment Notes

- **Port Binding**: The app binds to `os.environ.get("PORT")` to support cloud platforms like Render/Heroku.
- **Dependencies**: Uses `google-genai` (New SDK). `google-generativeai` is excluded to avoid namespace conflicts.
