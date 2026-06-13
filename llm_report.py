"""
LLM Medical Report Generator
Uses Meditron-7B via Ollama to produce a structured clinical description
based on the MRI classification results and confidence scores.

Meditron-7B is trained on PubMed, medical textbooks, and clinical guidelines
(EPFL, 2023) — well-suited for brain tumor case descriptions.

Setup (one time):
    curl -fsSL https://ollama.com/install.sh | sh
    ollama pull meditron

Then start the Ollama server:
    ollama serve

No API key needed — runs fully offline.
"""

import os

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

# Configurable via the OLLAMA_MODEL env var. Defaults to a small instruct model
# that runs comfortably on modest GPUs (~4 GB VRAM) and formats reports cleanly.
# Set OLLAMA_MODEL=meditron (and `ollama pull meditron`) for the medical 7B model
# (slower on small GPUs), or any other pulled model.
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:1.5b-instruct-q4_K_M")
# Cap output length (smaller = faster, esp. on CPU). Override with OLLAMA_NUM_PREDICT.
NUM_PREDICT = int(os.environ.get("OLLAMA_NUM_PREDICT", "520"))


def _strip_code_fence(text):
    """Some models wrap the whole answer in a ```markdown ... ``` block, which
    would render as a literal code block. Unwrap a single enclosing fence."""
    t = text.strip()
    if t.startswith("```"):
        nl = t.find("\n")
        if nl != -1 and t[3:nl].strip().lower() in ("markdown", "md", ""):
            body = t[nl + 1 :]
            if body.rstrip().endswith("```"):
                body = body.rstrip()[:-3]
            return body.strip()
    return text

_SYSTEM_PROMPT = (
    "You are a careful clinical AI assistant that explains brain-MRI findings in clear, "
    "compassionate language for both patients and clinicians, grounded in established "
    "radiology and oncology knowledge. Respond in well-structured GitHub-flavored Markdown, "
    "using exactly the section headings the user requests. Always remind the reader that your "
    "output is for education only and is not a substitute for professional diagnosis."
)

_REPORT_PROMPT = """\
A ResNet50 MRI brain-tumor classifier produced this result:

Primary finding: {tumor_class} ({confidence:.1f}% confidence).
Probabilities: Glioma {glioma:.1f}%, Meningioma {meningioma:.1f}%, \
Pituitary {pituitary:.1f}%, No Tumor {notumor:.1f}%.
A GradCAM heatmap highlighted the regions the model focused on.

Write a concise clinical report in Markdown with exactly these five sections, \
2-4 sentences each:

## Diagnosis Summary
## About {tumor_class}
## What the Heatmap Shows
## Recommended Next Steps
## Important Disclaimer

Write 1-3 short sentences per section and keep the whole report under 230 words. \
Be accurate, clear, and compassionate. Do not wrap the report in code fences.\
"""


def generate_medical_report(pil_image, tumor_class, confidence_scores):
    """
    Generate a structured clinical report using Meditron-7B via Ollama.

    Args:
        pil_image:         PIL Image (not used — Meditron is text-only)
        tumor_class:       str  — predicted class name (e.g. "Glioma")
        confidence_scores: dict — {class_name: float 0-1}

    Returns:
        str — markdown-formatted medical report, or an error/fallback string.
    """
    if not OLLAMA_AVAILABLE:
        return (
            "**LLM report unavailable** — install the Ollama Python client:\n\n"
            "```bash\npip install ollama\n```\n\n"
            "Then install and start Ollama:\n\n"
            "```bash\ncurl -fsSL https://ollama.com/install.sh | sh\n"
            "ollama pull meditron\nollama serve\n```"
        )

    def pct(key):
        return confidence_scores.get(key, 0.0) * 100

    prompt = _REPORT_PROMPT.format(
        tumor_class=tumor_class,
        confidence=pct(tumor_class),
        glioma=pct("Glioma"),
        meningioma=pct("Meningioma"),
        pituitary=pct("Pituitary"),
        notumor=pct("No Tumor"),
    )

    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user",   "content": prompt},
            ],
            options={
                "temperature": 0.3,     # low temperature for factual medical text
                "num_predict": NUM_PREDICT,
                "num_ctx": 2048,        # smaller context = less memory + faster
            },
        )
        return _strip_code_fence(response["message"]["content"])

    except ollama.ResponseError as exc:
        if "model" in str(exc).lower() or "not found" in str(exc).lower():
            return (
                f"**Model '{OLLAMA_MODEL}' not found in Ollama.**\n\n"
                f"Pull it with:\n```bash\nollama pull {OLLAMA_MODEL}\n```"
            )
        return f"**Ollama error:** {exc}"

    except Exception as exc:
        msg = str(exc).lower()
        if "connection" in msg or "refused" in msg or "connect" in msg:
            return (
                "**Ollama server is not running.**\n\n"
                "Start it with:\n```bash\nollama serve\n```"
            )
        return f"**Report generation failed:** {exc}"


def current_model():
    """Return the configured Ollama model name (OLLAMA_MODEL env, default llama3.2:3b)."""
    return OLLAMA_MODEL


def llm_available():
    """Return True if ollama is installed, the server is reachable, and the
    configured model is actually pulled (so /report won't 404 the model)."""
    if not OLLAMA_AVAILABLE:
        return False
    try:
        listed = ollama.list()
        models = [m.get("model") or m.get("name") for m in listed.get("models", [])]
        # Match exact tag or the base name (e.g. "llama3.2:3b" vs "llama3.2").
        base = OLLAMA_MODEL.split(":")[0]
        return any(m == OLLAMA_MODEL or (m or "").split(":")[0] == base for m in models)
    except Exception:
        return False
