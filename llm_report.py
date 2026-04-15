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

OLLAMA_MODEL = "meditron"

_SYSTEM_PROMPT = (
    "You are Meditron, a medical AI assistant trained on clinical guidelines, "
    "PubMed abstracts, and medical textbooks. You help explain brain MRI findings "
    "in clear, compassionate language for both patients and clinicians. "
    "Always remind the user that your output is not a substitute for professional diagnosis."
)

_REPORT_PROMPT = """\
A deep learning model (ResNet50 fine-tuned on the Brain Tumor MRI dataset, ~98.5% accuracy) \
has analyzed a brain MRI scan and produced the following classification:

**Primary finding:** {tumor_class} ({confidence:.1f}% confidence)

**All class probabilities:**
- Glioma:      {glioma:.1f}%
- Meningioma:  {meningioma:.1f}%
- Pituitary:   {pituitary:.1f}%
- No Tumor:    {notumor:.1f}%

A GradCAM heatmap has also been computed, highlighting the image regions the model \
focused on when making this prediction.

Please generate a structured clinical report with exactly these five sections:

## Diagnosis Summary
State what was detected and the confidence level. Note whether the differential \
diagnoses (other classes) were ruled out convincingly.

## About This Condition
Clinical characteristics of {tumor_class}: typical anatomical location, \
growth pattern, malignancy risk, WHO grade (if applicable), and general prevalence.

## What the GradCAM Heatmap Tells Us
Explain that the colored overlay shows the regions the AI focused on. \
Describe which brain regions are typically involved in {tumor_class} and \
what a clinician should look for in those areas on an MRI.

## Recommended Next Steps
List practical clinical actions in order of priority (e.g., specialist referral, \
contrast MRI, biopsy, surveillance). Be specific to {tumor_class}.

## Important Disclaimer
State clearly that this AI report is for educational and research purposes only \
and must be reviewed and confirmed by a licensed radiologist or neurologist \
before any medical decisions are made.

Use clear, accessible language. Be informative and compassionate.\
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
                "temperature": 0.3,   # low temperature for factual medical text
                "num_predict": 1024,  # max tokens to generate
            },
        )
        return response["message"]["content"]

    except ollama.ResponseError as exc:
        if "model" in str(exc).lower() or "not found" in str(exc).lower():
            return (
                f"**Model '{OLLAMA_MODEL}' not found in Ollama.**\n\n"
                f"Pull it with:\n```bash\nollama pull {OLLAMA_MODEL}\n```"
            )
        return f"**Ollama error:** {exc}"

    except Exception as exc:
        if "connection" in str(exc).lower() or "refused" in str(exc).lower():
            return (
                "**Ollama server is not running.**\n\n"
                "Start it with:\n```bash\nollama serve\n```"
            )
        return f"**Report generation failed:** {exc}"


def llm_available():
    """Return True if ollama is installed and the server appears reachable."""
    if not OLLAMA_AVAILABLE:
        return False
    try:
        ollama.list()   # lightweight ping to the local server
        return True
    except Exception:
        return False
