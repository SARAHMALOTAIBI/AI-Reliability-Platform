# AI Reliability Platform — System Architecture

## 1. Project Overview

AI Reliability Platform is a self-hosted platform designed to evaluate, monitor, diagnose, and improve AI applications built using Large Language Models, Retrieval-Augmented Generation, and AI Agents.

The platform receives execution data from an external AI application, evaluates the quality and reliability of its output, identifies the likely cause of failures, and generates an AI Health Report containing metrics, diagnoses, and recommended improvements.

The first version focuses on LLM and RAG applications. The architecture should remain extensible to support AI Agents and traditional machine learning models in future versions.

---

## 2. Primary Users

### AI Engineer

Uses the platform to evaluate answers, inspect RAG performance, detect hallucinations, and improve prompts and retrieval settings.

### ML Engineer

Uses the platform to compare models, prompts, retrievers, and application versions.

### Data Scientist

Uses the platform to analyze evaluation results, error distributions, trends, and drift.

### Engineering Manager

Uses the dashboard to monitor overall system health, critical issues, quality trends, latency, and cost.

---

## 3. Deployment Model

The first version will be self-hosted.

The platform will run using Docker Compose and will include:

* Backend API
* Background worker
* PostgreSQL database
* Redis
* Evaluation engine
* Monitoring components
* Dashboard

A future version may support a multi-tenant SaaS deployment.

---

## 4. Supported Integration Methods

### REST API

External AI applications send evaluation records using an HTTP API.

Example endpoint:

```text
POST /api/v1/health-checks
```

### Python SDK

A future Python package will allow developers to send traces and evaluation records directly from their applications.

Example:

```python
from ai_reliability import ReliabilityClient

client = ReliabilityClient(api_key="...")

client.health_check(
    question="What is the refund period?",
    answer="The refund period is 14 days.",
    contexts=["Customers may request refunds within 14 days."],
)
```

### File Upload

Users may upload JSON, JSONL, CSV, or Parquet files containing evaluation records through the dashboard.

---

## 5. Core Domain Objects

### Organization

Represents the company or team using the platform.

### Project

Represents one AI application being monitored.

Examples:

* Customer Support Assistant
* Internal Policy RAG
* SQL Agent
* Medical Knowledge Assistant

### Application Version

Represents a specific configuration of the AI application.

It may include:

* Model name
* Prompt version
* Embedding model
* Retriever configuration
* Chunking configuration
* Top-K
* Temperature

### AI Health Check

Represents one evaluation request.

It contains:

* User question
* Generated answer
* Retrieved contexts
* Reference answer if available
* Prompt
* Model configuration
* Retrieval configuration
* Latency
* Token usage
* Cost
* Metadata

### Evaluation Metric

Represents one calculated reliability score.

Examples:

* Faithfulness
* Answer Relevancy
* Context Precision
* Context Recall
* Answer Correctness
* Hallucination Risk
* Prompt Quality
* Latency Score

### Diagnosis

Represents the root cause identified by the platform.

Examples:

* Retrieval failure
* Generation hallucination
* Weak grounding prompt
* Missing knowledge
* Model reasoning failure
* System latency issue

### Recommendation

Represents an improvement suggested by the system.

Examples:

* Reduce model temperature
* Increase retrieval Top-K
* Use a reranker
* Improve chunking
* Update missing documents
* Strengthen grounding instructions

### AI Health Report

Represents the final output produced for an AI Health Check.

It contains:

* Overall health score
* Status
* Metric scores
* Failure category
* Root cause
* Severity
* Recommendations
* Supporting evidence

---

## 6. High-Level Architecture

