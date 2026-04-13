# Project Roadmap — CollabLearn

> **Project**: Human-Computer Collaborative Learning System Prototype  
> **Course**: Research on Intelligent Education and Industry Development  
> **Start date**: April 2026  
> **End date**: July 2026

---

## Vision

Build a working prototype of a human-computer collaborative learning system that:
1. Enables empirical study of HCCL interaction patterns in graduate seminars.
2. Demonstrates how knowledge graphs can ground AI contributions in domain knowledge.
3. Provides adaptive recommendations that adapt to learner knowledge states over time.
4. Generates rich log data for learning analytics research.

---

## Milestones

### Milestone 1 — Foundation (Weeks 1–3, target: 2026-05-03)

**Goal**: Set up the project infrastructure and implement core data models.

| Task | Owner | Status | Notes |
|------|-------|--------|-------|
| Repository setup (structure, CI, dependencies) | All | ✅ Done | |
| Define core data models (Session, Learner, KnowledgeNode) | Member 3 | 🔄 In progress | |
| Set up database (SQLite for prototype) | Member 3 | ⬜ Pending | |
| Implement basic logging infrastructure | Member 3 | ⬜ Pending | |
| Write unit tests for data models | Member 3 | ⬜ Pending | |

---

### Milestone 2 — Collaborative Session Engine (Weeks 4–6, target: 2026-05-24)

**Goal**: Implement the core human-AI collaborative session management module.

| Task | Owner | Status | Notes |
|------|-------|--------|-------|
| Design session state machine | Member 1 | ⬜ Pending | |
| Implement `SessionManager` class | Member 3 | ⬜ Pending | |
| Integrate LLM API (mock for testing) | Member 3 | ⬜ Pending | Use OpenAI-compatible API |
| Implement turn-taking protocol | Member 3 | ⬜ Pending | |
| Implement session export to JSON/Markdown | Member 4 | ⬜ Pending | |
| Write integration tests for session flow | Member 3 | ⬜ Pending | |

---

### Milestone 3 — Knowledge Graph Module (Weeks 5–7, target: 2026-06-07)

**Goal**: Build a lightweight knowledge graph for the target domain (intelligent education).

| Task | Owner | Status | Notes |
|------|-------|--------|-------|
| Select KG library (NetworkX for prototype) | Member 2 | ⬜ Pending | |
| Define ontology for intelligent education domain | Member 2 | ⬜ Pending | |
| Implement `KnowledgeGraphBuilder` | Member 3 | ⬜ Pending | |
| Implement KG query interface | Member 3 | ⬜ Pending | |
| Populate seed KG with 50 domain concepts | Member 2 | ⬜ Pending | |
| Write tests for KG operations | Member 3 | ⬜ Pending | |

---

### Milestone 4 — Adaptive Recommendation Module (Weeks 7–9, target: 2026-06-21)

**Goal**: Implement a basic knowledge-tracing-based adaptive recommendation engine.

| Task | Owner | Status | Notes |
|------|-------|--------|-------|
| Implement simplified BKT (Bayesian Knowledge Tracing) | Member 3 | ⬜ Pending | |
| Implement `LearnerModel` (tracks knowledge state) | Member 3 | ⬜ Pending | |
| Implement `Recommender` class | Member 3 | ⬜ Pending | |
| Connect recommender to session manager | Member 3 | ⬜ Pending | |
| Write tests for recommendation logic | Member 3 | ⬜ Pending | |

---

### Milestone 5 — Evaluation & User Study (Weeks 8–11, target: 2026-07-05)

**Goal**: Run a small-scale user study with the prototype and collect data for the Phase 3 report.

| Task | Owner | Status | Notes |
|------|-------|--------|-------|
| Design user study protocol | Member 1 | ⬜ Pending | |
| Obtain ethics approval | Member 1 | ⬜ Pending | |
| Recruit participants (n ≥ 12) | All | ⬜ Pending | |
| Run user study sessions | All | ⬜ Pending | |
| Collect log data, surveys, and interviews | All | ⬜ Pending | |
| Analyze results | Member 2 | ⬜ Pending | |

---

### Milestone 6 — Documentation & Submission (Weeks 10–12, target: 2026-07-19)

**Goal**: Complete documentation, clean up code, and prepare final report.

| Task | Owner | Status | Notes |
|------|-------|--------|-------|
| Write complete API documentation | Member 4 | ⬜ Pending | |
| Finalize architecture documentation | Member 4 | ⬜ Pending | |
| Write system development section for Phase 3 report | Member 3 | ⬜ Pending | |
| Code cleanup and final PR review | All | ⬜ Pending | |
| Tag final release `v1.0.0` | Member 1 | ⬜ Pending | |

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| LLM API access/cost constraints | Medium | High | Use local model (Ollama) as fallback |
| Participant recruitment difficulties | Medium | High | Recruit from own course cohort; backup: simulated sessions |
| Technical complexity exceeds timeline | Low | Medium | Reduce scope — drop KG module for Milestone 3 if needed |
| Data quality issues from user study | Low | Medium | Pilot test instruments thoroughly |

---

## Versioning

| Version | Description | Target Date |
|---------|-------------|-------------|
| v0.1.0 | Core data models + session engine skeleton | 2026-05-03 |
| v0.2.0 | Working session engine + basic CLI | 2026-05-24 |
| v0.3.0 | Knowledge graph integration | 2026-06-07 |
| v0.4.0 | Adaptive recommendation module | 2026-06-21 |
| v1.0.0 | Evaluation-ready prototype | 2026-07-05 |

---

_Roadmap last updated: 2026-04-13_
