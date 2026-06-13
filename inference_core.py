"""
Shared inference core for the brain-tumor MRI classifier.

This is the SINGLE SOURCE OF TRUTH for the model architecture, preprocessing,
class metadata, and the prediction pipeline. Both the Gradio UI (app.py) and the
FastAPI backend (backend/) should rely on this module so the model "head" can
never drift between training and serving.

Reuses the existing helper modules as-is:
    - gradcam_utils.generate_gradcam / gradcam_available
    - llm_report.generate_medical_report / llm_available  (imported by callers)

Designed to be import-safe: importing this module does NOT load the 98 MB
weights (unlike app.py). Call load_model() explicitly when you need the model.
"""

import os

import torch
import torch.nn as nn
from PIL import Image
from torchvision import models, transforms

from gradcam_utils import generate_gradcam, gradcam_available

# ─── Config / class metadata (canonical — keep in sync with app.py) ────────────
# Fixed class-index order. Do NOT reorder — model_class.pth was trained with it.
CLASSES = {0: "Pituitary", 1: "No Tumor", 2: "Meningioma", 3: "Glioma"}
CLASS_NAMES = [CLASSES[i] for i in range(len(CLASSES))]

CLASS_INFO = {
    "Pituitary":  "A pituitary tumor grows in the pituitary gland at the base of the brain. Most are benign (non-cancerous).",
    "No Tumor":   "No brain tumor was detected in this MRI scan.",
    "Meningioma": "A meningioma is a tumor that forms on the membranes (meninges) surrounding the brain and spinal cord.",
    "Glioma":     "A glioma is a tumor that originates in the glial cells of the brain. It can be benign or malignant.",
}

MODEL_PATH = os.environ.get("MODEL_PATH", "model_class.pth")
IMG_SIZE = 224

# Inference/eval transform — must match how model_class.pth was trained (ImageNet stats).
TRANSFORM = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])


# ─── Model ─────────────────────────────────────────────────────────────────────
def build_model() -> nn.Module:
    """Build the ResNet50 with the exact head that the shipped weights were saved with.

    IMPORTANT: the second ``nn.Dropout(0.3)`` is intentional and must stay.
    Dropout layers carry no parameters, so this duplicate is a no-op at eval(),
    but it keeps the trainable layers at state_dict indices ``fc.1`` (Linear 2048->512)
    and ``fc.5`` (Linear 512->4). Removing it would shift the final Linear to
    ``fc.4`` and break a strict load of model_class.pth. (train.py uses a different
    head with BatchNorm1d(512) — that head will NOT load these weights.)
    """
    model = models.resnet50(weights=None)
    in_features = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Dropout(0.5),                  # fc.0
        nn.Linear(in_features, 512),      # fc.1  (trainable)
        nn.ReLU(),                        # fc.2
        nn.Dropout(0.3),                  # fc.3
        nn.Dropout(0.3),                  # fc.4  (kept so final Linear stays at fc.5)
        nn.Linear(512, 4),                # fc.5  (trainable)
    )
    return model


def pick_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def load_model(device: torch.device | None = None, model_path: str | None = None) -> nn.Module:
    """Load model_class.pth onto ``device`` and return an eval-mode model.

    Tries a strict load first; on mismatch, falls back to ``strict=False`` but
    fails loudly if either trainable layer (``fc.1`` / ``fc.5``) is missing — a
    silently mis-loaded head produces plausible-looking but garbage predictions.
    """
    device = device or pick_device()
    path = model_path or MODEL_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Model file '{path}' not found. Run train.py to produce it, "
            "or set the MODEL_PATH environment variable."
        )

    model = build_model()
    state = torch.load(path, map_location=device)
    if isinstance(state, dict) and "state_dict" in state:
        state = state["state_dict"]

    try:
        model.load_state_dict(state, strict=True)
    except RuntimeError:
        missing, unexpected = model.load_state_dict(state, strict=False)
        critical = [k for k in missing if k.startswith("fc.1") or k.startswith("fc.5")]
        if critical:
            raise RuntimeError(
                "Incompatible checkpoint: classifier head did not load "
                f"(missing {critical}). The weights do not match build_model()."
            )

    model.to(device)
    model.eval()
    return model


# ─── Verdict text (mirrors app.py:97-100) ──────────────────────────────────────
def build_verdict(top_class: str, top_conf: float) -> str:
    info = CLASS_INFO.get(top_class, "")
    if top_class == "No Tumor":
        return f"**Result: {top_class}** ({top_conf * 100:.1f}% confidence)\n\n{info}"
    return f"**Result: {top_class} Tumor Detected** ({top_conf * 100:.1f}% confidence)\n\n{info}"


# ─── Prediction pipeline ───────────────────────────────────────────────────────
def predict_core(model: nn.Module, device: torch.device, pil_image: Image.Image,
                 want_gradcam: bool = True):
    """Run classification (and optionally GradCAM) on a single PIL image.

    Returns:
        label_probs:  dict {class_name: float 0-1} in canonical order
        top_class:    str
        top_conf:     float (0-1)
        verdict:      str (markdown)
        gradcam_np:   numpy uint8 (224,224,3) or None if want_gradcam is False
    """
    pil_rgb = pil_image.convert("RGB")
    img_tensor = TRANSFORM(pil_rgb).unsqueeze(0).to(device)

    with torch.no_grad():
        logits = model(img_tensor)
        probs = torch.softmax(logits, dim=1).squeeze().cpu().tolist()

    label_probs = {CLASSES[i]: round(float(probs[i]), 4) for i in range(len(CLASSES))}
    top_class = max(label_probs, key=label_probs.get)
    top_conf = label_probs[top_class]
    verdict = build_verdict(top_class, top_conf)

    gradcam_np = generate_gradcam(model, img_tensor, pil_rgb) if want_gradcam else None

    return label_probs, top_class, top_conf, verdict, gradcam_np


__all__ = [
    "CLASSES", "CLASS_NAMES", "CLASS_INFO", "MODEL_PATH", "IMG_SIZE", "TRANSFORM",
    "build_model", "pick_device", "load_model", "build_verdict", "predict_core",
    "gradcam_available",
]
