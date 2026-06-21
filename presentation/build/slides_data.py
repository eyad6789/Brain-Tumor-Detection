# -*- coding: utf-8 -*-
"""Slide deck content (English + Arabic) for NeuroScan.

Kept deliberately concise per slide — the deep-dive documents carry the
exhaustive detail. ~26 slides telling the full story end to end.
"""
from i18n import L

SLIDES = [
    # ── 0 · TITLE ────────────────────────────────────────────────────────
    {
        "type": "title",
        "tag": L("Explainable Deep Learning for Medical Imaging",
                 "تعلّم عميق قابل للتفسير في التصوير الطبي"),
        "title": L("NeuroScan", "NeuroScan"),
        "subtitle": L("Brain-Tumor MRI Classifier — ResNet50 → GradCAM → Local-LLM Report",
                      "مُصنِّف أورام الدماغ من صور الرنين المغناطيسي — ResNet50 ثم GradCAM ثم تقرير بنموذج لغوي محلي"),
        "foot": L("Educational & research prototype — not a medical device",
                  "نموذج تعليمي وبحثي — ليس جهازًا طبيًا"),
    },

    # ── 1 · SECTION ──────────────────────────────────────────────────────
    {"type": "section", "num": "01",
     "title": L("The Problem & The Idea", "المشكلة والفكرة"),
     "subtitle": L("Why a classifier alone is not enough",
                   "لماذا لا يكفي المُصنِّف وحده")},

    # ── 2 · MOTIVATION ───────────────────────────────────────────────────
    {"type": "bullets",
     "title": L("Why this project", "لماذا هذا المشروع"),
     "lead": L("Brain tumors are diagnosed from MRI scans — a slow, expert-dependent read.",
               "تُشخَّص أورام الدماغ من صور الرنين المغناطيسي، وهي قراءة بطيئة تعتمد على الخبير."),
     "bullets": [
        L("Deep learning can flag the likely tumor type in seconds.",
          "يستطيع التعلّم العميق ترشيح نوع الورم المُحتمَل خلال ثوانٍ."),
        L("But a bare prediction is a black box — clinicians won't trust a number.",
          "لكن التنبؤ المجرّد صندوق أسود، ولن يثق به الأطباء كرقم فقط."),
        L("So NeuroScan adds two trust layers: a visual explanation and a written report.",
          "لذا يضيف NeuroScan طبقتي ثقة: تفسيرًا بصريًا وتقريرًا مكتوبًا."),
        L("Everything runs locally — no cloud, no API keys, full privacy.",
          "كل شيء يعمل محليًا — دون سحابة ولا مفاتيح API، وبخصوصية كاملة."),
     ]},

    # ── 3 · WHAT IT DOES ─────────────────────────────────────────────────
    {"type": "bullets",
     "title": L("What NeuroScan does", "ماذا يفعل NeuroScan"),
     "lead": L("One upload drives a four-step experience:",
               "رفعٌ واحد يُشغِّل تجربة من أربع خطوات:"),
     "bullets": [
        L("① Upload an MRI image in the browser.",
          "① رفع صورة رنين مغناطيسي من المتصفح."),
        L("② Get the predicted class + confidence for all four classes.",
          "② الحصول على الفئة المتوقَّعة ونِسَب الثقة للفئات الأربع."),
        L("③ See a GradCAM heatmap of exactly where the model looked.",
          "③ رؤية خريطة حرارية GradCAM تُبيّن أين نظر النموذج تحديدًا."),
        L("④ Read an auto-generated, structured clinical report.",
          "④ قراءة تقرير سريري منظَّم يُولَّد تلقائيًا."),
     ],
     "foot": L("Two front-ends: a Next.js web app (primary) and a legacy Gradio UI.",
               "واجهتان: تطبيق ويب بـ Next.js (الأساسي) وواجهة Gradio قديمة.")},

    # ── 4 · PIPELINE IMAGE ───────────────────────────────────────────────
    {"type": "image",
     "title": L("The explainable pipeline", "خط المعالجة القابل للتفسير"),
     "image": "pipeline.png",
     "caption": L("Predict → explain → report: each stage adds trust.",
                  "تنبّؤ ← تفسير ← تقرير: كل مرحلة تزيد الثقة.")},

    # ── 5 · SECTION ──────────────────────────────────────────────────────
    {"type": "section", "num": "02",
     "title": L("The Data & The Classes", "البيانات والفئات"),
     "subtitle": L("What the model sees and predicts",
                   "ما الذي يراه النموذج ويتنبأ به")},

    # ── 6 · CLASSES TABLE ────────────────────────────────────────────────
    {"type": "table",
     "title": L("Four classes — a fixed index order", "أربع فئات بترتيب فهرسي ثابت"),
     "head": [L("Index", "الفهرس"), L("Class", "الفئة"), L("What it is", "ما هي")],
     "rows": [
        [L("0", "0"), L("Pituitary", "نخامية (Pituitary)"),
         L("Tumor of the pituitary gland; usually benign.",
           "ورم في الغدة النخامية، غالبًا حميد.")],
        [L("1", "1"), L("No Tumor", "لا يوجد ورم (No Tumor)"),
         L("Healthy / negative scan (note the space in the label).",
           "فحص سليم/سلبي (لاحظ المسافة في التسمية).")],
        [L("2", "2"), L("Meningioma", "سحائي (Meningioma)"),
         L("Tumor on the meninges around the brain.",
           "ورم في الأغشية السحائية المحيطة بالدماغ.")],
        [L("3", "3"), L("Glioma", "دبقي (Glioma)"),
         L("Tumor in the brain's glial cells; can be malignant.",
           "ورم في الخلايا الدبقية، وقد يكون خبيثًا.")],
     ],
     "foot": L("This order is identical in every file — the shipped weights depend on it.",
               "هذا الترتيب موحَّد في كل الملفات، وتعتمد عليه الأوزان المُسلَّمة.")},

    # ── 7 · PREPROCESSING ────────────────────────────────────────────────
    {"type": "bullets",
     "title": L("Preprocessing — same maths as ImageNet",
                "المعالجة المسبقة — رياضيات ImageNet نفسها"),
     "bullets": [
        L("Resize every scan to 224 × 224 pixels, RGB.",
          "تغيير حجم كل صورة إلى 224×224 بكسل بنظام RGB."),
        L("Convert to a tensor (pixels scaled 0 → 1).",
          "التحويل إلى Tensor (قيم البكسل من 0 إلى 1)."),
        L("Normalize with ImageNet mean [.485, .456, .406] and std [.229, .224, .225].",
          "التطبيع بمتوسط ImageNet ‏[.485, .456, .406] والانحراف [.229, .224, .225]."),
        L("Why ImageNet stats? The backbone was pretrained on ImageNet — inputs must match.",
          "لماذا إحصاءات ImageNet؟ لأن الشبكة دُرِّبت مسبقًا عليها، فيجب أن تطابقها المدخلات."),
     ]},

    # ── 8 · AUGMENTATION ─────────────────────────────────────────────────
    {"type": "bullets",
     "title": L("Data augmentation (training only)", "زيادة البيانات (في التدريب فقط)"),
     "lead": L("Random transforms make the model robust to real-world variation:",
               "تحويلات عشوائية تجعل النموذج أكثر متانة أمام تباين الواقع:"),
     "bullets": [
        L("Horizontal + vertical flips → orientation invariance.",
          "انعكاس أفقي ورأسي ← ثبات تجاه الاتجاه."),
        L("Rotation ±15° → tolerate slight scan misalignment.",
          "تدوير ‏±15° ← تحمُّل انحراف بسيط في المحاذاة."),
        L("ColorJitter → adapt to scanner brightness/contrast differences.",
          "ColorJitter ← التكيّف مع فروق السطوع/التباين بين الأجهزة."),
        L("GaussianBlur → simulate motion / out-of-focus artifacts.",
          "GaussianBlur ← محاكاة تشوّش الحركة أو فقد التركيز."),
     ],
     "foot": L("Validation uses NO augmentation — evaluation must be deterministic.",
               "التحقق لا يستخدم أي زيادة — يجب أن يكون التقييم حتميًا.")},

    # ── 9 · SECTION ──────────────────────────────────────────────────────
    {"type": "section", "num": "03",
     "title": L("The Model", "النموذج"),
     "subtitle": L("ResNet50 + transfer learning", "ResNet50 مع التعلّم بالنقل")},

    # ── 10 · WHY RESNET ──────────────────────────────────────────────────
    {"type": "bullets",
     "title": L("Why ResNet50 + transfer learning",
                "لماذا ResNet50 والتعلّم بالنقل"),
     "bullets": [
        L("ResNet50: 50-layer residual CNN — deep but trainable thanks to skip connections.",
          "ResNet50: شبكة التفافية متبقّية من 50 طبقة — عميقة وقابلة للتدريب بفضل الوصلات التخطّيّة."),
        L("Start from ImageNet weights → reuse generic edge/texture detectors.",
          "نبدأ من أوزان ImageNet ← إعادة استخدام كواشف الحواف والقوام العامة."),
        L("Freeze the early layers; fine-tune only layer3 + layer4 (high-level features).",
          "تجميد الطبقات المبكرة، وضبط layer3 وlayer4 فقط (السمات العليا)."),
        L("Replace the 1000-class head with a custom 4-class head.",
          "استبدال رأس الألف فئة برأس مخصَّص من 4 فئات."),
        L("Result: high accuracy from a small medical dataset, trained in minutes.",
          "النتيجة: دقة عالية من مجموعة بيانات طبية صغيرة، وتدريب خلال دقائق."),
     ]},

    # ── 11 · HEAD IMAGE ──────────────────────────────────────────────────
    {"type": "image",
     "title": L("The classifier head", "رأس المُصنِّف"),
     "image": "model_head.png",
     "caption": L("The duplicate Dropout(0.3) is intentional — it keeps the final layer at "
                  "state-dict key fc.5 so the saved weights load strictly.",
                  "تكرار Dropout(0.3) مقصود — يُبقي الطبقة الأخيرة عند المفتاح fc.5 لتُحمَّل الأوزان بدقّة.")},

    # ── 12 · SECTION ─────────────────────────────────────────────────────
    {"type": "section", "num": "04",
     "title": L("Training", "التدريب"),
     "subtitle": L("How the weights were learned", "كيف تعلَّم النموذج أوزانه")},

    # ── 13 · HYPERPARAMS TABLE ───────────────────────────────────────────
    {"type": "table",
     "title": L("Training recipe", "وصفة التدريب"),
     "head": [L("Setting", "الإعداد"), L("Value", "القيمة"), L("Why", "السبب")],
     "rows": [
        [L("Optimizer", "المُحسِّن"), L("Adam, lr 1e-4", "Adam، ‏lr=1e-4"),
         L("Adaptive, stable for fine-tuning.", "تكيّفي ومستقر للضبط الدقيق.")],
        [L("Loss", "دالة الخسارة"), L("CrossEntropy, smoothing 0.1", "CrossEntropy، تنعيم 0.1"),
         L("Label smoothing curbs over-confidence.", "تنعيم التسميات يحدّ من الإفراط في الثقة.")],
        [L("Regularization", "التنظيم"), L("Weight decay 1e-4 + dropout", "Weight decay 1e-4 مع dropout"),
         L("Fights overfitting.", "يقاوم فرط التخصيص.")],
        [L("Scheduler", "جدولة المعدّل"), L("ReduceLROnPlateau ×0.5", "ReduceLROnPlateau ×0.5"),
         L("Lower LR when val loss stalls.", "خفض المعدّل عند ثبات خسارة التحقق.")],
        [L("Batch / Epochs", "الدفعة/الحقب"), L("32 / max 20", "32 / حتى 20"),
         L("Early-stop patience = 5.", "إيقاف مبكر بصبر = 5.")],
     ]},

    # ── 14 · RESULTS IMAGE ───────────────────────────────────────────────
    {"type": "image",
     "title": L("Training results (real log)", "نتائج التدريب (السجل الحقيقي)"),
     "image": "training_curves.png",
     "caption": L("Converged fast; best validation accuracy 99.39% at epoch 6, then early-stopped.",
                  "تقارب سريع؛ أفضل دقة تحقق 99.39% عند الحقبة 6، ثم إيقاف مبكر.")},

    # ── 15 · BIG STAT + HONESTY ──────────────────────────────────────────
    {"type": "bigstat",
     "stat": "99.39%",
     "label": L("claimed validation accuracy", "دقة التحقق المُعلَنة"),
     "title": L("…but we call it “claimed” on purpose", "…لكننا نسمّيها «مُعلَنة» عن قصد"),
     "caption": L("train.py reuses the test set as the validation set (data leakage). So this is an "
                  "optimistic figure, not a validated generalization estimate — and the app says so.",
                  "يعيد train.py استخدام مجموعة الاختبار كمجموعة تحقق (تسريب بيانات)، فهي رقم متفائل لا "
                  "تقدير معمَّم مُتحقَّق منه — والتطبيق يصرّح بذلك.")},

    # ── 16 · LIMITATIONS ─────────────────────────────────────────────────
    {"type": "bullets",
     "title": L("Honest limitations", "حدود صادقة"),
     "lead": L("Owning the flaws is part of good science:",
               "الاعتراف بالعيوب جزء من العلم الجيد:"),
     "bullets": [
        L("Data leakage → accuracy is optimistic; a true held-out test set is needed.",
          "تسريب البيانات ← الدقة متفائلة؛ نحتاج مجموعة اختبار مستقلة فعلًا."),
        L("Trained on one dataset → may not generalize to other scanners/populations.",
          "دُرِّب على مجموعة واحدة ← قد لا يعمّم على أجهزة/مجتمعات أخرى."),
        L("Image classification ≠ diagnosis; no segmentation or staging.",
          "تصنيف الصور ليس تشخيصًا؛ لا تجزئة ولا تحديد مرحلة."),
        L("Strictly educational/research — never a clinical decision tool.",
          "للأغراض التعليمية/البحثية فقط — وليس أداة قرار سريري."),
     ]},

    # ── 17 · SECTION ─────────────────────────────────────────────────────
    {"type": "section", "num": "05",
     "title": L("Explainability & Reporting", "التفسير وكتابة التقرير"),
     "subtitle": L("Turning a number into trust", "تحويل الرقم إلى ثقة")},

    # ── 18 · GRADCAM ─────────────────────────────────────────────────────
    {"type": "bullets",
     "title": L("GradCAM — where the model looked", "GradCAM — أين نظر النموذج"),
     "bullets": [
        L("Gradient-weighted Class Activation Mapping on the last conv block (layer4).",
          "خرائط تنشيط الفئة الموزونة بالتدرّج على آخر كتلة التفافية (layer4)."),
        L("Gradients of the predicted class flow back → weight the feature maps.",
          "تتدفّق تدرّجات الفئة المتوقَّعة للخلف ← لترجيح خرائط السمات."),
        L("Produces a heatmap overlaid on the MRI (red = most influential regions).",
          "ينتج خريطة حرارية فوق صورة الرنين (الأحمر = أكثر المناطق تأثيرًا)."),
        L("aug_smooth + eigen_smooth reduce noise for a cleaner map.",
          "يقلّل aug_smooth وeigen_smooth الضوضاء لخريطة أوضح."),
        L("If grad-cam isn't installed → graceful fallback to the resized original.",
          "إن لم تُثبَّت grad-cam ← تراجُع آمن إلى الصورة الأصلية المُحجَّمة."),
     ]},

    # ── 19 · LLM REPORT ──────────────────────────────────────────────────
    {"type": "bullets",
     "title": L("Local-LLM clinical report", "تقرير سريري بنموذج لغوي محلي"),
     "bullets": [
        L("A local Ollama model (default qwen2.5:1.5b) writes the report — no cloud, no key.",
          "نموذج Ollama محلي (افتراضيًا qwen2.5:1.5b) يكتب التقرير — دون سحابة ولا مفتاح."),
        L("A structured prompt forces exactly 5 sections, < 230 words, temperature 0.3.",
          "موجّه منظَّم يفرض 5 أقسام بالضبط، أقل من 230 كلمة، حرارة 0.3."),
        L("Diagnosis summary · about the tumor · what the heatmap shows · next steps · disclaimer.",
          "ملخص التشخيص · عن الورم · ما تُظهره الخريطة · الخطوات التالية · إخلاء المسؤولية."),
        L("Why local? Privacy of medical data, offline use, zero cost.",
          "لماذا محلي؟ خصوصية البيانات الطبية، والعمل دون إنترنت، وبلا تكلفة."),
        L("If Ollama is down → the UI shows clear setup instructions, app keeps working.",
          "إن توقّف Ollama ← تعرض الواجهة تعليمات إعداد واضحة ويظل التطبيق يعمل."),
     ]},

    # ── 20 · SECTION ─────────────────────────────────────────────────────
    {"type": "section", "num": "06",
     "title": L("The Engineering", "الهندسة البرمجية"),
     "subtitle": L("Backend · Frontend · Deployment",
                   "الخادم · الواجهة · النشر")},

    # ── 21 · ARCHITECTURE IMAGE ──────────────────────────────────────────
    {"type": "image",
     "title": L("System architecture", "معمارية النظام"),
     "image": "architecture.png",
     "caption": L("nginx splits traffic: the page from Next.js, /api from FastAPI; "
                  "PyTorch, GradCAM and Ollama sit behind the backend.",
                  "يقسّم nginx حركة المرور: الصفحة من Next.js و/api من FastAPI؛ "
                  "وتقع PyTorch وGradCAM وOllama خلف الخادم.")},

    # ── 22 · BACKEND ─────────────────────────────────────────────────────
    {"type": "two_col",
     "title": L("Backend — FastAPI", "الخادم — FastAPI"),
     "left": {"head": L("Design", "التصميم"), "bullets": [
        L("Model loads once at startup (lifespan).", "يُحمَّل النموذج مرة عند الإقلاع (lifespan)."),
        L("If load fails, API stays up and reports via /health.",
          "عند فشل التحميل يبقى الـAPI ويُبلِّغ عبر /health."),
        L("INFERENCE_LOCK serializes the model (GradCAM hooks aren't thread-safe).",
          "يُسلسِل INFERENCE_LOCK الوصول للنموذج (خطّافات GradCAM ليست آمنة للخيوط)."),
        L("Runs inference in a threadpool to stay async.",
          "يُشغّل الاستدلال في threadpool ليبقى لا-تزامنيًا."),
     ]},
     "right": {"head": L("Endpoints", "نقاط النهاية"), "bullets": [
        L("GET /api/health — capabilities & device.", "GET /api/health — القدرات والجهاز."),
        L("POST /api/predict — image → class, probs, GradCAM.",
          "POST /api/predict — صورة ← فئة ونِسَب وGradCAM."),
        L("POST /api/report — scores → markdown report.",
          "POST /api/report — نِسَب ← تقرير Markdown."),
        L("GET /api/metrics — training history.", "GET /api/metrics — سجل التدريب."),
        L("Uploads validated: ≤15 MB, PNG/JPEG/WEBP/BMP.",
          "تُتحقَّق الملفات: ‏≤15 ميغابايت، PNG/JPEG/WEBP/BMP."),
     ]}},

    # ── 23 · FRONTEND ────────────────────────────────────────────────────
    {"type": "two_col",
     "title": L("Frontend — Next.js 16", "الواجهة — Next.js 16"),
     "left": {"head": L("Stack", "التقنيات"), "bullets": [
        L("Next.js 16, React 19, TypeScript.", "Next.js 16 وReact 19 وTypeScript."),
        L("Tailwind v4 (CSS-first) design tokens.", "رموز تصميم Tailwind v4 (CSS أولًا)."),
        L("Pages: / · /analyze · /metrics · /about.", "الصفحات: / · /analyze · /metrics · /about."),
        L("Dark/light “reading-room” theme; smooth motion.",
          "سمة «غرفة قراءة» داكنة/فاتحة مع حركة سلسة."),
     ]},
     "right": {"head": L("API seam", "وصلة الـAPI"), "bullets": [
        L("lib/api.ts maps snake_case ↔ camelCase.",
          "يربط lib/api.ts بين snake_case وcamelCase."),
        L("Calls the backend directly, not the Next proxy…",
          "ينادي الخادم مباشرة لا وكيل Next…"),
        L("…because the proxy's ~30s timeout cuts off slow CPU reports.",
          "…لأن مهلة الوكيل (~30 ثانية) تقطع التقارير البطيئة على المعالج."),
        L("Hand-drawn SVG charts on /metrics (no chart library).",
          "رسوم SVG يدوية في /metrics (دون مكتبة رسوم)."),
     ]}},

    # ── 24 · DEPLOYMENT ──────────────────────────────────────────────────
    {"type": "bullets",
     "title": L("Deployment — Docker + nginx", "النشر — Docker و nginx"),
     "bullets": [
        L("Three containers: backend, frontend, and an internal Ollama.",
          "ثلاث حاويات: الخادم، والواجهة، وOllama داخلي."),
        L("Backend pins CPU PyTorch 2.6.0 to match the saved weights.",
          "يثبّت الخادم PyTorch 2.6.0 (CPU) لمطابقة الأوزان المحفوظة."),
        L("Services bind to localhost; a host nginx vhost (:8086) is the public door.",
          "ترتبط الخدمات بـlocalhost، وبوّابة nginx على المضيف (:8086) هي المدخل العام."),
        L("nginx routes /api → backend, everything else → frontend.",
          "يوجّه nginx ‏/api ← الخادم، وكل ما عداه ← الواجهة."),
        L("Tuned for a shared box: 2 CPU threads, Ollama unloads after 2 min idle.",
          "مضبوط لجهاز مشترك: خيطا معالج، وتفريغ Ollama بعد دقيقتي خمول."),
        L("Healthchecks + restart policies keep it alive. Live on a VPS today.",
          "فحوص صحية وسياسات إعادة تشغيل تُبقيه حيًّا. ويعمل على VPS الآن."),
     ]},

    # ── 25 · TECH STACK ──────────────────────────────────────────────────
    {"type": "table",
     "title": L("Full tech stack", "حزمة التقنيات الكاملة"),
     "head": [L("Layer", "الطبقة"), L("Technology", "التقنية")],
     "rows": [
        [L("ML / model", "التعلّم الآلي"), L("Python 3.12, PyTorch, torchvision (ResNet50)",
                                          "Python 3.12، PyTorch، torchvision (ResNet50)")],
        [L("Explainability", "التفسير"), L("pytorch-grad-cam (GradCAM)", "pytorch-grad-cam (GradCAM)")],
        [L("Report LLM", "نموذج التقرير"), L("Ollama (qwen2.5:1.5b-instruct)", "Ollama (qwen2.5:1.5b-instruct)")],
        [L("Backend", "الخادم"), L("FastAPI + uvicorn, Pydantic", "FastAPI و uvicorn و Pydantic")],
        [L("Frontend", "الواجهة"), L("Next.js 16, React 19, TypeScript, Tailwind v4",
                                    "Next.js 16، React 19، TypeScript، Tailwind v4")],
        [L("Deployment", "النشر"), L("Docker Compose + nginx on a VPS", "Docker Compose و nginx على VPS")],
     ]},

    # ── 26 · SECTION Q&A ─────────────────────────────────────────────────
    {"type": "section", "num": "07",
     "title": L("Anticipated Questions", "أسئلة متوقَّعة"),
     "subtitle": L("Answers ready for the panel", "إجابات جاهزة للجنة")},

    # ── 27 · Q&A ─────────────────────────────────────────────────────────
    {"type": "two_col",
     "title": L("Q&A — be ready", "أسئلة وأجوبة — كن مستعدًا"),
     "left": {"head": L("Method", "المنهجية"), "bullets": [
        L("“Is 99% real?” → No — data leakage; it's a claimed figure.",
          "«هل الـ99% حقيقية؟» ← لا، بسبب تسريب البيانات؛ فهي رقم مُعلَن."),
        L("“Why ResNet50, not a ViT?” → Strong, data-efficient, easy to fine-tune.",
          "«لماذا ResNet50 لا ViT؟» ← قوي وكفء في البيانات وسهل الضبط."),
        L("“Overfitting?” → Dropout, weight decay, smoothing, augmentation.",
          "«فرط التخصيص؟» ← Dropout وweight decay وتنعيم وزيادة بيانات."),
     ]},
     "right": {"head": L("System", "النظام"), "bullets": [
        L("“Why a local LLM?” → Privacy, offline, no API cost.",
          "«لماذا نموذج محلي؟» ← خصوصية وعمل دون إنترنت وبلا تكلفة."),
        L("“How does GradCAM work?” → Gradients × activations at layer4.",
          "«كيف يعمل GradCAM؟» ← تدرّجات × تنشيطات عند layer4."),
        L("“Clinical use?” → No — research/education only, by design.",
          "«للاستخدام السريري؟» ← لا، للبحث/التعليم فقط، بحكم التصميم."),
     ]}},

    # ── 28 · CLOSING ─────────────────────────────────────────────────────
    {"type": "closing",
     "title": L("Thank you", "شكرًا لكم"),
     "subtitle": L("Future work: a true held-out test set · segmentation · DICOM support · clinician study.",
                   "أعمال مستقبلية: مجموعة اختبار مستقلة فعلًا · تجزئة · دعم DICOM · دراسة مع أطباء."),
     "foot": L("NeuroScan — explainable brain-tumor MRI analysis, fully local.",
               "NeuroScan — تحليل قابل للتفسير لأورام الدماغ، محليًا بالكامل.")},
]