```text
External AI Application
          |
          | HTTP / SDK / File Upload
          v
+--------------------------+
|       API Gateway        |
| Authentication           |
| Validation               |
| Rate Limiting            |
+------------+-------------+
             |
             v
+--------------------------+
| Health Check Service     |
| Creates evaluation job   |
| Stores request metadata  |
+------------+-------------+
             |
             v
+--------------------------+
|       Job Queue          |
|         Redis            |
+------------+-------------+
             |
             v
+--------------------------+
| Evaluation Worker        |
| Runs evaluation pipeline |
+------------+-------------+
             |
             v
+--------------------------------------------------+
|               Evaluation Engine                  |
|                                                  |
| Retrieval Evaluator                              |
| Generation Evaluator                             |
| RAG Evaluator                                    |
| Prompt Evaluator                                 |
| Safety Evaluator                                 |
| Performance Evaluator                            |
+---------------------+----------------------------+
                      |
                      v
+--------------------------+
| Root Cause Engine        |
| Rules                    |
| Statistical analysis     |
| LLM diagnosis agent      |
+------------+-------------+
             |
             v
+--------------------------+
| Recommendation Engine    |
| Rule-based actions       |
| LLM explanation          |
+------------+-------------+
             |
             v
+--------------------------+
| AI Health Report Service |
+------------+-------------+
             |
             v
+--------------------------+
| PostgreSQL               |
| Evaluations              |
| Metrics                  |
| Diagnoses                |
| Recommendations          |
| Configurations           |
+------------+-------------+
             |
             v
+--------------------------+
| Dashboard                |
| Monitoring               |
| Trends                   |
| Comparisons              |
| Reports                  |
+--------------------------+
```

---

## 7. Main Platform Modules

### API Service

Responsibilities:

* Accept incoming requests
* Validate request schemas
* Authenticate clients
* Create health-check jobs
* Return job status and results
* Support batch evaluation
* Support file uploads

Recommended technology:

* FastAPI
* Pydantic
* SQLAlchemy
* Alembic

---

### Health Check Service

Responsibilities:

* Create AI Health Check records
* Associate checks with projects and versions
* Store configuration and metadata
* Submit evaluation jobs
* Track execution status

Possible statuses:

```text
PENDING
RUNNING
COMPLETED
FAILED
CANCELLED
```

---

### Evaluation Worker

Responsibilities:

* Read jobs from Redis
* Execute evaluation pipelines
* Retry failed evaluations
* Store metrics and logs
* Generate traces

Recommended technology:

* Celery or Dramatiq
* Redis

---

### Evaluation Engine

The Evaluation Engine is the main technical component of the platform.

It should support independent evaluator plugins.

Each evaluator receives a normalized evaluation sample and returns one or more metric results.

Example interface:

```python
class BaseEvaluator:
    name: str

    async def evaluate(self, sample):
        raise NotImplementedError
```

Evaluator categories:

#### Retrieval Evaluation

* Context relevance
* Context precision
* Context recall
* Retrieval rank quality
* Duplicate context detection
* Missing context detection

#### Generation Evaluation

* Faithfulness
* Answer relevancy
* Answer correctness
* Completeness
* Contradiction detection
* Hallucination risk

#### Prompt Evaluation

* Instruction clarity
* Grounding strength
* Conflicting instructions
* Output-format compliance
* Prompt injection risk

#### Safety Evaluation

* Toxicity
* Sensitive data exposure
* Harmful content
* Prompt injection
* Policy violations

#### Performance Evaluation

* Latency
* Token usage
* Cost
* Timeouts
* Error rate

---

## 8. Root Cause Analysis Engine

The Root Cause Engine identifies why an AI application failed.

It uses three layers.

### Layer 1: Deterministic Rules

Examples:

```text
Context precision low
→ Retrieval quality issue
```

```text
Context precision high
+
Faithfulness low
→ Generation hallucination
```

```text
Context recall low
+
Reference answer contains missing information
→ Knowledge-base gap
```

```text
Answer relevancy low
+
Retrieval metrics good
→ Prompt or generation issue
```

### Layer 2: Statistical Analysis

Used to detect patterns across multiple health checks.

Examples:

* Quality decline after a prompt version change
* Increased hallucination after changing the model
* Increased latency after increasing Top-K
* Retrieval quality decline in one category

### Layer 3: Diagnosis Agent

An LLM-based agent receives:

* Input question
* Generated answer
* Retrieved contexts
* Metric scores
* Application configuration
* Relevant historical results
* Deterministic diagnosis

The agent explains the issue and ranks the probable causes.

The agent must not replace deterministic metrics. It only interprets and explains their results.

---

## 9. Recommendation Engine

The Recommendation Engine maps diagnoses to practical actions.

Examples:

### Retrieval Failure

Possible actions:

* Change embedding model
* Increase or decrease Top-K
* Add a reranker
* Change chunk size
* Increase chunk overlap
* Remove duplicate chunks
* Rebuild the vector index

