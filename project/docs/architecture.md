# System Architecture — CollabLearn

> **Version**: 0.1  
> **Last updated**: April 2026

---

## Overview

CollabLearn is a research prototype implementing human-computer collaborative learning (HCCL) for graduate-level education. The system follows a modular architecture with three core subsystems: Collaborative Session Engine, Knowledge Graph, and Adaptive Recommender.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CollabLearn System                        │
│                                                                  │
│  ┌──────────────┐    ┌──────────────────┐    ┌───────────────┐  │
│  │   CLI / UI   │    │  Session Manager │    │  LLM Backend  │  │
│  │  (main.py)   │───▶│ (session_manager │───▶│ (OpenAI/local)│  │
│  └──────────────┘    │      .py)        │    └───────────────┘  │
│                      └────────┬─────────┘                       │
│                               │                                  │
│                    ┌──────────┴──────────┐                       │
│                    │                     │                        │
│          ┌─────────▼──────┐   ┌──────────▼──────┐               │
│          │ Knowledge Graph │   │    Recommender   │               │
│          │ (graph_builder  │   │  (recommender.py)│               │
│          │     .py)        │   │                  │               │
│          └────────┬────────┘   └─────────┬────────┘              │
│                   │                      │                        │
│          ┌────────▼──────────────────────▼────────┐              │
│          │           Persistence Layer             │              │
│          │  (SQLite / JSON log files)              │              │
│          └─────────────────────────────────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Descriptions

### 1. CLI / UI (`src/main.py`)
- **Purpose**: Entry point; provides CLI commands for starting sessions and getting recommendations.
- **Technology**: Click + Rich for terminal formatting.
- **Key commands**: `collablearn session`, `collablearn recommend`

### 2. Session Manager (`src/collaborative_learning/session_manager.py`)
- **Purpose**: Manages the full lifecycle of an HCCL session — state, turn-taking, dialogue history, and export.
- **Key classes**: `SessionManager`, `SessionState`, `DialogueTurn`
- **State machine**: `ACTIVE → [human turn → AI turn]* → ENDED`
- **LLM integration**: Calls a pluggable `ai_backend` function; defaults to mock for testing.

### 3. Knowledge Graph (`src/knowledge_graph/graph_builder.py`)
- **Purpose**: Represents the intelligent education domain as a directed graph of concepts and relationships.
- **Technology**: NetworkX DiGraph
- **Seed graph**: 20 foundational concepts, 25 relationships
- **Relationship types**: `prerequisite`, `part-of`, `related-to`, `enables`, `foundation-of`, `applied-in`, `raises`, `context-for`

### 4. Recommender (`src/recommendation/recommender.py`)
- **Purpose**: Estimates learner knowledge states and recommends next concepts.
- **Algorithm**: Simplified Bayesian Knowledge Tracing (BKT)
- **Key classes**: `Recommender`, `LearnerKnowledgeModel`, `ConceptKnowledgeState`
- **BKT parameters**: P(L₀)=0.2, P(T)=0.15, P(S)=0.1, P(G)=0.2 (defaults)

### 5. Persistence Layer
- **Session logs**: JSON files for each session (used for research analysis)
- **Learner models**: In-memory for prototype; SQLite for production
- **Export**: Sessions exportable to Markdown for human review

---

## Data Flow — Session Lifecycle

```
1. Learner starts session via CLI
2. SessionManager initializes:
   - Creates SessionState (unique session_id)
   - Builds KnowledgeGraph for domain
   - Initializes Recommender with LearnerModel
3. Session loop:
   a. AI generates opening prompt
   b. Learner types input
   c. SessionManager.process_human_turn():
      - Detects concepts mentioned → active_concepts update
      - Records DialogueTurn (HUMAN)
   d. SessionManager.generate_response():
      - Builds context-aware prompt using recent turns + KG context
      - Calls LLM backend
      - Records DialogueTurn (AI)
   e. Recommender.get_recommendations():
      - Evaluates learner's BKT states
      - Filters by prerequisites
      - Returns top-k recommended concepts
4. Session ends (exit command or max_turns reached)
5. SessionManager.end_session():
   - Records end timestamp
   - Exports session to JSON + Markdown
```

---

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| NetworkX for KG | Simple, well-documented, sufficient for prototype; swap to Neo4j for production |
| BKT for knowledge tracing | Interpretable, minimal data requirements; upgrade to DKT for richer data |
| Pluggable LLM backend | Allows swapping between GPT-4, local Qwen, and mock for testing/cost control |
| SQLite for prototype | Zero-config, file-based; sufficient for small-scale user study |
| JSON session logs | Human-readable, version-control-friendly; suitable for research analysis |

---

## Extension Points

| Component | How to Extend |
|-----------|---------------|
| LLM backend | Pass a custom callable to `SessionManager(ai_backend=my_fn)` |
| Knowledge graph | Add nodes/edges via `KnowledgeGraphBuilder._add_seed_nodes()` |
| Knowledge tracing | Replace BKT with DKT by subclassing `ConceptKnowledgeState` |
| Persistence | Replace SQLite with PostgreSQL by changing SQLAlchemy connection string |
| UI | Replace Click CLI with a web frontend (FastAPI + React) |

---

## Dependencies

See [`../requirements.txt`](../requirements.txt) for full dependency list.

Key dependencies:
- `networkx` — Knowledge graph
- `openai` — LLM API client
- `pydantic` — Data validation
- `sqlalchemy` — ORM / persistence
- `click` + `rich` — CLI

---

_Architecture document version 0.1 — update as the system evolves._
