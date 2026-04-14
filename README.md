**[🇨🇳 中文版本](readme_zh.md)** | **[🇬🇧 English](#research-on-intelligent-education-and-industry-development)**

# 智能教育及行业发展研究
# Research on Intelligent Education and Industry Development

> Graduate-level course repository · Spring 2026 · Human-Computer Collaborative Learning Research Group

---

## 📋 Course Overview

This repository supports the graduate course **《智能教育及行业发展研究》(Research on Intelligent Education and Industry Development)**. It provides a structured workspace for course resources, group discussions, assignments, and a semester-long intelligent education system development project.

The research focus of this group is: **human-computer collaborative learning paradigms in educational technology within Chinese higher education institutions**.

---

## 👥 Team Members

| Name | Role | Responsibilities |
|------|------|-----------------|
| Member 1 | Project Lead | Architecture design, project coordination |
| Member 2 | Research Lead | Literature review, theoretical framework |
| Member 3 | Development Lead | System development, code review |
| Member 4 | Documentation Lead | Documentation, discussion facilitation |

> _Update this table with actual names and GitHub handles._

---

## 🗂️ Repository Structure

```
Research-on-Intelligent-Education-and-Industry-Development/
│
├── README.md                          # This file — repository overview
├── .gitignore                         # Global ignore rules
│
├── resources/                         # Course learning resources
│   ├── README.md                      # Resource management rules & naming conventions
│   ├── module-01-intro-to-intelligent-education/
│   ├── module-02-ai-in-education-systems/
│   ├── module-03-human-computer-collaborative-learning/
│   ├── module-04-educational-data-governance/
│   └── module-05-industry-development-and-applications/
│
├── discussion/                        # Group discussion area
│   ├── README.md                      # Discussion rules & export procedures
│   ├── main-discussion.md             # Master discussion thread index
│   ├── export_discussion.py           # Script to export discussion to formatted .md
│   ├── topic-01-human-computer-collaborative-learning/
│   ├── topic-02-educational-data-governance/
│   ├── topic-03-ai-tools-in-higher-education/
│   └── topic-04-industry-development-trends/
│
├── assignments/                       # Course assignments
│   ├── README.md                      # Submission requirements & review workflow
│   ├── phase-1-literature-review/
│   ├── phase-2-research-proposal/
│   └── phase-3-final-report/
│
└── project/                           # Intelligent education system project
    ├── PROJECT_README.md              # Project overview & quick-start guide
    ├── roadmap.md                     # Project roadmap & milestones
    ├── CONTRIBUTING.md                # Contribution guidelines
    ├── CODE_OF_CONDUCT.md             # Code of conduct
    ├── requirements.txt               # Python dependencies
    ├── setup.py                       # Package setup
    ├── .gitignore                     # Project-specific ignore rules
    ├── src/                           # Source code
    │   ├── collaborative_learning/    # Human-computer collaborative learning module
    │   ├── knowledge_graph/           # Knowledge graph module
    │   ├── recommendation/            # Adaptive recommendation module
    │   └── utils/                     # Shared utilities
    ├── docs/                          # Technical documentation
    ├── tests/                         # Unit tests
    ├── data/                          # Sample datasets (non-sensitive)
    └── models/                        # Pre-trained model configs (weights excluded)
```

---

## 🚀 Quick Start

### Clone the Repository
```bash
git clone https://github.com/chaogao512/Research-on-Intelligent-Education-and-Industry-Development.git
cd Research-on-Intelligent-Education-and-Industry-Development
```

### Set Up the Project Environment
```bash
cd project
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run the Project
```bash
python -m src.main
```

---

## 📚 Area Guides

| Area | Description | Link |
|------|-------------|------|
| Course Resources | Slides, papers, notes by module | [resources/README.md](resources/README.md) |
| Group Discussions | Async discussion threads & export tool | [discussion/README.md](discussion/README.md) |
| Assignments | Submission templates & review workflow | [assignments/README.md](assignments/README.md) |
| Project | Intelligent education system development | [project/PROJECT_README.md](project/PROJECT_README.md) |

---

## 🤝 Contribution Rules

1. **Branch naming**: `feature/<area>-<short-description>` (e.g., `feature/project-add-recommender`)
2. **Commit messages**: Use [Conventional Commits](https://www.conventionalcommits.org/) style
   - `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`
3. **Pull Requests**: All changes require at least one peer review before merging into `main`
4. **File naming**: Use lowercase with hyphens (e.g., `research-proposal-v1.md`)
5. **No large files**: Do not commit files >50 MB; use Git LFS or external storage
6. **No sensitive data**: Never commit API keys, passwords, or personal data

See [project/CONTRIBUTING.md](project/CONTRIBUTING.md) for detailed guidelines.

---

## 📄 License

This repository is for academic course use only. All course materials remain the intellectual property of the respective authors and instructors. Code developed in the project area is available under the MIT License unless otherwise noted.

---

_Last updated: April 2026_