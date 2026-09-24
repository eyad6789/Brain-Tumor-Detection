# -*- coding: utf-8 -*-
"""Extra deep-dive sections, part 2 — AI transcripts, engineering internals,
robustness, security, performance and the technology decision log.

Every prompt, header name, status code, port and file path quoted here is copied
verbatim from the source tree.
"""
from i18n import L

# ── F · AI TRANSCRIPTS ───────────────────────────────────────────────────
TRANSCRIPTS = {
    "id": "transcripts",
    "title": L("AI Transcripts: the Exact Prompts and What Comes Back",
               "نصوص الذكاء الاصطناعي: الموجِّهات الدقيقة وما يعود منها"),
    "lead": L(
        "There is no hidden magic in the report generator. This section prints every instruction the "
        "language model receives, character for character, plus the parameters and the fallbacks.",
        "لا سحر خفيًّا في مولِّد التقارير. يطبع هذا القسم كل تعليمة يتلقّاها النموذج اللغوي حرفًا "
        "بحرف، إضافةً إلى المعاملات والبدائل الاحتياطية."),
    "blocks": [
        {"type": "h", "text": L("Transcript part 1 — the system prompt (verbatim)",
                                "الجزء الأول — موجِّه النظام (حرفيًا)")},
        {"type": "p", "text": L(
            "The system prompt fixes the model's role for the whole conversation. Notice the three "
            "things it enforces: the audience (patients *and* clinicians), the format (GitHub-flavored "
            "Markdown with exactly the requested headings), and the safety rule (always remind the "
            "reader this is educational).",
            "يثبّت موجِّه النظام دور النموذج طوال المحادثة. ولاحظ ثلاثة أمور يفرضها: الجمهور (المرضى "
            "والأطباء معًا)، والصيغة (Markdown بنكهة GitHub وبالعناوين المطلوبة تحديدًا)، وقاعدة "
            "السلامة (تذكير القارئ دائمًا بأن هذا تعليمي).")},
        {"type": "code", "code":
            "You are a careful clinical AI assistant that explains brain-MRI\n"
            "findings in clear, compassionate language for both patients and\n"
            "clinicians, grounded in established radiology and oncology\n"
            "knowledge. Respond in well-structured GitHub-flavored Markdown,\n"
            "using exactly the section headings the user requests. Always\n"
            "remind the reader that your output is for education only and is\n"
            "not a substitute for professional diagnosis."},
        {"type": "h", "text": L("Transcript part 2 — the user prompt template (verbatim)",
                                "الجزء الثاني — قالب موجِّه المستخدم (حرفيًا)")},
        {"type": "code", "code":
            "A ResNet50 MRI brain-tumor classifier produced this result:\n"
            "\n"
            "Primary finding: {tumor_class} ({confidence:.1f}% confidence).\n"
            "Probabilities: Glioma {glioma:.1f}%, Meningioma {meningioma:.1f}%,\n"
            "Pituitary {pituitary:.1f}%, No Tumor {notumor:.1f}%.\n"
            "A GradCAM heatmap highlighted the regions the model focused on.\n"
            "\n"
            "Write a concise clinical report in Markdown with exactly these\n"
            "five sections, 2-4 sentences each:\n"
            "\n"
            "## Diagnosis Summary\n"
            "## About {tumor_class}\n"
            "## What the Heatmap Shows\n"
            "## Recommended Next Steps\n"
            "## Important Disclaimer\n"
            "\n"
            "Write 1-3 short sentences per section and keep the whole report\n"
            "under 230 words. Be accurate, clear, and compassionate. Do not\n"
            "wrap the report in code fences."},
        {"type": "h", "text": L("Transcript part 3 — the same prompt, filled in",
                                "الجزء الثالث — الموجِّه نفسه بعد ملئه")},
        {"type": "p", "text": L(
            "For a scan the classifier called Glioma at 95.1%, the placeholders resolve to this — the "
            "literal text sent to the model:",
            "لصورة صنّفها المُصنِّف بأنها ورم دبقي بنسبة 95.1%، تُحلّ العناصر النائبة إلى هذا — وهو "
            "النص الحرفي المُرسَل إلى النموذج:")},
        {"type": "code", "code":
            "A ResNet50 MRI brain-tumor classifier produced this result:\n"
            "\n"
            "Primary finding: Glioma (95.1% confidence).\n"
            "Probabilities: Glioma 95.1%, Meningioma 3.9%, Pituitary 0.7%,\n"
            "No Tumor 0.3%.\n"
            "A GradCAM heatmap highlighted the regions the model focused on.\n"
            "...(the five required headings follow, unchanged)"},
        {"type": "h", "text": L("Transcript part 4 — the shape of the answer",
                                "الجزء الرابع — شكل الإجابة")},
        {"type": "callout", "tone": "info",
         "title": L("Read this before quoting the example",
                    "اقرأ هذا قبل الاستشهاد بالمثال"),
         "text": L(
            "The block below is a representative example of the output the prompt is engineered to "
            "produce — the five headings, the length limit, the tone. It is not a captured transcript "
            "of one specific run: a language model generates fresh text every time, and the exact "
            "wording will differ on your machine. If a judge asks to see a real one, run the app live "
            "and let it write one in front of them; that is far more convincing than a printed page.",
            "الكتلة أدناه مثال تمثيلي للمخرَج الذي صُمِّم الموجِّه لإنتاجه — العناوين الخمسة، وحدّ "
            "الطول، والنبرة. وليست نصًّا ملتقطًا من تشغيل بعينه: فالنموذج اللغوي يولّد نصًّا جديدًا "
            "في كل مرة، وستختلف الصياغة الدقيقة على جهازك. وإن طلب المُحكِّم رؤية تقرير حقيقي، "
            "فشغّل التطبيق حيًّا ودعه يكتب واحدًا أمامه؛ فذلك أقنع بكثير من صفحة مطبوعة.")},
        {"type": "code", "code":
            "## Diagnosis Summary\n"
            "The classifier identified features consistent with a glioma with\n"
            "95.1% confidence. The remaining probability is distributed across\n"
            "meningioma (3.9%), pituitary (0.7%) and no-tumor (0.3%),\n"
            "indicating a clearly dominant single finding.\n"
            "\n"
            "## About Glioma\n"
            "Gliomas arise from the glial cells that support neurons and range\n"
            "from slow-growing low-grade tumors to aggressive high-grade forms.\n"
            "Grading cannot be determined from this classification alone.\n"
            "\n"
            "## What the Heatmap Shows\n"
            "The GradCAM overlay marks the regions that most influenced the\n"
            "decision. Attention concentrated on the lesion region rather than\n"
            "on image borders or annotations, which is the expected pattern for\n"
            "a reliable prediction.\n"
            "\n"
            "## Recommended Next Steps\n"
            "Review by a qualified radiologist, correlation with the full MRI\n"
            "series, and consideration of contrast-enhanced imaging or biopsy\n"
            "where clinically indicated.\n"
            "\n"
            "## Important Disclaimer\n"
            "This report is generated by an experimental educational system. It\n"
            "is not a medical diagnosis and must not be used to guide treatment."},
        {"type": "h", "text": L("The generation parameters — and why each value",
                                "معاملات التوليد — ولماذا كل قيمة")},
        {"type": "table",
         "head": [L("Parameter", "المعامل"), L("Value", "القيمة"), L("Why", "لماذا")],
         "rows": [
            [L("model", "النموذج"), L("qwen2.5:1.5b-instruct-q4_K_M (default)",
                                      "qwen2.5:1.5b-instruct-q4_K_M (الافتراضي)"),
             L("A small, 4-bit quantized instruct model that runs on ~4 GB of memory and formats "
               "Markdown cleanly. Override with OLLAMA_MODEL — e.g. `meditron`, a 7B model trained on "
               "PubMed and clinical guidelines, which is more medically knowledgeable but much slower "
               "on modest hardware.",
               "نموذج تعليمات صغير مُكمَّم بأربع بتّات يعمل بنحو 4 غيغابايت من الذاكرة وينسّق Markdown "
               "بنظافة. ويمكن تجاوزه بـOLLAMA_MODEL — مثل `meditron`، وهو نموذج بسبعة مليارات معامل "
               "مُدرَّب على PubMed والأدلة السريرية، أغزر معرفةً طبيةً لكنه أبطأ بكثير على العتاد "
               "المتواضع.")],
            [L("temperature", "الحرارة"), L("0.3", "0.3"),
             L("Low. Temperature controls randomness; near 0 the model picks the most likely word "
               "almost every time. For medical text we want repeatable, factual phrasing, not "
               "creativity.",
               "منخفضة. تتحكّم الحرارة في العشوائية؛ وقرب الصفر يختار النموذج الكلمة الأرجح في كل مرة "
               "تقريبًا. وفي النص الطبي نريد صياغة واقعية قابلة للتكرار، لا إبداعًا.")],
            [L("num_predict", "num_predict"), L("520 tokens (OLLAMA_NUM_PREDICT)",
                                                "520 رمزًا (OLLAMA_NUM_PREDICT)"),
             L("A hard cap on output length. Roughly matches the 230-word instruction and stops a "
               "runaway generation from hanging a CPU-only server.",
               "حدّ صارم لطول المخرَج. يوافق تقريبًا تعليمة الـ230 كلمة ويمنع توليدًا جامحًا من تعليق "
               "خادم يعمل بالمعالج فقط.")],
            [L("num_ctx", "num_ctx"), L("2048 tokens", "2048 رمزًا"),
             L("The context window. Our prompt is a few hundred tokens, so a small window is enough "
               "and uses much less memory.",
               "نافذة السياق. وموجِّهنا بضع مئات من الرموز، فنافذة صغيرة تكفي وتستهلك ذاكرة أقل بكثير.")],
        ]},
        {"type": "h", "text": L("Post-processing and failure handling",
                                "المعالجة اللاحقة ومعالجة الإخفاق")},
        {"type": "p", "text": L(
            "Some models wrap their entire answer in a ```markdown fence, which would render as a grey "
            "code block instead of a formatted report. A helper, _strip_code_fence, unwraps exactly "
            "one enclosing fence if it finds it. Beyond that, every failure mode returns readable "
            "instructions instead of a stack trace:",
            "تُغلِّف بعض النماذج إجابتها كلها بسياج ```markdown، فتُعرَض ككتلة شيفرة رمادية بدل تقرير "
            "منسَّق. ويقوم مساعدٌ اسمه _strip_code_fence بإزالة سياج واحد مُحيط إن وجده. وفيما عدا "
            "ذلك، يُعيد كل نمط إخفاق تعليمات مقروءة بدل أثر خطأ برمجي:")},
        {"type": "table",
         "head": [L("What went wrong", "ما الخطأ"), L("What the user sees", "ما يراه المستخدم")],
         "rows": [
            [L("The `ollama` Python package is not installed.", "حزمة `ollama` لبايثون غير مثبَّتة."),
             L("A short block showing `pip install ollama` and the Ollama install command.",
               "كتلة قصيرة تُظهر `pip install ollama` وأمر تثبيت Ollama.")],
            [L("The Ollama server is not running.", "خادم Ollama لا يعمل."),
             L("\"Ollama server is not running\" plus `ollama serve`.",
               "«خادم Ollama لا يعمل» مع `ollama serve`.")],
            [L("The configured model was never pulled.", "النموذج المُهيَّأ لم يُنزَّل قط."),
             L("\"Model '<name>' not found in Ollama\" plus the exact `ollama pull <name>` command.",
               "«النموذج '<الاسم>' غير موجود في Ollama» مع أمر `ollama pull <الاسم>` بالضبط.")],
            [L("Any other exception.", "أي استثناء آخر."),
             L("\"Report generation failed: …\" — the app keeps working; only the report panel is "
               "affected.",
               "«فشل توليد التقرير: …» — ويستمرّ التطبيق في العمل؛ ولا يتأثر سوى لوحة التقرير.")],
        ]},
        {"type": "callout", "tone": "warn",
         "title": L("The honest limitation of the report",
                    "الحدّ الصادق للتقرير"),
         "text": L(
            "The language model never sees the MRI. It receives only four numbers and a class name. "
            "It is therefore a communication layer that puts the classifier's output into readable "
            "clinical language — it is not a second opinion, and it cannot detect anything the "
            "classifier missed. Saying this clearly before a judge asks is worth more than any "
            "feature.",
            "لا يرى النموذج اللغوي صورة الرنين إطلاقًا، بل يتلقّى أربعة أرقام واسم فئة فقط. فهو إذًا "
            "طبقة تواصل تضع مخرَج المُصنِّف في لغة سريرية مقروءة — وليس رأيًا ثانيًا، ولا يستطيع كشف "
            "أي شيء فات المُصنِّف. وقول هذا بوضوح قبل أن يسأل المُحكِّم يساوي أكثر من أي ميزة.")},
    ],
}

