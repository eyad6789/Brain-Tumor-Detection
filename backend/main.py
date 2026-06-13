"""
FastAPI backend for the brain-tumor MRI classifier.

Run from the REPO ROOT (so model_class.pth and the root helper modules resolve):

    uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

Routes (all under /api):
    GET  /api/health    capabilities + model status
    POST /api/predict   multipart image -> classification + GradCAM heatmap
    POST /api/report    {tumor_class, confidence_scores} -> local Meditron report
    GET  /api/metrics   training metrics + class metadata for the dashboard
"""

import asyncio
import os
import threading
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, Query, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from inference_core import (
    CLASS_NAMES,
    gradcam_available,
    load_model,
    pick_device,
    predict_core,
)
from llm_report import current_model, generate_medical_report, llm_available

from .imaging import ImageValidationError, load_upload_image, numpy_to_data_url
from .metrics import load_metrics
from .schemas import (
    ClassProb,
    HealthResponse,
    PredictResponse,
    ReportRequest,
    ReportResponse,
)

# Serialize model-touching work. GradCAM registers backward hooks on the shared
# model and is not safe to run concurrently; inference shares buffers too.
INFERENCE_LOCK = threading.Lock()

# Cache the (slow) Ollama server ping so /health stays fast.
_OLLAMA_TTL = 30.0
_ollama_cache = {"value": None, "ts": 0.0}


def cached_ollama_available() -> bool:
    now = time.monotonic()
    if _ollama_cache["value"] is None or now - _ollama_cache["ts"] > _OLLAMA_TTL:
        _ollama_cache["value"] = bool(llm_available())
        _ollama_cache["ts"] = now
    return _ollama_cache["value"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Lazy-load the model at startup. On failure, keep the API up and report it
    # via /health instead of crashing (unlike app.py which raises at import time).
    app.state.device = pick_device()
    app.state.model = None
    app.state.model_error = None
    try:
        app.state.model = load_model(app.state.device)
    except Exception as exc:  # noqa: BLE001 - surfaced to clients via /health
        app.state.model_error = str(exc)
    yield


app = FastAPI(title="NeuroScan API — Brain Tumor MRI Classifier", lifespan=lifespan)

_origins = os.environ.get(
    "FRONTEND_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000"
).split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in _origins if o.strip()],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# ─── Uniform error envelope ────────────────────────────────────────────────────
def error_response(status: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"error": {"code": code, "message": message}})


@app.exception_handler(ImageValidationError)
async def _image_error_handler(_request: Request, exc: ImageValidationError):
    return error_response(exc.status, exc.code, exc.message)


# ─── Routes ────────────────────────────────────────────────────────────────────
@app.get("/api/health", response_model=HealthResponse)
async def health(request: Request):
    state = request.app.state
    return HealthResponse(
        status="ok",
        model_loaded=state.model is not None,
        model_error=state.model_error,
        device=str(state.device),
        gradcam_available=gradcam_available(),
        ollama_available=cached_ollama_available(),
        ollama_model=current_model(),
        classes=CLASS_NAMES,
    )


@app.post("/api/predict", response_model=PredictResponse)
async def predict(
    request: Request,
    file: UploadFile = File(...),
    gradcam: bool = Query(True),
):
    state = request.app.state
    if state.model is None:
        return error_response(
            503, "model_not_loaded",
            f"Model is not loaded: {state.model_error or 'unknown error'}",
        )

    raw = await file.read()
    pil_image = load_upload_image(raw, file.content_type)  # raises ImageValidationError

    def _run():
        with INFERENCE_LOCK:
            return predict_core(state.model, state.device, pil_image, want_gradcam=gradcam)

    label_probs, top_class, top_conf, verdict, gradcam_np = await asyncio.get_event_loop().run_in_executor(None, _run)

    probabilities = sorted(
        [ClassProb(label=name, prob=prob) for name, prob in label_probs.items()],
        key=lambda c: c.prob,
        reverse=True,
    )
    is_heatmap = bool(gradcam) and gradcam_available()
    data_url = numpy_to_data_url(gradcam_np) if gradcam_np is not None else None

    return PredictResponse(
        top_class=top_class,
        confidence=top_conf,
        probabilities=probabilities,
        verdict_markdown=verdict,
        gradcam_data_url=data_url,
        gradcam_is_heatmap=is_heatmap,
    )


@app.post("/api/report", response_model=ReportResponse)
async def report(req: ReportRequest):
    available = cached_ollama_available()

    def _run():
        # pil_image is unused by the text-only Meditron prompt; pass None.
        return generate_medical_report(None, req.tumor_class, req.confidence_scores)

    markdown = await asyncio.get_event_loop().run_in_executor(None, _run)
    return ReportResponse(report_markdown=markdown, available=available)


@app.get("/api/metrics")
async def metrics():
    return load_metrics()
