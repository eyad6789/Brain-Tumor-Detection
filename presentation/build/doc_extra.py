# -*- coding: utf-8 -*-
"""Splices the extra sections (doc_x1 / doc_x2 / doc_x3) into doc_data.SECTIONS
and renumbers everything, so section numbers are never maintained by hand.

Called once, from the bottom of doc_data.py.
"""
import doc_x1
import doc_x2
import doc_x3

# Each entry: (anchor section id, [sections to insert immediately after it]).
# Order within this list does not matter — each insert is resolved by anchor id.
INSERTS = [
    ("problem",     [doc_x1.PITCH]),
    ("architecture", [doc_x1.EVOLUTION]),
    ("augment",     [doc_x1.CNN, doc_x1.WHY_CNN]),
    ("model",       [doc_x1.MATH]),
    ("llm",         [doc_x2.TRANSCRIPTS, doc_x2.AI_DEV]),
    ("frontend",    [doc_x2.COMPONENTS, doc_x2.LIFECYCLE,
                     doc_x2.ROBUSTNESS, doc_x2.SECURITY, doc_x2.PERF]),
    ("stack",       [doc_x2.DECISIONS]),
    ("run",         [doc_x3.TESTING, doc_x3.ROADMAP, doc_x3.BUSINESS, doc_x3.DEMO]),
    ("qa",          [doc_x3.HARD_QA]),
    ("conclusion",  [doc_x3.FILEMAP]),
]


def splice(sections):
    """Insert every extra section after its anchor, then renumber 01, 02, 03…"""
    for anchor, extras in INSERTS:
        idx = next((i for i, s in enumerate(sections) if s["id"] == anchor), None)
        if idx is None:
            raise KeyError(
                f"doc_extra: anchor section id '{anchor}' not found in doc_data.SECTIONS"
            )
        sections[idx + 1:idx + 1] = extras

    ids = [s["id"] for s in sections]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise ValueError(f"doc_extra: duplicate section ids after splice: {sorted(dupes)}")

    for i, s in enumerate(sections, start=1):
        s["num"] = f"{i:02d}"
    return sections