# ── G · AI-ASSISTED DEVELOPMENT ──────────────────────────────────────────
AI_DEV = {
    "id": "aidev",
    "title": L("How the Project Itself Was Built with AI Assistance",
               "كيف بُني المشروع نفسه بمساعدة الذكاء الاصطناعي"),
    "lead": L(
        "There are two kinds of AI in this repository: the AI inside the product, and the AI used to "
        "build the product. Both are documented in the code, and a judge is entitled to ask about "
        "either.",
        "في هذا المستودع نوعان من الذكاء الاصطناعي: الذكاء داخل المنتج، والذكاء المستخدَم في بناء "
        "المنتج. وكلاهما موثَّق في الشيفرة، وللمُحكِّم أن يسأل عن أيّهما."),
    "blocks": [
        {"type": "p", "text": L(
            "The repository contains CLAUDE.md at the root and AGENTS.md inside frontend/ — instruction "
            "files that configure an AI coding assistant working on this codebase. They are not "
            "decoration; they encode the project's hard-won rules so that neither a human nor an "
            "assistant can break them by accident.",
            "يحتوي المستودع على CLAUDE.md في الجذر و AGENTS.md داخل frontend/ — وهما ملفا تعليمات "
            "يضبطان مساعد برمجة بالذكاء الاصطناعي يعمل على هذه الشيفرة. وليسا زينةً، بل يرمّزان "
            "قواعد المشروع المكتسَبة بجهد حتى لا يكسرها إنسان ولا مساعد عن غير قصد.")},
        {"type": "h", "text": L("What CLAUDE.md actually pins down", "ما الذي يثبّته CLAUDE.md فعلًا")},
        {"type": "bullets", "items": [
            L("The class index order (pituitary=0, notumor=1, meningioma=2, glioma=3) is fixed "
              "everywhere, because the trained weights depend on it. Reordering it silently would "
              "swap every label.",
              "ترتيب فهارس الفئات (pituitary=0 و notumor=1 و meningioma=2 و glioma=3) ثابت في كل "
              "مكان، لأن الأوزان المدرَّبة تعتمد عليه. وإعادة ترتيبه بصمت ستبدّل كل تسمية."),
            L("The duplicate Dropout(0.3) in the inference head is intentional and must not be "
              "\"cleaned up\" — with an explicit warning that train.py's BatchNorm head will not load "
              "the shipped weights.",
              "تكرار Dropout(0.3) في رأس الاستدلال مقصود ولا يجوز «تنظيفه» — مع تحذير صريح بأن رأس "
              "train.py ذا BatchNorm لن يحمّل الأوزان المُسلَّمة."),
            L("The accuracy figure must keep the word \"claimed\" and its caveat, in the API, in the "
              "UI, and in every document.",
              "يجب أن يحتفظ رقم الدقة بكلمة «مُعلَنة» وبتنبيهها، في الـAPI وفي الواجهة وفي كل مستند."),
            L("A do-not-read list — the 98 MB weights file, node_modules/, the virtual environments, "
              "the 2.8 MB legacy notebook — so tooling never wastes effort on generated artifacts.",
              "قائمة «لا تُقرأ» — ملف الأوزان بحجم 98 ميغابايت، و node_modules/، والبيئات "
              "الافتراضية، والدفتر القديم بحجم 2.8 ميغابايت — حتى لا تُهدَر الأدوات جهدها على مخرجات "
              "مولَّدة."),
        ]},
        {"type": "h", "text": L("What AGENTS.md pins down", "ما الذي يثبّته AGENTS.md")},
        {"type": "p", "text": L(
            "One short, sharp rule: this is Next.js 16, which has breaking changes relative to what a "
            "model trained on older material would assume, so the local documentation in "
            "node_modules/next/dist/docs/ must be consulted before writing Next-specific code. It is a "
            "neat illustration of the real risk of AI-assisted development — confidently outdated "
            "answers — and of the correct mitigation: point the tool at the ground truth.",
            "قاعدة واحدة قصيرة وحادّة: هذا Next.js 16، وفيه تغييرات كاسرة مقارنةً بما يفترضه نموذج "
            "مُدرَّب على مواد أقدم، فيجب مراجعة التوثيق المحلي في node_modules/next/dist/docs/ قبل "
            "كتابة شيفرة خاصة بـNext. وهي صورة أنيقة للخطر الحقيقي في التطوير بمساعدة الذكاء "
            "الاصطناعي — إجابات قديمة تُقال بثقة — وللعلاج الصحيح: وجِّه الأداة إلى المصدر "
            "الموثوق.")},
        {"type": "h", "text": L("The workflow that was actually used", "سير العمل المُتَّبع فعليًا")},
        {"type": "num", "items": [
            L("A human decides the goal and the architecture — what to build and why.",
              "يقرّر الإنسان الهدف والمعمارية — ماذا يُبنى ولماذا."),
            L("The assistant drafts the implementation, guided by the rules in CLAUDE.md.",
              "يصوغ المساعد التنفيذ مسترشدًا بقواعد CLAUDE.md."),
            L("A review pass reads the result critically — this is where the data-leakage problem in "
              "train.py was identified and written up rather than buried.",
              "تقرأ جولة مراجعة النتيجةَ بعين ناقدة — وهنا اكتُشفت مشكلة تسريب البيانات في train.py "
              "وكُتبت صراحةً بدل دفنها."),
            L("Anything the review discovers becomes a new permanent rule in CLAUDE.md, so the same "
              "mistake cannot recur.",
              "كل ما تكتشفه المراجعة يصير قاعدةً دائمة جديدة في CLAUDE.md، فلا يتكرّر الخطأ نفسه."),
            L("This documentation package itself is generated from a single bilingual data file, so "
              "the English and Arabic editions can never drift apart.",
              "وهذه الحزمة التوثيقية نفسها مولَّدة من ملف بيانات ثنائي اللغة واحد، فلا تتباعد "
              "النسختان الإنجليزية والعربية أبدًا."),
        ]},
        {"type": "callout", "tone": "good",
         "title": L("If a judge asks \"did AI write this?\"",
                    "إن سأل مُحكِّم: «هل كتب الذكاءُ الاصطناعي هذا؟»"),
         "text": L(
            "Answer directly and without defensiveness: yes, an AI assistant was used as a tool, the "
            "same way a compiler or a linter is a tool, and the repository documents exactly how — "
            "that is what CLAUDE.md and AGENTS.md are. The engineering judgement is human and "
            "demonstrable: the decision to split Gradio into FastAPI + Next.js, the extraction of "
            "inference_core.py to stop the training and serving heads from drifting, the "
            "INFERENCE_LOCK around non-thread-safe GradCAM hooks, and above all the decision to "
            "publish the data-leakage flaw instead of quietly reporting 99%. A team that hides its "
            "tools looks weaker than a team that documents them.",
            "أجب مباشرةً وبلا دفاعية: نعم، استُخدم مساعد ذكاء اصطناعي أداةً، تمامًا كما أن المُصرِّف "
            "أو المُدقِّق أداة، والمستودع يوثّق كيف بالضبط — وهذا ما يمثّله CLAUDE.md و AGENTS.md. "
            "أما الحُكم الهندسي فبشري وقابل للإثبات: قرار تقسيم Gradio إلى FastAPI و Next.js، "
            "واستخراج inference_core.py لمنع تباعد رأسَي التدريب والخدمة، و INFERENCE_LOCK حول "
            "خطّافات GradCAM غير الآمنة للخيوط، وقبل ذلك كله قرار نشر خلل تسريب البيانات بدل "
            "الإبلاغ الصامت عن 99%. والفريق الذي يخفي أدواته يبدو أضعف من الفريق الذي يوثّقها.")},
    ],
}