### Generation Hallucination

Possible actions:

* Reduce temperature
* Strengthen grounding instructions
* Require citations
* Add an abstention policy
* Use a stronger model
* Add structured output constraints

### Prompt Failure

Possible actions:

* Remove conflicting instructions
* Add examples
* Define a strict response format
* Clarify the task
* Separate system and user instructions

### Knowledge-Base Failure

Possible actions:

* Add missing documents
* Replace outdated documents
* improve metadata
* Re-index documents
* Add document freshness checks

Recommendations should include:

* Priority
* Expected impact
* Difficulty
* Affected component
* Supporting evidence

---

## 10. Overall Health Score

The platform generates a score from 0 to 100.

Initial weighting:

```text
Faithfulness:       25%
Answer Relevancy:   15%
Answer Correctness: 20%
Context Precision:  15%
Context Recall:     10%
Prompt Quality:      5%
Performance:         5%
Safety:              5%
```

Example:

```text
Overall Health Score = 86
Status = GOOD
```

Possible statuses:

```text
90–100  EXCELLENT
80–89   GOOD
65–79   WARNING
40–64   POOR
0–39    CRITICAL
```

Weights should be configurable for each project.

---

## 11. Data Flow

### Step 1

An external application sends a health-check request.

### Step 2

The API validates the payload.

### Step 3

The Health Check Service stores the request and creates a job.

### Step 4

The worker reads the job from Redis.

### Step 5

The Evaluation Engine runs the selected evaluators.

### Step 6

Metric results are stored in PostgreSQL.

### Step 7

The Root Cause Engine identifies likely failure causes.

### Step 8

The Recommendation Engine generates improvement actions.

### Step 9

The Report Service calculates the overall health score.

### Step 10

The dashboard and API expose the final AI Health Report.

---

## 12. Standard Health-Check Input

```json
{
  "project_id": "project_uuid",
  "application_version": "1.0.0",
  "question": "What is the refund period?",
  "answer": "Customers can request a refund within 30 days.",
  "contexts": [
    {
      "text": "Customers may request a refund within 14 days.",
      "source": "refund_policy.pdf",
      "rank": 1,
      "retrieval_score": 0.92
    }
  ],
  "reference_answer": "Customers may request a refund within 14 days.",
  "prompt": "Answer only using the provided context.",
  "model": {
    "provider": "google",
    "name": "gemini-model",
    "temperature": 0.2
  },
  "retriever": {
    "embedding_model": "embedding-model-name",
    "top_k": 5,
    "chunk_size": 500,
    "chunk_overlap": 50
  },
  "performance": {
    "latency_ms": 1400,
    "input_tokens": 450,
    "output_tokens": 70,
    "estimated_cost": 0.002
  },
  "metadata": {
    "environment": "production",
    "language": "en",
    "category": "refund_policy"
  }
}
```

---

## 13. Standard AI Health Report Output

```json
{
  "health_check_id": "health_check_uuid",
  "status": "COMPLETED",
  "overall_health_score": 58,
  "health_status": "POOR",
  "metrics": {
    "faithfulness": 0.35,
    "answer_relevancy": 0.94,
    "answer_correctness": 0.20,
    "context_precision": 0.92,
    "context_recall": 1.0,
    "hallucination_risk": 0.75
  },
  "diagnosis": {
    "primary_category": "GENERATION_FAILURE",
    "subcategory": "UNSUPPORTED_CLAIM",
    "severity": "HIGH",
    "confidence": 0.96,
    "explanation": "The retrieved context is relevant and contains the correct refund period, but the generated answer contradicts the supplied evidence."
  },
  "recommendations": [
    {
      "priority": 1,
      "action": "Strengthen the grounding instruction",
      "expected_impact": "HIGH",
      "difficulty": "LOW"
    },
    {
      "priority": 2,
      "action": "Require the model to cite the supporting context",
      "expected_impact": "HIGH",
      "difficulty": "MEDIUM"
    },
    {
      "priority": 3,
      "action": "Add an automatic contradiction check before returning the answer",
      "expected_impact": "MEDIUM",
      "difficulty": "MEDIUM"
    }
  ]
}
```

---

## 14. Database Components

The initial database should contain these main tables:

