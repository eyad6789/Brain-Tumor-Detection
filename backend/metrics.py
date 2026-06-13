"""Parse model_log.csv into the /api/metrics payload, with class metadata."""

import csv
import os

from inference_core import CLASS_INFO, CLASSES

from .schemas import ClassMeta, EpochRow, MetricsResponse

MODEL_LOG_PATH = os.environ.get("MODEL_LOG_PATH", "model_log.csv")

# AUDIT.md [H2]: the test set was used as the validation/early-stopping set, so
# the headline accuracy is optimistically biased — surface this honestly.
ACCURACY_CAVEAT = (
    "Claimed accuracy. AUDIT.md [H2] flags that the test set was reused as the "
    "validation set (data leakage), so this is an optimistic figure, not a "
    "validated generalization estimate."
)
FALLBACK_ACCURACY = 0.9847


def _to_float(value: str | None):
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _to_int(value: str | None):
    f = _to_float(value)
    return int(f) if f is not None else None


def _class_meta() -> list[ClassMeta]:
    return [
        ClassMeta(name=CLASSES[i], index=i, description=CLASS_INFO.get(CLASSES[i], ""))
        for i in range(len(CLASSES))
    ]


def load_metrics() -> MetricsResponse:
    epochs: list[EpochRow] = []

    if os.path.exists(MODEL_LOG_PATH):
        with open(MODEL_LOG_PATH, newline="") as f:
            for row in csv.DictReader(f):
                epochs.append(EpochRow(
                    epoch=_to_int(row.get("epoch")) or 0,
                    train_loss=_to_float(row.get("train_loss")),
                    train_acc=_to_float(row.get("train_acc")),
                    val_loss=_to_float(row.get("val_loss")),
                    val_acc=_to_float(row.get("val_acc")),
                    lr=_to_float(row.get("lr")),
                ))

    # Best/last validation accuracy is the model-selection metric.
    val_accs = [e.val_acc for e in epochs if e.val_acc is not None]
    claimed = max(val_accs) if val_accs else FALLBACK_ACCURACY

    return MetricsResponse(
        claimed_accuracy=claimed,
        accuracy_caveat=ACCURACY_CAVEAT,
        epochs=epochs,
        confusion_matrix=None,   # not present in model_log.csv — do not fabricate
        per_class=None,          # ditto
        classes=_class_meta(),
    )
