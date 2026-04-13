# Contributing to CollabLearn

Thank you for contributing to the CollabLearn project! This document outlines the conventions and workflow for all contributors.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Workflow](#development-workflow)
3. [Code Style](#code-style)
4. [Commit Messages](#commit-messages)
5. [Pull Request Process](#pull-request-process)
6. [Testing](#testing)
7. [Documentation](#documentation)

---

## Getting Started

### Prerequisites
- Python 3.10 or later
- Git 2.x

### Setup

```bash
git clone <repo-url>
cd Research-on-Intelligent-Education-and-Industry-Development/project
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

### Verify Installation

```bash
python -m pytest tests/ -v
```

---

## Development Workflow

1. **Check the roadmap** (`project/roadmap.md`) to pick a task.
2. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/<short-description>
   # Examples:
   # feature/add-session-export
   # fix/knowledge-graph-query-bug
   # docs/update-architecture-diagram
   ```
3. **Make your changes** in small, focused commits.
4. **Write / update tests** in `tests/`.
5. **Run tests locally** before pushing:
   ```bash
   pytest tests/ -v
   ```
6. **Push your branch** and open a Pull Request.
7. **Address review comments** and iterate.
8. Once approved, the PR author **merges** (squash merge for feature branches).

---

## Code Style

- Follow **PEP 8** for all Python code.
- Use **type annotations** for all public functions and methods.
- Use **Google-style docstrings**:

  ```python
  def compute_score(learner_id: str, concept_id: str) -> float:
      """Compute the mastery score for a learner on a concept.

      Args:
          learner_id: Unique identifier for the learner.
          concept_id: Unique identifier for the knowledge concept.

      Returns:
          A float between 0.0 (no mastery) and 1.0 (full mastery).

      Raises:
          ValueError: If learner_id or concept_id is not found in the database.
      """
  ```

- **Line length**: 100 characters maximum.
- **Imports**: Group in order — standard library, third-party, local — separated by blank lines.
- **No magic numbers**: Use named constants or configuration values.

---

## Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short description>

[optional body]

[optional footer(s)]
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`

**Scopes**: `session`, `knowledge-graph`, `recommendation`, `utils`, `tests`, `docs`, `ci`

**Examples**:
```
feat(session): implement turn-taking protocol for HCCL sessions
fix(knowledge-graph): resolve null pointer in node lookup
docs(architecture): add sequence diagram for session flow
test(recommendation): add unit tests for BKT update function
chore(deps): update networkx to 3.3
```

---

## Pull Request Process

1. **Title**: Use Conventional Commits format (same as commit messages).
2. **Description**: Fill in the PR template:
   - What changes were made and why
   - How to test the changes
   - Screenshots or output (if applicable)
   - Related issue or roadmap task
3. **Reviewers**: Assign at least **1 team member** as reviewer.
4. **Checks**: All CI checks must pass before merging.
5. **Merge strategy**: Squash merge for feature branches; regular merge for release branches.

---

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run a specific test file
pytest tests/test_collaborative_learning.py -v

# Run with coverage report
pytest tests/ --cov=src --cov-report=html
```

### Writing Tests

- Place tests in `tests/` mirroring the `src/` structure.
- Test file names: `test_<module_name>.py`
- Use `pytest` conventions (functions prefixed with `test_`).
- Aim for >80% code coverage on all new modules.
- Mock external services (LLM APIs, databases) in unit tests.

---

## Documentation

- **Docstrings**: Required for all public classes, methods, and functions.
- **Architecture docs**: Update `docs/architecture.md` when making structural changes.
- **Roadmap**: Update `project/roadmap.md` when completing tasks or adding new ones.
- **Changelog**: Add entries to `CHANGELOG.md` (if maintained) for all user-facing changes.

---

## Questions?

Open a GitHub Issue or reach out to the team via the agreed communication channel.
