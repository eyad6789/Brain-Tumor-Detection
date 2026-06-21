# -*- coding: utf-8 -*-
"""Exhaustive deep-dive content (English + Arabic) for the NeuroScan documents.

This is the *complete* technical reference behind the project — written so the
reader can answer any question about how every part was built and why. The same
SECTIONS structure renders to both report-en/ar.html and report-en/ar.docx.

Block types consumed by the renderers:
  p        {"type":"p", "text": L()}
  h        {"type":"h", "text": L()}                       # sub-heading
  bullets  {"type":"bullets", "items":[L(), ...]}
  num      {"type":"num", "items":[L(), ...]}              # ordered list
  table    {"type":"table", "head":[L(),...], "rows":[[L(),...],...]}
  code     {"type":"code", "code": "..."}                  # verbatim (untranslated)
  callout  {"type":"callout", "tone":"info|warn|good", "title":L(), "text":L()}
  image    {"type":"image", "src":"x.png", "caption":L()}
  kv       {"type":"kv", "pairs":[[L(),L()], ...]}         # definition rows
"""
from i18n import L

SECTIONS = []

# ── 01 · OVERVIEW ────────────────────────────────────────────────────────
SECTIONS.append({
    "id": "overview", "num": "01",
    "title": L("Project Overview", "نظرة عامة على المشروع"),
    "lead": L(
        "NeuroScan is an explainable deep-learning system that classifies a brain-MRI scan into one of "
        "four categories and then explains itself — visually and in words.",
        "‏NeuroScan نظام تعلّم عميق قابل للتفسير يُصنِّف صورة الرنين المغناطيسي للدماغ إلى إحدى أربع فئات، "
        "ثم يشرح قراره بصريًا وبالكلمات."),
    "blocks": [
        {"type": "p", "text": L(
            "Most student ML projects stop at a prediction. NeuroScan goes three steps further: it (1) "
            "classifies the scan with a fine-tuned ResNet50 convolutional network, (2) draws a GradCAM "
            "heatmap showing exactly which pixels drove that decision, and (3) writes a short, structured "
            "clinical report using a local large-language model. The whole pipeline runs offline on the "
            "user's own machine — no cloud services and no API keys.",
            "تتوقّف معظم مشاريع التعلّم الآلي الطلابية عند التنبؤ، أما NeuroScan فيمضي ثلاث خطوات أبعد: "
            "(1) يُصنِّف الصورة بشبكة التفافية ResNet50 مضبوطة، و(2) يرسم خريطة حرارية GradCAM تُظهر البكسلات "
            "التي قادت القرار، و(3) يكتب تقريرًا سريريًا قصيرًا منظَّمًا بنموذج لغوي كبير محلي. ويعمل خط "
            "المعالجة كاملًا دون اتصال على جهاز المستخدم نفسه — بلا خدمات سحابية ولا مفاتيح API.")},
        {"type": "h", "text": L("The three pillars", "الركائز الثلاث")},
        {"type": "bullets", "items": [
            L("Classification — what is it? A ResNet50 network outputs a probability for each of the four classes.",
              "التصنيف — ما هو؟ تُخرج شبكة ResNet50 احتمالًا لكل فئة من الفئات الأربع."),
            L("Explainability — why did it say that? GradCAM highlights the regions the model relied on.",
              "التفسير — لماذا قال ذلك؟ يُبرز GradCAM المناطق التي اعتمد عليها النموذج."),
            L("Communication — what does it mean? A local LLM turns the numbers into a readable report.",
              "التواصل — ماذا يعني ذلك؟ يحوّل نموذج لغوي محلي الأرقام إلى تقرير مقروء."),
        ]},
        {"type": "p", "text": L(
            "There are two front-ends over the same model core: a professional Next.js + FastAPI web app "
            "(the primary product) and a legacy Gradio interface kept for quick local demos.",
            "توجد واجهتان فوق نواة النموذج نفسها: تطبيق ويب احترافي بـ Next.js و FastAPI (المنتج الأساسي)، "
            "وواجهة Gradio قديمة محفوظة للعروض المحلية السريعة.")},
        {"type": "callout", "tone": "warn",
         "title": L("Scope & safety", "النطاق والسلامة"),
         "text": L(
            "NeuroScan is an educational and research prototype. It is not a medical device and must never "
            "be used for real diagnosis or treatment decisions.",
            "‏NeuroScan نموذج تعليمي وبحثي، وليس جهازًا طبيًا، ويجب ألا يُستخدم مطلقًا في قرارات تشخيص أو "
            "علاج حقيقية.")},
    ],
})

# ── 02 · PROBLEM & MOTIVATION ────────────────────────────────────────────
SECTIONS.append({
    "id": "problem", "num": "02",
    "title": L("The Problem & Motivation", "المشكلة والدافع"),
    "lead": L(
        "Reading brain MRIs is slow, requires a trained radiologist, and varies between readers. AI can "
        "assist — but only if clinicians can trust and understand it.",
        "قراءة صور رنين الدماغ بطيئة، وتتطلّب أخصائي أشعة مدرَّبًا، وتتفاوت بين القُرّاء. يمكن للذكاء "
        "الاصطناعي أن يساعد — لكن فقط إذا استطاع الأطباء الوثوق به وفهمه."),
    "blocks": [
        {"type": "p", "text": L(
            "A bare classifier that only prints \"Glioma, 92%\" is hard to trust: the user cannot tell "
            "whether the model looked at the tumor or at an irrelevant artifact. This is the classic "
            "\"black box\" problem in medical AI. NeuroScan is designed around the idea that an AI tool "
            "in medicine must be transparent and communicative, not just accurate.",
            "المُصنِّف المجرّد الذي يطبع فقط «دبقي، 92%» يصعب الوثوق به: لا يستطيع المستخدم معرفة هل نظر "
            "النموذج إلى الورم أم إلى تشويش غير ذي صلة. هذه مشكلة «الصندوق الأسود» الكلاسيكية في الذكاء "
            "الطبي. صُمِّم NeuroScan حول فكرة أن أداة الذكاء الاصطناعي في الطب يجب أن تكون شفافة "
            "وتواصلية، لا دقيقة فحسب.")},
        {"type": "h", "text": L("Design goals", "أهداف التصميم")},
        {"type": "bullets", "items": [
            L("Accuracy — a strong classifier via transfer learning on a pretrained backbone.",
              "الدقة — مُصنِّف قوي عبر التعلّم بالنقل على شبكة مُدرَّبة مسبقًا."),
            L("Transparency — every prediction comes with a visual explanation (GradCAM).",
              "الشفافية — كل تنبؤ مصحوب بتفسير بصري (GradCAM)."),
            L("Accessibility — a clear, written report a non-expert can read.",
              "سهولة الفهم — تقرير مكتوب واضح يستطيع غير المختص قراءته."),
            L("Privacy — fully local; medical images never leave the machine.",
              "الخصوصية — محلي بالكامل؛ لا تغادر الصور الطبية الجهاز."),
            L("Honesty — the app states its own limitations instead of overclaiming.",
              "الصدق — يصرّح التطبيق بحدوده بدل المبالغة."),
        ]},
    ],
})