# ── H · REQUEST LIFECYCLE ────────────────────────────────────────────────
LIFECYCLE = {
    "id": "lifecycle",
    "title": L("One Request, End to End", "طلب واحد من أوله إلى آخره"),
    "lead": L(
        "Follow a single MRI from the moment it is dropped on the page to the moment the report "
        "appears — through every function, in order.",
        "تتبّع صورة رنين واحدة من لحظة إفلاتها على الصفحة إلى لحظة ظهور التقرير — عبر كل دالة "
        "بالترتيب."),
    "blocks": [
        {"type": "num", "items": [
            L("The user drops a file on UploadDropzone. The browser checks it client-side: MIME type "
              "must be PNG/JPEG/WEBP/BMP and size at most 10 MB. A local object URL is created for the "
              "preview — the file is not uploaded yet.",
              "يُفلِت المستخدم ملفًا على UploadDropzone. ويفحصه المتصفح محليًا: يجب أن يكون نوع MIME "
              "من PNG/JPEG/WEBP/BMP وألا يتجاوز الحجم 10 ميغابايت. ويُنشَأ عنوان كائن محلي للمعاينة — "
              "ولم يُرفَع الملف بعد."),
            L("The user presses Analyze. AnalyzeWorkspace aborts any in-flight request via an "
              "AbortController, then calls predict() in lib/api.ts.",
              "يضغط المستخدم «تحليل». فتُلغي AnalyzeWorkspace أي طلب جارٍ عبر AbortController، ثم "
              "تنادي predict() في lib/api.ts."),
            L("predict() builds a FormData with the file and POSTs it to /api/predict. It deliberately "
              "does not set a Content-Type header, so the browser can generate the multipart boundary "
              "itself.",
              "تبني predict() كائن FormData بالملف وترسله بطريقة POST إلى /api/predict. ولا تضبط "
              "عمدًا ترويسة Content-Type، ليولّد المتصفح حدّ multipart بنفسه."),
            L("In production the request reaches nginx on port 8086, which routes anything under /api "
              "to the backend container and everything else to the frontend container. In development "
              "the browser calls the backend directly, using NEXT_PUBLIC_API_BASE.",
              "في الإنتاج يصل الطلب إلى nginx على المنفذ 8086، فيوجّه كل ما تحت /api إلى حاوية الخادم "
              "وكل ما عداه إلى حاوية الواجهة. وفي التطوير ينادي المتصفح الخادم مباشرةً مستخدمًا "
              "NEXT_PUBLIC_API_BASE."),
            L("FastAPI receives the upload. If app.state.model is None (loading failed at startup) it "
              "returns 503 model_not_loaded immediately, with the original error message.",
              "يستقبل FastAPI الملف المرفوع. فإن كان app.state.model يساوي None (أي فشل التحميل عند "
              "الإقلاع) أعاد فورًا 503 model_not_loaded مع رسالة الخطأ الأصلية."),
            L("load_upload_image() validates the bytes server-side: not empty, at most 15 MB, an "
              "allowed content type, and — crucially — Image.verify() must actually succeed, so a "
              "renamed .exe cannot pass as a PNG. Failures raise ImageValidationError and are turned "
              "into 413 / 415 / 422 by a global exception handler.",
              "تتحقّق load_upload_image() من البايتات على الخادم: غير فارغة، وبحد أقصى 15 ميغابايت، "
              "ونوع محتوى مسموح، والأهم أن تنجح Image.verify() فعلًا، فلا يمرّ ملف .exe أُعيدت "
              "تسميته بوصفه PNG. وترفع الإخفاقات ImageValidationError ويحوّلها معالج استثناءات عام "
              "إلى 413 أو 415 أو 422."),
            L("The heavy work is pushed to a threadpool with run_in_executor, so the async event loop "
              "is never blocked; inside it, INFERENCE_LOCK serializes access because GradCAM registers "
              "backward hooks on the shared model that are not thread-safe.",
              "يُدفَع العمل الثقيل إلى مجمع خيوط عبر run_in_executor، فلا تُحجَب حلقة الأحداث "
              "اللاتزامنية أبدًا؛ وداخله يُسلسِل INFERENCE_LOCK الوصول لأن GradCAM يسجّل خطّافات "
              "خلفية على النموذج المشترك غير آمنة للخيوط."),
            L("predict_core() converts to RGB, applies TRANSFORM (resize 224 × 224 → tensor → ImageNet "
              "normalize), adds a batch dimension, and runs the forward pass under torch.no_grad().",
              "تحوّل predict_core() الصورة إلى RGB، وتطبّق TRANSFORM (تحجيم 224×224 ثم موتِّر ثم "
              "تطبيع ImageNet)، وتضيف بُعد الدفعة، وتنفّذ التمريرة الأمامية تحت torch.no_grad()."),
            L("Softmax converts the 4 logits into probabilities; the highest becomes the top class and "
              "a Markdown verdict string is built from it.",
              "يحوّل softmax اللوغيتات الأربعة إلى احتمالات؛ ويصير الأعلى الفئة الأولى ويُبنى منها نص "
              "حُكم بصيغة Markdown."),
            L("generate_gradcam() re-runs the model with gradients enabled on layer4[-1], with "
              "aug_smooth and eigen_smooth on, and blends the resulting 224 × 224 heatmap over the "
              "original scan.",
              "تُعيد generate_gradcam() تشغيل النموذج مع تفعيل التدرّجات على layer4[-1] وبتشغيل "
              "aug_smooth و eigen_smooth، وتمزج الخريطة الحرارية الناتجة 224×224 فوق الصورة الأصلية."),
            L("numpy_to_data_url() encodes that array as a base64 PNG data URL, so the browser can "
              "display it with no second request and nothing is ever written to disk.",
              "تُرمِّز numpy_to_data_url() تلك المصفوفة كعنوان بيانات PNG بترميز base64، فيعرضها "
              "المتصفح بلا طلب ثانٍ ولا يُكتب شيء على القرص أبدًا."),
            L("A Pydantic PredictResponse is validated and serialized; probabilities are sorted "
              "descending so the UI can render them in display order without re-sorting.",
              "يُتحقَّق من PredictResponse بواسطة Pydantic ويُسلسَل؛ وتُرتَّب الاحتمالات تنازليًا "
              "لتعرضها الواجهة بترتيب العرض دون إعادة ترتيب."),
            L("lib/api.ts maps the snake_case JSON to camelCase types; React state moves to "
              "{status:'success'} and PredictionResult, ConfidenceBar and GradCamViewer render.",
              "تُحوِّل lib/api.ts صيغة snake_case في JSON إلى أنواع camelCase؛ وتنتقل حالة React إلى "
              "{status:'success'} وتُعرَض PredictionResult و ConfidenceBar و GradCamViewer."),
            L("Immediately afterwards, runReport() fires a second call to /api/report with the class "
              "and the four scores — but only if /api/health reported that Ollama is actually "
              "available. Otherwise the panel shows setup instructions instead of spinning forever.",
              "وفور ذلك تُطلِق runReport() نداءً ثانيًا إلى /api/report بالفئة والدرجات الأربع — لكن "
              "فقط إن أفاد /api/health بأن Ollama متاح فعلًا. وإلا عرضت اللوحة تعليمات الإعداد بدل "
              "الدوران إلى الأبد."),
            L("The report call runs in the threadpool too, streams back Markdown, and ReportPanel "
              "renders it with react-markdown + remark-gfm.",
              "يعمل نداء التقرير في مجمع الخيوط أيضًا، ويعيد Markdown، وتعرضه ReportPanel بواسطة "
              "react-markdown مع remark-gfm."),
        ]},
        {"type": "h", "text": L("Where the time goes", "أين يذهب الوقت")},
        {"type": "table",
         "head": [L("Stage", "المرحلة"), L("Typical cost", "التكلفة النمطية"), L("Note", "ملاحظة")],
         "rows": [
            [L("Upload + validation", "الرفع والتحقّق"), L("milliseconds", "أجزاء من الألف من الثانية"),
             L("A typical MRI JPEG is well under 100 KB.", "صورة الرنين النمطية بصيغة JPEG أقل بكثير من 100 كيلوبايت.")],
            [L("Classification forward pass", "التمريرة الأمامية للتصنيف"),
             L("well under a second on CPU", "أقل من ثانية بكثير على المعالج"),
             L("One image, batch size 1, no gradients.", "صورة واحدة، وحجم دفعة 1، وبلا تدرّجات.")],
            [L("GradCAM", "GradCAM"), L("the dominant cost of /predict", "التكلفة الغالبة في /predict"),
             L("aug_smooth runs the model over several augmented copies and eigen_smooth adds a "
               "decomposition — both are enabled deliberately, trading speed for a cleaner, more "
               "trustworthy map. Pass ?gradcam=false to skip it entirely.",
               "يشغّل aug_smooth النموذج على عدّة نسخ مُزادة ويضيف eigen_smooth تحليلًا — وكلاهما "
               "مُفعَّل عمدًا، مقايضةً للسرعة بخريطة أنظف وأجدر بالثقة. ومرِّر ?gradcam=false لتخطّيه "
               "تمامًا.")],
            [L("LLM report", "تقرير النموذج اللغوي"), L("~15 s on GPU · 1–2 min on CPU",
                                                        "نحو 15 ثانية على كرت الرسوم · دقيقة إلى دقيقتين على المعالج"),
             L("This is why the frontend bypasses the Next.js proxy, whose ~30 s timeout would cut a "
               "slow CPU report off mid-sentence.",
               "ولهذا تتجاوز الواجهة وكيل Next.js، إذ ستقطع مهلته البالغة نحو 30 ثانية تقريرًا بطيئًا "
               "على المعالج في منتصف الجملة.")],
        ]},
    ],
}

