# -*- coding: utf-8 -*-
"""Render report-en.html / report-ar.html to PDF using headless Chrome.

Chrome is used rather than a Python PDF library on purpose: it is the same
engine that renders the HTML on screen, so the PDF is guaranteed to match, and
it handles Arabic shaping and RTL layout natively with no font installation.

Run (after build_html.py):
    ../.venv/bin/python build_pdf.py
"""
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, ".."))

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "google-chrome", "chromium", "chromium-browser", "microsoft-edge",
]

TARGETS = [
    ("report-en.html", "NeuroScan_Report_en.pdf"),
    ("report-ar.html", "NeuroScan_Report_ar.pdf"),
]


def find_chrome():
    for c in CHROME_CANDIDATES:
        if os.path.isabs(c):
            if os.path.exists(c):
                return c
        else:
            found = shutil.which(c)
            if found:
                return found
    return None


def main():
    chrome = find_chrome()
    if not chrome:
        sys.exit(
            "No Chrome/Chromium/Edge found. Install one, or open the HTML file and\n"
            "use Cmd/Ctrl+P -> Save as PDF (tick 'Background graphics')."
        )

    for src, dst in TARGETS:
        src_path = os.path.join(OUT, src)
        dst_path = os.path.join(OUT, dst)
        if not os.path.exists(src_path):
            sys.exit(f"Missing {src} — run build_html.py first.")
        subprocess.run(
            [
                chrome,
                "--headless",
                "--disable-gpu",
                "--no-pdf-header-footer",
                # Give the browser time to decode the embedded base64 diagrams.
                "--virtual-time-budget=20000",
                f"--print-to-pdf={dst_path}",
                f"file://{src_path}",
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        size = os.path.getsize(dst_path) / 1024 / 1024
        print(f"wrote {dst}  ({size:.1f} MB)")


if __name__ == "__main__":
    main()
