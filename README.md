# RAG

A local Retrieval-Augmented Generation (RAG) question-answering API built with FastAPI, FAISS, and a Hugging Face extractive QA model — plus a standalone research notebook exploring a more advanced, multi-format, LLM-based version of the same idea.

## Overview

The core of this project is a small FastAPI service (`app/`) that answers questions against a local text knowledge base:

1. Documents are embedded and indexed with **FAISS**.
2. A question comes in via the `/ask` endpoint.
3. The top matching chunks are retrieved and fed to a local **extractive QA model** (`deepset/roberta-base-squad2`), which pulls the answer directly out of the retrieved text.
4. Requests are rate-limited with `slowapi`.

Alongside the app, `q-a-using-rag-genai.ipynb` is a separate, more elaborate RAG walkthrough (originally a Kaggle notebook) that ingests PDF/PPTX/DOCX files and uses a **generative** Cohere LLM instead of an extractive model. It's a prototype/reference, not wired into the API.

## Features

- **`POST /ask`** — question-answering endpoint backed by FAISS similarity search + a local extractive QA model.
- **Automatic indexing** — builds and persists a FAISS index from `data/my_docs.txt` on first run; reuses it on subsequent runs.
- **Rate limiting** — 5 requests/minute per client IP via `slowapi`.
- **API-key auth helper** (`app/auth.py`) and **Redis caching helper** (`app/cache.py`) are implemented but **not currently wired into `/ask`** — see [Known Issues](#known-issues--todo).
- **Research notebook** — a separate, generative-LLM RAG pipeline (Cohere) over PDF/PPTX/DOCX inputs, for comparison/experimentation.

## Project Structure

```
RAG/
├── README.md
├── requirements.txt
├── q-a-using-rag-genai.ipynb     # standalone Cohere-based RAG notebook (not used by the API)
├── app/
│   ├── __init__.py               # legacy/incomplete QAPipeline — see Known Issues
│   ├── main.py                   # FastAPI app, rate limiting, /ask endpoint
│   ├── qa_pipeline.py            # the QAPipeline actually used by the API
│   ├── auth.py                   # API-key check helper (not yet wired in)
│   ├── cache.py                  # Redis caching helper (not yet wired in)
│   └── config.py                 # loads API_KEY from .env
├── data/
│   ├── my_docs.txt               # sample knowledge base (~6 short unrelated paragraphs)
│   └── faiss_index/              # persisted FAISS index (pre-built)
│       ├── index.faiss
│       └── index.pkl
└── graphify-out/                 # codebase graph/visualization output from the `graphify` tool
```

## How It Works

**Indexing** (`QAPipeline.__init__` in `app/qa_pipeline.py`):
- If `data/faiss_index/` already exists, it's loaded directly.
- Otherwise, `data/my_docs.txt` is loaded via `TextLoader`, embedded with a local `sentence-transformers/all-MiniLM-L6-v2` model, indexed with FAISS, and the index is saved to `data/faiss_index/` for reuse.

**Answering** (`QAPipeline.get_answer`):
- Retrieves the top 3 most similar chunks from the FAISS index.
- Concatenates them into a single context string.
- Runs a local Hugging Face extractive QA pipeline (`deepset/roberta-base-squad2`) with `{question, context}`.
- Returns the extracted answer span, or a fallback string if nothing relevant is found.

Note this is **extractive**, not generative — the answer is always a literal span pulled from the source text, unlike the Cohere-based notebook, which generates a free-form answer from a prompt.

## Getting Started

### Prerequisites
- Python 3.9+
- (Optional, currently unused by the API) Redis, if you wire in `app/cache.py`

### Installation
```bash
git clone <repo-url>
cd RAG
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
> `app/qa_pipeline.py` imports `transformers` directly, but it isn't listed in `requirements.txt` — it currently installs transitively via `sentence-transformers`. Consider pinning it explicitly.

### Configuration
Create a `.env` file in the project root:
```
API_KEY=choose-a-real-secret-here
```
`app/config.py` falls back to a hardcoded default (`"secret123"`) if `API_KEY` isn't set — don't rely on that default outside local dev, and note that no endpoint currently enforces this key anyway (see below).

### Running the API
```bash
uvicorn app.main:app --reload
```
The first request will build the FAISS index if it doesn't already exist (this can take a moment); subsequent runs reuse `data/faiss_index/`.

## API Reference

### `POST /ask`
Rate limited to **5 requests/minute per client IP**.

`question` is passed as a **query parameter** (not a JSON body), since it's declared as a plain `str` in the route:

```bash
curl -X POST "http://localhost:8000/ask?question=What%20is%20machine%20learning%3F"
```

Response:
```json
{ "answer": "a subset of AI that involves training algorithms on data..." }
```

If the rate limit is exceeded (HTTP 429):
```json
{ "detail": "Rate limit exceeded" }
```

## Security Notes

- **`q-a-using-rag-genai.ipynb` contains hardcoded API keys** (Hugging Face Hub, Google, Cohere) directly in the source. If this notebook has ever been committed to a shared or public repo, **rotate/revoke those keys now** and load them from `.env` instead, the same way `app/config.py` already does for `API_KEY`.
- `app/config.py`'s fallback default `API_KEY = "secret123"` should not be relied on outside local development.

## Known Issues / TODO

- **Duplicate `QAPipeline` classes**: `app/__init__.py` defines a second, incomplete `QAPipeline` (references `self.embeddings`, `FAISS`, `TextLoader` without importing them) alongside the working implementation in `app/qa_pipeline.py`, which is what `main.py` actually imports. The one in `__init__.py` looks like leftover/dead code and is worth removing or consolidating.
- **Auth isn't enforced**: `app/auth.py`'s `check_auth()` is never called from `app/main.py` — `/ask` currently has no API-key requirement despite the auth module existing.
- **Caching isn't wired in**: `app/cache.py`'s Redis helpers are never called from `app/main.py` — repeated identical questions currently always re-run retrieval + QA inference.
- **`openai` in `requirements.txt` is unused**: nothing in `app/` imports it; the pipeline is fully local (HuggingFace embeddings + HuggingFace extractive QA). Either drop the dependency or this is a planned code path.
- **Sample data**: `data/my_docs.txt` is ~6 short, unrelated paragraphs (AI, Python, climate change, the Great Wall of China, machine learning, EVs) — fine for testing, but should be replaced with real content before this is used for anything real.

## Testing
No test suite is currently present. Suggested next step:
```bash
pip install pytest
pytest
```

## License
open - source for now.
Author: Vaibhav Kumar Singh
IIT Bombay
24b2725@iitb.ac.in