# ── I · FRONTEND COMPONENT INVENTORY ─────────────────────────────────────
COMPONENTS = {
    "id": "components",
    "title": L("Frontend Component Inventory", "جرد مكوّنات الواجهة"),
    "lead": L(
        "Thirty-two TypeScript files, about 2,600 lines. Every one of them, and what it is for.",
        "اثنان وثلاثون ملف TypeScript، بنحو 2600 سطر. وإليك كلًّا منها ووظيفته."),
    "blocks": [
        {"type": "h", "text": L("Pages (App Router)", "الصفحات (App Router)")},
        {"type": "table",
         "head": [L("File", "الملف"), L("Purpose", "الغرض")],
         "rows": [
            [L("app/layout.tsx", "app/layout.tsx"),
             L("The root shell: fonts (Geist + Bricolage Grotesque), ThemeProvider, PaletteProvider, "
               "Navbar and Footer.",
               "الغلاف الجذري: الخطوط (Geist و Bricolage Grotesque)، و ThemeProvider، و "
               "PaletteProvider، وشريط التنقّل والتذييل.")],
            [L("app/page.tsx", "app/page.tsx"),
             L("The landing page — hero, the three-pillar pipeline, the four class cards.",
               "صفحة الهبوط — الواجهة البارزة، وخط المعالجة بركائزه الثلاث، وبطاقات الفئات الأربع.")],
            [L("app/analyze/page.tsx", "app/analyze/page.tsx"),
             L("A thin wrapper that mounts AnalyzeWorkspace.", "غلاف رفيع يركّب AnalyzeWorkspace.")],
            [L("app/metrics/page.tsx", "app/metrics/page.tsx"),
             L("Mounts MetricsDashboard.", "يركّب MetricsDashboard.")],
            [L("app/about/page.tsx", "app/about/page.tsx"),
             L("How it works, plus the honest list of limitations.",
               "كيف يعمل، مع القائمة الصادقة بالحدود.")],
            [L("app/globals.css", "app/globals.css"),
             L("398 lines: the entire design system as CSS custom properties — light and dark "
               "palettes, four accent palettes, per-class colors, panel/eyebrow/skeleton utilities.",
               "‏398 سطرًا: نظام التصميم كاملًا كخصائص CSS مخصَّصة — لوحتان فاتحة وداكنة، وأربع لوحات "
               "لألوان التمييز، وألوان لكل فئة، وأدوات panel و eyebrow و skeleton.")],
        ]},
        {"type": "h", "text": L("The analyze workspace", "مساحة عمل التحليل")},
        {"type": "table",
         "head": [L("Component", "المكوّن"), L("Purpose", "الغرض")],
         "rows": [
            [L("AnalyzeWorkspace (243 lines)", "AnalyzeWorkspace ‏(243 سطرًا)"),
             L("The orchestrator. Holds the file, the preview URL and two AsyncState machines "
               "(idle → loading → success | error | unavailable) for prediction and report; owns two "
               "AbortControllers and revokes object URLs on unmount so nothing leaks.",
               "المنسِّق. يحتفظ بالملف وعنوان المعاينة وآلتَي حالة AsyncState ‏(خامل ← تحميل ← نجاح | "
               "خطأ | غير متاح) للتنبؤ والتقرير؛ ويملك متحكّمَي إلغاء ويُبطل عناوين الكائنات عند "
               "التفكيك فلا يتسرّب شيء.")],
            [L("UploadDropzone (143)", "UploadDropzone ‏(143)"),
             L("Drag-and-drop plus a file picker, with client-side type and 10 MB size checks and "
               "inline error messages.",
               "سحب وإفلات مع منتقي ملفات، وفحوص نوع وحجم (10 ميغابايت) على العميل، ورسائل خطأ "
               "مضمّنة.")],
            [L("PredictionResult (105)", "PredictionResult ‏(105)"),
             L("The verdict card: top class, confidence, and the four ConfidenceBars in class color.",
               "بطاقة الحُكم: الفئة الأولى ونسبة الثقة وأشرطة الثقة الأربعة بلون كل فئة.")],
            [L("ConfidenceBar (57)", "ConfidenceBar ‏(57)"),
             L("One animated probability bar, colored by CSS custom property per class.",
               "شريط احتمال متحرّك واحد، ملوَّن بخاصية CSS مخصَّصة لكل فئة.")],
            [L("GradCamViewer (156)", "GradCamViewer ‏(156)"),
             L("Two viewing modes — Split (original beside heatmap) and Overlay with an opacity "
               "slider defaulting to 0.6. If grad-cam is unavailable it shows the original with a "
               "one-line setup hint instead of a broken image.",
               "وضعا عرض — «مُقسَّم» (الأصل بجانب الخريطة الحرارية) و«تراكب» بمنزلق شفافية افتراضيّته "
               "0.6. وإن كان grad-cam غير متاح عرض الأصل مع تلميح إعداد من سطر واحد بدل صورة "
               "مكسورة.")],
            [L("ReportPanel (100)", "ReportPanel ‏(100)"),
             L("Renders the Markdown report; shows a skeleton while generating, a retry button on "
               "error, and setup instructions when Ollama is absent.",
               "يعرض تقرير Markdown؛ ويُظهر هيكلًا أثناء التوليد، وزرّ إعادة محاولة عند الخطأ، "
               "وتعليمات إعداد عند غياب Ollama.")],
        ]},
        {"type": "h", "text": L("Metrics, layout, shared and theme", "المقاييس والتخطيط والمشترك والسمات")},
        {"type": "table",
         "head": [L("Component", "المكوّن"), L("Purpose", "الغرض")],
         "rows": [
            [L("MetricsDashboard (96)", "MetricsDashboard ‏(96)"),
             L("Fetches /api/metrics on mount, shows skeletons while loading, and renders the caveat "
               "banner above everything else.",
               "يجلب /api/metrics عند التركيب، ويعرض هياكل أثناء التحميل، ويعرض شريط التنبيه فوق كل "
               "شيء.")],
            [L("LearningCurves (155)", "LearningCurves ‏(155)"),
             L("Accuracy and loss curves drawn by hand as inline SVG paths — no charting library, so "
               "the bundle stays small and the colors follow the theme automatically.",
               "منحنيات الدقة والخسارة مرسومة يدويًا كمسارات SVG مضمّنة — بلا مكتبة رسوم، فتبقى "
               "الحزمة صغيرة وتتبع الألوان السمة تلقائيًا.")],
            [L("ConfusionMatrix (77) · PerClassTable (34) · StatCard (41)",
               "ConfusionMatrix ‏(77) · PerClassTable ‏(34) · StatCard ‏(41)"),
             L("The confusion matrix renders an explicit empty state, because the API honestly "
               "returns null rather than inventing one.",
               "تعرض مصفوفة الالتباس حالة فراغ صريحة، لأن الـAPI يُعيد بصدق قيمة فارغة بدل اختلاق "
               "مصفوفة.")],
            [L("Navbar (128) · Footer (56) · Logo · PageHeader",
               "Navbar ‏(128) · Footer ‏(56) · Logo · PageHeader"),
             L("Navigation shell, brand mark and page headings.",
               "غلاف التنقّل وعلامة الهوية وعناوين الصفحات.")],
            [L("HealthPill + useHealth (69)", "HealthPill مع useHealth ‏(69)"),
             L("Polls /api/health and shows a live status pill: model loaded, device (CPU/GPU), and "
               "whether GradCAM and Ollama are available. This is what lets every other component "
               "degrade gracefully instead of failing.",
               "يستطلع /api/health ويعرض شارة حالة حيّة: هل حُمِّل النموذج، وما الجهاز (معالج/كرت "
               "رسوم)، وهل يتوفّر GradCAM و Ollama. وهذا ما يتيح لكل مكوّن آخر التراجع بأمان بدل "
               "الفشل.")],
            [L("DisclaimerBanner · ClassCard · Ticks · MarkdownView",
               "DisclaimerBanner · ClassCard · Ticks · MarkdownView"),
             L("The safety banner (shown on every analysis), per-class info cards, the radiological "
               "tick marks that frame the viewer, and the Markdown renderer.",
               "شريط السلامة (يظهر في كل تحليل)، وبطاقات معلومات الفئات، وعلامات التدريج الإشعاعية "
               "التي تؤطّر العارض، وعارض Markdown.")],
            [L("ThemeProvider / ThemeToggle · PaletteProvider / PaletteToggle",
               "ThemeProvider و ThemeToggle · PaletteProvider و PaletteToggle"),
             L("Dark/light via next-themes, plus four switchable accent palettes (cyan, rose, violet, "
               "emerald) persisted to localStorage and applied by an inline script before first paint "
               "so there is no flash of the wrong theme.",
               "الداكن والفاتح عبر next-themes، مع أربع لوحات تمييز قابلة للتبديل (سماوي ووردي "
               "وبنفسجي وزمرّدي) تُحفظ في localStorage ويطبّقها سكربت مضمّن قبل أول رسم فلا يومض "
               "التطبيق بالسمة الخاطئة.")],
        ]},
        {"type": "callout", "tone": "info",
         "title": L("A deliberate 10 MB vs 15 MB mismatch",
                    "تباين مقصود بين 10 و15 ميغابايت"),
         "text": L(
            "The browser rejects files above 10 MB; the server rejects files above 15 MB. That is not "
            "a bug — the client limit is a fast, friendly guard, and the server limit is the real "
            "security boundary, set slightly higher so a legitimate borderline file is never lost to "
            "a rounding difference. Client-side validation is convenience; server-side validation is "
            "the one that counts, because anyone can call the API directly with curl.",
            "يرفض المتصفح الملفات فوق 10 ميغابايت، ويرفض الخادم ما فوق 15 ميغابايت. وليس هذا خطأً — "
            "فحدّ العميل حارس سريع ولطيف، وحدّ الخادم هو الحدّ الأمني الحقيقي، ووُضع أعلى قليلًا "
            "حتى لا يضيع ملف مشروع على الحافة بسبب فرق تقريب. فالتحقّق على العميل رفاهية، والتحقّق "
            "على الخادم هو المُعتبَر، لأن بإمكان أي أحد مناداة الـAPI مباشرةً بـcurl.")},
    ],
}