# ── 03 · THE FOUR CLASSES ────────────────────────────────────────────────
SECTIONS.append({
    "id": "classes", "num": "03",
    "title": L("The Four Classes", "الفئات الأربع"),
    "lead": L(
        "The model distinguishes three tumor types plus a healthy class. The index order is fixed "
        "everywhere in the code because the trained weights depend on it.",
        "يميّز النموذج بين ثلاثة أنواع أورام إضافةً إلى فئة سليمة. وترتيب الفهرس ثابت في كل مكان في "
        "الشيفرة لأن الأوزان المدرَّبة تعتمد عليه."),
    "blocks": [
        {"type": "table",
         "head": [L("Index", "الفهرس"), L("Class", "الفئة"), L("Medical description", "الوصف الطبي")],
         "rows": [
            [L("0", "0"), L("Pituitary", "نخامية (Pituitary)"),
             L("A tumor of the pituitary gland at the base of the brain. Most are benign (non-cancerous).",
               "ورم في الغدة النخامية أسفل الدماغ. معظمها حميد (غير سرطاني).")],
            [L("1", "1"), L("No Tumor", "لا يوجد ورم (No Tumor)"),
             L("A healthy scan in which no tumor is detected. Note the space in the label string.",
               "فحص سليم لا يُكتشف فيه ورم. لاحظ المسافة في نص التسمية.")],
            [L("2", "2"), L("Meningioma", "سحائي (Meningioma)"),
             L("A tumor forming on the meninges, the membranes surrounding the brain and spinal cord.",
               "ورم ينشأ على الأغشية السحائية المحيطة بالدماغ والنخاع الشوكي.")],
            [L("3", "3"), L("Glioma", "دبقي (Glioma)"),
             L("A tumor originating in the brain's glial cells. It can be benign or malignant.",
               "ورم ينشأ في الخلايا الدبقية بالدماغ، وقد يكون حميدًا أو خبيثًا.")],
         ]},
        {"type": "callout", "tone": "info",
         "title": L("Why the fixed order matters", "لماذا يهمّ الترتيب الثابت"),
         "text": L(
            "The network's final layer outputs four numbers in this exact order. If the order were changed, "
            "the saved weights (model_class.pth) would map to the wrong labels. That is why the order "
            "Pituitary=0, No Tumor=1, Meningioma=2, Glioma=3 is duplicated identically in the model core, "
            "the backend and the frontend.",
            "تُخرج الطبقة الأخيرة أربعة أرقام بهذا الترتيب بالضبط. ولو تغيّر الترتيب لارتبطت الأوزان "
            "المحفوظة (model_class.pth) بتسميات خاطئة. لذلك يتكرّر الترتيب نخامية=0، لا ورم=1، سحائي=2، "
            "دبقي=3 بصورة متطابقة في نواة النموذج والخادم والواجهة.")},
    ],
})

# ── 04 · SYSTEM ARCHITECTURE ─────────────────────────────────────────────
SECTIONS.append({
    "id": "architecture", "num": "04",
    "title": L("System Architecture", "معمارية النظام"),
    "lead": L(
        "How the pieces connect: a browser talks to nginx, which routes the web page to Next.js and the "
        "API calls to FastAPI; the backend wraps the PyTorch model, GradCAM and a local LLM.",
        "كيف تتّصل الأجزاء: يتحدّث المتصفح إلى nginx الذي يوجّه صفحة الويب إلى Next.js ونداءات الـAPI إلى "
        "FastAPI؛ ويغلِّف الخادم نموذج PyTorch وGradCAM ونموذجًا لغويًا محليًا."),
    "blocks": [
        {"type": "image", "src": "architecture.png",
         "caption": L("End-to-end architecture, from the browser to the model core.",
                      "المعمارية من المتصفح إلى نواة النموذج.")},
        {"type": "h", "text": L("The shared model core", "نواة النموذج المشتركة")},
        {"type": "p", "text": L(
            "At the center is inference_core.py — the single source of truth for the model. It defines how "
            "to build the network, the image transform, the class names, and the predict function. Crucially "
            "it is import-safe: importing it does NOT load the 98 MB weights, so the backend can start "
            "instantly and load the model deliberately at startup.",
            "في المركز يقع inference_core.py — المصدر الوحيد للحقيقة بشأن النموذج. يُعرِّف كيفية بناء الشبكة، "
            "وتحويل الصورة، وأسماء الفئات، ودالة التنبؤ. والأهم أنه آمن للاستيراد: استيراده لا يُحمِّل "
            "الأوزان البالغة 98 ميغابايت، فيبدأ الخادم فورًا ويُحمِّل النموذج عمدًا عند الإقلاع.")},
        {"type": "kv", "pairs": [
            [L("inference_core.py", "inference_core.py"),
             L("build_model, load_model, TRANSFORM, CLASSES/CLASS_INFO, predict_core.",
               "‏build_model و load_model و TRANSFORM و CLASSES/CLASS_INFO و predict_core.")],
            [L("backend/", "backend/"),
             L("The FastAPI app: routes, schemas, image validation, metrics parsing.",
               "تطبيق FastAPI: المسارات، والمخطّطات، والتحقق من الصور، وقراءة المقاييس.")],
            [L("frontend/", "frontend/"),
             L("The Next.js web app: pages, components, and the API seam.",
               "تطبيق Next.js: الصفحات والمكوّنات ووصلة الـAPI.")],
            [L("gradcam_utils.py / llm_report.py", "gradcam_utils.py / llm_report.py"),
             L("Optional explainability and reporting helpers (degrade gracefully if absent).",
               "مساعدا التفسير وكتابة التقرير الاختياريان (يتراجعان بأمان عند غيابهما).")],
        ]},
    ],
})

# ── 05 · DATASET & PREPROCESSING ─────────────────────────────────────────
SECTIONS.append({
    "id": "data", "num": "05",
    "title": L("The Dataset & Preprocessing", "البيانات والمعالجة المسبقة"),
    "lead": L(
        "Every image is resized and normalized to look exactly like the data the ResNet50 backbone was "
        "originally trained on (ImageNet).",
        "تُحجَّم كل صورة وتُطبَّع لتبدو تمامًا كالبيانات التي دُرِّبت عليها شبكة ResNet50 أصلًا (ImageNet)."),
    "blocks": [
        {"type": "p", "text": L(
            "The model expects a 224×224 RGB image. The inference transform (the canonical TRANSFORM in "
            "inference_core.py) applies three deterministic steps:",
            "يتوقّع النموذج صورة 224×224 بنظام RGB. ويطبّق تحويل الاستدلال (التحويل القياسي TRANSFORM في "
            "inference_core.py) ثلاث خطوات حتمية:")},
        {"type": "num", "items": [
            L("Resize to 224 × 224 pixels.", "تغيير الحجم إلى 224×224 بكسل."),
            L("Convert to a tensor (rescaling pixel values from 0–255 to 0.0–1.0).",
              "التحويل إلى Tensor (إعادة قياس قيم البكسل من 0–255 إلى 0.0–1.0)."),
            L("Normalize per channel with ImageNet mean [0.485, 0.456, 0.406] and std [0.229, 0.224, 0.225].",
              "التطبيع لكل قناة بمتوسط ImageNet ‏[0.485, 0.456, 0.406] والانحراف [0.229, 0.224, 0.225]."),
        ]},
        {"type": "code", "code":
            "TRANSFORM = transforms.Compose([\n"
            "    transforms.Resize((224, 224)),\n"
            "    transforms.ToTensor(),\n"
            "    transforms.Normalize(mean=[0.485, 0.456, 0.406],\n"
            "                         std=[0.229, 0.224, 0.225]),\n"
            "])"},
        {"type": "callout", "tone": "info",
         "title": L("Why ImageNet statistics?", "لماذا إحصاءات ImageNet؟"),
         "text": L(
            "ResNet50's weights were learned on ImageNet, where inputs were normalized with these exact "
            "numbers. Feeding differently-scaled inputs would shift the distribution the network expects "
            "and hurt accuracy, so we reuse the same mean and standard deviation.",
            "تعلّمت أوزان ResNet50 على ImageNet حيث طُبِّعت المدخلات بهذه الأرقام بالضبط. وإدخال قيم بمقياس "
            "مختلف يزيح التوزيع الذي تتوقّعه الشبكة ويضرّ بالدقة، لذا نعيد استخدام المتوسط والانحراف "
            "نفسيهما.")},
    ],
})

