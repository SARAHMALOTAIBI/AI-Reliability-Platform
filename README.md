# AI Reliability Platform

AI Reliability Platform evaluates RAG applications, diagnoses likely failure causes, tracks reliability over time, and independently verifies generated answers against company knowledge-base documents.

## Current capabilities

- FastAPI health-check API
- RAG evaluation metrics: correctness, faithfulness, context precision, context recall, answer relevancy, and hallucination risk
- Numeric contradiction detection
- Deterministic root-cause diagnosis
- Overall reliability health score
- Recommendation engine
- PostgreSQL persistence and Health Check History API
- Company Knowledge Base with PDF extraction, chunking, multilingual embeddings, and persistent Chroma storage
- Independent answer verification using Question + RAG Answer + RAG Context against company evidence
- Streamlit dashboard with English and Arabic interfaces

## Root-cause logic with company evidence

When indexed company documents are available, independent evidence is used before proxy-only rules:

- Company evidence is missing -> `KNOWLEDGE_BASE_FAILURE`
- Company evidence exists but RAG context missed it -> `RETRIEVAL_FAILURE`
- RAG context contains the evidence but the generated answer conflicts with it -> `GENERATION_FAILURE`

If no company Knowledge Base is available, the existing evaluation-based rules continue to work normally.

## Local setup

Requirements:

- Python 3.12+
- PostgreSQL
- `uv`

Install dependencies:

```powershell
uv sync
```

Create `.env` from `.env.example` and set your PostgreSQL password. Never commit the real `.env` file.

Apply database migrations:

```powershell
uv run alembic upgrade head
```

Start FastAPI:

```powershell
uv run python -m uvicorn app.main:app --host 127.0.0.1 --port 8002
```

Swagger UI is available at `http://127.0.0.1:8002/docs`.

Start Streamlit in another terminal:

```powershell
uv run streamlit run dashboard/app.py --server.port 8501
```

Dashboard: `http://localhost:8501`

## Main API endpoints

- `GET /health`
- `POST /api/v1/health-checks`
- `GET /api/v1/health-checks`
- `GET /api/v1/health-checks/{health_check_id}`
- `POST /api/v1/knowledge-base/upload`
- `POST /api/v1/knowledge-base/verify`

The Knowledge Base verification endpoint requires the generated RAG answer. An optional retrieved RAG context can also be supplied to help distinguish retrieval failures from generation failures.

## Storage

- PostgreSQL: health checks, evaluation metrics, diagnoses, recommendations, indexed-document metadata, and Knowledge Base verification results
- Chroma: document chunk vectors under `./chroma_db` by default

Both `.env` and `chroma_db/` are excluded from Git.

## Tests

```powershell
uv run pytest -q
uv run alembic check
```

## Notes

The semantic scores are reliability proxies rather than logical-entailment probabilities. Numeric duration contradictions are checked explicitly. Thresholds should be calibrated on representative production data before using them as enforcement criteria.
