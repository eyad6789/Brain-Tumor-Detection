# -*- coding: utf-8 -*-
"""Render report-en.html and report-ar.html from doc_data.SECTIONS.

Self-contained (inline CSS, no build step). A light "clinical paper" theme with
NeuroScan accent colors — readable on screen and clean when printed to PDF
(Cmd/Ctrl+P → Save as PDF). Fully RTL-aware for the Arabic edition.

Run:  ../.venv/bin/python build_html.py
"""
import os
import base64
import html as _html

import doc_data
from i18n import tr

HERE = os.path.dirname(__file__)
ASSETS = os.path.join(HERE, "..", "assets")
OUT = os.path.join(HERE, "..")

META = {
    "en": {
        "title": "NeuroScan — Technical Deep-Dive",
        "subtitle": "Explainable Brain-Tumor MRI Classification · ResNet50 → GradCAM → Local-LLM Report",
        "kicker": "Complete Technical Reference",
        "toc": "Contents",
        "disclaimer": "Educational & research prototype — not a medical device. Never use for diagnosis.",
        "dir": "ltr",
    },
    "ar": {
        "title": "NeuroScan — تقرير تقني معمّق",
        "subtitle": "تصنيف قابل للتفسير لأورام الدماغ · ResNet50 ثم GradCAM ثم تقرير بنموذج لغوي محلي",
        "kicker": "مرجع تقني كامل",
        "toc": "المحتويات",
        "disclaimer": "نموذج تعليمي وبحثي — ليس جهازًا طبيًا. لا تستخدمه للتشخيص.",
        "dir": "rtl",
    },
}

CALLOUT_LABEL = {
    "info": {"en": "Note", "ar": "ملاحظة"},
    "warn": {"en": "Important", "ar": "تنبيه مهم"},
    "good": {"en": "Good to know", "ar": "جيد أن تعرف"},
}


def esc(s):
    return _html.escape(s, quote=True)


def img_data_uri(src):
    path = os.path.join(ASSETS, src)
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:image/png;base64,{b64}"


def render_block(b, lang):
    t = b["type"]
    if t == "p":
        return f"<p>{esc(tr(b['text'], lang))}</p>"
    if t == "h":
        return f"<h3>{esc(tr(b['text'], lang))}</h3>"
    if t == "bullets":
        lis = "".join(f"<li>{esc(tr(x, lang))}</li>" for x in b["items"])
        return f"<ul>{lis}</ul>"
    if t == "num":
        lis = "".join(f"<li>{esc(tr(x, lang))}</li>" for x in b["items"])
        return f"<ol>{lis}</ol>"
    if t == "table":
        head = "".join(f"<th>{esc(tr(h, lang))}</th>" for h in b["head"])
        rows = ""
        for r in b["rows"]:
            cells = "".join(f"<td>{esc(tr(c, lang))}</td>" for c in r)
            rows += f"<tr>{cells}</tr>"
        return f"<div class='tablewrap'><table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>"
    if t == "code":
        return f"<pre><code>{esc(b['code'])}</code></pre>"
    if t == "callout":
        lab = CALLOUT_LABEL[b["tone"]][lang]
        title = esc(tr(b["title"], lang))
        text = esc(tr(b["text"], lang))
        return (f"<div class='callout {b['tone']}'>"
                f"<div class='callout-h'><span class='dot'></span>{lab} · {title}</div>"
                f"<div class='callout-b'>{text}</div></div>")
    if t == "image":
        cap = esc(tr(b["caption"], lang)) if b.get("caption") else ""
        capdiv = f"<figcaption>{cap}</figcaption>" if cap else ""
        return f"<figure><img src='{img_data_uri(b['src'])}' alt='{cap}'/>{capdiv}</figure>"
    if t == "kv":
        rows = ""
        for k, v in b["pairs"]:
            rows += (f"<div class='kv-row'><div class='kv-k'>{esc(tr(k, lang))}</div>"
                     f"<div class='kv-v'>{esc(tr(v, lang))}</div></div>")
        return f"<div class='kv'>{rows}</div>"
    return ""


def render_section(s, lang):
    inner = "".join(render_block(b, lang) for b in s["blocks"])
    lead = f"<p class='lead'>{esc(tr(s['lead'], lang))}</p>" if s.get("lead") else ""
    return (f"<section id='{s['id']}'>"
            f"<div class='sec-head'><span class='sec-num'>{s['num']}</span>"
            f"<h2>{esc(tr(s['title'], lang))}</h2></div>"
            f"{lead}{inner}</section>")


