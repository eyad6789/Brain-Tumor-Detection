"""Render the project's diagrams as high-DPI PNGs into ../assets/.

One diagram engine, embedded in every artifact (pptx/docx/html) so the
visuals stay identical across languages. Labels are kept in neutral English
tech terms (ResNet50, GradCAM, FastAPI, Ollama ...) which read correctly in
both the English and Arabic decks and avoid matplotlib's Arabic-shaping pain.

Run:  ../.venv/bin/python diagrams.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D

import theme as T

ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(ASSETS, exist_ok=True)

BG   = T.hx(T.BG)
SURF = T.hx(T.SURFACE_2)
LINE = T.hx(T.LINE)
INK  = T.hx(T.INK)
INKS = T.hx(T.INK_STRONG)
MUT  = T.hx(T.MUTED)
CYAN = T.hx(T.PRIMARY)
VIO  = T.hx(T.ACCENT)
GRN  = T.hx(T.SAFE)
AMB  = T.hx(T.ALERT)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 12,
})


def _new(w=12, h=7):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, text, *, fc=SURF, ec=CYAN, tc=INKS, fs=12,
        lw=1.6, weight="bold", sub=None, sub_color=None):
    """Rounded box centered at (x, y)."""
    patch = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.02,rounding_size=2.2",
        linewidth=lw, edgecolor=ec, facecolor=fc, mutation_aspect=1)
    ax.add_patch(patch)
    if sub:
        ax.text(x, y + h * 0.16, text, ha="center", va="center",
                color=tc, fontsize=fs, fontweight=weight, zorder=5)
        ax.text(x, y - h * 0.24, sub, ha="center", va="center",
                color=sub_color or MUT, fontsize=fs - 3.5, zorder=5)
    else:
        ax.text(x, y, text, ha="center", va="center", color=tc,
                fontsize=fs, fontweight=weight, zorder=5)
    return patch


def arrow(ax, x1, y1, x2, y2, color=MUT, lw=2.0, style="-|>", ls="-"):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2), arrowstyle=style, mutation_scale=18,
        linewidth=lw, color=color, linestyle=ls,
        shrinkA=2, shrinkB=2, zorder=2))


def title(ax, t, sub=None):
    ax.text(50, 96, t, ha="center", va="center", color=INKS,
            fontsize=19, fontweight="bold")
    if sub:
        ax.text(50, 90.5, sub, ha="center", va="center", color=MUT, fontsize=12)


def save(fig, name):
    path = os.path.join(ASSETS, name)
    fig.savefig(path, facecolor=BG, bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    print("wrote", os.path.relpath(path))


# ─────────────────────────────────────────────────────────────────────────
# 1) SYSTEM ARCHITECTURE
# ─────────────────────────────────────────────────────────────────────────
def architecture():
    fig, ax = _new(13, 7.6)
    title(ax, "NeuroScan — System Architecture",
          "Browser → nginx → Next.js / FastAPI → PyTorch · GradCAM · local LLM")

    # Client
    box(ax, 13, 70, 20, 13, "User / Browser", sub="uploads an MRI scan",
        ec=INK, fc=T.hx(T.SURFACE), fs=13)

    # nginx edge
    box(ax, 13, 42, 20, 13, "nginx vhost", sub="public :8086  ·  routes / and /api",
        ec=CYAN, fs=13)
    arrow(ax, 13, 63.5, 13, 48.5, color=INK)

    # Docker boundary
    dock = FancyBboxPatch((30, 12), 64, 74,
                          boxstyle="round,pad=0.02,rounding_size=2",
                          linewidth=1.6, edgecolor=VIO, facecolor="none",
                          linestyle=(0, (6, 4)), zorder=1)
    ax.add_patch(dock)
    ax.text(92.5, 83, "Docker Compose", ha="right", va="center",
            color=VIO, fontsize=11, fontstyle="italic")

    # Frontend
    box(ax, 50, 70, 26, 14, "Next.js 16 Frontend",
        sub="React 19 · Tailwind v4  ·  :3040", ec=CYAN, fs=13)
    arrow(ax, 23, 45, 38, 66, color=CYAN)          # nginx -> frontend (page)
    ax.text(29, 58, "/", color=MUT, fontsize=10)

    # Backend
    box(ax, 50, 44, 26, 14, "FastAPI Backend",
        sub="uvicorn  ·  :8110→8000", ec=CYAN, fs=13)
    arrow(ax, 23, 41, 36, 44, color=CYAN)          # nginx -> backend (api)
    ax.text(29, 39.5, "/api", color=MUT, fontsize=10)
    arrow(ax, 50, 63, 50, 51, color=MUT, ls="--")  # frontend <-> backend
    ax.text(53, 57, "JSON / multipart", color=MUT, fontsize=9, ha="left")

    # Core modules inside backend
    box(ax, 44, 22, 18, 11, "inference_core", sub="ResNet50 (PyTorch)",
        ec=GRN, fs=11)
    box(ax, 64, 22, 14, 11, "gradcam_utils", sub="heatmaps", ec=GRN, fs=11)
    box(ax, 83, 44, 18, 12, "Ollama", sub="local LLM  ·  :11434 (internal)",
        ec=AMB, fs=12)
    arrow(ax, 46, 37, 44.5, 27.5, color=GRN)
    arrow(ax, 54, 37, 62, 27.5, color=GRN)
    arrow(ax, 63, 44, 74, 44, color=AMB)
    ax.text(68, 46.5, "report", color=MUT, fontsize=9)

    # weights chip
    box(ax, 20, 22, 16, 9, "model_class.pth", sub="98 MB weights",
        ec=LINE, fc=T.hx(T.SURFACE), fs=10, tc=INK)
    arrow(ax, 28, 22, 35, 22, color=MUT, ls="--")

    save(fig, "architecture.png")


# ─────────────────────────────────────────────────────────────────────────
# 2) 3-STAGE AI PIPELINE
# ─────────────────────────────────────────────────────────────────────────
def pipeline():
    fig, ax = _new(13, 6.2)
    title(ax, "The Explainable AI Pipeline",
          "one upload → prediction → visual explanation → readable report")

    y = 55
    box(ax, 11, y, 17, 22, "MRI Scan", sub="224×224 RGB", ec=INK,
        fc=T.hx(T.SURFACE), fs=13)
    box(ax, 35, y, 19, 22, "1 · ResNet50", sub="classify → softmax", ec=CYAN, fs=13)
    box(ax, 60, y, 19, 22, "2 · GradCAM", sub="layer4 heatmap", ec=VIO, fs=13)
    box(ax, 86, y, 19, 22, "3 · Local LLM", sub="clinical report", ec=AMB, fs=13)

    for x1, x2, c in [(19.5, 25.5, INK), (44.5, 50.5, CYAN), (69.5, 76.5, VIO)]:
        arrow(ax, x1, y, x2, y, color=c, lw=2.4)

    # outputs row
    ax.text(35, 33, "4-class probabilities", ha="center", color=CYAN, fontsize=10)
    ax.text(60, 33, "where the model looked", ha="center", color=VIO, fontsize=10)
    ax.text(86, 33, "5-section markdown", ha="center", color=AMB, fontsize=10)
    for x in (35, 60, 86):
        arrow(ax, x, 44, x, 36, color=MUT, lw=1.4)

    save(fig, "pipeline.png")


# ─────────────────────────────────────────────────────────────────────────
# 3) MODEL HEAD STACK
# ─────────────────────────────────────────────────────────────────────────
def model_head():
    fig, ax = _new(9.5, 9.5)
    title(ax, "Model: ResNet50 + Custom Head",
          "transfer learning — backbone frozen, layer3/4 + head fine-tuned")

    # backbone
    box(ax, 50, 80, 56, 11, "ResNet50 backbone (ImageNet)",
        sub="conv1·layer1·layer2 FROZEN   ·   layer3·layer4 FINE-TUNED",
        ec=CYAN, fs=12)
    ax.text(50, 71.5, "2048-d feature vector", ha="center", color=MUT, fontsize=10)
    arrow(ax, 50, 74, 50, 68, color=MUT)

    layers = [
        ("Dropout(0.5)",            "fc.0", VIO),
        ("Linear(2048 → 512)",      "fc.1  · trainable", CYAN),
        ("ReLU",                    "fc.2", MUT),
        ("Dropout(0.3)",            "fc.3", VIO),
        ("Dropout(0.3)  ← duplicate (intentional)", "fc.4 · keeps final layer at fc.5", AMB),
        ("Linear(512 → 4)",         "fc.5  · trainable", CYAN),
    ]
    y = 62
    for name, key, ec in layers:
        box(ax, 50, y, 64, 7.0, name, sub=key, ec=ec, fs=11)
        y -= 9.0

    arrow(ax, 50, y + 4.5, 50, y + 1.0, color=MUT)
    box(ax, 50, y - 3.5, 40, 7, "Softmax → 4 probabilities",
        sub="Pituitary · No Tumor · Meningioma · Glioma", ec=GRN, fs=11)

    save(fig, "model_head.png")


# ─────────────────────────────────────────────────────────────────────────
# 4) TRAINING CURVES (real numbers from model_log.csv)
# ─────────────────────────────────────────────────────────────────────────
def training_curves():
    epochs    = [1, 2, 3, 4, 5, 6, 7]
    train_acc = [0.8820, 0.9678, 0.9800, 0.9834, 0.9884, 0.9905, 0.9877]
    val_acc   = [0.9436, 0.9847, 0.9832, 0.9863, 0.9825, 0.9939, 0.9916]
    train_los = [0.3306, 0.0999, 0.0683, 0.0540, 0.0438, 0.0305, 0.0482]
    val_los   = [0.1575, 0.0525, 0.0525, 0.0438, 0.0644, 0.0197, 0.0279]

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2), dpi=200)
    fig.patch.set_facecolor(BG)
    fig.suptitle("Training History (model_log.csv · 7 epochs, early-stopped)",
                 color=INKS, fontsize=16, fontweight="bold", y=1.0)

    def style(ax):
        ax.set_facecolor(T.hx(T.SURFACE))
        for s in ax.spines.values():
            s.set_color(LINE)
        ax.tick_params(colors=MUT)
        ax.grid(True, color=LINE, linewidth=0.6, alpha=0.6)
        ax.set_xlabel("epoch", color=MUT)

    a = axes[0]; style(a)
    a.plot(epochs, train_acc, "-o", color=MUT, label="train acc", lw=2, ms=5)
    a.plot(epochs, val_acc, "-o", color=CYAN, label="val acc", lw=2.4, ms=6)
    a.scatter([6], [0.9939], s=220, marker="*", color=AMB, zorder=5)
    a.annotate("best 0.9939\n(epoch 6)", (6, 0.9939), (4.1, 0.957),
               color=AMB, fontsize=10, fontweight="bold",
               arrowprops=dict(arrowstyle="->", color=AMB))
    a.set_title("Accuracy", color=INKS, fontsize=13)
    a.set_ylim(0.86, 1.005)
    a.legend(facecolor=T.hx(T.SURFACE_2), edgecolor=LINE, labelcolor=INK)

    b = axes[1]; style(b)
    b.plot(epochs, train_los, "-o", color=MUT, label="train loss", lw=2, ms=5)
    b.plot(epochs, val_los, "-o", color=VIO, label="val loss", lw=2.4, ms=6)
    b.set_title("Loss", color=INKS, fontsize=13)
    b.legend(facecolor=T.hx(T.SURFACE_2), edgecolor=LINE, labelcolor=INK)

    fig.tight_layout(rect=(0, 0, 1, 0.96))
    save(fig, "training_curves.png")


if __name__ == "__main__":
    architecture()
    pipeline()
    model_head()
    training_curves()
    print("All diagrams rendered.")