# ── J · ROBUSTNESS ───────────────────────────────────────────────────────
ROBUSTNESS = {
    "id": "robustness",
    "title": L("Error Handling, Edge Cases & Robustness",
               "معالجة الأخطاء والحالات الحدّية والمتانة"),
    "lead": L(
        "What separates a demo from a product is what happens when something goes wrong. Here is "
        "every failure this system anticipates, and exactly what it does.",
        "ما يفصل العرض التجريبي عن المنتج هو ما يحدث حين يسوء شيء. وإليك كل إخفاق يتوقّعه هذا "
        "النظام، وما يفعله بالضبط."),
    "blocks": [
        {"type": "table",
         "head": [L("Failure", "الإخفاق"), L("Detected where", "أين يُكتشَف"),
                  L("Behaviour", "السلوك"), L("Status", "الرمز")],
         "rows": [
            [L("Weights file missing or corrupt at startup", "ملف الأوزان مفقود أو معطوب عند الإقلاع"),
             L("lifespan handler", "معالج lifespan"),
             L("The API still starts; the error is stored and reported through /api/health, and "
               "/api/predict returns a clear message. The legacy Gradio app, by contrast, raises at "
               "import time and refuses to start at all — a deliberate improvement.",
               "يقلع الـAPI رغم ذلك؛ ويُخزَّن الخطأ ويُبلَّغ عنه عبر /api/health، ويُعيد /api/predict "
               "رسالة واضحة. أما تطبيق Gradio القديم فيرفع استثناءً عند الاستيراد ويرفض الإقلاع "
               "أصلًا — وهذا تحسين مقصود."),
             L("503 model_not_loaded", "503 model_not_loaded")],
            [L("Checkpoint head does not match the architecture",
               "رأس ملف الأوزان لا يطابق المعمارية"),
             L("load_model()", "load_model()"),
             L("A strict load is attempted first; on mismatch it retries non-strict, but if fc.1 or "
               "fc.5 — the two layers that actually carry weights — are missing it raises loudly. A "
               "silently half-loaded head would produce plausible-looking garbage, which is the most "
               "dangerous failure mode in a medical tool.",
               "تُجرَّب قراءة صارمة أولًا، وعند عدم التطابق تُعاد المحاولة بغير صرامة، لكن إن كانت "
               "fc.1 أو fc.5 — الطبقتان الحاملتان للأوزان فعلًا — مفقودةً رفعت خطأً صريحًا. فالرأس "
               "المُحمَّل نصفيًا بصمت سيُنتج هراءً يبدو معقولًا، وهو أخطر أنماط الإخفاق في أداة "
               "طبية."),
             L("RuntimeError", "RuntimeError")],
            [L("Empty file uploaded", "ملف مرفوع فارغ"), L("load_upload_image()", "load_upload_image()"),
             L("Rejected before any model work.", "يُرفض قبل أي عمل للنموذج."), L("422 empty_file", "422 empty_file")],
            [L("File larger than 15 MB", "ملف أكبر من 15 ميغابايت"), L("load_upload_image()", "load_upload_image()"),
             L("Rejected; protects memory on a shared box.", "يُرفض؛ ويحمي الذاكرة على جهاز مشترك."),
             L("413 file_too_large", "413 file_too_large")],
            [L("Wrong content type (PDF, video, executable)", "نوع محتوى خاطئ (PDF أو فيديو أو تنفيذي)"),
             L("load_upload_image()", "load_upload_image()"),
             L("Rejected by MIME allow-list.", "يُرفض بقائمة السماح لأنواع MIME."),
             L("415 unsupported_type", "415 unsupported_type")],
            [L("A renamed non-image with an image MIME type",
               "ملف غير صوري أُعيدت تسميته بنوع MIME صوري"),
             L("Image.verify()", "Image.verify()"),
             L("Pillow actually parses the bytes; a fake PNG fails here. This is the check that "
               "matters — extensions and headers can both be forged.",
               "تُحلّل Pillow البايتات فعلًا؛ فيفشل ملف PNG المزيّف هنا. وهذا هو الفحص المُعتبَر — "
               "فالامتدادات والترويسات كلاهما قابل للتزوير."),
             L("422 invalid_image", "422 invalid_image")],
            [L("Concurrent requests hitting GradCAM", "طلبات متزامنة تصيب GradCAM"),
             L("INFERENCE_LOCK", "INFERENCE_LOCK"),
             L("Serialized. GradCAM registers backward hooks on the shared model object; two "
               "simultaneous calls would interleave hooks and corrupt each other's heatmaps.",
               "تُسلسَل. إذ يسجّل GradCAM خطّافات خلفية على كائن النموذج المشترك؛ ونداءان متزامنان "
               "سيتداخل خطّافاهما ويُفسد كلٌّ منهما خريطة الآخر."),
             L("— (queued)", "— (تُصفَّف)")],
            [L("grad-cam package not installed", "حزمة grad-cam غير مثبَّتة"),
             L("gradcam_utils", "gradcam_utils"),
             L("Returns the resized original instead of crashing; the response sets "
               "gradcam_is_heatmap = false and the UI shows an install hint.",
               "تُعيد الأصل بعد التحجيم بدل الانهيار؛ وتضبط الاستجابة gradcam_is_heatmap = false "
               "وتعرض الواجهة تلميح تثبيت."),
             L("200 (degraded)", "200 (بأداء منقوص)")],
            [L("Ollama missing / stopped / model not pulled", "Ollama مفقود أو متوقّف أو النموذج غير منزَّل"),
             L("llm_available() + generate_medical_report()", "llm_available() و generate_medical_report()"),
             L("The report panel shows the exact command needed. Everything else keeps working. "
               "Availability is cached for 30 seconds so /health never becomes slow.",
               "تعرض لوحة التقرير الأمر المطلوب بالضبط. ويستمرّ كل ما عداها في العمل. وتُخزَّن حالة "
               "التوفّر مؤقتًا 30 ثانية فلا يبطؤ /health أبدًا."),
             L("200 available=false", "200 available=false")],
            [L("Backend unreachable from the browser", "تعذّر وصول المتصفح إلى الخادم"),
             L("lib/api.ts", "lib/api.ts"),
             L("A network failure is converted into a typed ApiError with the message \"Could not "
               "reach the backend. Make sure the API server is running.\" — not an unhandled promise "
               "rejection.",
               "يُحوَّل فشل الشبكة إلى ApiError مُوصَّف النوع برسالة «تعذّر الوصول إلى الخادم. تأكّد "
               "من تشغيل خادم الـAPI.» — لا إلى رفض وعد غير معالَج."),
             L("0 network_error", "0 network_error")],
            [L("User uploads a new file mid-analysis", "يرفع المستخدم ملفًا جديدًا أثناء التحليل"),
             L("AbortController", "AbortController"),
             L("The previous prediction and report requests are aborted, so a stale response can "
               "never overwrite a newer one.",
               "يُلغى طلبا التنبؤ والتقرير السابقان، فلا تستطيع استجابة قديمة الكتابة فوق أحدث "
               "منها."),
             L("— (aborted)", "— (مُلغى)")],
            [L("A request from an unapproved website", "طلب من موقع غير معتمَد"),
             L("CORS middleware", "وسيط CORS"),
             L("Only the origins in FRONTEND_ORIGINS are allowed, and only GET and POST.",
               "لا يُسمح إلا بالمصادر المدرَجة في FRONTEND_ORIGINS، وبطريقتي GET و POST فقط."),
             L("blocked by browser", "يحجبه المتصفح")],
        ]},
        {"type": "callout", "tone": "good",
         "title": L("The design principle behind all of it",
                    "مبدأ التصميم وراء ذلك كله"),
         "text": L(
            "Optional capabilities degrade; required capabilities fail loudly. GradCAM and the LLM "
            "report are enhancements, so their absence produces a hint and a working app. The model "
            "weights are essential, so a mismatch raises rather than silently serving nonsense. "
            "Getting that distinction right is the difference between a tool that is safe to be wrong "
            "and one that is not.",
            "القدرات الاختيارية تتراجع بلطف، والقدرات الضرورية تفشل بصوت عالٍ. فـGradCAM وتقرير "
            "النموذج اللغوي تحسينان، لذا يُنتج غيابهما تلميحًا وتطبيقًا يعمل. أما أوزان النموذج "
            "فأساسية، لذا يرفع عدم التطابق خطأً بدل تقديم هراء بصمت. وضبط هذا التمييز هو الفرق بين "
            "أداة يَسلَم خطؤها وأداة لا يَسلَم.")},
    ],
}

