# NeuroScan — Brain Tumor MRI Analyzer

An explainable deep-learning pipeline that classifies brain MRI scans into **four classes**
— **Glioma, Meningioma, Pituitary, No Tumor** — visualizes *why* with **GradCAM** heatmaps,
and drafts a **local clinical report** with Meditron-7B. Ships with a professional
**Next.js + FastAPI** web app and a legacy Gradio UI.

> ⚠️ **Educational & research use only.** Not a medical device and not a substitute for
> professional diagnosis. Reported accuracy is *claimed* (see [Limitations](#limitations)).

---

## Stack

- **Model:** PyTorch + torchvision — ResNet50 fine-tune (4-class head)
- **Explainability:** pytorch-grad-cam (GradCAM on `layer4`)
- **Report:** Meditron-7B via local Ollama (offline, no API key)
- **Web app:** FastAPI backend + Next.js 16 / React 19 / TypeScript / Tailwind v4 (dual light/dark theme)
- **Legacy UI:** Gradio (`app.py`)

## Project structure

| Path | Purpose |
|---|---|
| `inference_core.py` | Shared model core: architecture, loader, transform, `predict_core` (used by the API) |
| `backend/` | FastAPI app — `/api/health`, `/api/predict`, `/api/report`, `/api/metrics` |
| `frontend/` | Next.js web app (NeuroScan UI) — pages: `/`, `/analyze`, `/metrics`, `/about` |
| `app.py` | Legacy Gradio UI (still works standalone) |
| `train.py` | Training script (CLI args, early stopping, plots, CSV log) |
| `gradcam_utils.py` | GradCAM overlay helper |
| `llm_report.py` | Meditron-7B report via Ollama |
| `model_class.pth` | Trained weights |
| `model_log.csv` | Per-epoch training metrics |

---

## Quick start — the web app

Two terminals. The frontend proxies `/api/*` to the backend (no CORS needed).

**1) Backend** (run from the repo root so `model_class.pth` resolves):

```bash
source venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --port 8000 --reload
```

**2) Frontend:**

```bash
cd frontend
cp .env.example .env.local      # optional; defaults work
npm install
npm run dev                     # http://localhost:3000
```

**3) (Optional) Local LLM report** — without it, the rest of the app works and the
report panel shows setup instructions:

```bash
ollama serve
ollama pull meditron
```

Open **http://localhost:3000**, go to **Analyze**, upload an MRI → prediction + confidence
bars + GradCAM heatmap, then a local clinical report.

### API endpoints

| Method | Route | Description |
|---|---|---|
| `GET` | `/api/health` | Model status + capabilities (gradcam / ollama) |
| `POST` | `/api/predict` | multipart `file` → class, confidences, verdict, GradCAM (base64 PNG) |
| `POST` | `/api/report` | `{tumor_class, confidence_scores}` → local Meditron report |
| `GET` | `/api/metrics` | Training-log metrics + class metadata for the dashboard |

---

## Legacy Gradio UI

```bash
source venv/bin/activate
python app.py            # http://localhost:7860
```

## Training

```bash
python train.py --train_dir dataset/Training --test_dir dataset/Testing
```

Writes `model_class.pth`, `model_log.csv`, `learning_curves.png`, `confusion_matrix.png`.

---

## Limitations

- **Accuracy is "claimed", not validated.** In the recorded training run the test set was
  reused for validation/early-stopping (data leakage), so the headline figure is optimistic.
- Trained on one public dataset; may not generalize across scanners, sequences, or populations.
- GradCAM shows model *attention*, not a clinical tumor segmentation.
- The Meditron report is text-only — it reasons over the classification, not the pixels.

## License & author

For educational and research purposes only.

Developed by **Eyad Qasim Raheem** —
[LinkedIn](https://www.linkedin.com/in/eyad-qasim-2a96b624b/) ·
[GitHub](https://github.com/eyad6789)