# ── 06 · DATA AUGMENTATION ───────────────────────────────────────────────
SECTIONS.append({
    "id": "augment", "num": "06",
    "title": L("Data Augmentation", "زيادة البيانات"),
    "lead": L(
        "During training only, each image is randomly transformed so the model sees more variety and "
        "learns features that survive real-world noise.",
        "في التدريب فقط، تُحوَّل كل صورة عشوائيًا ليرى النموذج تنوّعًا أكبر ويتعلّم سمات تصمد أمام ضوضاء "
        "الواقع."),
    "blocks": [
        {"type": "table",
         "head": [L("Transform", "التحويل"), L("Setting", "الإعداد"), L("Why (medical rationale)", "السبب (مبرّر طبي)")],
         "rows": [
            [L("Horizontal flip", "انعكاس أفقي"), L("p = 0.5", "‏p = 0.5"),
             L("Left/right symmetry — orientation should not change the class.",
               "تماثل يسار/يمين — لا ينبغي أن يغيّر الاتجاه الفئة.")],
            [L("Vertical flip", "انعكاس رأسي"), L("p = 0.5", "‏p = 0.5"),
             L("Robustness to how a scan was loaded/oriented.",
               "متانة تجاه طريقة تحميل/توجيه الصورة.")],
            [L("Rotation", "تدوير"), L("±15°", "‏±15°"),
             L("Tolerate small misalignment of the patient's head.",
               "تحمُّل انحراف بسيط في محاذاة رأس المريض.")],
            [L("ColorJitter", "ColorJitter"), L("brightness/contrast 0.2", "سطوع/تباين 0.2"),
             L("Different scanners produce different brightness and contrast.",
               "تُنتج الأجهزة المختلفة سطوعًا وتباينًا مختلفين.")],
            [L("GaussianBlur", "GaussianBlur"), L("kernel 3", "نواة 3"),
             L("Simulate motion blur and out-of-focus artifacts.",
               "محاكاة تشوّش الحركة وفقد التركيز.")],
        ]},
        {"type": "callout", "tone": "good",
         "title": L("Validation stays clean", "يبقى التحقق نظيفًا"),
         "text": L(
            "The validation transform applies only resize + normalize — no randomness. Evaluation must be "
            "deterministic so the reported numbers are reproducible.",
            "يطبّق تحويل التحقق تغيير الحجم والتطبيع فقط — بلا عشوائية. يجب أن يكون التقييم حتميًا لتكون "
            "الأرقام المُبلَّغ عنها قابلة للتكرار.")},
    ],
})

# ── 07 · THE MODEL ───────────────────────────────────────────────────────
SECTIONS.append({
    "id": "model", "num": "07",
    "title": L("The Model: ResNet50 + Transfer Learning", "النموذج: ResNet50 والتعلّم بالنقل"),
    "lead": L(
        "Rather than training a network from scratch, NeuroScan starts from an ImageNet-pretrained ResNet50 "
        "and adapts it to brain MRIs — the standard, data-efficient approach.",
        "بدل تدريب شبكة من الصفر، يبدأ NeuroScan من ResNet50 مُدرَّبة مسبقًا على ImageNet ويكيّفها لصور رنين "
        "الدماغ — وهو النهج القياسي الكفء في البيانات."),
    "blocks": [
        {"type": "h", "text": L("What is ResNet50?", "ما هي ResNet50؟")},
        {"type": "p", "text": L(
            "ResNet50 is a 50-layer convolutional neural network. Its key innovation is the residual (skip) "
            "connection, which lets gradients flow through very deep networks without vanishing — making it "
            "possible to train 50 layers reliably. Pretrained on ImageNet (1.2M images, 1000 classes), its "
            "early layers already detect generic edges, textures and shapes that are useful for any image task.",
            "‏ResNet50 شبكة عصبية التفافية من 50 طبقة. وابتكارها الأساسي هو الوصلة المتبقّية (التخطّيّة) التي "
            "تتيح تدفّق التدرّجات عبر شبكات عميقة جدًا دون تلاشٍ — مما يجعل تدريب 50 طبقة موثوقًا. وبعد تدريبها "
            "مسبقًا على ImageNet (1.2 مليون صورة و1000 فئة)، تكتشف طبقاتها المبكرة حوافًا وقوامًا وأشكالًا "
            "عامة مفيدة لأي مهمة صور.")},
        {"type": "h", "text": L("Freezing and fine-tuning", "التجميد والضبط الدقيق")},
        {"type": "bullets", "items": [
            L("All backbone layers are frozen first (their weights won't change).",
              "تُجمَّد كل طبقات الشبكة أولًا (لن تتغيّر أوزانها)."),
            L("Then layer3 and layer4 — the deepest blocks holding high-level features — are unfrozen.",
              "ثم تُفكّ layer3 وlayer4 — أعمق الكتل التي تحمل السمات العليا."),
            L("The optimizer updates only those unfrozen layers plus the new classifier head.",
              "يحدّث المُحسِّن تلك الطبقات المفكوكة فقط إضافةً إلى رأس المُصنِّف الجديد."),
            L("This adapts the high-level features to MRIs while keeping the proven low-level detectors.",
              "هذا يكيّف السمات العليا لصور الرنين مع الإبقاء على الكواشف الدنيا المُثبَتة."),
        ]},
        {"type": "image", "src": "model_head.png",
         "caption": L("The custom classifier head replaces ResNet50's original 1000-class layer.",
                      "يستبدل رأس المُصنِّف المخصَّص طبقة الألف فئة الأصلية في ResNet50.")},
        {"type": "h", "text": L("The classifier head — and a subtle detail", "رأس المُصنِّف — وتفصيل دقيق")},
        {"type": "p", "text": L(
            "The original 1000-class layer is swapped for a small head that maps the 2048-dimensional feature "
            "vector down to 4 class scores, with dropout for regularization:",
            "تُستبدَل طبقة الألف فئة الأصلية برأس صغير يُحوِّل متجه السمات ذا 2048 بُعدًا إلى 4 درجات فئوية، "
            "مع dropout للتنظيم:")},
        {"type": "code", "code":
            "model.fc = nn.Sequential(\n"
            "    nn.Dropout(0.5),              # fc.0\n"
            "    nn.Linear(2048, 512),         # fc.1  (trainable)\n"
            "    nn.ReLU(),                    # fc.2\n"
            "    nn.Dropout(0.3),              # fc.3\n"
            "    nn.Dropout(0.3),              # fc.4  <- duplicate, intentional\n"
            "    nn.Linear(512, 4),            # fc.5  (trainable)\n"
            ")"},
        {"type": "callout", "tone": "info",
         "title": L("The intentional duplicate Dropout", "تكرار Dropout المقصود"),
         "text": L(
            "Dropout layers have no learnable weights, so the duplicate Dropout(0.3) changes nothing "
            "numerically. Its only job is to keep the final Linear layer at state-dict key fc.5. The training "
            "script's head used a BatchNorm at that position; to load the shipped weights *strictly* at "
            "inference time, the inference head reproduces the same key layout with a second Dropout instead "
            "of BatchNorm. Remove it and the final layer shifts to fc.4 and the weights fail to load.",
            "طبقات Dropout بلا أوزان قابلة للتعلّم، لذا فإن تكرار Dropout(0.3) لا يغيّر شيئًا عدديًا. ومهمّته "
            "الوحيدة إبقاء طبقة Linear الأخيرة عند المفتاح fc.5. استخدم رأس سكربت التدريب طبقة BatchNorm في "
            "ذلك الموضع؛ ولتحميل الأوزان المُسلَّمة بدقّة وقت الاستدلال، يُعيد رأس الاستدلال التخطيط نفسه "
            "بطبقة Dropout ثانية بدل BatchNorm. وإزالتها تُزيح الطبقة الأخيرة إلى fc.4 فيفشل تحميل الأوزان.")},
    ],
})

