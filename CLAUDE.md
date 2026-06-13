# brain_tumor — NeuroScan

Brain-tumor MRI classifier (4 classes: Glioma, Meningioma, Pituitary, No Tumor) with an
explainable pipeline: ResNet50 classification → GradCAM heatmaps → local-LLM clinical report.
Two front-ends: a professional **Next.js + FastAPI** web app ("NeuroScan", primary) and a
legacy **Gradio** UI (`app.py`). Active prototype, educational/research only.

## Stack
- **ML:** Python 3.12, PyTorch + torchvision (ResNet50 fine-tune; ~99% *claimed* val acc — see gotchas)
- **Backend:** FastAPI + uvicorn (`backend/`), reuses the inference/GradCAM/LLM code
- **Frontend:** Next.js 16 / React 19 / TypeScript / **Tailwind v4** (CSS-first), dual light/dark theme (`frontend/`)
- **Explain/LLM:** pytorch-grad-cam (heatmaps); Ollama Python client for local reports (no API key)
- **Deps:** `backend/requirements.txt` (Python); `frontend/package.json` (Node). `venv/` holds the Python env.

## Structure
| Path | Purpose |
|---|---|
| `inference_core.py` | **Shared model core** — `build_model`, `load_model`, `TRANSFORM`, `CLASSES`/`CLASS_INFO`, `predict_core`. Single source of truth; import-safe (does NOT load weights on import). |
| `backend/main.py` | FastAPI app: lifespan model load, CORS, routes, threadpool + `INFERENCE_LOCK` |
| `backend/{schemas,imaging,metrics}.py` | Pydantic models · upload validation + base64-PNG · `model_log.csv` parsing |
| `frontend/` | Next.js app (App Router). Pages: `/`, `/analyze`, `/metrics`, `/about`. `lib/api.ts` = snake↔camel API seam. |
| `app.py` | Legacy Gradio UI (still works standalone; loads `model_class.pth` at import) |
| `train.py` | Training script (CLI `--train_dir`/`--test_dir`, early stopping, plots, CSV log) |
| `gradcam_utils.py` | GradCAM overlay helper (graceful fallback if grad-cam missing) |
| `llm_report.py` | Local LLM report via Ollama. Model from `OLLAMA_MODEL` env (default `qwen2.5:1.5b-instruct-q4_K_M`) |
| `model_class.pth` | 98 MB trained weights, committed to git |
| `model_log.csv` | Per-epoch training log: `epoch,train_loss,train_acc,val_loss,val_acc,lr` |

## Commands
**Backend** (run from repo root so `model_class.pth` + root modules resolve):
```bash
source venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --port 8000 --reload
```
**Frontend:**
```bash
cd frontend && npm install && npm run dev   # http://localhost:3000
```
**Local LLM report (optional):** `ollama serve` + `ollama pull qwen2.5:1.5b-instruct-q4_K_M`
**Legacy Gradio UI:** `python app.py` (port 7860). **Train:** `python train.py --train_dir ... --test_dir ...`
No automated tests exist.

## API (all under `/api`)
`GET /api/health` (capabilities + model name) · `POST /api/predict` (multipart `file` → class/probs/verdict/base64 GradCAM) · `POST /api/report` (`{tumor_class, confidence_scores}` → markdown) · `GET /api/metrics`.

## Conventions & Gotchas
- **Class index order is fixed everywhere:** pituitary=0, notumor=1, meningioma=2, glioma=3. Strings have a space: `"No Tumor"`.
- **Model head:** `inference_core.build_model()` replicates `app.py`'s head — `Dropout(0.5), Linear(2048,512), ReLU, Dropout(0.3), Dropout(0.3), Linear(512,4)`. The **duplicate `Dropout(0.3)` is intentional** so the final Linear stays at state_dict key `fc.5` and the shipped `model_class.pth` loads strictly. `train.py`'s head has `BatchNorm1d(512)` and will NOT load these weights — don't "unify" them blindly.
- **Accuracy is "claimed", not validated** — `train.py` reuses the test set for validation/early-stopping (data leakage). UI labels it "claimed" with a caveat; keep that framing.
- **LLM report is configurable + degrades gracefully.** `OLLAMA_MODEL` env picks the model. On a CPU-only Ollama or weak GPU it's slow (~1-2 min); on GPU it's ~15s. The frontend calls the backend directly (`frontend/.env.local` → `NEXT_PUBLIC_API_BASE`) because the Next proxy has a ~30s timeout that cuts off slow CPU reports.
- **GradCAM + Ollama are optional** — absent ⇒ graceful fallback (resized image / setup hint).
- `frontend/AGENTS.md` warns Next 16 has breaking changes vs. older knowledge — read `frontend/node_modules/next/dist/docs/` before writing Next-specific code.
- `train.py` writes `model_class.pth`, `model_log.csv`, `learning_curves.png`, `confusion_matrix.png` into the repo root.
- No secrets/keys required; everything runs offline/local.

## Do NOT read (large/irrelevant; also denied in .claude/settings.json)
- `venv/`, `frontend/node_modules/`, `frontend/.next/`, `__pycache__/`, `.git/`
- `brain-tumor.ipynb` (2.8 MB legacy TensorFlow notebook), `model_class.pth` (98 MB), any `*.pth`/`*.pkl`/`*.h5`/`*.onnx`
- `dataset/`, `data/`, `datasets/` (MRI images if present), `.ipynb_checkpoints/`
- Generated plots: `learning_curves.png`, `confusion_matrix.png`
