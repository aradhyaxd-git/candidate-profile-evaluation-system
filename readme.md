<div align="center">

# Candidate Profile Evaluation System (CPES)

A deterministic, explainable backend system for evaluating candidate profiles using structured rules and real-world context.

</div>

---

## 1. Problem Statement

Hiring teams often face inconsistency during early-stage candidate evaluation. Different evaluators prioritize different signals, and automated systems frequently provide scores without justification.

The objective of this system is to design a backend service that:

- Evaluates candidates using **deterministic rules**
- Produces a **normalized score out of 100**
- Clearly explains **how the score was derived**
- Incorporates **real-world context** without introducing bias
- Remains auditable, predictable, and extensible

---

## 2. What Was Designed

The **Candidate Profile Evaluation System (CPES)** is a rule-based evaluation engine that converts structured candidate data into a transparent evaluation outcome.

The system deliberately avoids machine learning in favor of **fixed logic**, ensuring:

- Repeatability (same input → same output)
- Explainability (no black-box decisions)
- Ease of iteration and review

### Core Capabilities

| Capability | Description |
|---------|-------------|
| Deterministic Scoring | Fixed weights with strict caps |
| Explainability | Human-readable reasoning for each score |
| Context Awareness | Student vs professional evaluation |
| Persistence | Stores evaluations for future audits |
| API-First Design | Submit and fetch evaluations via REST |

---

## 3. High-Level Idea

At a conceptual level, CPES works as follows:

1. Accept candidate profile data through an API
2. Apply mandatory scoring rules
3. Detect candidate career stage
4. Apply small, capped contextual adjustments
5. Normalize total score to 100
6. Generate explanations
7. Persist the evaluation
8. Allow retrieval by evaluation ID

This keeps the system **simple, predictable, and production-ready**.

---

## 4. System Architecture

The system follows a **layered architecture** with strict separation of concerns.

<div align="center">
  <img src="docs/design.png" width="85%" alt="System Architecture Diagram" />
</div>

### Architecture Layers

| Layer | Responsibility |
|------|---------------|
| API Layer | HTTP handling and input validation |
| Service Layer | Evaluation orchestration |
| Utility Layer | Scoring and explainability logic |
| Repository Layer | Database interactions |
| Storage Layer | PostgreSQL (Neon) |

---

## 5. Database Design (ER Diagram)

CPES uses a **hybrid SQL + JSON approach**:
- Relational tables for identity and relationships
- JSONB for flexible evaluation evidence

<div align="center">
  <img src="docs/er_diagram.jpg" width="75%" alt="ER Diagram" />
</div>

### Tables

#### `candidates`

| Field | Type | Purpose |
|------|------|--------|
| id | UUID | Unique candidate identifier |
| email | String | Candidate identity (MVP) |
| college_tier | Integer | Contextual signal |
| created_at | Timestamp | Audit trail |

#### `evaluations`

| Field | Type | Purpose |
|------|------|--------|
| id | UUID | Evaluation identifier |
| candidate_id | UUID | FK to candidates |
| total_score | Integer | Final score |
| fit_category | String | Evaluation outcome |
| input_details | JSONB | Raw input snapshot |
| score_breakdown | JSONB | Numerical breakdown |
| explanation | JSONB | Human-readable reasoning |
| evaluated_at | Timestamp | Time of evaluation |

---

## 6. Career Stage–Aware Evaluation

Real hiring decisions value **different signals at different career stages**.

<div align="center">
  <img src="docs/context_awareness.png" width="70%" alt="Career Stage Aware Evaluation" />
</div>

### Context Logic

| Candidate Stage | Signals Considered |
|---------------|-------------------|
| Student / Early Career | CGPA, GitHub activity, practice consistency |
| Working Professional | Experience, projects, skill alignment |

Academic signals are ignored for experienced professionals.

---

## 7. Deterministic Evaluation Pipeline

Each evaluation follows a **fixed and predictable pipeline**.

<div align="center">
  <img src="docs/evaluation_pipeline.png" width="85%" alt="Evaluation Pipeline" />
</div>

### Pipeline Steps