# ── 08 · TRAINING ────────────────────────────────────────────────────────
SECTIONS.append({
    "id": "training", "num": "08",
    "title": L("Training Procedure & Results", "إجراء التدريب والنتائج"),
    "lead": L(
        "The model was trained with the Adam optimizer, label-smoothed cross-entropy, a learning-rate "
        "scheduler and early stopping — converging in only seven epochs.",
        "دُرِّب النموذج بمُحسِّن Adam، وخسارة الإنتروبيا المتقاطعة مع تنعيم التسميات، ومُجدوِل لمعدّل التعلّم، "
        "وإيقاف مبكر — متقاربًا في سبع حقب فقط."),
    "blocks": [
        {"type": "table",
         "head": [L("Hyperparameter", "المعامل الفائق"), L("Value", "القيمة"), L("Purpose", "الغرض")],
         "rows": [
            [L("Optimizer", "المُحسِّن"), L("Adam, lr = 1e-4", "Adam، ‏lr = 1e-4"),
             L("Adaptive per-parameter step size; stable for fine-tuning.",
               "خطوة تكيّفية لكل معامل؛ مستقرة للضبط الدقيق.")],
            [L("Loss", "الخسارة"), L("CrossEntropy, label_smoothing = 0.1", "CrossEntropy، ‏label_smoothing = 0.1"),
             L("Softens hard labels to reduce over-confidence and overfitting.",
               "يخفّف التسميات الحادّة لتقليل الإفراط في الثقة وفرط التخصيص.")],
            [L("Weight decay", "اضمحلال الوزن"), L("1e-4", "1e-4"),
             L("L2 regularization on trainable weights.", "تنظيم L2 على الأوزان القابلة للتدريب.")],
            [L("Scheduler", "المُجدوِل"), L("ReduceLROnPlateau, ×0.5", "ReduceLROnPlateau، ‏×0.5"),
             L("Halves the LR when validation loss stops improving.",
               "يُنصِّف معدّل التعلّم عند توقّف تحسّن خسارة التحقق.")],
            [L("Batch size", "حجم الدفعة"), L("32", "32"),
             L("Samples per gradient update.", "عيّنات لكل تحديث للتدرّج.")],
            [L("Epochs", "الحقب"), L("max 20, patience 5", "حتى 20، صبر 5"),
             L("Early stopping ends training when val accuracy stalls.",
               "ينهي الإيقاف المبكر التدريب عند ثبات دقة التحقق.")],
        ]},
        {"type": "h", "text": L("Actual training log (model_log.csv)", "سجل التدريب الفعلي (model_log.csv)")},
        {"type": "table",
         "head": [L("Epoch", "الحقبة"), L("Train acc", "دقة التدريب"), L("Val acc", "دقة التحقق"),
                  L("Train loss", "خسارة التدريب"), L("Val loss", "خسارة التحقق")],
         "rows": [
            [L("1","1"), L("88.20%","88.20%"), L("94.36%","94.36%"), L("0.3306","0.3306"), L("0.1575","0.1575")],
            [L("2","2"), L("96.78%","96.78%"), L("98.47%","98.47%"), L("0.0999","0.0999"), L("0.0525","0.0525")],
            [L("3","3"), L("98.00%","98.00%"), L("98.32%","98.32%"), L("0.0683","0.0683"), L("0.0525","0.0525")],
            [L("4","4"), L("98.34%","98.34%"), L("98.63%","98.63%"), L("0.0540","0.0540"), L("0.0438","0.0438")],
            [L("5","5"), L("98.84%","98.84%"), L("98.25%","98.25%"), L("0.0438","0.0438"), L("0.0644","0.0644")],
            [L("6","6"), L("99.05%","99.05%"), L("99.39%","99.39%"), L("0.0305","0.0305"), L("0.0197","0.0197")],
            [L("7","7"), L("98.77%","98.77%"), L("99.16%","99.16%"), L("0.0482","0.0482"), L("0.0279","0.0279")],
         ]},
        {"type": "image", "src": "training_curves.png",
         "caption": L("Accuracy and loss over the 7 epochs. Best validation accuracy was 99.39% at epoch 6.",
                      "الدقة والخسارة عبر الحقب السبع. أفضل دقة تحقق كانت 99.39% عند الحقبة 6.")},
        {"type": "p", "text": L(
            "Training also writes the weights (model_class.pth), the log (model_log.csv), and two plots "
            "(learning_curves.png, confusion_matrix.png) to the repository root.",
            "يكتب التدريب أيضًا الأوزان (model_class.pth) والسجل (model_log.csv) ورسمين بيانيين "
            "(learning_curves.png و confusion_matrix.png) في جذر المستودع.")},
    ],
})

# ── 09 · HONEST LIMITATIONS ──────────────────────────────────────────────
SECTIONS.append({
    "id": "limits", "num": "09",
    "title": L("Honest Limitations & the “Claimed” Accuracy", "حدود صادقة والدقة «المُعلَنة»"),
    "lead": L(
        "The headline 99% number is presented as “claimed,” not validated — because of a known "
        "methodological flaw the project openly documents.",
        "يُقدَّم رقم الـ99% البارز بوصفه «مُعلَنًا» لا مُتحقَّقًا منه — بسبب خلل منهجي معروف يوثّقه المشروع "
        "بصراحة."),
    "blocks": [
        {"type": "callout", "tone": "warn",
         "title": L("Data leakage: test set reused for validation", "تسريب البيانات: إعادة استخدام مجموعة الاختبار للتحقق"),
         "text": L(
            "train.py uses the same test set for validation and early-stopping. That means model selection "
            "(when to stop, when to lower the LR) was tuned on the very data used to report accuracy. The "
            "result is an optimistic figure, not an unbiased estimate of how the model performs on truly "
            "unseen scans.",
            "يستخدم train.py مجموعة الاختبار نفسها للتحقق والإيقاف المبكر. أي أن اختيار النموذج (متى نتوقّف، "
            "ومتى نخفّض معدّل التعلّم) ضُبِط على البيانات نفسها المستخدمة للإبلاغ عن الدقة. والنتيجة رقم "
            "متفائل، لا تقدير غير متحيّز لأداء النموذج على صور غير مرئية فعلًا.")},
        {"type": "p", "text": L(
            "The backend's metrics endpoint and the web UI both surface this caveat explicitly, labelling the "
            "figure “claimed accuracy.” Acknowledging the flaw is deliberate: it is more scientifically "
            "honest than presenting 99% as a validated result.",
            "تُظهر نقطة المقاييس في الخادم والواجهة كلتاهما هذا التنبيه صراحةً، وتصفان الرقم بـ«الدقة "
            "المُعلَنة». والاعتراف بالخلل مقصود: فهو أكثر أمانة علميًا من تقديم 99% كنتيجة مُتحقَّق منها.")},
        {"type": "h", "text": L("Other limitations", "حدود أخرى")},
        {"type": "bullets", "items": [
            L("Single-source data: the model may not generalize to other scanners, hospitals or populations.",
              "بيانات من مصدر واحد: قد لا يعمّم النموذج على أجهزة أو مستشفيات أو مجتمعات أخرى."),
            L("Classification only: it does not localize, segment or stage a tumor.",
              "تصنيف فقط: لا يحدّد موقع الورم ولا يجزّئه ولا يحدّد مرحلته."),
            L("No clinical validation: it has never been tested in a real clinical workflow.",
              "لا تحقّق سريري: لم يُختبر قط في مسار سريري حقيقي."),
            L("Educational use only: by design, never a diagnostic tool.",
              "للاستخدام التعليمي فقط: بحكم التصميم، ليس أداة تشخيص أبدًا."),
        ]},
    ],
})

# ── 10 · INFERENCE FLOW ──────────────────────────────────────────────────
SECTIONS.append({
    "id": "inference", "num": "10",
    "title": L("Inference Flow", "مسار الاستدلال"),
    "lead": L(
        "What happens, step by step, when one image is classified inside predict_core().",
        "ما الذي يحدث خطوة بخطوة عند تصنيف صورة واحدة داخل predict_core()."),
    "blocks": [
        {"type": "num", "items": [
            L("Convert the uploaded image to RGB (drops any alpha channel).",
              "تحويل الصورة المرفوعة إلى RGB (يُسقط أي قناة شفافية)."),
            L("Apply TRANSFORM and add a batch dimension → tensor shape (1, 3, 224, 224).",
              "تطبيق TRANSFORM وإضافة بُعد الدفعة ← شكل Tensor ‏(1, 3, 224, 224)."),
            L("Run a forward pass with gradients disabled (torch.no_grad) → 4 raw logits.",
              "تمريرة أمامية مع تعطيل التدرّجات (torch.no_grad) ← 4 لوغيتات خام."),
            L("Apply softmax to turn logits into probabilities that sum to 1.",
              "تطبيق softmax لتحويل اللوغيتات إلى احتمالات مجموعها 1."),
            L("Map each probability to its class name and pick the highest as the top class.",
              "ربط كل احتمال باسم فئته واختيار الأعلى بوصفه الفئة الأولى."),
            L("Build a short markdown verdict from the class and confidence.",
              "بناء حُكم Markdown قصير من الفئة ونسبة الثقة."),
            L("Optionally generate the GradCAM heatmap for that prediction.",
              "اختياريًا توليد خريطة GradCAM الحرارية لذلك التنبؤ."),
        ]},
        {"type": "code", "code":
            "with torch.no_grad():\n"
            "    logits = model(img_tensor)\n"
            "    probs = torch.softmax(logits, dim=1).squeeze().cpu().tolist()\n"
            "label_probs = {CLASSES[i]: round(probs[i], 4) for i in range(4)}\n"
            "top_class = max(label_probs, key=label_probs.get)"},
        {"type": "p", "text": L(
            "The function returns the per-class probabilities, the top class and its confidence, the markdown "
            "verdict, and the GradCAM image — everything the API needs to build a response.",
            "تُعيد الدالة احتمالات كل فئة، والفئة الأولى ونسبة ثقتها، وحُكم Markdown، وصورة GradCAM — كل ما "
            "يحتاجه الـAPI لبناء الاستجابة.")},
    ],
})

