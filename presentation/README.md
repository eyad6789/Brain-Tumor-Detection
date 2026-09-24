# NeuroScan — Presentation & Documentation Package

Everything you need to present the **NeuroScan** brain-tumor MRI project and to answer any
technical question about it. All content is cross-checked against the actual source code.

## Start here

| File | What it is | How to use |
|---|---|---|
| **`NeuroScan_Report_en.pdf`** | **English deep-dive — 39 sections, ~83 pages** | The main deliverable. Read it, print it, send it. |
| **`NeuroScan_Report_ar.pdf`** | **Arabic deep-dive (right-to-left), same 39 sections** | Same — Arabic version. |
| `report-en.html` / `report-ar.html` | The same documents as self-contained web pages | Open in any browser. Diagrams are embedded, so they work offline. |
| `report-en.docx` / `report-ar.docx` | The same documents, editable | Open / edit in Microsoft Word. |
| `NeuroScan_EN.pptx` / `NeuroScan_AR.pptx` | Slide decks (29 slides each) | The **summary** version for presenting on screen. The PDFs are the deep-dive. |
| `assets/` | The diagrams (PNG) used in every file | — |
| `build/` + `.venv/` | The toolchain that generated everything (see *Rebuild*) | Optional — delete if you only want the outputs. |

## What's in the report

Sections 01–08 are the story and the data. **09–12** are the theory: what a CNN is from first
principles, why a CNN rather than an SVM / ViT / U-Net / YOLO, and every formula the system
uses. **13–19** are the model, its honest limitations, GradCAM, and the exact LLM prompts
(printed verbatim). **20–29** are the engineering: backend, every frontend component, the
end-to-end request lifecycle, the error/robustness matrix, security, performance, and a
decision log covering every technology and the alternatives that were rejected. **30–34** are
practical: how to run it, a hands-on script for a judge to *break* it on purpose, the roadmap,
commercialization, and a minute-by-minute demo script. **35–39** are Q&A, hard questions, the
glossary, the conclusion and a file-by-file code map.

Three sections are worth reading first if you are short on time: **03 · The 3-Minute
Explanation**, **31 · Test It Yourself**, and **34 · The Live Demo Script**.

## Presenting the slides
- **Best:** open the `.pptx` in PowerPoint or Keynote and press Play / Slideshow.
- **No PowerPoint?** Upload the `.pptx` to Google Slides (File → Import).
- **Export slides to PDF:** PowerPoint → File → Export → PDF (or Keynote → Export To → PDF).

## Arabic notes
- The Arabic files are laid out **right-to-left**; headings, bullets, and tables all mirror correctly.
- Arabic shaping is handled natively by the browser / Word / PowerPoint — no special fonts to install.
- Technical terms (ResNet50, GradCAM, FastAPI, Next.js, Ollama…) stay in English on purpose, and
  code blocks stay left-to-right so formulas and commands read correctly.

## Rebuild (optional)

```bash
cd presentation
./.venv/bin/python build/diagrams.py     # regenerate the PNG diagrams
./.venv/bin/python build/build_html.py   # → report-en.html, report-ar.html
./.venv/bin/python build/build_pdf.py    # → NeuroScan_Report_en/ar.pdf   (needs Chrome)
./.venv/bin/python build/build_docx.py   # → report-en.docx, report-ar.docx
./.venv/bin/python build/build_pptx.py   # → NeuroScan_EN.pptx, NeuroScan_AR.pptx
```

Run `build_html.py` before `build_pdf.py` — the PDF builder prints the HTML files with headless
Chrome, which is why the PDF always matches what you see in the browser and why Arabic shaping
needs no extra fonts. If Chrome is unavailable, open the HTML and press **Cmd/Ctrl + P → Save as
PDF** (tick **"Background graphics"**).

### Where the text lives
- `build/doc_data.py` — the original 20 sections.
- `build/doc_x1.py` — concepts, CNN theory, the mathematics.
- `build/doc_x2.py` — AI transcripts, engineering internals, security, performance, decisions.
- `build/doc_x3.py` — testing, roadmap, commercialization, demo script, hard questions, file map.
- `build/doc_extra.py` — splices x1–x3 into `doc_data.SECTIONS` and **renumbers every section**,
  so section numbers are never maintained by hand. Add a section there, not by editing numbers.
- `build/slides_data.py` — the slide decks (separate from the documents).

Every translatable string is written once as `L("english", "arabic")`, so the two languages
share one data structure and can never drift apart structurally.

## Optional: embed a *real* GradCAM example
The decks/docs currently use a schematic of the pipeline. If you drop a sample MRI image into this
folder, the model (`model_class.pth`) can be run locally to produce a genuine GradCAM heatmap +
real probability bars to embed — the most impressive visual for an explainable-AI talk.

---
*Educational & research prototype — not a medical device. Never use for diagnosis.*
