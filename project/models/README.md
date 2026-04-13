# 🤖 Models Directory

This folder contains model configuration files, metadata, and small helper scripts.
**Model weight files (`.pt`, `.pth`, `.bin`, `.ckpt`, `.h5`, etc.) are excluded from version control.**

---

## Contents

| File / Subfolder | Description |
|------------------|-------------|
| `README.md` | This file |
| `configs/` | YAML configuration files for model parameters |
| `bkt_params.yaml` | BKT parameter settings for the recommender |

---

## Model Registry

| Model | Type | Version | Source | Weights Location |
|-------|------|---------|--------|-----------------|
| BKT Knowledge Tracer | Custom | 0.1 | Implemented in `src/recommendation/` | N/A (parameterized) |
| LLM Backend | GPT-4o / Qwen2.5 | — | OpenAI API / Local Ollama | External |

---

## How to Use Pre-trained Models

If the project requires pre-trained model weights:
1. Download weights from the shared team drive (link in private channel).
2. Place in `models/weights/` (this folder is `.gitignore`d).
3. Update the model registry above with version and location.

---

## Notes

- Model weights are excluded from git via `.gitignore` to keep the repository size manageable.
- For reproducibility, always document the model version, training data, and hyperparameters.

---

_Last updated: April 2026_