# ── 11 · GRADCAM ─────────────────────────────────────────────────────────
SECTIONS.append({
    "id": "gradcam", "num": "11",
    "title": L("Explainability: GradCAM", "التفسير: GradCAM"),
    "lead": L(
        "GradCAM answers “where did the model look?” by producing a heatmap over the MRI that highlights the "
        "regions most responsible for the prediction.",
        "يُجيب GradCAM عن سؤال «أين نظر النموذج؟» بإنتاج خريطة حرارية فوق صورة الرنين تُبرز المناطق الأكثر "
        "مسؤوليةً عن التنبؤ."),
    "blocks": [
        {"type": "h", "text": L("How it works (intuition)", "كيف يعمل (الحدس)")},
        {"type": "num", "items": [
            L("Take the activations of the last convolutional block (model.layer4[-1]).",
              "نأخذ تنشيطات آخر كتلة التفافية (model.layer4[-1])."),
            L("Compute the gradient of the predicted class score with respect to those activations.",
              "نحسب تدرّج درجة الفئة المتوقَّعة بالنسبة إلى تلك التنشيطات."),
            L("Use the gradients as weights: feature maps that strongly raise the score count more.",
              "نستخدم التدرّجات أوزانًا: خرائط السمات التي ترفع الدرجة بقوة تُحسَب أكثر."),
            L("Combine the weighted maps into a coarse heatmap and overlay it on the original scan.",
              "ندمج الخرائط الموزونة في خريطة حرارية خشنة ونُركّبها فوق الصورة الأصلية."),
        ]},
        {"type": "p", "text": L(
            "The implementation enables aug_smooth (averaging over small augmentations) and eigen_smooth "
            "(keeping the dominant component) to suppress noise and produce a cleaner, more trustworthy map. "
            "Red areas are the most influential; cool areas matter least.",
            "تُفعِّل الشيفرة aug_smooth (المتوسط على زيادات صغيرة) وeigen_smooth (الإبقاء على المكوّن "
            "المهيمن) لكبح الضوضاء وإنتاج خريطة أنظف وأجدر بالثقة. المناطق الحمراء هي الأكثر تأثيرًا، "
            "والباردة هي الأقل أهمية.")},
        {"type": "callout", "tone": "good",
         "title": L("Graceful fallback", "تراجُع آمن"),
         "text": L(
            "If the grad-cam package is not installed, generate_gradcam simply returns the resized original "
            "image instead of crashing, and the UI shows a one-line setup hint. Explainability is optional, "
            "never a hard dependency.",
            "إذا لم تُثبَّت حزمة grad-cam، تُعيد generate_gradcam ببساطة الصورة الأصلية المُحجَّمة بدل "
            "الانهيار، وتعرض الواجهة تلميح إعداد من سطر واحد. التفسير اختياري وليس اعتمادًا صارمًا أبدًا.")},
        {"type": "callout", "tone": "info",
         "title": L("Why explainability matters here", "لماذا يهمّ التفسير هنا"),
         "text": L(
            "In medical AI, a correct answer for the wrong reason is dangerous. A heatmap lets a human verify "
            "that the model focused on the lesion rather than on text, borders, or scanning artifacts — "
            "turning a black box into something a clinician can sanity-check.",
            "في الذكاء الطبي، الإجابة الصحيحة لسبب خاطئ خطيرة. تتيح الخريطة الحرارية لإنسان التحقّق من أن "
            "النموذج ركّز على الآفة لا على نص أو حدود أو تشويش تصوير — فتحوّل الصندوق الأسود إلى شيء يمكن "
            "للطبيب مراجعته.")},
    ],
})

# ── 12 · LLM REPORT ──────────────────────────────────────────────────────
SECTIONS.append({
    "id": "llm", "num": "12",
    "title": L("The Local-LLM Clinical Report", "التقرير السريري بنموذج لغوي محلي"),
    "lead": L(
        "A local large-language model turns the raw prediction into a structured, human-readable report — "
        "with no cloud service and no API key.",
        "يحوّل نموذج لغوي كبير محلي التنبؤ الخام إلى تقرير منظَّم مقروء — دون خدمة سحابية ولا مفتاح API."),
    "blocks": [
        {"type": "p", "text": L(
            "The report is produced by Ollama, a tool that runs LLMs locally. The model is configurable via "
            "the OLLAMA_MODEL environment variable and defaults to qwen2.5:1.5b-instruct-q4_K_M — a small, "
            "quantized instruct model that runs even on modest hardware.",
            "يُنتَج التقرير بواسطة Ollama، وهي أداة تشغّل النماذج اللغوية محليًا. والنموذج قابل للضبط عبر "
            "متغيّر البيئة OLLAMA_MODEL، وافتراضيًا qwen2.5:1.5b-instruct-q4_K_M — نموذج تعليمات صغير مُكمَّم "
            "يعمل حتى على عتاد متواضع.")},
        {"type": "h", "text": L("Prompt design", "تصميم الموجِّه")},
        {"type": "p", "text": L(
            "A system prompt sets the role (a careful, compassionate clinical assistant that always adds an "
            "educational disclaimer). A user prompt injects the prediction and probabilities and demands "
            "exactly five sections, 2–4 sentences each, under 230 words:",
            "يحدّد موجِّه النظام الدور (مساعد سريري دقيق ورحيم يضيف دائمًا إخلاء مسؤولية تعليميًا). ويُدخِل "
            "موجِّه المستخدم التنبؤ والاحتمالات ويطلب خمسة أقسام بالضبط، من 2 إلى 4 جُمل لكلٍّ، وأقل من 230 "
            "كلمة:")},
        {"type": "bullets", "items": [
            L("Diagnosis Summary", "ملخص التشخيص"),
            L("About <the tumor type>", "عن <نوع الورم>"),
            L("What the Heatmap Shows", "ما تُظهره الخريطة الحرارية"),
            L("Recommended Next Steps", "الخطوات التالية المقترحة"),
            L("Important Disclaimer", "إخلاء مسؤولية مهم"),
        ]},
        {"type": "p", "text": L(
            "Generation uses temperature 0.3 (factual, low-variance text), a 2048-token context, and a "
            "capped output length. A helper strips any stray markdown code fence the model might add.",
            "يستخدم التوليد حرارة 0.3 (نص واقعي قليل التباين)، وسياقًا من 2048 رمزًا، وطولًا أقصى للمخرجات. "
            "ويزيل مساعدٌ أي سياج شيفرة Markdown زائد قد يضيفه النموذج.")},
        {"type": "callout", "tone": "info",
         "title": L("Why a local LLM?", "لماذا نموذج لغوي محلي؟"),
         "text": L(
            "Privacy — medical images and findings never leave the machine. Cost — no per-call API fees. "
            "Availability — it works fully offline. The trade-off is speed: on CPU a report can take 1–2 "
            "minutes; on a GPU about 15 seconds.",
            "الخصوصية — لا تغادر الصور والنتائج الطبية الجهاز. التكلفة — بلا رسوم API لكل نداء. التوفّر — يعمل "
            "دون اتصال تمامًا. والمقايضة هي السرعة: على المعالج قد يستغرق التقرير دقيقة إلى دقيقتين، وعلى "
            "كرت الرسوم نحو 15 ثانية.")},
        {"type": "callout", "tone": "good",
         "title": L("Degrades gracefully", "يتراجع بأمان"),
         "text": L(
            "If the Ollama client isn't installed, the server isn't running, or the model isn't pulled, the "
            "endpoint returns clear setup instructions instead of an error — and the rest of the app keeps "
            "working.",
            "إذا لم يكن عميل Ollama مُثبَّتًا، أو الخادم لا يعمل، أو النموذج غير مُنزَّل، تُعيد نقطة النهاية "
            "تعليمات إعداد واضحة بدل خطأ — ويظلّ بقية التطبيق يعمل.")},
    ],
})