| Step | Description |
|----|------------|
| Input Validation | Schema enforcement |
| Base Scoring | Fixed category weights |
| Context Detection | Career stage identification |
| Contextual Boosters | Optional, capped signals |
| Normalization | Score capped at 100 |
| Explainability | Reason generation |
| Persistence | Store in database |
| Response | Return evaluation result |

---

## 8. Scoring Breakdown

The scoring system strictly follows the provided structure.

<div align="center">
  <img src="docs/scoring1.jpeg" width="75%" alt="Scoring Breakdown" />
</div>

### Fixed Scoring Structure

| Category | Max Points |
|--------|------------|
| Experience | 25 |
| Project Exposure | 25 |
| Skill Match | 20 |
| Learning Velocity | 15 |
| Role Readiness | 15 |
| **Total** | **100** |

Optional contextual signals are **normalized and capped**, ensuring fairness.

---

## 9. API Design

### Submit Evaluation

**POST** `/api/v1/evaluations/`

Creates an evaluation and returns:
- evaluation_id
- total_score
- fit_category
- score_breakdown
- explanation

### Fetch Evaluation

**GET** `/api/v1/evaluations/{evaluation_id}`

Fetches a previously stored evaluation for audit or review.

---

## 10. Edge Case Handling

The system explicitly accounts for critical edge cases to ensure robustness, fairness, and predictable behavior.

### 1. Zero Experience or Zero Projects

**Scenario:**  
A candidate submits a profile with `0` years of experience or `0` completed projects.

**Handling:**  
- Input is considered valid.
- Experience and project scores are calculated as `0`.
- Other dimensions (skills, learning velocity, readiness) are still evaluated.

**Reasoning:**  
Early-stage candidates should not be rejected due to lack of experience alone.  
The system avoids hard cutoffs and instead reflects the profile accurately.

---

### 2. CGPA or Academic Signals for Working Professionals

**Scenario:**  
A working professional provides CGPA or academic-related inputs.

**Handling:**  
- Academic signals are **ignored** when experience exceeds the early-career threshold.
- No penalty is applied.

**Reasoning:**  
Academic performance loses relevance with professional experience.  
This prevents outdated signals from skewing results.

---

### 3. Extreme or Inflated Inputs

**Scenario:**  
A candidate provides unusually large values (e.g., very high project count or activity metrics).

**Handling:**  
- All scoring dimensions have strict caps.
- The final score is always normalized to a maximum of 100.

**Reasoning:**  
Capping prevents any single signal from dominating the evaluation and ensures fairness.

---

### 4. Missing Optional Context Signals

**Scenario:**  
Optional inputs such as GitHub activity or competitive programming stats are not provided.

**Handling:**  
- The system proceeds with base scoring.
- No penalties are applied for missing optional data.

**Reasoning:**  
Optional signals are treated as enhancers, not requirements.  
The system remains functional with minimal mandatory input.

---

## 11. Tech Stack

| Layer | Technology |
|------|-----------|
| Language | Python 3.10+ |
| Framework | FastAPI |
| Database | PostgreSQL (Neon) |
| ORM | SQLAlchemy 2.0 (Async) |
| Validation | Pydantic v2 |
| DB Driver | asyncpg |

---

## 12. Use Cases

| Use Case | Description |
|--------|-------------|
| Hiring Pre-Screening | Structured early evaluation |
| Internal Assessment Tools | Consistent candidate scoring |
| Auditable Decisions | Fetch past evaluations |
| Educational Systems | Explainable evaluation engines |

---

## 13. Installation & Setup

### Clone Repository

```bash
git clone https://github.com/<your-username>/candidate-profile-evaluation-system
cd candidate-profile-evaluation-system
```

### Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment

Create a `.env` file:

```
DATABASE_URL=postgresql+asyncpg://user:password@host/db
```

### Create Tables

```bash
python -m app.create_tables
```

### Run Server

```bash
uvicorn app.main:app --reload
```

Access API documentation at: `http://127.0.0.1:8000/docs`

---

## 14. Final Notes

CPES is intentionally deterministic and explainable.

It prioritizes:

- Clarity over complexity
- Predictability over heuristics
- Transparency over automation

This makes it suitable for real-world evaluation workflows where trust and reasoning matter.

<div align="center"><b>Developed by Aradhya</b></div>