# ── K · SECURITY & PRIVACY ───────────────────────────────────────────────
SECURITY = {
    "id": "security",
    "title": L("Security, Privacy & Data Governance", "الأمن والخصوصية وحوكمة البيانات"),
    "lead": L(
        "Medical images are among the most sensitive data that exist. This is what the system does "
        "with them — and, more importantly, what it deliberately does not do.",
        "الصور الطبية من أشد البيانات حساسيةً على الإطلاق. وهذا ما يفعله النظام بها — والأهم، ما "
        "يمتنع عن فعله عمدًا."),
    "blocks": [
        {"type": "h", "text": L("What happens to an uploaded scan", "ماذا يحدث للصورة المرفوعة")},
        {"type": "bullets", "items": [
            L("It is read into memory as bytes, decoded by Pillow, converted to a tensor, and "
              "discarded when the request ends. It is never written to disk.",
              "تُقرأ إلى الذاكرة كبايتات، وتفكّها Pillow، وتُحوَّل إلى موتِّر، وتُتلَف عند انتهاء "
              "الطلب. ولا تُكتب على القرص أبدًا."),
            L("There is no database, no upload folder, no cache, and no logging of image content.",
              "لا قاعدة بيانات ولا مجلد رفع ولا ذاكرة تخزين مؤقت ولا تسجيل لمحتوى الصور."),
            L("The GradCAM heatmap is returned inline as a base64 data URL rather than as a file the "
              "server has to store and later serve — so no image ever becomes a URL somebody could "
              "guess or share.",
              "تُعاد خريطة GradCAM مضمّنةً كعنوان بيانات base64 بدل ملف يخزّنه الخادم ثم يقدّمه — فلا "
              "تصير أي صورة عنوانًا يمكن تخمينه أو مشاركته."),
            L("The language model runs on the same machine. Nothing is sent to OpenAI, Anthropic, "
              "Google, or any other third party. There is no API key in the project because there is "
              "nothing to authenticate to.",
              "يعمل النموذج اللغوي على الجهاز نفسه. ولا يُرسَل شيء إلى OpenAI أو Anthropic أو Google "
              "أو أي طرف ثالث. ولا مفتاح API في المشروع لأنه لا جهة للاستيثاق معها."),
        ]},
        {"type": "h", "text": L("Network posture", "الوضع الشبكي")},
        {"type": "table",
         "head": [L("Control", "الضابط"), L("Implementation", "التنفيذ")],
         "rows": [
            [L("Nothing exposed by default", "لا شيء مكشوف افتراضيًا"),
             L("Both application containers bind to 127.0.0.1 only (ports 8110 and 3040 on the host). "
               "A single nginx virtual host on port 8086 is the one public door.",
               "ترتبط حاويتا التطبيق بـ127.0.0.1 فقط (المنفذان 8110 و3040 على المضيف). ومضيف nginx "
               "افتراضي واحد على المنفذ 8086 هو الباب العام الوحيد.")],
            [L("The LLM is not reachable from outside", "النموذج اللغوي غير قابل للوصول من الخارج"),
             L("The ollama service uses `expose` rather than `ports`, so 11434 exists only on the "
               "internal Docker network. An exposed Ollama endpoint is a well-known way to hand "
               "strangers free compute.",
               "تستخدم خدمة ollama توجيه `expose` لا `ports`، فلا يوجد المنفذ 11434 إلا على شبكة "
               "Docker الداخلية. وكشف نقطة Ollama طريقة معروفة لمنح الغرباء حوسبة مجانية.")],
            [L("CORS allow-list", "قائمة سماح CORS"),
             L("Only the origins named in FRONTEND_ORIGINS, and only GET and POST.",
               "المصادر المسمّاة في FRONTEND_ORIGINS فقط، وبطريقتي GET و POST فقط.")],
            [L("Input hardening", "تقوية المدخلات"),
             L("Size cap, MIME allow-list, and real decode verification before the bytes go anywhere "
               "near the model.",
               "حدّ للحجم، وقائمة سماح لأنواع MIME، وتحقّق فعلي من الفك قبل أن تقترب البايتات من "
               "النموذج.")],
            [L("Schema validation", "التحقّق من المخطّطات"),
             L("Pydantic validates every request and response; /api/report rejects any tumor_class "
               "that is not one of the four known names.",
               "تتحقّق Pydantic من كل طلب واستجابة؛ ويرفض /api/report أي tumor_class ليس من الأسماء "
               "الأربعة المعروفة.")],
        ]},
        {"type": "h", "text": L("What is deliberately missing — and would be needed to sell it",
                                "ما هو غائب عمدًا — وما يلزم لبيعه")},
        {"type": "p", "text": L(
            "The current build has no authentication, no user accounts, no rate limiting, no audit "
            "log, no HTTPS termination of its own (nginx would supply it), and no DICOM support or "
            "PHI handling. That is entirely correct for an educational prototype that stores nothing "
            "— but every one of those items is mandatory before the software could be sold into a "
            "clinical setting. They are listed explicitly in the commercialization section rather "
            "than glossed over.",
            "لا يحوي البناء الحالي استيثاقًا ولا حسابات مستخدمين ولا تحديدًا لمعدّل الطلبات ولا "
            "سجلّ تدقيق ولا إنهاءً خاصًا به لـHTTPS (يوفّره nginx) ولا دعمًا لـDICOM ولا معالجةً "
            "للبيانات الصحية المُعرِّفة. وهذا صحيح تمامًا لنموذج تعليمي لا يخزّن شيئًا — لكن كل بند "
            "من تلك البنود إلزامي قبل بيع البرمجية لبيئة سريرية. وهي مذكورة صراحةً في قسم "
            "التسويق التجاري بدل التغاضي عنها.")},
    ],
}