# ── 13 · BACKEND ─────────────────────────────────────────────────────────
SECTIONS.append({
    "id": "backend", "num": "13",
    "title": L("Backend: FastAPI", "الخادم: FastAPI"),
    "lead": L(
        "A small, robust FastAPI service wraps the model core, validates uploads, serializes inference, and "
        "exposes four JSON endpoints.",
        "خدمة FastAPI صغيرة ومتينة تغلِّف نواة النموذج، وتتحقّق من الملفات المرفوعة، وتُسلسِل الاستدلال، "
        "وتعرض أربع نقاط نهاية JSON."),
    "blocks": [
        {"type": "h", "text": L("Startup & robustness", "الإقلاع والمتانة")},
        {"type": "bullets", "items": [
            L("A lifespan handler loads the model once, at startup, onto the chosen device (GPU or CPU).",
              "يُحمِّل مُعالِج lifespan النموذج مرة عند الإقلاع على الجهاز المختار (كرت رسوم أو معالج)."),
            L("If loading fails, the API stays up and reports the error via /api/health — it does not crash.",
              "إذا فشل التحميل يبقى الـAPI ويُبلِّغ عن الخطأ عبر /api/health — ولا ينهار."),
            L("An INFERENCE_LOCK serializes model access because GradCAM registers hooks that are not "
              "thread-safe; requests run in a threadpool to keep the server responsive.",
              "يُسلسِل INFERENCE_LOCK الوصول للنموذج لأن GradCAM يسجّل خطّافات غير آمنة للخيوط؛ وتعمل "
              "الطلبات في threadpool لإبقاء الخادم مستجيبًا."),
            L("CORS is restricted to the configured frontend origins.",
              "‏CORS مقيَّد بمصادر الواجهة المُهيّأة."),
        ]},
        {"type": "h", "text": L("The four endpoints", "نقاط النهاية الأربع")},
        {"type": "table",
         "head": [L("Endpoint", "نقطة النهاية"), L("Method", "الطريقة"), L("Purpose", "الغرض")],
         "rows": [
            [L("/api/health", "/api/health"), L("GET", "GET"),
             L("Liveness + capabilities (device, GradCAM, Ollama, class list).",
               "الحيوية والقدرات (الجهاز، GradCAM، Ollama، قائمة الفئات).")],
            [L("/api/predict", "/api/predict"), L("POST", "POST"),
             L("Multipart image → top class, all probabilities, verdict, base64 GradCAM.",
               "صورة multipart ← الفئة الأولى، كل الاحتمالات، الحُكم، GradCAM بترميز base64.")],
            [L("/api/report", "/api/report"), L("POST", "POST"),
             L("Class + scores → a markdown clinical report.",
               "الفئة والنِسَب ← تقرير سريري بصيغة Markdown.")],
            [L("/api/metrics", "/api/metrics"), L("GET", "GET"),
             L("Parsed training history + the accuracy caveat.",
               "سجل التدريب المُحلَّل مع تنبيه الدقة.")],
        ]},
        {"type": "h", "text": L("Upload validation", "التحقّق من الملفات المرفوعة")},
        {"type": "p", "text": L(
            "Before any inference, uploads are validated: the file must be non-empty, at most 15 MB, and a "
            "PNG/JPEG/WEBP/BMP image that actually decodes. Failures return precise HTTP codes (413 too "
            "large, 415 unsupported type, 422 empty/undecodable) in a uniform error envelope. The GradCAM "
            "output is encoded as a base64 PNG data URL so the browser can show it directly.",
            "قبل أي استدلال، تُتحقَّق الملفات المرفوعة: يجب أن يكون الملف غير فارغ، وبحجم 15 ميغابايت كحدّ "
            "أقصى، وصورة PNG/JPEG/WEBP/BMP تُفكَّك فعلًا. وتُعيد الإخفاقات رموز HTTP دقيقة (413 كبير جدًا، "
            "415 نوع غير مدعوم، 422 فارغ/غير قابل للفك) في غلاف خطأ موحَّد. وتُرمَّز مخرجات GradCAM كعنوان "
            "بيانات PNG بترميز base64 ليعرضها المتصفح مباشرة.")},
        {"type": "p", "text": L(
            "Request and response shapes are defined with Pydantic models (HealthResponse, PredictResponse, "
            "ReportRequest, MetricsResponse …), which validate types automatically and document the API.",
            "تُعرَّف أشكال الطلب والاستجابة بنماذج Pydantic ‏(HealthResponse و PredictResponse و ReportRequest "
            "و MetricsResponse …) التي تتحقّق من الأنواع تلقائيًا وتوثّق الـAPI.")},
    ],
})

# ── 14 · FRONTEND ────────────────────────────────────────────────────────
SECTIONS.append({
    "id": "frontend", "num": "14",
    "title": L("Frontend: the Next.js Web App", "الواجهة: تطبيق Next.js"),
    "lead": L(
        "A modern, polished single-page experience built with Next.js 16, React 19, TypeScript and "
        "Tailwind v4, with a clinical dark/light theme.",
        "تجربة حديثة ومصقولة بصفحة واحدة، مبنية بـ Next.js 16 و React 19 و TypeScript و Tailwind v4، مع "
        "سمة سريرية داكنة/فاتحة."),
    "blocks": [
        {"type": "h", "text": L("Pages & flow", "الصفحات والتدفّق")},
        {"type": "bullets", "items": [
            L("/ — a landing page introducing the pipeline and the four classes.",
              "/ — صفحة هبوط تُعرِّف بخط المعالجة والفئات الأربع."),
            L("/analyze — the workspace: upload, prediction, GradCAM viewer, and the report panel.",
              "/analyze — مساحة العمل: الرفع، والتنبؤ، وعارض GradCAM، ولوحة التقرير."),
            L("/metrics — training history with hand-drawn SVG charts and the accuracy caveat.",
              "/metrics — سجل التدريب برسوم SVG يدوية مع تنبيه الدقة."),
            L("/about — how it works and an honest list of limitations.",
              "/about — كيف يعمل وقائمة صادقة بالحدود."),
        ]},
        {"type": "h", "text": L("The API seam", "وصلة الـAPI")},
        {"type": "p", "text": L(
            "All network calls go through lib/api.ts, a single seam that converts the backend's snake_case "
            "JSON into the frontend's camelCase TypeScript types (and back). It calls the FastAPI backend "
            "directly rather than through Next.js's proxy, because the proxy's ~30-second timeout would cut "
            "off a slow CPU-generated report; the backend base URL is set via NEXT_PUBLIC_API_BASE.",
            "تمرّ كل نداءات الشبكة عبر lib/api.ts، وهي وصلة واحدة تحوّل JSON بصيغة snake_case من الخادم إلى "
            "أنواع TypeScript بصيغة camelCase في الواجهة (والعكس). وتنادي خادم FastAPI مباشرة بدل وكيل "
            "Next.js، لأن مهلة الوكيل (~30 ثانية) ستقطع تقريرًا بطيئًا مُولَّدًا على المعالج؛ ويُضبَط عنوان "
            "الخادم عبر NEXT_PUBLIC_API_BASE.")},
        {"type": "h", "text": L("Design system", "نظام التصميم")},
        {"type": "p", "text": L(
            "Tailwind v4's CSS-first approach defines the whole palette as CSS variables, with an instant "
            "dark/light switch. The dark “reading-room” theme uses a near-black background with cyan and "
            "violet accents; charts on the metrics page are drawn by hand in SVG (no charting library) for a "
            "lighter bundle and full control. Subtle motion and a radiological grid texture complete the look.",
            "يُعرِّف نهج Tailwind v4 «CSS أولًا» اللوحة اللونية كاملةً كمتغيّرات CSS، مع تبديل فوري بين "
            "الداكن والفاتح. وتستخدم سمة «غرفة القراءة» الداكنة خلفية شبه سوداء بلمسات سماوية وبنفسجية؛ "
            "وتُرسم رسوم صفحة المقاييس يدويًا بـ SVG (دون مكتبة رسوم) لحزمة أخفّ وتحكّم كامل. وتُكمل حركةٌ "
            "خفيفة ونسيجُ شبكة إشعاعية المظهرَ.")},
    ],
})

