"""Pydantic request/response models — snake_case is the canonical wire format."""

from typing import Optional

from pydantic import BaseModel, field_validator

CLASS_NAMES = ["Pituitary", "No Tumor", "Meningioma", "Glioma"]


class ClassProb(BaseModel):
    label: str
    prob: float


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_error: Optional[str] = None
    device: str
    gradcam_available: bool
    ollama_available: bool
    ollama_model: str
    classes: list[str]


class PredictResponse(BaseModel):
    top_class: str
    confidence: float
    probabilities: list[ClassProb]          # sorted descending (display order)
    verdict_markdown: str
    gradcam_data_url: Optional[str] = None   # data:image/png;base64,... or null
    gradcam_is_heatmap: bool                 # False => fallback (grad-cam missing/skipped)


class ReportRequest(BaseModel):
    tumor_class: str
    confidence_scores: dict[str, float]      # {class_name: 0-1 float}

    @field_validator("tumor_class")
    @classmethod
    def _known_class(cls, v: str) -> str:
        if v not in CLASS_NAMES:
            raise ValueError(f"tumor_class must be one of {CLASS_NAMES}")
        return v


class ReportResponse(BaseModel):
    report_markdown: str
    available: bool


class EpochRow(BaseModel):
    epoch: int
    train_loss: Optional[float] = None
    train_acc: Optional[float] = None
    val_loss: Optional[float] = None
    val_acc: Optional[float] = None
    lr: Optional[float] = None


class ClassMeta(BaseModel):
    name: str
    index: int
    description: str


class MetricsResponse(BaseModel):
    claimed_accuracy: float
    accuracy_caveat: str
    epochs: list[EpochRow]
    confusion_matrix: Optional[list[list[float]]] = None
    per_class: Optional[list[dict]] = None
    classes: list[ClassMeta]
