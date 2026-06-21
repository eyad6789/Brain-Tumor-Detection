# NeuroScan — Presentation & Documentation Package

Everything you need to present the **NeuroScan** brain-tumor MRI project and to answer any
technical question about it. All content is cross-checked against the actual source code.

## What's in this folder

| File | What it is | How to use |
|---|---|---|
| **`NeuroScan_EN.pptx`** | English slide deck (29 slides) | Open in PowerPoint / Keynote / Google Slides and present |
| **`NeuroScan_AR.pptx`** | Arabic slide deck (29 slides, right-to-left) | Same — Arabic version |
| **`report-en.html`** | English deep-dive (20 sections) | Open in any browser; **Cmd/Ctrl + P → Save as PDF** for a clean PDF |
| **`report-ar.html`** | Arabic deep-dive (right-to-left) | Same — Arabic version |
| **`report-en.docx`** | English deep-dive, editable | Open / edit in Microsoft Word |
| **`report-ar.docx`** | Arabic deep-dive, editable (RTL) | Open / edit in Microsoft Word |
| `assets/` | The diagrams (PNG) used in every file | — |
| `build/` + `.venv/` | The toolchain that generated everything (see *Rebuild*) | Optional — delete if you only want the outputs |

> The two HTML files are fully self-contained (the diagrams are embedded), so they work offline
> and can be emailed or opened on any computer.

## Presenting the slides
- **Best:** open the `.pptx` in PowerPoint or Keynote and press Play / Slideshow.
- **No PowerPoint?** Upload the `.pptx` to Google Slides (File → Import), or open the matching
  HTML report fullscreen.
- **Export slides to PDF:** PowerPoint → File → Export → PDF (or Keynote → Export To → PDF).

## Exporting the documents to PDF
1. Double-click `report-en.html` (or `report-ar.html`) — it opens in your browser.
2. Press **Cmd + P** (Mac) / **Ctrl + P** (Windows).
3. Destination → **Save as PDF**. Tick **"Background graphics"** so the colors print.

The `.docx` files can also be exported from Word: File → Save As → PDF.

## Arabic notes
- The Arabic files are laid out **right-to-left**; headings, bullets, and tables all mirror correctly.
- Arabic shaping is handled natively by the browser / Word / PowerPoint — no special fonts to install.
- Technical terms (ResNet50, GradCAM, FastAPI, Next.js, Ollama…) stay in English on purpose.

## Rebuild (optional)
If you edit the content and want to regenerate the files:

```bash
cd presentation
./.venv/bin/python build/diagrams.py     # regenerate the PNG diagrams
./.venv/bin/python build/build_pptx.py   # → NeuroScan_EN.pptx, NeuroScan_AR.pptx
./.venv/bin/python build/build_docx.py   # → report-en.docx, report-ar.docx
./.venv/bin/python build/build_html.py   # → report-en.html, report-ar.html
```

All text lives in two files: `build/slides_data.py` (the decks) and `build/doc_data.py` (the
documents). Each string is written once as `L("english", "arabic")`, so the two languages can
never drift apart structurally.

## Optional: embed a *real* GradCAM example
The decks/docs currently use a schematic of the pipeline. If you drop a sample MRI image into this
folder, the model (`model_class.pth`) can be run locally to produce a genuine GradCAM heatmap +
real probability bars to embed — the most impressive visual for an explainable-AI talk.

---
*Educational & research prototype — not a medical device. Never use for diagnosis.*