# ── 15 · DEPLOYMENT ──────────────────────────────────────────────────────
SECTIONS.append({
    "id": "deploy", "num": "15",
    "title": L("Deployment: Docker + nginx", "النشر: Docker و nginx"),
    "lead": L(
        "The whole stack is containerized with Docker Compose and published behind an nginx reverse proxy on "
        "a VPS.",
        "تُحزَّم الحزمة كاملةً بـ Docker Compose وتُنشَر خلف وكيل nginx عكسي على خادم VPS."),
    "blocks": [
        {"type": "h", "text": L("Three services", "ثلاث خدمات")},
        {"type": "bullets", "items": [
            L("backend — the FastAPI container, pinned to CPU PyTorch 2.6.0 to match the saved weights.",
              "‏backend — حاوية FastAPI، مثبَّتة على PyTorch 2.6.0 للمعالج لمطابقة الأوزان المحفوظة."),
            L("frontend — the Next.js production server.",
              "‏frontend — خادم إنتاج Next.js."),
            L("ollama — a local LLM service, internal-only, never exposed to the public.",
              "‏ollama — خدمة نموذج لغوي محلية، داخلية فقط، لا تُعرَض للعموم أبدًا."),
        ]},
        {"type": "p", "text": L(
            "The application services bind only to localhost; a host nginx virtual host on port 8086 is the "
            "single public entry point. nginx routes /api requests to the backend and everything else to the "
            "frontend, so the browser sees one origin.",
            "ترتبط خدمات التطبيق بـlocalhost فقط؛ ومضيف nginx افتراضي على المنفذ 8086 هو نقطة الدخول العامة "
            "الوحيدة. ويوجّه nginx طلبات /api إلى الخادم وكل ما عداها إلى الواجهة، فيرى المتصفح مصدرًا "
            "واحدًا.")},
        {"type": "h", "text": L("Tuned for a shared box", "مضبوط لجهاز مشترك")},
        {"type": "bullets", "items": [
            L("PyTorch limited to 2 CPU threads (OMP_NUM_THREADS=2).",
              "‏PyTorch محدود بخيطي معالج (OMP_NUM_THREADS=2)."),
            L("Ollama unloads the model after 2 minutes idle and loads at most one model at a time.",
              "يُفرِّغ Ollama النموذج بعد دقيقتي خمول، ويُحمِّل نموذجًا واحدًا على الأكثر في وقت واحد."),
            L("Health checks and restart policies keep the containers alive.",
              "تُبقي الفحوص الصحية وسياسات إعادة التشغيل الحاويات حيّة."),
        ]},
    ],
})

# ── 16 · TECH STACK ──────────────────────────────────────────────────────
SECTIONS.append({
    "id": "stack", "num": "16",
    "title": L("The Full Tech Stack", "حزمة التقنيات الكاملة"),
    "lead": L("Every major technology used, and what it is responsible for.",
              "كل تقنية رئيسية مستخدمة، وما هي مسؤولة عنه."),
    "blocks": [
        {"type": "table",
         "head": [L("Layer", "الطبقة"), L("Technology", "التقنية"), L("Role", "الدور")],
         "rows": [
            [L("Language", "اللغة"), L("Python 3.12 · TypeScript", "Python 3.12 · TypeScript"),
             L("Backend/ML in Python; frontend in TypeScript.",
               "الخادم/التعلّم بالبايثون؛ والواجهة بـ TypeScript.")],
            [L("Model", "النموذج"), L("PyTorch · torchvision", "PyTorch · torchvision"),
             L("ResNet50 definition, training and inference.",
               "تعريف ResNet50 وتدريبه واستدلاله.")],
            [L("Explainability", "التفسير"), L("pytorch-grad-cam", "pytorch-grad-cam"),
             L("GradCAM heatmaps.", "خرائط GradCAM الحرارية.")],
            [L("Report LLM", "نموذج التقرير"), L("Ollama", "Ollama"),
             L("Runs a local LLM for the clinical report.",
               "يشغّل نموذجًا لغويًا محليًا لكتابة التقرير.")],
            [L("Backend", "الخادم"), L("FastAPI · uvicorn · Pydantic", "FastAPI · uvicorn · Pydantic"),
             L("HTTP API, async server, schema validation.",
               "واجهة HTTP، خادم لا-تزامني، التحقّق من المخطّطات.")],
            [L("Frontend", "الواجهة"), L("Next.js 16 · React 19 · Tailwind v4", "Next.js 16 · React 19 · Tailwind v4"),
             L("The web UI, routing and styling.", "واجهة الويب والتوجيه والتنسيق.")],
            [L("Packaging", "التحزيم"), L("Docker Compose · nginx", "Docker Compose · nginx"),
             L("Containerization and reverse proxy.", "التحزيم والوكيل العكسي.")],
        ]},
    ],
})

# ── 17 · RUN IT YOURSELF ─────────────────────────────────────────────────
SECTIONS.append({
    "id": "run", "num": "17",
    "title": L("How to Run It Yourself", "كيف تشغّله بنفسك"),
    "lead": L("The exact commands to start the backend, the frontend, and the optional local LLM.",
              "الأوامر الدقيقة لتشغيل الخادم والواجهة والنموذج اللغوي المحلي الاختياري."),
    "blocks": [
        {"type": "h", "text": L("Backend (from the repo root)", "الخادم (من جذر المستودع)")},
        {"type": "code", "code":
            "source venv/bin/activate\n"
            "pip install -r backend/requirements.txt\n"
            "uvicorn backend.main:app --port 8000 --reload"},
        {"type": "h", "text": L("Frontend", "الواجهة")},
        {"type": "code", "code":
            "cd frontend && npm install && npm run dev   # http://localhost:3000"},
        {"type": "h", "text": L("Optional local LLM report", "تقرير النموذج اللغوي المحلي (اختياري)")},
        {"type": "code", "code":
            "ollama serve\n"
            "ollama pull qwen2.5:1.5b-instruct-q4_K_M"},
        {"type": "p", "text": L(
            "A legacy Gradio UI is also available with `python app.py` (port 7860), and the model can be "
            "retrained with `python train.py --train_dir ... --test_dir ...`.",
            "تتوفّر أيضًا واجهة Gradio قديمة عبر `python app.py` (المنفذ 7860)، ويمكن إعادة تدريب النموذج "
            "بـ `python train.py --train_dir ... --test_dir ...`.")},
    ],
})