def toc(lang):
    items = "".join(
        f"<li><a href='#{s['id']}'><span class='tnum'>{s['num']}</span>"
        f"<span>{esc(tr(s['title'], lang))}</span></a></li>"
        for s in doc_data.SECTIONS)
    return f"<nav class='toc'><h2>{META[lang]['toc']}</h2><ol>{items}</ol></nav>"


CSS = """
:root{
  --ink:#1a2433; --ink-strong:#0b1422; --muted:#5d6b80; --line:#e2e8f2;
  --paper:#ffffff; --paper-2:#f5f8fc; --paper-3:#eef3fa;
  --primary:#0891a8; --accent:#5b54e6; --safe:#0f8a55; --alert:#b9701a;
  --glioma:#d62b6a; --mening:#6d52e6; --pit:#b9701a; --notumor:#0f8a55;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--paper-2);color:var(--ink);
  font:16px/1.65 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  -webkit-print-color-adjust:exact;print-color-adjust:exact;}
.rtl body,body.rtl{font-family:"SF Arabic","Geeza Pro","Tajawal","Cairo","Segoe UI",Tahoma,sans-serif;}
.wrap{max-width:880px;margin:0 auto;padding:0 22px 80px;}
code,pre{font-family:"SF Mono",Consolas,Menlo,monospace;}

/* Cover */
.cover{background:linear-gradient(135deg,#06080f 0%,#0b1730 55%,#10233f 100%);
  color:#eaf2fb;padding:64px 22px 56px;text-align:center;position:relative;overflow:hidden;}
.cover:before{content:"";position:absolute;inset:0;
  background:radial-gradient(60% 80% at 50% 0,rgba(44,212,238,.22),transparent 70%),
             radial-gradient(50% 70% at 100% 100%,rgba(139,123,255,.18),transparent 70%);}
.cover>*{position:relative}
.cover .kicker{letter-spacing:.32em;text-transform:uppercase;font-size:12px;color:#2cd4ee;font-weight:700;}
.cover h1{font-size:54px;margin:14px 0 6px;letter-spacing:-.02em;color:#fff;}
.cover .sub{color:#a9bdd6;font-size:18px;max-width:680px;margin:0 auto;}
.cover .rule{width:80px;height:4px;background:#2cd4ee;margin:22px auto 0;border-radius:3px;}
.cover .pills{margin-top:24px;display:flex;gap:8px;justify-content:center;flex-wrap:wrap;}
.cover .pill{border:1px solid rgba(255,255,255,.18);border-radius:999px;padding:6px 14px;font-size:13px;color:#cfe0f2;}

/* TOC */
.toc{background:var(--paper);border:1px solid var(--line);border-radius:16px;
  padding:22px 26px;margin:34px 0 10px;box-shadow:0 18px 40px -28px rgba(15,28,48,.4);}
.toc h2{margin:.1em 0 .5em;font-size:18px;color:var(--ink-strong);}
.toc ol{list-style:none;margin:0;padding:0;columns:2;column-gap:34px;}
.toc li{break-inside:avoid;margin:5px 0;}
.toc a{text-decoration:none;color:var(--ink);display:flex;gap:10px;align-items:baseline;padding:3px 0;}
.toc a:hover{color:var(--primary);}
.tnum{color:var(--primary);font-weight:700;font-variant-numeric:tabular-nums;min-width:24px;}

/* Sections */
section{background:var(--paper);border:1px solid var(--line);border-radius:16px;
  padding:6px 30px 26px;margin:22px 0;box-shadow:0 18px 40px -30px rgba(15,28,48,.35);}
.sec-head{display:flex;align-items:center;gap:14px;border-bottom:2px solid var(--paper-3);
  padding:22px 0 14px;margin-bottom:8px;}
.sec-num{font-size:15px;font-weight:800;color:#fff;background:var(--primary);
  border-radius:9px;padding:6px 11px;letter-spacing:.04em;}
.rtl .sec-num{background:var(--accent);}
h2{font-size:27px;margin:0;color:var(--ink-strong);letter-spacing:-.01em;}
h3{font-size:18px;margin:26px 0 6px;color:var(--ink-strong);}
.lead{font-size:18px;color:var(--muted);margin:14px 0 6px;}
p{margin:11px 0;}
ul,ol{margin:11px 0;padding-inline-start:24px;}
li{margin:6px 0;}
ul li::marker{color:var(--primary);}
ol li::marker{color:var(--primary);font-weight:700;}

/* Tables */
.tablewrap{overflow-x:auto;margin:16px 0;}
table{width:100%;border-collapse:collapse;font-size:14.5px;}
th,td{text-align:start;padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top;}
thead th{background:var(--paper-3);color:var(--ink-strong);font-weight:700;
  border-bottom:2px solid var(--line);}
tbody tr:nth-child(even){background:var(--paper-2);}

/* Code */
pre{background:#0d1424;color:#d7e3f4;border:1px solid #1d2942;border-radius:12px;
  padding:16px 18px;overflow-x:auto;font-size:13.5px;line-height:1.55;direction:ltr;text-align:left;}

/* Callouts */
.callout{border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin:16px 0;
  border-inline-start:5px solid var(--primary);background:var(--paper-2);break-inside:avoid;}
.callout.info{border-inline-start-color:var(--primary);background:#eef9fb;}
.callout.warn{border-inline-start-color:var(--alert);background:#fdf4e8;}
.callout.good{border-inline-start-color:var(--safe);background:#ecf8f1;}
.callout-h{font-weight:700;color:var(--ink-strong);display:flex;align-items:center;gap:8px;margin-bottom:4px;}
.dot{width:9px;height:9px;border-radius:50%;background:var(--primary);}
.warn .dot{background:var(--alert);} .good .dot{background:var(--safe);}
.callout-b{color:var(--ink);}

/* Figures */
figure{margin:18px 0;text-align:center;break-inside:avoid;}
figure img{max-width:100%;border:1px solid var(--line);border-radius:12px;background:#06080f;}
figcaption{color:var(--muted);font-size:13.5px;margin-top:8px;}

/* Key-value */
.kv{margin:14px 0;border:1px solid var(--line);border-radius:12px;overflow:hidden;}
.kv-row{display:grid;grid-template-columns:34% 66%;}
.kv-row:nth-child(even){background:var(--paper-2);}
.kv-k{font-weight:700;color:var(--ink-strong);padding:11px 14px;border-inline-end:1px solid var(--line);}
.kv-v{padding:11px 14px;color:var(--ink);}

footer{text-align:center;color:var(--muted);font-size:13px;margin-top:34px;padding-top:20px;
  border-top:1px solid var(--line);}

@media print{
  body{background:#fff;font-size:11.5pt;}
  .wrap{max-width:none;padding:0;}
  section,.toc{box-shadow:none;border-color:#d8e0ec;break-inside:avoid;}
  .cover{padding:48px 22px;}
  section{margin:12px 0;}
  a{color:inherit;text-decoration:none;}
  .toc ol{columns:2;}
}
@media (max-width:640px){.toc ol{columns:1;}.kv-row{grid-template-columns:1fr;}.cover h1{font-size:38px;}}
"""


def build(lang):
    m = META[lang]
    pills = ["ResNet50", "GradCAM", "FastAPI", "Next.js", "Ollama", "Docker"]
    pills_html = "".join(f"<span class='pill'>{p}</span>" for p in pills)
    sections = "".join(render_section(s, lang) for s in doc_data.SECTIONS)
    rtlclass = "rtl" if lang == "ar" else ""
    doc = f"""<!doctype html>
<html lang="{lang}" dir="{m['dir']}" class="{rtlclass}">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{esc(m['title'])}</title>
<style>{CSS}</style>
</head>
<body class="{rtlclass}">
<header class="cover">
  <div class="kicker">{esc(m['kicker'])}</div>
  <h1>{esc(m['title'])}</h1>
  <div class="sub">{esc(m['subtitle'])}</div>
  <div class="rule"></div>
  <div class="pills">{pills_html}</div>
</header>
<div class="wrap">
  {toc(lang)}
  {sections}
  <footer>{esc(m['disclaimer'])}</footer>
</div>
</body>
</html>"""
    path = os.path.join(OUT, f"report-{lang}.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"wrote report-{lang}.html  ({len(doc)//1024} KB)")


if __name__ == "__main__":
    build("en")
    build("ar")