# ── L · PERFORMANCE ──────────────────────────────────────────────────────
PERF = {
    "id": "perf",
    "title": L("Performance, Size & Resource Budget", "الأداء والحجم وميزانية الموارد"),
    "lead": L(
        "The concrete numbers behind the model and the running system.",
        "الأرقام الملموسة وراء النموذج والنظام أثناء التشغيل."),
    "blocks": [
        {"type": "h", "text": L("Parameter budget", "ميزانية المعاملات")},
        {"type": "table",
         "head": [L("Component", "المكوّن"), L("Parameters", "المعاملات"), L("Status in training", "حالتها في التدريب")],
         "rows": [
            [L("conv1 + bn1", "conv1 و bn1"), L("9,536", "9,536"), L("Frozen", "مجمَّدة")],
            [L("layer1", "layer1"), L("215,808", "215,808"), L("Frozen", "مجمَّدة")],
            [L("layer2", "layer2"), L("1,219,584", "1,219,584"), L("Frozen", "مجمَّدة")],
            [L("layer3", "layer3"), L("7,098,368", "7,098,368"), L("Trained", "تُدرَّب")],
            [L("layer4", "layer4"), L("14,964,736", "14,964,736"), L("Trained", "تُدرَّب")],
            [L("Classifier head (2048→512→4)", "رأس المُصنِّف ‏(2048←512←4)"),
             L("1,051,140", "1,051,140"), L("Trained from scratch", "يُدرَّب من الصفر")],
            [L("Total", "الإجمالي"), L("24,559,172 (~24.6M)", "24,559,172 (نحو 24.6 مليون)"),
             L("~94% trainable, ~6% frozen", "نحو 94% قابلة للتدريب و6% مجمَّدة")],
        ]},
        {"type": "p", "text": L(
            "Note what the freezing strategy buys: only about 1.4 million parameters are held fixed, "
            "but they are exactly the generic edge-and-texture detectors that a 5,712-image dataset "
            "could never learn well from scratch. The 23 million trainable parameters are the ones "
            "that need to become MRI-specific.",
            "لاحظ ما تشتريه استراتيجية التجميد: لا يُثبَّت سوى نحو 1.4 مليون معامل، لكنها بالضبط "
            "كواشف الحواف والقوام العامة التي لا يمكن لمجموعة من 5712 صورة أن تتعلّمها جيدًا من "
            "الصفر. أما المعاملات الـ23 مليونًا القابلة للتدريب فهي التي يجب أن تصير خاصة بصور "
            "الرنين.")},
        {"type": "h", "text": L("Footprint", "البصمة")},
        {"type": "table",
         "head": [L("Item", "البند"), L("Size", "الحجم"), L("Note", "ملاحظة")],
         "rows": [
            [L("model_class.pth", "model_class.pth"), L("98.6 MB (94 MiB)", "98.6 ميغابايت (94 ميبي)"),
             L("24.6M float32 weights ≈ 98.2 MB, plus BatchNorm running statistics.",
               "‏24.6 مليون وزن من نوع float32 ≈ 98.2 ميغابايت، مع الإحصاءات الجارية للتطبيع "
               "الدُّفعي.")],
            [L("Committed to git", "مُودَع في git"), L("Yes", "نعم"),
             L("Convenient for a demo, but a 98 MB binary in version control is the kind of thing a "
               "reviewer may flag — a model registry or Git LFS is the production answer.",
               "مريح للعرض، لكن ملفًا ثنائيًا بحجم 98 ميغابايت في نظام الإصدارات مما قد يشير إليه "
               "المُراجع — والجواب الإنتاجي سجلّ نماذج أو Git LFS.")],
            [L("Backend Docker image", "صورة Docker للخادم"), L("CPU-only PyTorch 2.6.0 + torchvision 0.21.0",
                                                                "‏PyTorch 2.6.0 للمعالج مع torchvision 0.21.0"),
             L("Pinned deliberately to the versions the weights were saved under; the CPU wheel index "
               "avoids pulling ~2 GB of CUDA libraries that a CPU server would never use.",
               "مثبَّتة عمدًا على الإصدارات التي حُفظت تحتها الأوزان؛ ويتجنّب فهرس عجلات المعالج جلب "
               "نحو 2 غيغابايت من مكتبات CUDA لن يستخدمها خادم بمعالج فقط.")],
            [L("Runtime threads", "خيوط التشغيل"), L("OMP_NUM_THREADS = 2", "OMP_NUM_THREADS = 2"),
             L("Caps PyTorch's CPU parallelism so one prediction cannot starve the other services on "
               "a shared VPS.",
               "يحدّ من توازي PyTorch على المعالج فلا يُجوِّع تنبؤٌ واحد بقية الخدمات على خادم "
               "مشترك.")],
            [L("Ollama memory policy", "سياسة ذاكرة Ollama"),
             L("KEEP_ALIVE 2m · MAX_LOADED_MODELS 1 · NUM_PARALLEL 1",
               "KEEP_ALIVE دقيقتان · MAX_LOADED_MODELS 1 · NUM_PARALLEL 1"),
             L("The model is unloaded two minutes after the last report, so several gigabytes are not "
               "held hostage between demos.",
               "يُفرَّغ النموذج بعد دقيقتين من آخر تقرير، فلا تبقى عدّة غيغابايت محتجزة بين "
               "العروض.")],
        ]},
        {"type": "h", "text": L("Latency", "زمن الاستجابة")},
        {"type": "bullets", "items": [
            L("Classification alone is a single forward pass over one image — well under a second on "
              "an ordinary CPU, and a few milliseconds on a GPU.",
              "التصنيف وحده تمريرة أمامية واحدة على صورة واحدة — أقل من ثانية بكثير على معالج عادي، "
              "وبضعة أجزاء من الألف من الثانية على كرت رسوم."),
            L("GradCAM dominates /api/predict, because aug_smooth deliberately runs the model over "
              "several augmented copies of the image and averages the result. This is a conscious "
              "accuracy-for-speed trade: a noisy heatmap is worse than a slow one. Clients that do "
              "not need it can pass ?gradcam=false.",
              "يهيمن GradCAM على /api/predict، لأن aug_smooth يشغّل النموذج عمدًا على عدّة نسخ مُزادة "
              "من الصورة ويتوسّط النتيجة. وهذه مقايضة واعية للسرعة بالدقة: فالخريطة الحرارية "
              "المشوَّشة أسوأ من البطيئة. ومن لا يحتاجها من العملاء يمرّر ?gradcam=false."),
            L("The LLM report is by far the slowest step (~15 s on GPU, 1–2 minutes on CPU) and is "
              "why it runs as a separate, second request — the prediction and heatmap appear "
              "immediately, and the report streams in afterwards instead of blocking the whole "
              "screen.",
              "تقرير النموذج اللغوي أبطأ الخطوات بفارق كبير (نحو 15 ثانية على كرت الرسوم ودقيقة إلى "
              "دقيقتين على المعالج)، ولهذا يعمل بوصفه طلبًا ثانيًا منفصلًا — فيظهر التنبؤ والخريطة "
              "فورًا، ويصل التقرير بعدهما بدل حجب الشاشة كلها."),
            L("The /api/health Ollama probe is cached for 30 seconds, so polling the status pill "
              "never costs a round-trip to the model server.",
              "يُخزَّن فحص Ollama في /api/health مؤقتًا لثلاثين ثانية، فلا يكلّف استطلاع شارة الحالة "
              "رحلةً إلى خادم النموذج أبدًا."),
        ]},
    ],
}