* organizations
* users
* projects
* application_versions
* prompts
* health_checks
* retrieved_contexts
* evaluation_metrics
* diagnoses
* recommendations
* model_executions
* evaluation_datasets
* dataset_samples
* alerts
* audit_logs

Detailed database design will be stored in:

```text
docs/database_design.md
```

---

## 15. API Endpoints

Initial endpoints:

```text
POST   /api/v1/projects
GET    /api/v1/projects
GET    /api/v1/projects/{project_id}

POST   /api/v1/health-checks
POST   /api/v1/health-checks/batch
GET    /api/v1/health-checks/{health_check_id}
GET    /api/v1/health-checks/{health_check_id}/report

POST   /api/v1/datasets
POST   /api/v1/datasets/{dataset_id}/run
GET    /api/v1/evaluation-runs/{run_id}

GET    /api/v1/projects/{project_id}/metrics
GET    /api/v1/projects/{project_id}/trends
GET    /api/v1/projects/{project_id}/issues
GET    /api/v1/projects/{project_id}/model-comparison
```

---

## 16. Technology Stack

### Backend

* Python 3.12
* FastAPI
* Pydantic
* SQLAlchemy
* Alembic

### Background Processing

* Redis
* Celery or Dramatiq

### Database

* PostgreSQL
* pgvector where needed

### Evaluation

* Ragas
* DeepEval
* Custom deterministic evaluators
* Custom LLM-as-a-Judge evaluators

### Observability

* OpenTelemetry
* Prometheus
* Grafana
* Structured logging

### Experiment Tracking

* MLflow

### Dashboard

Initial option:

* React or Next.js

Alternative development interface:

* Streamlit for internal testing only

### Infrastructure

* Docker
* Docker Compose
* GitHub Actions

---

## 17. Repository Architecture

```text
AI-Reliability-Platform/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── schemas/
│   ├── services/
│   ├── repositories/
│   ├── models/
│   ├── workers/
│   └── main.py
│
├── evaluation/
│   ├── base/
│   ├── retrieval/
│   ├── generation/
│   ├── rag/
│   ├── prompt/
│   ├── safety/
│   └── performance/
│
├── root_cause/
│   ├── rules/
│   ├── statistical/
│   └── agent/
│
├── recommendations/
│   ├── rules/
│   └── agent/
│
├── monitoring/
│   ├── metrics/
│   ├── drift/
│   └── alerts/
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── custom/
│   └── schemas/
│
├── datasets/
│   ├── loaders/
│   ├── converters/
│   ├── validators/
│   └── generators/
│
├── database/
│   ├── migrations/
│   └── seeds/
│
├── dashboard/
│
├── infrastructure/
│   ├── docker/
│   ├── monitoring/
│   └── ci/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── evaluation/
│   └── end_to_end/
│
├── docs/
│   ├── architecture.md
│   ├── requirements.md
│   ├── roadmap.md
│   └── database_design.md
│
├── configs/
├── scripts/
├── notebooks/
├── pyproject.toml
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 18. Design Principles

### Modular Architecture

The first version will use a modular monolith rather than separate microservices.

Modules will have clear boundaries, but they will initially run in one backend application.

This reduces infrastructure complexity while preserving future scalability.

### Explainable Evaluation

Every metric and diagnosis must include supporting evidence.

The platform should not return unexplained scores.

### Provider Independence

The system must not depend on one LLM provider.

It should support multiple providers and local models.

### Reproducibility

Evaluation results must record:

* Model
* Prompt version
* Dataset version
* Evaluator version
* Retrieval configuration
* Timestamp

### Configurable Evaluation

Different projects may use different metrics and weights.

### Privacy

Sensitive prompts, contexts, and answers must be protected.

Self-hosted deployments should allow companies to keep data inside their environment.

---

## 19. First Development Milestone

The first technical milestone is called:

```text
Evaluation Foundation
```

It includes:

* Standard evaluation schema
* PostgreSQL data model
* Dataset loader
* Evaluator plugin interface
* Basic evaluation pipeline
* Faithfulness evaluator
* Answer relevancy evaluator
* Context precision evaluator
* Deterministic root-cause rules
* AI Health Report generator
* Unit tests
* Docker development environment

The dashboard and advanced agent will be built after the Evaluation Foundation is stable.
