# 📝 Assignments

This folder contains all course assignments for the course **《智能教育及行业发展研究》**, organized by phase. Assignments are generated from group discussions and individual research, then refined through peer review.

---

## Assignment Phases

| Phase | Name | Description | Due Date |
|-------|------|-------------|----------|
| 1 | Literature Review | Systematic review of HCCL research (5,000–8,000 words) | — |
| 2 | Research Proposal | Full research proposal with methodology (8,000–12,000 words) | — |
| 3 | Final Report | Completed research report or system documentation (15,000+ words) | — |

---

## Folder Structure

```
assignments/
├── README.md                              # This file
├── phase-1-literature-review/
│   ├── README.md                          # Phase instructions & rubric
│   ├── template-literature-review.md      # Markdown template
│   └── [submitted assignments go here]
├── phase-2-research-proposal/
│   ├── README.md
│   ├── template-research-proposal.md
│   └── [submitted assignments go here]
└── phase-3-final-report/
    ├── README.md
    ├── template-final-report.md
    └── [submitted assignments go here]
```

---

## Submission Requirements

### File Naming Convention
```
<assignment-type>-<author-initials>-v<version>.<ext>
```
Examples:
- `literature-review-draft-v1.md`
- `research-proposal-final-v2.pdf`
- `final-report-group-v1.docx`

### Version Control Rules
1. **Draft versions** (v0.x): Working drafts — commit freely with descriptive messages.
2. **Review versions** (v1.x): Ready for peer review — create a PR and tag reviewers.
3. **Final versions** (vFinal): Instructor submission version — tagged and frozen.

### Review Workflow
```
Draft (vN-draft) → Peer Review (PR) → Revision → Final (vFinal)
       ↓                  ↓               ↓              ↓
   commit freely    open PR, assign    address        tag + submit
                    2 reviewers        comments
```

### Supported Formats
| Format | Use Case |
|--------|----------|
| `.md` | Primary authoring format (version-control-friendly) |
| `.pdf` | Final submission to instructor |
| `.docx` | When instructor requires Word format |
| `.ipynb` | When assignment includes code/analysis |

---

## Peer Review Guidelines

- Each assignment requires reviews from **at least 2 team members** before finalization.
- Review comments should be added as GitHub PR review comments or inline in the `.md` file using `> **[Reviewer Name]**: comment`.
- Reviews should address: clarity, completeness, argument quality, evidence quality, and formatting.

---

## Academic Integrity

- All submitted work must be original or properly cited.
- AI tool use must be disclosed: add a note at the end of the document describing any AI assistance used.
- The group is jointly responsible for all group assignments.