# ── M · TECHNOLOGY DECISION LOG ──────────────────────────────────────────
DECISIONS = {
    "id": "decisions",
    "title": L("Technology Decision Log — Every Choice and Its Alternatives",
               "سجل قرارات التقنية — كل اختيار وبدائله"),
    "lead": L(
        "For each technology in the stack: what it is, why it was chosen, and what was rejected. "
        "This is the section to read the night before the presentation.",
        "لكل تقنية في الحزمة: ما هي، ولماذا اختيرت، وما الذي رُفض. وهذا هو القسم الذي يُقرأ في "
        "الليلة السابقة للعرض."),
    "blocks": [
        {"type": "h", "text": L("Machine learning", "التعلّم الآلي")},
        {"type": "kv", "pairs": [
            [L("PyTorch (over TensorFlow/Keras)", "‏PyTorch (بدل TensorFlow/Keras)"),
             L("The project literally started in Keras — brain-tumor.ipynb is still in the repo — and "
               "moved. PyTorch's define-by-run graph makes debugging ordinary Python debugging; "
               "torchvision ships pretrained weights in one line; and pytorch-grad-cam, the "
               "explainability library the whole project depends on, is PyTorch-native. It is also "
               "what most current medical-imaging research publishes in, so results are easier to "
               "reproduce.",
               "بدأ المشروع فعليًا بـKeras — وما زال brain-tumor.ipynb في المستودع — ثم انتقل. فرسم "
               "PyTorch البياني أثناء التنفيذ يجعل التنقيح تنقيحًا بايثونيًا عاديًا؛ وتقدّم "
               "torchvision الأوزان المُدرَّبة مسبقًا بسطر واحد؛ ومكتبة pytorch-grad-cam التي يقوم "
               "عليها المشروع كله أصيلة في PyTorch. كما أن معظم أبحاث التصوير الطبي الحالية تُنشر "
               "بها، فيسهل تكرار النتائج.")],
            [L("Transfer learning (over training from scratch)",
               "التعلّم بالنقل (بدل التدريب من الصفر)"),
             L("5,712 images is a small dataset by deep-learning standards. ImageNet's 1.2 million "
               "photographs already taught ResNet50 edges, textures and shapes; reusing that costs "
               "nothing and saves both accuracy and hours of GPU time.",
               "‏5712 صورة مجموعة صغيرة بمقاييس التعلّم العميق. وقد علّمت صور ImageNet البالغة 1.2 "
               "مليون شبكةَ ResNet50 الحوافَ والقوامَ والأشكال؛ وإعادة استخدام ذلك بلا تكلفة وتوفّر "
               "الدقة وساعات من زمن كرت الرسوم.")],
            [L("pytorch-grad-cam (over LIME, SHAP, occlusion, attention maps)",
               "‏pytorch-grad-cam (بدل LIME و SHAP والحجب وخرائط الانتباه)"),
             L("LIME and SHAP need hundreds or thousands of perturbed forward passes per image — far "
               "too slow for an interactive tool — and they explain a surrogate model rather than the "
               "network itself. Occlusion sliding is similarly expensive. Attention maps require a "
               "transformer, which we are not using. GradCAM needs exactly one backward pass, works "
               "on any CNN, and is the standard, peer-reviewed method for convolutional networks.",
               "يحتاج LIME و SHAP مئات أو آلاف التمريرات الأمامية المضطربة لكل صورة — وهو أبطأ بكثير "
               "من أن يصلح لأداة تفاعلية — كما يشرحان نموذجًا بديلًا لا الشبكة نفسها. والحجب "
               "الانزلاقي مكلف بالمثل. وخرائط الانتباه تتطلّب محوّلًا لا نستخدمه. أما GradCAM "
               "فيحتاج تمريرة خلفية واحدة بالضبط، ويعمل على أي شبكة التفافية، وهو المنهج القياسي "
               "المُحكَّم للشبكات الالتفافية.")],
            [L("Adam (over SGD with momentum)", "‏Adam (بدل SGD مع الزخم)"),
             L("Per-parameter adaptive step sizes suit fine-tuning, where a pretrained backbone needs "
               "tiny updates while a randomly-initialized head needs large ones. SGD can reach "
               "slightly better final accuracy on long training runs, but needs careful learning-rate "
               "scheduling — not worth it for a 7-epoch fine-tune.",
               "أحجام الخطوات التكيّفية لكل معامل تناسب الضبط الدقيق، حيث تحتاج الشبكة المُدرَّبة "
               "مسبقًا تحديثات ضئيلة بينما يحتاج الرأس المُهيَّأ عشوائيًا تحديثات كبيرة. وقد يبلغ "
               "SGD دقة نهائية أفضل قليلًا في التدريبات الطويلة، لكنه يحتاج جدولةً دقيقة لمعدّل "
               "التعلّم — وهو ما لا يستحق العناء لضبطٍ من سبع حقب.")],
            [L("Ollama (over the OpenAI / Anthropic / Google APIs)",
               "‏Ollama (بدل واجهات OpenAI و Anthropic و Google)"),
             L("Three decisive reasons: privacy (a patient scan's findings never leave the building), "
               "cost (zero per call, forever), and availability (it works with no internet at all — "
               "which matters in exactly the low-resource hospitals this kind of tool is aimed at). "
               "The price paid is speed on CPU, and it is paid consciously.",
               "ثلاثة أسباب حاسمة: الخصوصية (لا تغادر نتائج صورة المريض المبنى)، والتكلفة (صفر لكل "
               "نداء وإلى الأبد)، والتوفّر (يعمل بلا إنترنت إطلاقًا — وهو ما يهمّ تحديدًا في "
               "المستشفيات محدودة الموارد التي تستهدفها هذه الأداة). والثمن المدفوع هو السرعة على "
               "المعالج، ويُدفع عن وعي.")],
        ]},
        {"type": "h", "text": L("Backend", "الخادم")},
        {"type": "kv", "pairs": [
            [L("FastAPI (over Flask, Django, Node)", "‏FastAPI (بدل Flask و Django و Node)"),
             L("Async by default, so a two-minute LLM report does not block every other user; "
               "automatic OpenAPI documentation at /docs, which is worth a lot in a live demo; and "
               "Pydantic validation built into the signature so malformed requests are rejected "
               "before any code runs. Flask would need extensions for all three. Django brings an ORM "
               "and admin panel this project has no use for. Node would mean re-implementing the "
               "model layer outside Python.",
               "لاتزامني افتراضيًا، فلا يحجب تقريرٌ يستغرق دقيقتين كلَّ مستخدم آخر؛ وتوثيق OpenAPI "
               "تلقائي على /docs، وهو ذو قيمة كبيرة في عرض حيّ؛ وتحقّق Pydantic مدمج في توقيع الدالة "
               "فتُرفض الطلبات المشوّهة قبل تنفيذ أي شيفرة. وسيحتاج Flask إضافات للثلاثة جميعًا. "
               "ويجلب Django مُخطِّط كائنات ولوحة إدارة لا حاجة للمشروع بهما. وسيعني Node إعادة "
               "بناء طبقة النموذج خارج بايثون.")],
            [L("uvicorn", "uvicorn"),
             L("The standard ASGI server that actually runs the async application.",
               "خادم ASGI القياسي الذي يشغّل التطبيق اللاتزامني فعليًا.")],
            [L("Pydantic", "Pydantic"),
             L("Types the wire format in both directions and doubles as the API documentation. "
               "/api/report will reject a tumor_class that is not one of the four known names before "
               "the request touches the model.",
               "يوصّف صيغة الشبكة في الاتجاهين ويؤدي دور توثيق الـAPI في الوقت نفسه. وسيرفض "
               "/api/report أي tumor_class ليس من الأسماء الأربعة المعروفة قبل أن يمسّ الطلبُ "
               "النموذجَ.")],
            [L("A shared inference_core.py", "ملف inference_core.py مشترك"),
             L("Not a framework choice but the most important architectural one: the model "
               "architecture, the preprocessing transform and the class order exist in exactly one "
               "place, imported by the API and the Gradio app alike. Duplicating them is how "
               "training/serving skew — the classic silent ML production bug — begins. It is also "
               "written to be import-safe: importing it does not load the 98 MB weights.",
               "ليس خيارًا لإطار عمل بل أهم خيار معماري: إذ توجد معمارية النموذج وتحويل المعالجة "
               "المسبقة وترتيب الفئات في مكان واحد بالضبط، يستوردها الـAPI وتطبيق Gradio معًا. "
               "وتكرارها هو بداية انحراف التدريب عن الخدمة — وهو الخلل الصامت الكلاسيكي في إنتاج "
               "التعلّم الآلي. كما كُتب ليكون آمنًا عند الاستيراد: فاستيراده لا يحمّل الأوزان "
               "البالغة 98 ميغابايت.")],
        ]},
        {"type": "h", "text": L("Frontend", "الواجهة")},
        {"type": "kv", "pairs": [
            [L("Next.js 16 + React 19 (over plain React, Streamlit or staying on Gradio)",
               "‏Next.js 16 و React 19 (بدل React المجرّد أو Streamlit أو البقاء على Gradio)"),
             L("Gradio and Streamlit produce a recognizable \"ML demo\" look with almost no control "
               "over layout, typography or motion — and in a competition, looking like a product is "
               "part of the argument. Next.js gives file-based routing, server components, image and "
               "font optimization, and a real production build. Plain React would mean assembling "
               "routing and bundling by hand.",
               "تُنتج Gradio و Streamlit مظهر «عرض تعلّم آلي» معروفًا بلا تحكّم يُذكر في التخطيط أو "
               "الطباعة أو الحركة — وفي مسابقةٍ، يكون الظهور بمظهر منتج جزءًا من الحُجّة. ويمنح "
               "Next.js توجيهًا قائمًا على الملفات، ومكوّنات خادم، وتحسينًا للصور والخطوط، وبناءً "
               "إنتاجيًا حقيقيًا. أما React المجرّد فسيعني تجميع التوجيه والتحزيم يدويًا.")],
            [L("TypeScript (over JavaScript)", "‏TypeScript (بدل JavaScript)"),
             L("The API returns snake_case and the UI uses camelCase; types make lib/api.ts the one "
               "place that conversion can happen, and the compiler catches a renamed field instead of "
               "the user seeing \"undefined\".",
               "يُعيد الـAPI صيغة snake_case وتستخدم الواجهة camelCase؛ وتجعل الأنواعُ lib/api.ts "
               "المكانَ الوحيد الذي يحدث فيه التحويل، ويلتقط المُصرِّف حقلًا أُعيدت تسميته بدل أن "
               "يرى المستخدم كلمة undefined.")],
            [L("Tailwind v4 (CSS-first)", "‏Tailwind v4 (بأسلوب CSS أولًا)"),
             L("The entire palette is CSS custom properties, so dark/light and four accent themes "
               "switch instantly with no JavaScript re-render and no duplicated stylesheets.",
               "لوحة الألوان كلها خصائص CSS مخصَّصة، فتتبدّل السمتان الداكنة والفاتحة وأربع لوحات "
               "تمييز فورًا بلا إعادة رسم من JavaScript وبلا أوراق أنماط مكرَّرة.")],
            [L("Hand-drawn SVG charts (over Chart.js / Recharts / D3)",
               "رسوم SVG يدوية (بدل Chart.js و Recharts و D3)"),
             L("The metrics page needs two line charts and a matrix. A charting library would add "
               "hundreds of kilobytes to the bundle and fight the theme system over colors; ~150 "
               "lines of SVG paths do the job, weigh nothing, and inherit the theme variables for "
               "free.",
               "تحتاج صفحة المقاييس مخطّطَي خطوط ومصفوفة. وستضيف مكتبة رسوم مئات الكيلوبايتات إلى "
               "الحزمة وتصارع نظام السمات على الألوان؛ بينما يؤدي نحو 150 سطرًا من مسارات SVG المهمة "
               "بلا وزن يُذكر، وترث متغيّرات السمة مجانًا.")],
            [L("react-markdown + remark-gfm", "‏react-markdown مع remark-gfm"),
             L("The LLM returns Markdown; this renders it as safe React elements rather than "
               "injecting raw HTML.",
               "يُعيد النموذج اللغوي Markdown؛ وهذه المكتبة تعرضه عناصر React آمنة بدل حقن HTML "
               "خام.")],
        ]},
        {"type": "h", "text": L("Packaging and deployment", "التحزيم والنشر")},
        {"type": "kv", "pairs": [
            [L("Docker Compose (over bare-metal installs)", "‏Docker Compose (بدل التثبيت المباشر)"),
             L("Three services with one command, identical on any machine, with health checks and "
               "restart policies. It also solves a real trap: PyTorch's version must match the one "
               "the weights were saved under, and the Dockerfile pins torch 2.6.0 / torchvision "
               "0.21.0 from the CPU wheel index for exactly that reason.",
               "ثلاث خدمات بأمر واحد، متطابقة على أي جهاز، مع فحوص صحة وسياسات إعادة تشغيل. كما "
               "تحلّ فخًّا حقيقيًا: إذ يجب أن يطابق إصدار PyTorch الإصدارَ الذي حُفظت تحته الأوزان، "
               "ويثبّت ملف Docker الإصدارين torch 2.6.0 و torchvision 0.21.0 من فهرس عجلات المعالج "
               "لهذا السبب بالضبط.")],
            [L("opencv-python-headless", "‏opencv-python-headless"),
             L("grad-cam pulls in full OpenCV, which expects GUI libraries that do not exist in a "
               "slim server image. The Dockerfile explicitly uninstalls it and reinstalls the "
               "headless build — a small detail that is the difference between the image building "
               "and not.",
               "يجلب grad-cam مكتبة OpenCV الكاملة التي تتوقّع مكتبات واجهة رسومية غير موجودة في "
               "صورة خادم نحيلة. لذا يزيلها ملف Docker صراحةً ويعيد تثبيت النسخة بلا واجهة — وهو "
               "تفصيل صغير هو الفرق بين نجاح بناء الصورة وفشله.")],
            [L("nginx", "nginx"),
             L("One public origin that routes /api to the backend and everything else to the "
               "frontend, so the browser never sees two hosts and CORS stays a non-issue in "
               "production.",
               "مصدر عام واحد يوجّه /api إلى الخادم وكل ما عداه إلى الواجهة، فلا يرى المتصفح مضيفين "
               "ولا يبقى CORS مشكلةً في الإنتاج.")],
        ]},
    ],
}
