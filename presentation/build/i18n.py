"""Bilingual content helper.

Every translatable string is written once as ``L("english", "arabic")`` so the
English and Arabic artifacts share *one* data structure and can never drift
apart structurally. Renderers call ``tr(node, lang)`` to resolve a leaf.
"""

def L(en: str, ar: str) -> dict:
    return {"en": en, "ar": ar}


def tr(node, lang: str = "en") -> str:
    """Resolve a bilingual leaf (or pass a plain string through unchanged)."""
    if isinstance(node, dict) and ("en" in node or "ar" in node):
        return node.get(lang) or node.get("en") or ""
    return node if node is not None else ""


# Strings that are identical in both languages (product name, tech terms used
# as headings) can still go through L() for uniformity, but plain strings work.
RTL = {"ar"}
