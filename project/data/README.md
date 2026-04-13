# 📊 Data Directory

This folder contains sample datasets used for development and testing of the CollabLearn prototype.

---

## Contents

| Subfolder / File | Description | Sensitive? |
|------------------|-------------|------------|
| `sample_sessions/` | Anonymized HCCL session logs (JSON) for development | No |
| `sample_learner_profiles/` | Synthetic learner knowledge state data | No |
| `domain_ontology/` | Exported knowledge graph data (node/edge CSVs) | No |

> **Raw and processed research data from human participant studies are NOT stored here.**  
> All participant data is stored in a separate, access-controlled repository/drive.

---

## Data Management Rules

1. **No personal data**: Never commit data that can identify real participants.
2. **Anonymization required**: All session data must be anonymized before committing.
3. **Small files only**: Files in this folder should be < 5 MB. Large datasets go to external storage.
4. **Document everything**: Add a `README.md` to any new subfolder explaining its contents.
5. **PIPL compliance**: All data handling must comply with China's Personal Information Protection Law.

---

## Adding Sample Data

To add sample data:
1. Ensure it is fully anonymized and does not contain personal information.
2. Place it in the appropriate subfolder.
3. Update this README's contents table.
4. Commit with message: `data: add sample [description]`

---

_Last updated: April 2026_
