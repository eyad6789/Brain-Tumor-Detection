"""Shared NeuroScan visual identity — palette + fonts.

Colors mirror the live web app's dark "reading-room" theme
(frontend/app/globals.css) so every artifact looks like one product.
All builders (pptx/docx/html/diagrams) import from here.
"""

# ── Core dark palette (hex, no leading #) ───────────────────────────────
BG          = "06080F"   # near-black page background
SURFACE     = "0B101D"   # card background
SURFACE_2   = "0F1626"   # alt surface
SURFACE_3   = "151E31"   # inputs / chips
LINE        = "1E2A40"   # borders
INK         = "C5D2E3"   # body text on dark
INK_STRONG  = "F2F6FC"   # headings on dark
MUTED       = "7E8DA4"   # secondary text

PRIMARY     = "2CD4EE"   # clinical cyan (signature accent)
ACCENT      = "8B7BFF"   # violet (secondary accent)
SAFE        = "34D39A"   # green (No Tumor / healthy)
ALERT       = "F3B740"   # amber (caution / limitations)

# ── Per-class colors (match the web app) ────────────────────────────────
C_GLIOMA      = "FB6F97"  # magenta-pink
C_MENINGIOMA  = "A78BFF"  # purple
C_PITUITARY   = "F3B740"  # amber
C_NOTUMOR     = "34D39A"  # green

CLASS_COLORS = {
    "Glioma": C_GLIOMA,
    "Meningioma": C_MENINGIOMA,
    "Pituitary": C_PITUITARY,
    "No Tumor": C_NOTUMOR,
}

# ── Light surfaces (used for the printed/PDF HTML if ever needed) ────────
PAPER       = "FFFFFF"

# ── Fonts ───────────────────────────────────────────────────────────────
# Latin: Calibri/Helvetica are universally present in PowerPoint/Word.
# Arabic: faces that exist on macOS *and* Windows so the decks render
# correctly on the presentation machine without installing anything.
FONT_DISPLAY = "Arial"            # universal sans on macOS + Windows (no serif fallback)
FONT_BODY    = "Arial"
FONT_MONO    = "Consolas"
FONT_AR      = "Geeza Pro"        # macOS Arabic; PowerPoint/Word substitute per-platform
FONT_AR_WIN  = "Arial"            # safe Arabic fallback on Windows

def hx(c: str) -> str:
    """Return a #-prefixed hex for matplotlib/html."""
    return c if c.startswith("#") else f"#{c}"