# ── 18 · Q&A ─────────────────────────────────────────────────────────────
SECTIONS.append({
    "id": "qa", "num": "18",
    "title": L("Anticipated Questions & Answers", "أسئلة متوقَّعة وإجاباتها"),
    "lead": L("The questions a panel is most likely to ask — with crisp, defensible answers.",
              "الأسئلة الأرجح أن تطرحها اللجنة — بإجابات موجزة قابلة للدفاع."),
    "blocks": [
        {"type": "kv", "pairs": [
            [L("Is the 99% accuracy real?", "هل دقة الـ99% حقيقية؟"),
             L("It is a “claimed” figure. Because the test set was reused for validation (data leakage), the "
               "number is optimistic. A proper train/validation/test split or cross-validation is needed for "
               "an unbiased estimate.",
               "إنه رقم «مُعلَن». ولأن مجموعة الاختبار أُعيد استخدامها للتحقق (تسريب بيانات)، فالرقم متفائل. "
               "ونحتاج تقسيمًا سليمًا تدريب/تحقق/اختبار أو تحقّقًا متقاطعًا لتقدير غير متحيّز.")],
            [L("Why ResNet50 and not a Vision Transformer?", "لماذا ResNet50 لا Vision Transformer؟"),
             L("CNNs like ResNet50 are extremely data-efficient and easy to fine-tune on small medical "
               "datasets, whereas ViTs typically need far more data. ResNet50 is a proven, well-understood "
               "baseline.",
               "الشبكات الالتفافية مثل ResNet50 كفؤة جدًا في البيانات وسهلة الضبط على مجموعات طبية صغيرة، "
               "بينما تحتاج محوّلات الرؤية عادةً بيانات أكثر بكثير. وResNet50 خط أساس مُثبَت ومفهوم جيدًا.")],
            [L("How do you fight overfitting?", "كيف تقاوم فرط التخصيص؟"),
             L("Four ways: dropout in the head, L2 weight decay, label smoothing, and heavy data "
               "augmentation. The tiny train/validation gap supports that it generalized within this dataset.",
               "بأربع طرق: dropout في الرأس، واضمحلال وزن L2، وتنعيم التسميات، وزيادة بيانات مكثّفة. والفجوة "
               "الضئيلة بين التدريب والتحقق تدعم تعميمه ضمن هذه المجموعة.")],
            [L("Why a local LLM instead of an API?", "لماذا نموذج لغوي محلي بدل API؟"),
             L("Privacy of medical data, zero per-call cost, and full offline operation. The cost is speed "
               "on CPU-only machines.",
               "خصوصية البيانات الطبية، وانعدام تكلفة كل نداء، والعمل دون اتصال تمامًا. والثمن هو السرعة على "
               "الأجهزة ذات المعالج فقط.")],
            [L("How does GradCAM actually work?", "كيف يعمل GradCAM فعليًا؟"),
             L("It weights the activations of the last convolutional layer by the gradient of the predicted "
               "class, producing a heatmap of the most influential regions.",
               "يرجّح تنشيطات آخر طبقة التفافية بتدرّج الفئة المتوقَّعة، فيُنتج خريطة حرارية لأكثر المناطق "
               "تأثيرًا.")],
            [L("Could this be used in a hospital?", "هل يمكن استخدامه في مستشفى؟"),
             L("No. It is an educational/research prototype with no clinical validation and known data "
               "issues; it is explicitly not a medical device.",
               "لا. إنه نموذج تعليمي/بحثي بلا تحقّق سريري وبه مشكلات بيانات معروفة؛ وهو صراحةً ليس جهازًا "
               "طبيًا.")],
            [L("Why two front-ends?", "لماذا واجهتان؟"),
             L("Gradio gave a fast prototype UI; the Next.js + FastAPI app is the polished, production-style "
               "product. Both reuse the same inference_core, so behavior is consistent.",
               "أعطت Gradio واجهة نموذج أولي سريعة؛ وتطبيق Next.js مع FastAPI هو المنتج المصقول بأسلوب "
               "الإنتاج. وكلاهما يعيد استخدام inference_core نفسه، فالسلوك متّسق.")],
        ]},
    ],
})

# ── 19 · GLOSSARY ────────────────────────────────────────────────────────
SECTIONS.append({
    "id": "glossary", "num": "19",
    "title": L("Glossary of Key Terms", "مسرد المصطلحات الأساسية"),
    "lead": L("Plain-language definitions for the technical vocabulary used above.",
              "تعريفات مبسّطة للمفردات التقنية المستخدمة أعلاه."),
    "blocks": [
        {"type": "kv", "pairs": [
            [L("CNN", "الشبكة الالتفافية (CNN)"),
             L("A neural network that learns visual patterns through layers of small filters.",
               "شبكة عصبية تتعلّم الأنماط البصرية عبر طبقات من مرشّحات صغيرة.")],
            [L("Transfer learning", "التعلّم بالنقل"),
             L("Reusing a model pretrained on a large dataset and adapting it to a new, smaller task.",
               "إعادة استخدام نموذج مُدرَّب مسبقًا على مجموعة كبيرة وتكييفه لمهمة جديدة أصغر.")],
            [L("Residual connection", "الوصلة المتبقّية"),
             L("A “shortcut” that adds a layer's input to its output, enabling very deep networks.",
               "«اختصار» يضيف مدخل الطبقة إلى مخرجها، مما يتيح شبكات عميقة جدًا.")],
            [L("Softmax", "Softmax"),
             L("A function that turns raw scores into probabilities that sum to one.",
               "دالة تحوّل الدرجات الخام إلى احتمالات مجموعها واحد.")],
            [L("Dropout", "Dropout"),
             L("Randomly disabling neurons during training to prevent over-reliance and overfitting.",
               "تعطيل عصبونات عشوائيًا أثناء التدريب لمنع الاعتماد المفرط وفرط التخصيص.")],
            [L("Logits", "اللوغيتات"),
             L("The raw, un-normalized output scores of the network before softmax.",
               "درجات الخرج الخام غير المُطبَّعة قبل softmax.")],
            [L("Epoch", "الحقبة"),
             L("One full pass of the training data through the model.",
               "تمريرة كاملة واحدة لبيانات التدريب عبر النموذج.")],
            [L("Early stopping", "الإيقاف المبكر"),
             L("Halting training when validation performance stops improving, to avoid overfitting.",
               "إيقاف التدريب عند توقّف تحسّن أداء التحقق، لتجنّب فرط التخصيص.")],
        ]},
    ],
})

# ── 20 · CONCLUSION ──────────────────────────────────────────────────────
SECTIONS.append({
    "id": "conclusion", "num": "20",
    "title": L("Conclusion & Future Work", "الخاتمة والأعمال المستقبلية"),
    "lead": L(
        "NeuroScan shows that a student project can be accurate, transparent, private and honest at the same "
        "time.",
        "يُظهر NeuroScan أن مشروعًا طلابيًا يمكن أن يكون دقيقًا وشفافًا وخصوصيًا وصادقًا في آن واحد."),
    "blocks": [
        {"type": "p", "text": L(
            "By pairing a fine-tuned ResNet50 with GradCAM explanations and a local-LLM report, NeuroScan "
            "turns a bare prediction into something a human can inspect and understand — all running offline "
            "on the user's machine, wrapped in a polished web app and deployed with Docker.",
            "بإقران ResNet50 المضبوطة بتفسيرات GradCAM وتقرير بنموذج لغوي محلي، يحوّل NeuroScan التنبؤ "
            "المجرّد إلى شيء يستطيع الإنسان فحصه وفهمه — وكل ذلك يعمل دون اتصال على جهاز المستخدم، ضمن تطبيق "
            "ويب مصقول ومنشور بـ Docker.")},
        {"type": "h", "text": L("Future work", "أعمال مستقبلية")},
        {"type": "bullets", "items": [
            L("Fix the evaluation: a true held-out test set or k-fold cross-validation.",
              "إصلاح التقييم: مجموعة اختبار مستقلة فعلًا أو تحقّق متقاطع k-fold."),
            L("Add tumor segmentation to localize, not just classify.",
              "إضافة تجزئة الورم لتحديد الموقع لا التصنيف فقط."),
            L("Support native DICOM medical-image input.",
              "دعم إدخال صور DICOM الطبية الأصلية."),
            L("Calibrate confidence and report uncertainty.",
              "معايرة الثقة والإبلاغ عن عدم اليقين."),
            L("Evaluate across multiple datasets and scanners for real generalization.",
              "التقييم عبر مجموعات وأجهزة متعددة لتعميم حقيقي."),
        ]},
        {"type": "callout", "tone": "warn",
         "title": L("Final reminder", "تذكير أخير"),
         "text": L(
            "NeuroScan is for education and research only. It is not a medical device and must not be used "
            "for diagnosis.",
            "‏NeuroScan للتعليم والبحث فقط. وهو ليس جهازًا طبيًا ويجب ألا يُستخدم للتشخيص.")},
    ],
})
