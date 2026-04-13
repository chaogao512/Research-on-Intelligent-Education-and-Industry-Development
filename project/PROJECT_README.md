# CollabLearn — Human-Computer Collaborative Learning System

> A prototype intelligent education system for exploring human-computer collaborative learning paradigms in Chinese higher education.

---

## 🎯 Project Overview

**CollabLearn** is a research prototype developed as part of the graduate course *Research on Intelligent Education and Industry Development* (《智能教育及行业发展研究》). It implements and evaluates key human-computer collaborative learning (HCCL) mechanisms, providing an empirical testbed for the group's research on HCCL paradigms in Chinese higher education.

### Research Alignment

This project directly supports the research question:

> *How can human-computer collaborative learning systems be effectively designed to support graduate-level research learning in Chinese higher education institutions?*

The system prototype incorporates three core HCCL mechanisms:
1. **Collaborative Session Management** — structures the human-AI interaction flow for joint knowledge construction
2. **Knowledge Graph Integration** — represents domain knowledge to enable context-aware AI contributions
3. **Adaptive Recommendation** — personalizes learning pathways based on learner knowledge states

---

## 🗂️ Project Structure

```
project/
├── PROJECT_README.md        # This file
├── roadmap.md               # Project roadmap & milestones
├── CONTRIBUTING.md          # How to contribute
├── CODE_OF_CONDUCT.md       # Team code of conduct
├── requirements.txt         # Python dependencies
├── setup.py                 # Package installation
├── .gitignore               # Project-specific ignores
│
├── src/                     # Source code
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── collaborative_learning/   # HCCL session management
│   ├── knowledge_graph/          # Knowledge representation
│   ├── recommendation/           # Adaptive recommendation
│   └── utils/                    # Shared utilities
│
├── docs/                    # Technical documentation
│   └── architecture.md      # System architecture overview
│
├── tests/                   # Unit tests
│   └── test_collaborative_learning.py
│
├── data/                    # Sample datasets (anonymized)
│   └── README.md
│
└── models/                  # Model configurations (weights excluded)
    └── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Git

### Installation

```bash
# Navigate to the project directory
cd project

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

### Running the Prototype

```bash
# Start the collaborative learning session CLI
python -m src.main

# Run with a specific configuration
python -m src.main --config configs/default.yaml
```

### Running Tests

```bash
pytest tests/ -v
```

---

## 🔧 Development Workflow

1. **Create a feature branch**: `git checkout -b feature/<short-description>`
2. **Make changes** following the coding style in `CONTRIBUTING.md`
3. **Write tests** for new functionality in `tests/`
4. **Run tests** before committing: `pytest tests/`
5. **Commit** with Conventional Commits style: `feat: add knowledge graph node expansion`
6. **Open a Pull Request** and request review from at least one team member

---

## 📖 Documentation

- **Architecture**: [docs/architecture.md](docs/architecture.md)
- **API Reference**: Generated from docstrings with `make docs`
- **Roadmap**: [roadmap.md](roadmap.md)

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📄 License

MIT License — see root repository for details.

---

_Last updated: April 2026_
