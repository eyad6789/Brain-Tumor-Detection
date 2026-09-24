# -*- coding: utf-8 -*-
"""Extra deep-dive sections, part 1 — concepts, CNN theory, and the mathematics.

Spliced into doc_data.SECTIONS by doc_extra.splice(). Same block vocabulary as
doc_data.py. Every number quoted here is taken from the repository itself
(brain-tumor.ipynb outputs, model_log.csv, the source files) — nothing invented.
"""
from i18n import L

# ── A · THE 3-MINUTE EXPLANATION ─────────────────────────────────────────
PITCH = {
    "id": "pitch",
    "title": L("The 3-Minute Explanation", "الشرح في ثلاث دقائق"),
    "lead": L(
        "If you remember only one page of this document, remember this one. It is the whole project "
        "in plain language, in the order you should say it out loud.",
        "إن لم تتذكّر من هذا المستند سوى صفحة واحدة، فلتكن هذه. إنها المشروع كاملًا بلغة بسيطة، "
        "وبالترتيب الذي ينبغي أن تقوله به."),
    "blocks": [
        {"type": "h", "text": L("Say this first — the problem", "قُل هذا أولًا — المشكلة")},
        {"type": "p", "text": L(
            "A brain MRI is a stack of grayscale images. Deciding whether there is a tumor, and which "
            "of the three common types it is, requires a trained radiologist and takes time. In many "
            "hospitals there are far more scans than radiologists. AI can help with triage — but a "
            "doctor will never trust a program that just prints a word and a percentage.",
            "صورة الرنين المغناطيسي للدماغ مجموعة من الصور الرمادية. وتحديد وجود ورم من عدمه، وأيّ "
            "الأنواع الثلاثة الشائعة هو، يتطلّب أخصائي أشعة مدرَّبًا ويستغرق وقتًا. وفي كثير من "
            "المستشفيات عدد الصور أكبر بكثير من عدد الأخصائيين. يستطيع الذكاء الاصطناعي المساعدة في "
            "الفرز — لكن الطبيب لن يثق أبدًا ببرنامج يطبع كلمة ونسبة مئوية فقط.")},
        {"type": "h", "text": L("Then this — what we built", "ثم هذا — ما الذي بنيناه")},
        {"type": "p", "text": L(
            "NeuroScan takes one MRI image and answers three questions instead of one. WHAT: a "
            "convolutional neural network (ResNet50) classifies the scan as Glioma, Meningioma, "
            "Pituitary, or No Tumor, with a probability for each. WHERE: GradCAM draws a heatmap "
            "directly on the scan showing the exact pixels that drove the decision, so a human can "
            "check that the model looked at the lesion and not at a label or an artifact. WHAT IT "
            "MEANS: a language model running locally on the same machine writes a short, structured "
            "clinical report in five sections that a non-specialist can read.",
            "يأخذ NeuroScan صورة رنين واحدة ويُجيب عن ثلاثة أسئلة بدل سؤال واحد. ماذا: تُصنِّف شبكة "
            "عصبية التفافية (ResNet50) الصورة إلى ورم دبقي أو سحائي أو نخامي أو لا ورم، مع احتمال "
            "لكل فئة. أين: يرسم GradCAM خريطة حرارية فوق الصورة نفسها تُظهر البكسلات التي قادت "
            "القرار، ليتحقّق الإنسان من أن النموذج نظر إلى الآفة لا إلى مُلصَق أو تشويش. وما معنى "
            "ذلك: يكتب نموذج لغوي يعمل محليًا على الجهاز نفسه تقريرًا سريريًا قصيرًا منظَّمًا في خمسة "
            "أقسام يستطيع غير المختص قراءته.")},
        {"type": "h", "text": L("Then this — why it is different", "ثم هذا — لماذا هو مختلف")},
        {"type": "bullets", "items": [
            L("It explains itself. Most student projects stop at the prediction; we added the "
              "\"why\" (GradCAM) and the \"so what\" (the report).",
              "يشرح نفسه. تتوقّف معظم المشاريع الطلابية عند التنبؤ، أما نحن فأضفنا «لماذا» (GradCAM) "
              "و«وماذا بعد» (التقرير)."),
            L("It is 100% offline and private. No cloud, no API key, no upload of a patient's scan "
              "to anyone's server. The image never leaves the machine.",
              "يعمل بلا اتصال بنسبة 100% ويحفظ الخصوصية. لا سحابة ولا مفتاح API ولا رفع لصورة مريض "
              "إلى خادم أحد. لا تغادر الصورة الجهاز إطلاقًا."),
            L("It is a real product, not a notebook: a typed REST API, a production web app, Docker "
              "containers, health checks and graceful degradation when a component is missing.",
              "إنه منتج حقيقي لا دفتر ملاحظات: واجهة REST مُوصَّفة الأنواع، وتطبيق ويب إنتاجي، "
              "وحاويات Docker، وفحوص صحة، وتراجُع آمن عند غياب أي مكوّن."),
            L("It is honest. We label our own headline accuracy \"claimed\" and publish the exact "
              "methodological flaw that makes it optimistic. That is what a reviewer wants to hear.",
              "إنه صادق. نصف دقّتنا المُعلَنة بأنها «مُعلَنة» وننشر الخلل المنهجي الدقيق الذي يجعلها "
              "متفائلة. وهذا ما يريد المُحكِّم سماعه."),
        ]},
        {"type": "h", "text": L("The numbers to memorize", "الأرقام التي تُحفظ")},
        {"type": "table",
         "head": [L("Fact", "المعطى"), L("Value", "القيمة")],
         "rows": [
            [L("Classes", "الفئات"), L("4 — Glioma, Meningioma, Pituitary, No Tumor",
                                       "4 — دبقي، سحائي، نخامي، لا ورم")],
            [L("Training images", "صور التدريب"), L("5,712", "5,712")],
            [L("Test images", "صور الاختبار"), L("1,311", "1,311")],
            [L("Model", "النموذج"), L("ResNet50, 50 layers, ~24.6M parameters, 94 MB",
                                      "‏ResNet50، 50 طبقة، نحو 24.6 مليون معامل، 94 ميغابايت")],
            [L("Input", "المدخل"), L("224 × 224 RGB", "224 × 224 بنظام RGB")],
            [L("Best validation accuracy", "أفضل دقة تحقق"), L("99.39% (epoch 6) — claimed, see §Limitations",
                                                              "99.39% (الحقبة 6) — مُعلَنة، انظر قسم الحدود")],
            [L("Training time", "زمن التدريب"), L("7 epochs, early-stopped", "7 حقب، بإيقاف مبكر")],
            [L("Inference time", "زمن الاستدلال"), L("well under a second on CPU (a few seconds with GradCAM)",
                                                     "أقل من ثانية بكثير على المعالج (بضع ثوانٍ مع GradCAM)")],
            [L("Report time", "زمن التقرير"), L("~15 s on GPU, 1–2 min on CPU",
                                                "نحو 15 ثانية على كرت الرسوم، ودقيقة إلى دقيقتين على المعالج")],
        ]},
        {"type": "callout", "tone": "good",
         "title": L("The one sentence that wins the room", "الجملة الواحدة التي تكسب القاعة"),
         "text": L(
            "\"Any team can train a classifier. We built the part that makes a classifier usable by a "
            "human being: it shows you where it looked, it writes down what it found, it runs entirely "
            "on your own machine, and it tells you honestly what it cannot do.\"",
            "«أي فريق يستطيع تدريب مُصنِّف. أما نحن فبنينا الجزء الذي يجعل المُصنِّف صالحًا لاستخدام "
            "إنسان: يُريك أين نظر، ويكتب ما وجد، ويعمل كاملًا على جهازك، ويخبرك بصدق بما لا يستطيع "
            "فعله.»")},
    ],
}

# ── B · PROJECT EVOLUTION ────────────────────────────────────────────────
EVOLUTION = {
    "id": "evolution",
    "title": L("From Notebook to Product: How the Project Evolved",
               "من دفتر ملاحظات إلى منتج: كيف تطوّر المشروع"),
    "lead": L(
        "NeuroScan was not built in one pass. It went through five distinct versions, and every "
        "version fixed a specific weakness in the one before it. The repository still contains the "
        "evidence of each stage.",
        "لم يُبنَ NeuroScan دفعة واحدة، بل مرّ بخمس نسخ متمايزة، وأصلحت كل نسخة ضعفًا محدَّدًا في "
        "سابقتها. وما زال المستودع يحتفظ بأثر كل مرحلة."),
    "blocks": [
        {"type": "h", "text": L("v0 — the Kaggle notebook (TensorFlow / Keras)",
                                "النسخة صفر — دفتر Kaggle ‏(TensorFlow / Keras)")},
        {"type": "p", "text": L(
            "The project began as brain-tumor.ipynb, a 2.8 MB Kaggle notebook using TensorFlow/Keras. "
            "It loaded the whole dataset into RAM as one NumPy array, built a ResNet50 with "
            "include_top=False, froze the first 80 Keras layers, and trained a Flatten → Dropout(0.5) "
            "→ Dense(512, relu) → Dropout(0.3) → Dropout(0.3) → Dense(4, softmax) head for 7 epochs. "
            "It reached 98.47% test accuracy and saved model_class.h5.",
            "بدأ المشروع بوصفه brain-tumor.ipynb، وهو دفتر Kaggle بحجم 2.8 ميغابايت يستخدم "
            "TensorFlow/Keras. حمّل المجموعة كاملةً في الذاكرة كمصفوفة NumPy واحدة، وبنى ResNet50 بـ "
            "include_top=False، وجمّد أول 80 طبقة Keras، ودرّب رأسًا من Flatten ثم Dropout(0.5) ثم "
            "Dense(512, relu) ثم Dropout(0.3) ثم Dropout(0.3) ثم Dense(4, softmax) لسبع حقب. وبلغ دقة "
            "اختبار 98.47% وحفظ model_class.h5.")},
        {"type": "callout", "tone": "info",
         "title": L("Where the famous duplicate Dropout came from",
                    "من أين جاء تكرار Dropout الشهير"),
         "text": L(
            "The duplicated Dropout(0.3) that the PyTorch inference head still preserves is not a "
            "PyTorch invention — it is visible in cell 17 of the original Keras notebook, written "
            "twice in a row. When the head was ported to PyTorch it was reproduced faithfully, layer "
            "for layer, and once weights were saved against that layout the duplicate became load-"
            "bearing. It is a small, honest piece of software archaeology and a good story to tell.",
            "تكرار Dropout(0.3) الذي ما زال رأس الاستدلال في PyTorch يحافظ عليه ليس اختراعًا من "
            "PyTorch — بل هو ظاهر في الخلية 17 من دفتر Keras الأصلي، مكتوبًا مرّتين متتاليتين. وحين "
            "نُقِل الرأس إلى PyTorch أُعيد إنتاجه بأمانة طبقةً بطبقة، وما إن حُفِظت الأوزان على ذلك "
            "التخطيط حتى صار التكرار حاملًا للبنية. إنها قطعة صغيرة وصادقة من «آثار البرمجيات» "
            "وحكاية جديرة بأن تُروى.")},
        {"type": "h", "text": L("v1 — the PyTorch rewrite", "النسخة الأولى — إعادة الكتابة بـ PyTorch")},
        {"type": "p", "text": L(
            "The notebook was rewritten as a PyTorch training script with a streaming Dataset (images "
            "read from disk on demand instead of a 5,712 × 224 × 224 × 3 array held in RAM), an "
            "adaptive-average-pool head (2048 → 512 → 4 instead of Keras's Flatten over 100,352 "
            "features), and per-epoch CSV logging. This run produced the shipped model_class.pth and "
            "model_log.csv — 7 epochs, best validation accuracy 99.39%.",
            "أُعيدت كتابة الدفتر بوصفه سكربت تدريب بـ PyTorch مع Dataset تدفّقي (تُقرأ الصور من "
            "القرص عند الطلب بدل مصفوفة 5712×224×224×3 في الذاكرة)، ورأسٍ يعتمد التجميع المتوسط "
            "التكيّفي ‏(2048 ← 512 ← 4 بدل Flatten على 100,352 سمة في Keras)، وتسجيلٍ لكل حقبة في "
            "ملف CSV. أنتج هذا التشغيل model_class.pth و model_log.csv المُسلَّمين — سبع حقب، وأفضل "
            "دقة تحقق 99.39%.")},
        {"type": "h", "text": L("v2 — Gradio: the first usable interface",
                                "النسخة الثانية — Gradio: أول واجهة صالحة للاستخدام")},
        {"type": "p", "text": L(
            "app.py wrapped the model in a Gradio UI so a non-programmer could drag an image in. This "
            "is where the two ideas that define the project were added: GradCAM heatmaps "
            "(gradcam_utils.py) and the local-LLM report (llm_report.py). Gradio was chosen because it "
            "turns a Python function into a web UI in about twenty lines — perfect for proving the "
            "concept quickly.",
            "غلّف app.py النموذج بواجهة Gradio ليتمكّن غير المبرمج من سحب صورة إليها. وهنا أُضيفت "
            "الفكرتان اللتان تُعرّفان المشروع: خرائط GradCAM الحرارية (gradcam_utils.py) وتقرير "
            "النموذج اللغوي المحلي (llm_report.py). واختيرت Gradio لأنها تحوّل دالة بايثون إلى واجهة "
            "ويب في نحو عشرين سطرًا — وهو مثالي لإثبات الفكرة بسرعة.")},
        {"type": "h", "text": L("v3 — the real product: FastAPI + Next.js",
                                "النسخة الثالثة — المنتج الحقيقي: FastAPI و Next.js")},
        {"type": "p", "text": L(
            "Gradio's limits showed quickly: no control over the design, no real API other systems "
            "could call, everything in one process, and the model loaded at import time so a bad "
            "checkpoint crashed the whole app. The project was split into a FastAPI backend and a "
            "Next.js frontend, and the model code was extracted into inference_core.py so that both "
            "front-ends and the training pipeline could never drift apart. This is the version that is "
            "presented as the product.",
            "ظهرت حدود Gradio سريعًا: لا تحكّم في التصميم، ولا واجهة برمجية حقيقية تناديها أنظمة "
            "أخرى، وكل شيء في عملية واحدة، والنموذج يُحمَّل عند الاستيراد فينهار التطبيق كلّه بسبب "
            "ملف أوزان معطوب. فقُسِّم المشروع إلى خادم FastAPI وواجهة Next.js، واستُخرجت شيفرة "
            "النموذج إلى inference_core.py حتى لا تتباعد الواجهتان وخط التدريب أبدًا. وهذه هي النسخة "
            "المقدَّمة بوصفها المنتج.")},
        {"type": "h", "text": L("v4 — deployment: Docker + nginx",
                                "النسخة الرابعة — النشر: Docker و nginx")},
        {"type": "p", "text": L(
            "Three containers (backend, frontend, ollama) behind an nginx reverse proxy on a VPS, with "
            "pinned CPU PyTorch wheels, health checks, restart policies, and memory limits tuned for a "
            "shared machine.",
            "ثلاث حاويات (الخادم، الواجهة، Ollama) خلف وكيل nginx عكسي على خادم VPS، مع عجلات "
            "PyTorch للمعالج مثبّتة الإصدار، وفحوص صحة، وسياسات إعادة تشغيل، وضبطٍ للذاكرة يناسب "
            "جهازًا مشتركًا.")},
        {"type": "h", "text": L("What changed, version by version", "ما الذي تغيّر، نسخةً بنسخة")},
        {"type": "table",
         "head": [L("Version", "النسخة"), L("Weakness it fixed", "الضعف الذي عالجته"),
                  L("Artifact still in the repo", "الأثر الباقي في المستودع")],
         "rows": [
            [L("v0 Keras notebook", "النسخة صفر: دفتر Keras"),
             L("Nothing yet — proved the idea works.", "لا شيء بعد — أثبتت أن الفكرة تعمل."),
             L("brain-tumor.ipynb", "brain-tumor.ipynb")],
            [L("v1 PyTorch script", "النسخة الأولى: سكربت PyTorch"),
             L("RAM blow-up, no logging, no reproducible CLI.",
               "انفجار الذاكرة، وغياب التسجيل، وغياب سطر أوامر قابل للتكرار."),
             L("model_class.pth · model_log.csv", "model_class.pth · model_log.csv")],
            [L("v2 Gradio", "النسخة الثانية: Gradio"),
             L("No interface a non-programmer could use; no explanation of the prediction.",
               "لا واجهة يستخدمها غير المبرمج؛ ولا تفسير للتنبؤ."),
             L("app.py · gradcam_utils.py · llm_report.py", "app.py · gradcam_utils.py · llm_report.py")],
            [L("v3 FastAPI + Next.js", "النسخة الثالثة: FastAPI و Next.js"),
             L("No API, no design control, crash-on-bad-model, duplicated model code.",
               "لا واجهة برمجية، ولا تحكّم في التصميم، وانهيار عند خطأ النموذج، وتكرار شيفرة النموذج."),
             L("backend/ · frontend/ · inference_core.py", "backend/ · frontend/ · inference_core.py")],
            [L("v4 Docker", "النسخة الرابعة: Docker"),
             L("\"Works on my machine\"; unpinned dependencies; no restart on failure.",
               "«يعمل على جهازي»؛ واعتماديات غير مثبّتة؛ ولا إعادة تشغيل عند الفشل."),
             L("Dockerfile.backend · docker-compose.yml", "Dockerfile.backend · docker-compose.yml")],
            [L("v5 improved training", "النسخة الخامسة: تدريب محسَّن"),
             L("Overfitting risk: weak augmentation, no weight decay, no label smoothing, no LR schedule.",
               "خطر فرط التخصيص: زيادة بيانات ضعيفة، ولا اضمحلال وزن، ولا تنعيم تسميات، ولا جدولة "
               "لمعدّل التعلّم."),
             L("train.py (current script)", "train.py (السكربت الحالي)")],
        ]},
        {"type": "callout", "tone": "warn",
         "title": L("An honest note on the shipped weights", "ملاحظة صادقة عن الأوزان المُسلَّمة"),
         "text": L(
            "model_class.pth and model_log.csv come from the v1 training run. The train.py in the "
            "repository today is the improved v5 script — it adds BatchNorm1d(512) to the head, "
            "stronger augmentation, weight decay, label smoothing and a learning-rate column in the "
            "log. Because of the BatchNorm, re-running train.py produces a checkpoint that is "
            "deliberately not interchangeable with the shipped one; you can see the difference in the "
            "log itself, where the current script writes an 'lr' column the shipped CSV does not have. "
            "The project documents this in CLAUDE.md rather than hiding it.",
            "يأتي model_class.pth و model_log.csv من تشغيل التدريب في النسخة الأولى. أما train.py "
            "الموجود اليوم في المستودع فهو سكربت النسخة الخامسة المحسَّن — يضيف BatchNorm1d(512) إلى "
            "الرأس، وزيادة بيانات أقوى، واضمحلال وزن، وتنعيم تسميات، وعمودًا لمعدّل التعلّم في "
            "السجل. وبسبب BatchNorm فإن إعادة تشغيل train.py تُنتج ملف أوزان غير قابل للتبادل عمدًا "
            "مع المُسلَّم؛ ويظهر الفرق في السجل نفسه، إذ يكتب السكربت الحالي عمود lr الذي لا يوجد في "
            "ملف CSV المُسلَّم. ويوثّق المشروع ذلك في CLAUDE.md بدل إخفائه.")},
    ],
}

# ── C · WHAT A CNN ACTUALLY IS ───────────────────────────────────────────
CNN = {
    "id": "cnn",
    "title": L("What a Neural Network — and a CNN — Actually Is",
               "ما هي الشبكة العصبية — والشبكة الالتفافية — حقًّا"),
    "lead": L(
        "This section assumes zero background. It builds from a single artificial neuron up to the "
        "exact 50-layer network this project uses, and explains what each piece is for.",
        "لا يفترض هذا القسم أي خلفية سابقة. يبني من عصبون اصطناعي واحد وصولًا إلى الشبكة ذات الخمسين "
        "طبقة التي يستخدمها هذا المشروع بالضبط، ويشرح وظيفة كل جزء."),
    "blocks": [
        {"type": "h", "text": L("1 · The neuron", "1 · العصبون")},
        {"type": "p", "text": L(
            "An artificial neuron takes several numbers, multiplies each by a weight, adds them up, "
            "adds a bias, and passes the result through a simple non-linear function. That is all it "
            "is: y = f(w₁x₁ + w₂x₂ + … + b). Learning means finding the weights w and the bias b that "
            "make the output right. A network is thousands of such neurons in layers, where each "
            "layer's output is the next layer's input.",
            "يأخذ العصبون الاصطناعي عدّة أرقام، ويضرب كلًّا منها في وزن، ويجمعها، ويضيف انحيازًا، "
            "ويُمرِّر الناتج عبر دالة غير خطية بسيطة. هذا كل ما في الأمر: y = f(w₁x₁ + w₂x₂ + … + b). "
            "والتعلّم يعني إيجاد الأوزان w والانحياز b التي تجعل المخرج صحيحًا. والشبكة آلاف من هذه "
            "العصبونات في طبقات، مخرج كل طبقة هو مدخل التالية.")},
        {"type": "h", "text": L("2 · Why a plain network fails on images",
                                "2 · لماذا تفشل الشبكة العادية مع الصور")},
        {"type": "p", "text": L(
            "Our input is a 224 × 224 colour image — that is 224 × 224 × 3 = 150,528 numbers. If the "
            "first hidden layer were fully connected with 1,000 neurons, it alone would need "
            "150,528 × 1,000 ≈ 150 million weights. Three problems follow: (a) that many parameters "
            "would memorize 5,712 training images instead of learning from them; (b) the network has "
            "no idea that two neighbouring pixels are related, since every pixel is just an "
            "independent input; and (c) a tumor learned in the top-left corner would have to be "
            "re-learned from scratch for the bottom-right corner.",
            "مدخلنا صورة ملوّنة 224×224 — أي 224×224×3 = 150,528 رقمًا. ولو كانت الطبقة المخفية الأولى "
            "متّصلة اتصالًا كاملًا بألف عصبون لاحتاجت وحدها 150,528×1,000 ≈ 150 مليون وزن. وتتبع ذلك "
            "ثلاث مشكلات: (أ) هذا العدد من المعاملات سيحفظ صور التدريب الـ5712 عن ظهر قلب بدل أن "
            "يتعلّم منها؛ (ب) لا تعلم الشبكة أن بكسلين متجاورين مترابطان، لأن كل بكسل مجرّد مدخل "
            "مستقل؛ (ج) الورم الذي تعلّمته في الزاوية العليا اليسرى سيلزم تعلُّمه من جديد للزاوية "
            "السفلى اليمنى.")},
        {"type": "h", "text": L("3 · The convolution — the one idea that fixes all three",
                                "3 · الالتفاف — الفكرة الواحدة التي تحلّ الثلاث")},
        {"type": "p", "text": L(
            "Instead of connecting every pixel to every neuron, a convolutional layer uses a tiny "
            "window of weights called a kernel or filter — typically 3 × 3 — and slides it across the "
            "whole image. At each position it multiplies the nine weights by the nine pixels "
            "underneath and sums them into a single output number. The grid of all those output "
            "numbers is called a feature map.",
            "بدل ربط كل بكسل بكل عصبون، تستخدم الطبقة الالتفافية نافذة صغيرة من الأوزان تُسمّى نواة "
            "أو مرشّحًا — عادةً 3×3 — وتُمرِّرها على الصورة كلها. وفي كل موضع تضرب الأوزان التسعة في "
            "البكسلات التسعة تحتها وتجمعها في رقم مخرج واحد. وتُسمّى شبكة تلك الأرقام خريطة سمات.")},
        {"type": "code", "code":
            "Image patch          Kernel (vertical-edge detector)     Output\n"
            "                                                          \n"
            "  10  10  90           -1   0  +1                          \n"
            "  10  10  90     *     -1   0  +1        =    (-30) + (270) = +240\n"
            "  10  10  90           -1   0  +1                          \n"
            "\n"
            "(-1*10 -1*10 -1*10) + (0*10 0*10 0*10) + (+1*90 +1*90 +1*90) = 240\n"
            "A large positive number => \"there is a bright-on-the-right edge here\"."},
        {"type": "bullets", "items": [
            L("Parameter sharing — the same 3 × 3 × 3 kernel (28 weights including the bias) is used "
              "at every position, instead of 150 million separate weights. A pattern learned once is "
              "recognized everywhere in the image.",
              "مشاركة المعاملات — تُستخدم النواة 3×3×3 نفسها (28 وزنًا مع الانحياز) في كل موضع، بدل "
              "150 مليون وزن منفصل. والنمط الذي يُتعلَّم مرة يُتعرَّف عليه في كل مكان من الصورة."),
            L("Locality — a kernel only ever looks at neighbouring pixels, which is exactly how "
              "visual structure works: edges, textures and lesions are local.",
              "المحلّية — لا تنظر النواة إلا إلى بكسلات متجاورة، وهذا بالضبط كيف تعمل البنية "
              "البصرية: الحواف والقوام والآفات كلها محلّية."),
            L("Translation tolerance — because the same kernel sweeps the whole image, a tumor is "
              "detected wherever it sits.",
              "تحمُّل الإزاحة — لأن النواة نفسها تمسح الصورة كلها، يُكتشف الورم أينما وقع."),
        ]},
        {"type": "h", "text": L("4 · Stride, padding and output size",
                                "4 · الخطوة والحشو وحجم المخرج")},
        {"type": "p", "text": L(
            "Stride is how far the kernel jumps between positions; stride 2 halves the width and "
            "height. Padding adds a border of zeros so the kernel can also sit on the edges. Together "
            "they determine the size of the output:",
            "الخطوة هي مقدار قفز النواة بين المواضع؛ فالخطوة 2 تُنصِّف العرض والارتفاع. والحشو يضيف "
            "إطارًا من الأصفار لتستطيع النواة الجلوس على الحواف أيضًا. وهما معًا يحدّدان حجم "
            "المخرج:")},
        {"type": "code", "code":
            "  out = floor( (in + 2*padding - kernel) / stride ) + 1\n"
            "\n"
            "  ResNet50's first layer: kernel 7, stride 2, padding 3, input 224\n"
            "      out = floor( (224 + 6 - 7) / 2 ) + 1 = 112"},
        {"type": "h", "text": L("5 · Channels: many kernels, many feature maps",
                                "5 · القنوات: نوى كثيرة وخرائط سمات كثيرة")},
        {"type": "p", "text": L(
            "One kernel detects one kind of pattern. A convolutional layer therefore holds many "
            "kernels — ResNet50's first layer has 64 — and produces one feature map per kernel. So a "
            "224 × 224 × 3 image becomes a 112 × 112 × 64 stack: 64 different \"views\" of the same "
            "scan, one per learned pattern. The next layer's kernels then look at all 64 maps at once.",
            "تكشف النواة الواحدة نمطًا واحدًا. لذا تحوي الطبقة الالتفافية نوى كثيرة — الطبقة الأولى في "
            "ResNet50 فيها 64 — وتُنتج خريطة سمات لكل نواة. فتصير الصورة 224×224×3 كومةً بحجم "
            "112×112×64: أربعًا وستين «رؤية» مختلفة للصورة نفسها، واحدة لكل نمط مُتعلَّم. ثم تنظر نوى "
            "الطبقة التالية إلى الخرائط الـ64 كلها دفعةً واحدة.")},
        {"type": "h", "text": L("6 · ReLU — the non-linearity", "6 · ReLU — اللاخطّية")},
        {"type": "p", "text": L(
            "After every convolution the network applies ReLU: f(x) = max(0, x) — keep positive "
            "values, zero out negative ones. Without a non-linear function, stacking fifty linear "
            "layers would be mathematically identical to one linear layer, and the network could never "
            "learn anything but straight-line relationships. ReLU is chosen over older functions "
            "(sigmoid, tanh) because it is extremely cheap to compute and its gradient is exactly 1 "
            "for positive inputs, which keeps gradients from shrinking to nothing across deep stacks.",
            "بعد كل التفاف تُطبِّق الشبكة ReLU: ‏f(x) = max(0, x) — تُبقي القيم الموجبة وتُصفِّر "
            "السالبة. ولولا دالة غير خطية لكان تكديس خمسين طبقة خطية مكافئًا رياضيًا لطبقة خطية "
            "واحدة، ولما استطاعت الشبكة تعلُّم شيء سوى العلاقات المستقيمة. واختيرت ReLU على الدوال "
            "الأقدم (sigmoid و tanh) لأن حسابها بالغ الرخص، ولأن تدرّجها يساوي 1 تمامًا للمدخلات "
            "الموجبة، مما يمنع تلاشي التدرّجات عبر الأكوام العميقة.")},
        {"type": "h", "text": L("7 · Pooling and downsampling", "7 · التجميع وتقليل الأبعاد")},
        {"type": "p", "text": L(
            "Pooling shrinks a feature map by summarizing each small region with one number — max "
            "pooling keeps the strongest response in each 2 × 2 or 3 × 3 window. This reduces "
            "computation, widens what each later neuron effectively \"sees\", and makes the network "
            "tolerant to a pattern shifting by a pixel or two. ResNet50 uses one 3 × 3 max-pool right "
            "after the first convolution and then relies mostly on stride-2 convolutions to "
            "downsample, finishing with a global average pool that collapses each of the final 2048 "
            "feature maps to a single number.",
            "يُقلِّص التجميع خريطة السمات بتلخيص كل منطقة صغيرة برقم واحد — فالتجميع الأقصى يُبقي "
            "أقوى استجابة في كل نافذة 2×2 أو 3×3. وهذا يقلّل الحساب، ويوسّع ما «يراه» كل عصبون لاحق "
            "فعليًا، ويجعل الشبكة متسامحة مع إزاحة النمط بكسلًا أو اثنين. وتستخدم ResNet50 تجميعًا "
            "أقصى 3×3 مباشرةً بعد الالتفاف الأول، ثم تعتمد أساسًا على التفافات بخطوة 2 لتقليل "
            "الأبعاد، وتنتهي بتجميع متوسط شامل يطوي كلًّا من خرائط السمات الـ2048 النهائية إلى رقم "
            "واحد.")},
        {"type": "h", "text": L("8 · Batch normalization", "8 · التطبيع الدُّفعي")},
        {"type": "p", "text": L(
            "After a convolution, the numbers flowing through the network can drift to very large or "
            "very small scales, which makes training unstable. Batch normalization re-centres and "
            "re-scales each channel using the statistics of the current batch, then lets the network "
            "learn its own scale and shift. ResNet50 has a BatchNorm after essentially every "
            "convolution — 53 of them — which is why it trains reliably at 50 layers.",
            "بعد الالتفاف قد تنجرف الأرقام السارية في الشبكة إلى مقاييس كبيرة جدًا أو صغيرة جدًا، مما "
            "يزعزع استقرار التدريب. ويعيد التطبيع الدُّفعي توسيط كل قناة وتحجيمها بإحصاءات الدفعة "
            "الحالية، ثم يترك للشبكة تعلُّم مقياسها وإزاحتها. وفي ResNet50 طبقة تطبيع دُفعي بعد كل "
            "التفاف تقريبًا — 53 طبقة — ولهذا تتدرّب بموثوقية عند خمسين طبقة.")},
        {"type": "h", "text": L("9 · The hierarchy of features — why depth matters",
                                "9 · تسلسل السمات — لماذا يهمّ العمق")},
        {"type": "p", "text": L(
            "Each successive block sees a wider area of the original image (its receptive field grows) "
            "and therefore learns more abstract things. This hierarchy is what the whole method rests "
            "on, and it maps directly onto the layers this project freezes and unfreezes:",
            "ترى كل كتلة تالية مساحة أوسع من الصورة الأصلية (يتّسع مجالها الاستقبالي) فتتعلّم أشياء "
            "أكثر تجريدًا. وهذا التسلسل هو ما يقوم عليه المنهج كله، وينطبق مباشرةً على الطبقات التي "
            "يجمّدها هذا المشروع ويفكّها:")},
        {"type": "table",
         "head": [L("Stage", "المرحلة"), L("Output shape", "شكل المخرج"),
                  L("What it learns", "ما تتعلّمه"), L("In this project", "في هذا المشروع")],
         "rows": [
            [L("conv1 (7×7, stride 2)", "conv1 ‏(7×7، خطوة 2)"), L("112 × 112 × 64", "112 × 112 × 64"),
             L("Edges, blobs, light/dark transitions.", "الحواف والبقع وانتقالات الإضاءة."),
             L("Frozen", "مجمَّدة")],
            [L("maxpool (3×3, stride 2)", "maxpool ‏(3×3، خطوة 2)"), L("56 × 56 × 64", "56 × 56 × 64"),
             L("Downsamples; adds shift tolerance.", "يقلّل الأبعاد ويضيف تحمُّل الإزاحة."),
             L("Frozen", "مجمَّدة")],
            [L("layer1 (3 blocks)", "layer1 ‏(3 كتل)"), L("56 × 56 × 256", "56 × 56 × 256"),
             L("Corners, simple textures.", "الزوايا والقوام البسيط."), L("Frozen", "مجمَّدة")],
            [L("layer2 (4 blocks)", "layer2 ‏(4 كتل)"), L("28 × 28 × 512", "28 × 28 × 512"),
             L("Texture patterns, contours.", "أنماط القوام والمحيطات."), L("Frozen", "مجمَّدة")],
            [L("layer3 (6 blocks)", "layer3 ‏(6 كتل)"), L("14 × 14 × 1024", "14 × 14 × 1024"),
             L("Object parts, tissue structures.", "أجزاء الأجسام وبِنى الأنسجة."),
             L("Unfrozen — trained", "مفكوكة — تُدرَّب")],
            [L("layer4 (3 blocks)", "layer4 ‏(3 كتل)"), L("7 × 7 × 2048", "7 × 7 × 2048"),
             L("Whole structures — the lesion itself.", "بِنى كاملة — الآفة نفسها."),
             L("Unfrozen — trained · GradCAM taps here", "مفكوكة — تُدرَّب · ومنها يأخذ GradCAM")],
            [L("global average pool", "التجميع المتوسط الشامل"), L("1 × 1 × 2048", "1 × 1 × 2048"),
             L("Collapses each map to its average activation.", "يطوي كل خريطة إلى متوسط تنشيطها."),
             L("Fixed operation (no weights)", "عملية ثابتة (بلا أوزان)")],
            [L("classifier head", "رأس المُصنِّف"), L("4", "4"),
             L("Maps the 2048-number fingerprint to 4 class scores.",
               "يحوّل بصمة الـ2048 رقمًا إلى 4 درجات فئوية."),
             L("New — trained from scratch", "جديد — يُدرَّب من الصفر")],
        ]},
        {"type": "h", "text": L("10 · The residual connection — what makes it a ResNet",
                                "10 · الوصلة المتبقّية — ما يجعلها ResNet")},
        {"type": "p", "text": L(
            "Before 2015, making networks deeper eventually made them worse, not better: gradients "
            "shrank as they were multiplied backwards through many layers, and deep networks became "
            "untrainable. ResNet's answer is a shortcut: each block computes y = F(x) + x, adding its "
            "input back onto its output. If a block has nothing useful to add, it can learn F(x) ≈ 0 "
            "and simply pass the input through unchanged. The addition also gives the gradient a "
            "direct path backwards, so it never vanishes. This single trick is what makes 50 — or "
            "even 152 — layers practical.",
            "قبل 2015 كان تعميق الشبكات يزيدها سوءًا لا تحسّنًا: إذ تتقلّص التدرّجات وهي تُضرب رجوعًا "
            "عبر طبقات كثيرة، فتصير الشبكات العميقة غير قابلة للتدريب. وجواب ResNet اختصار: تحسب كل "
            "كتلة y = F(x) + x، فتضيف مدخلها إلى مخرجها. فإن لم يكن لدى الكتلة ما تضيفه، أمكنها تعلُّم "
            "F(x) ≈ 0 وتمرير المدخل كما هو. كما تمنح الإضافةُ التدرّجَ مسارًا مباشرًا للرجوع فلا "
            "يتلاشى أبدًا. هذه الحيلة وحدها هي ما يجعل خمسين — بل مئةً واثنتين وخمسين — طبقة أمرًا "
            "عمليًا.")},
        {"type": "h", "text": L("11 · The bottleneck block", "11 · كتلة عنق الزجاجة")},
        {"type": "p", "text": L(
            "ResNet50 does not use plain 3 × 3 blocks; it uses a three-convolution \"bottleneck\": a "
            "1 × 1 convolution that squeezes the channel count down, a 3 × 3 convolution that does the "
            "spatial work cheaply on the squeezed tensor, and a 1 × 1 convolution that expands back "
            "up. This gets the accuracy of a deep network at roughly a third of the computation. The "
            "16 bottleneck blocks are arranged 3-4-6-3 across the four stages, which — with the first "
            "convolution and the final fully-connected layer — is where the number 50 comes from.",
            "لا تستخدم ResNet50 كتلًا بسيطة 3×3، بل تستخدم «عنق زجاجة» من ثلاثة التفافات: التفاف 1×1 "
            "يضغط عدد القنوات، والتفاف 3×3 ينجز العمل المكاني بثمن رخيص على المُوتِّر المضغوط، والتفاف "
            "1×1 يعيد التوسيع. وهذا يمنح دقة شبكة عميقة بنحو ثلث الحساب. وتُرتَّب كتل عنق الزجاجة "
            "الستّ عشرة بنسق 3-4-6-3 عبر المراحل الأربع، ومن ذلك — مع الالتفاف الأول والطبقة "
            "المتّصلة النهائية — يأتي الرقم 50.")},
        {"type": "h", "text": L("12 · How the network learns", "12 · كيف تتعلّم الشبكة")},
        {"type": "num", "items": [
            L("Forward pass — a batch of 32 images flows through the network and produces 32 sets of "
              "4 scores.",
              "التمريرة الأمامية — تسري دفعة من 32 صورة عبر الشبكة فتُنتج 32 مجموعة من 4 درجات."),
            L("Loss — a formula compares those scores to the true labels and produces a single number "
              "measuring how wrong the network was.",
              "الخسارة — تقارن صيغةٌ تلك الدرجات بالتسميات الحقيقية وتُنتج رقمًا واحدًا يقيس مقدار خطأ "
              "الشبكة."),
            L("Backward pass — the chain rule computes, for every single weight, how much that weight "
              "contributed to the error (its gradient).",
              "التمريرة الخلفية — تحسب قاعدة السلسلة، لكل وزن على حدة، مقدار إسهامه في الخطأ (تدرّجه)."),
            L("Update — the optimizer nudges each weight a small step in the direction that reduces "
              "the error.",
              "التحديث — يزيح المُحسِّن كل وزن خطوةً صغيرة في الاتجاه الذي يقلّل الخطأ."),
            L("Repeat — 179 batches make one epoch over the 5,712 training images; this project ran 7 "
              "epochs.",
              "التكرار — 179 دفعة تُكوّن حقبة واحدة على صور التدريب الـ5712؛ وقد نفّذ هذا المشروع سبع "
              "حقب."),
        ]},
        {"type": "callout", "tone": "info",
         "title": L("Why we do not train it from scratch",
                    "لماذا لا ندرّبها من الصفر"),
         "text": L(
            "The first layers of any vision network learn edges and textures — knowledge that is "
            "identical whether the image is a cat or a brain slice. ImageNet gave ResNet50 that "
            "knowledge for free from 1.2 million photographs. We keep it (frozen) and only retrain "
            "the last two stages, where the features become task-specific. With only 5,712 MRI "
            "images, training all 24.6 million parameters from random initialization would overfit "
            "badly and would take far longer.",
            "تتعلّم الطبقات الأولى في أي شبكة رؤية الحواف والقوام — وهي معرفة واحدة سواء كانت الصورة "
            "قطة أم شريحة دماغ. وقد منحت ImageNet شبكة ResNet50 تلك المعرفة مجانًا من 1.2 مليون "
            "صورة. فنُبقيها (مجمَّدة) ولا نعيد تدريب سوى المرحلتين الأخيرتين حيث تصير السمات خاصة "
            "بالمهمّة. وبـ5712 صورة رنين فقط، فإن تدريب المعاملات الـ24.6 مليون كلها من تهيئة عشوائية "
            "سيؤدي إلى فرط تخصيص شديد وسيستغرق وقتًا أطول بكثير.")},
    ],
}

# ── D · WHY A CNN AND NOT SOMETHING ELSE ─────────────────────────────────
WHY_CNN = {
    "id": "whycnn",
    "title": L("Why a CNN — and Not Any Other Algorithm",
               "لماذا شبكة التفافية — لا خوارزمية أخرى"),
    "lead": L(
        "Every alternative below is a real, reasonable option that was considered and rejected for a "
        "specific reason. Knowing why each one is wrong for this task is the difference between "
        "\"we used a CNN\" and \"we chose a CNN\".",
        "كل بديل أدناه خيار حقيقي ومعقول جرى النظر فيه ورفضه لسبب محدَّد. ومعرفة سبب عدم مناسبة كلٍّ "
        "منه لهذه المهمة هي الفرق بين «استخدمنا شبكة التفافية» و«اخترنا شبكة التفافية»."),
    "blocks": [
        {"type": "table",
         "head": [L("Alternative", "البديل"), L("What it is", "ما هو"),
                  L("Why not here", "لماذا لا يصلح هنا"), L("When it would be right", "متى يكون صحيحًا")],
         "rows": [
            [L("Fully-connected network (MLP)", "شبكة متّصلة اتصالًا كاملًا (MLP)"),
             L("Every pixel wired to every neuron.", "كل بكسل موصول بكل عصبون."),
             L("~150 million weights in the first layer alone, no notion of locality, no translation "
               "tolerance — it would memorize 5,712 images rather than learn.",
               "نحو 150 مليون وزن في الطبقة الأولى وحدها، ولا مفهوم للمحلّية، ولا تحمُّل للإزاحة — "
               "سيحفظ 5712 صورة بدل أن يتعلّم."),
             L("Tabular data — patient age, lab values, blood counts.",
               "البيانات الجدولية — عمر المريض والقيم المخبرية وتعداد الدم.")],
            [L("SVM / Random Forest / k-NN on raw pixels",
               "آلة المتجهات الداعمة / الغابة العشوائية / أقرب الجيران على البكسلات الخام"),
             L("Classical machine learning fed the flattened image.",
               "تعلّم آلي كلاسيكي يُغذَّى بالصورة المسطَّحة."),
             L("150,528 features with no spatial structure; a one-pixel shift changes every feature. "
               "Accuracy on this kind of task typically lands 15–30 points below a fine-tuned CNN.",
               "‏150,528 سمة بلا بنية مكانية؛ وإزاحة بكسل واحد تغيّر كل سمة. وتقلّ الدقة في هذا النوع "
               "من المهام عادةً بمقدار 15 إلى 30 نقطة عن شبكة التفافية مضبوطة."),
             L("Small, low-dimensional, already-structured data.",
               "بيانات صغيرة قليلة الأبعاد ومهيكلة أصلًا.")],
            [L("Hand-crafted features + SVM (radiomics, HOG, GLCM)",
               "سمات مصمَّمة يدويًا مع SVM ‏(radiomics و HOG و GLCM)"),
             L("A human designs texture/shape descriptors; a classical model classifies them.",
               "يصمّم إنسانٌ واصفاتٍ للقوام والشكل، ويصنّفها نموذج كلاسيكي."),
             L("Requires expert feature engineering per tumor type, is brittle across scanners, and "
               "is capped by whatever the designer thought to measure. A CNN learns the features "
               "instead of being told them.",
               "يتطلّب هندسة سمات خبيرة لكل نوع ورم، وهو هشّ عبر الأجهزة، ومحدود بما فكّر المصمّم في "
               "قياسه. أما الشبكة الالتفافية فتتعلّم السمات بدل أن تُملى عليها."),
             L("Datasets of a few hundred images, or where regulators demand fully interpretable "
               "features.",
               "مجموعات من بضع مئات من الصور، أو حين يطلب المنظّمون سمات قابلة للتفسير بالكامل.")],
            [L("Vision Transformer (ViT)", "محوّل الرؤية (ViT)"),
             L("Splits the image into patches and uses self-attention instead of convolution.",
               "يقسّم الصورة إلى رقع ويستخدم الانتباه الذاتي بدل الالتفاف."),
             L("ViTs have no built-in assumption of locality, so they must learn it from data — they "
               "typically need an order of magnitude more images than our 5,712 to beat a CNN, and "
               "they are heavier to run on CPU.",
               "لا تفترض محوّلات الرؤية المحلّية ضمنيًا، فعليها تعلُّمها من البيانات — وهي تحتاج عادةً "
               "صورًا أكثر بمقدار رتبة عشرية من صورنا الـ5712 لتتفوّق على شبكة التفافية، كما أنها "
               "أثقل تشغيلًا على المعالج."),
             L("With 100k+ images, or starting from a large medical-imaging foundation model.",
               "مع أكثر من مئة ألف صورة، أو انطلاقًا من نموذج أساس كبير للتصوير الطبي.")],
            [L("YOLO / Faster R-CNN (object detection)", "‏YOLO أو Faster R-CNN (كشف الأجسام)"),
             L("Predicts bounding boxes around objects.", "يتنبّأ بمربّعات إحاطة حول الأجسام."),
             L("Needs box annotations on every training image. Our dataset has one class label per "
               "image and no boxes at all — the labels required simply do not exist.",
               "يحتاج تعليمات مربّعات على كل صورة تدريب. ومجموعتنا فيها تسمية فئة واحدة لكل صورة "
               "ولا مربّعات إطلاقًا — فالتعليمات المطلوبة غير موجودة أصلًا."),
             L("When you have box-annotated data and need explicit tumor localization.",
               "حين تتوافر بيانات معلَّمة بالمربّعات وتحتاج تحديدًا صريحًا لموقع الورم.")],
            [L("U-Net (segmentation)", "‏U-Net (التجزئة)"),
             L("Labels every pixel as tumor or not.", "يُسمّي كل بكسل بأنه ورم أو لا."),
             L("Requires a pixel-perfect mask drawn by a radiologist for every training image — "
               "expensive expert work our dataset does not include.",
               "يتطلّب قناعًا دقيقًا بكسلًا بكسل يرسمه أخصائي أشعة لكل صورة تدريب — وهو عمل خبير مكلف "
               "لا تتضمّنه مجموعتنا."),
             L("The natural next version, if a segmented dataset (e.g. BraTS) is added.",
               "النسخة التالية الطبيعية إن أُضيفت مجموعة مجزَّأة مثل BraTS.")],
            [L("A CNN trained from scratch", "شبكة التفافية مُدرَّبة من الصفر"),
             L("Same architecture, random initial weights.", "المعمارية نفسها بأوزان ابتدائية عشوائية."),
             L("5,712 images is far too few to learn generic edge and texture detectors from nothing; "
               "it would overfit and train much more slowly.",
               "‏5712 صورة أقلّ بكثير من أن تُتعلَّم منها كواشف الحواف والقوام العامة من العدم؛ سيقع "
               "فرط تخصيص وسيبطؤ التدريب كثيرًا."),
             L("Millions of images, or a domain visually unlike anything in ImageNet.",
               "ملايين الصور، أو مجال يختلف بصريًا عن كل ما في ImageNet.")],
        ]},
        {"type": "h", "text": L("And why ResNet50 among CNNs?", "ولماذا ResNet50 بين الشبكات الالتفافية؟")},
        {"type": "table",
         "head": [L("Backbone", "الشبكة الأساس"), L("Parameters", "المعاملات"),
                  L("Trade-off", "المقايضة")],
         "rows": [
            [L("VGG16", "VGG16"), L("~138M", "نحو 138 مليون"),
             L("Older, far heavier, no residual connections, weaker accuracy per parameter.",
               "أقدم وأثقل بكثير، وبلا وصلات متبقّية، ودقّتها لكل معامل أضعف.")],
            [L("ResNet18 / ResNet34", "ResNet18 / ResNet34"), L("~11M / ~21M", "نحو 11 / 21 مليون"),
             L("Faster, but shallower features; measurably weaker on fine-grained medical texture.",
               "أسرع لكن سماتها أقل عمقًا؛ وأضعف بوضوح في القوام الطبي الدقيق.")],
            [L("ResNet50 ✓", "ResNet50 ✓"), L("~24.6M (this project)", "نحو 24.6 مليون (هذا المشروع)"),
             L("The standard, best-understood medical-imaging baseline: deep enough for rich "
               "features, light enough for CPU inference, and its layer4 is the canonical GradCAM tap "
               "point with published, reproducible behaviour.",
               "خط الأساس القياسي والأكثر فهمًا في التصوير الطبي: عميق بما يكفي لسمات غنية، وخفيف بما "
               "يكفي للاستدلال على المعالج، وطبقته layer4 هي نقطة أخذ GradCAM القياسية بسلوك منشور "
               "وقابل للتكرار.")],
            [L("DenseNet121", "DenseNet121"), L("~8M", "نحو 8 ملايين"),
             L("Excellent accuracy per parameter but heavier memory traffic and slower on CPU.",
               "دقة ممتازة لكل معامل لكن حركة ذاكرة أثقل وبطء على المعالج.")],
            [L("EfficientNet-B0 / MobileNetV3", "EfficientNet-B0 / MobileNetV3"),
             L("~5M / ~5M", "نحو 5 / 5 ملايين"),
             L("Best choice for a phone or an edge device; more sensitive to fine-tuning settings and "
               "less standard as a research baseline.",
               "الخيار الأفضل لهاتف أو جهاز طرفي؛ لكنه أكثر حساسية لإعدادات الضبط وأقل قياسيةً كخط "
               "أساس بحثي.")],
        ]},
        {"type": "callout", "tone": "good",
         "title": L("The defensible answer", "الجواب القابل للدفاع"),
         "text": L(
            "\"We chose a CNN because the input is an image, where meaning is local and position-"
            "independent — exactly the two assumptions a convolution builds in. We chose ResNet50 "
            "specifically because it is deep enough to learn tissue-level features, light enough to "
            "run on a CPU in a fraction of a second, pretrained weights are freely available, and its "
            "final convolutional stage is the standard, well-validated layer for GradCAM — which our "
            "whole explainability story depends on.\"",
            "«اخترنا شبكة التفافية لأن المدخل صورة، والمعنى فيها محلّي ومستقل عن الموضع — وهما "
            "بالضبط الافتراضان اللذان يبنيهما الالتفاف. واخترنا ResNet50 تحديدًا لأنها عميقة بما يكفي "
            "لتعلُّم سمات على مستوى النسيج، وخفيفة بما يكفي للعمل على معالج في جزء من الثانية، "
            "وأوزانها المُدرَّبة مسبقًا متاحة مجانًا، ومرحلتها الالتفافية الأخيرة هي الطبقة القياسية "
            "المُتحقَّق منها لـGradCAM — الذي تقوم عليه حكاية التفسير كلها عندنا.»")},
    ],
}

# ── E · THE MATHEMATICS ──────────────────────────────────────────────────
MATH = {
    "id": "math",
    "title": L("The Mathematics, Step by Step", "الرياضيات خطوةً بخطوة"),
    "lead": L(
        "Every formula the system actually uses, written out and explained. A judge who asks \"what "
        "is the loss function?\" should get this answer.",
        "كل صيغة يستخدمها النظام فعليًا، مكتوبةً ومشروحة. والمُحكِّم الذي يسأل «ما دالة الخسارة؟» "
        "ينبغي أن يحصل على هذه الإجابة."),
    "blocks": [
        {"type": "h", "text": L("1 · The convolution", "1 · الالتفاف")},
        {"type": "code", "code":
            "                K-1  K-1  C-1\n"
            "  Out[i,j,f]  =  ΣΣΣ  W[u,v,c,f] · In[i·s+u, j·s+v, c]  +  b[f]\n"
            "                u=0  v=0  c=0\n"
            "\n"
            "  K = kernel size (3)      C = input channels\n"
            "  s = stride               f = filter index"},
        {"type": "h", "text": L("2 · ReLU and BatchNorm", "2 · ReLU والتطبيع الدُّفعي")},
        {"type": "code", "code":
            "  ReLU(x) = max(0, x)\n"
            "\n"
            "  BN(x) = γ · (x − μ_batch) / sqrt(σ²_batch + ε)  +  β\n"
            "\n"
            "  γ and β are learned;  μ and σ² come from the batch during\n"
            "  training, and from stored running averages at inference time."},
        {"type": "h", "text": L("3 · Softmax — turning scores into probabilities",
                                "3 · Softmax — تحويل الدرجات إلى احتمالات")},
        {"type": "p", "text": L(
            "The network's last layer outputs 4 raw numbers called logits. They can be any size, "
            "positive or negative. Softmax exponentiates each and divides by the total, producing four "
            "positive numbers that sum to exactly 1:",
            "تُخرج الطبقة الأخيرة في الشبكة أربعة أرقام خام تُسمّى لوغيتات، وقد تكون بأي مقدار موجب "
            "أو سالب. ويُطبِّق softmax الأُسّ على كلٍّ منها ويقسم على المجموع، فيُنتج أربعة أرقام موجبة "
            "مجموعها واحد بالضبط:")},
        {"type": "code", "code":
            "  p_i = exp(z_i) / Σ_j exp(z_j)\n"
            "\n"
            "  Worked example (illustrative logits), in class-index order\n"
            "  Pituitary, No Tumor, Meningioma, Glioma:\n"
            "\n"
            "    z      = [ 1.2 ,  0.4 ,  2.9 ,   6.1  ]\n"
            "    exp(z) = [ 3.32 , 1.49 , 18.17 , 445.86 ]   sum = 468.84\n"
            "    p      = [ 0.007, 0.003, 0.039 , 0.951 ]\n"
            "\n"
            "  => \"Glioma, 95.1% confidence\". The four bars shown in the UI\n"
            "     are exactly these numbers."},
        {"type": "callout", "tone": "warn",
         "title": L("Confidence is not probability of correctness",
                    "الثقة ليست احتمال الصواب"),
         "text": L(
            "Softmax always produces a confident-looking distribution, even for an input the model has "
            "never seen anything like — feed it a photograph of a car and it will still report ~90% "
            "for some tumor class. The number is a relative ranking of four options, not a calibrated "
            "probability that the answer is correct. This is a known limitation and a planned fix "
            "(temperature scaling + an out-of-distribution check).",
            "يُنتج softmax دائمًا توزيعًا يبدو واثقًا، حتى لمدخل لم يرَ النموذج مثله قط — أعطِه صورة "
            "سيارة وسيُبلِغ مع ذلك بنحو 90% لإحدى فئات الأورام. فالرقم ترتيب نسبي بين أربعة خيارات، "
            "لا احتمالًا معايَرًا بأن الجواب صحيح. وهذا حدٌّ معروف وإصلاحٌ مخطَّط له (قياس الحرارة مع "
            "فحص الخروج عن التوزيع).")},
        {"type": "h", "text": L("4 · Cross-entropy loss with label smoothing",
                                "4 · خسارة الإنتروبيا المتقاطعة مع تنعيم التسميات")},
        {"type": "code", "code":
            "  Plain cross-entropy:   L = − log( p_correct )\n"
            "\n"
            "  With label smoothing ε = 0.1 and C = 4 classes, the hard target\n"
            "  [0, 0, 0, 1] becomes  [0.025, 0.025, 0.025, 0.925]:\n"
            "\n"
            "    target_i = ε/C            wrong classes  (0.1/4 = 0.025)\n"
            "    target_i = 1 − ε + ε/C    correct class  (0.925)\n"
            "\n"
            "    L = − Σ_i  target_i · log(p_i)"},
        {"type": "p", "text": L(
            "Why smooth the labels? Plain cross-entropy is only satisfied when the correct probability "
            "reaches 1.0, which pushes the network to become absurdly over-confident and to overfit. "
            "Smoothing tells it \"be about 92.5% sure, not 100% sure\", which improves calibration and "
            "generalization at essentially no cost.",
            "لماذا نُنعِّم التسميات؟ لا تُرضى الإنتروبيا المتقاطعة البسيطة إلا ببلوغ احتمال الصواب 1.0، "
            "مما يدفع الشبكة إلى ثقة مفرطة سخيفة وإلى فرط التخصيص. ويقول لها التنعيم «كُن واثقًا بنحو "
            "92.5% لا 100%»، فيحسّن المعايرة والتعميم بلا تكلفة تُذكر.")},
        {"type": "h", "text": L("5 · Gradient descent and the Adam optimizer",
                                "5 · النزول التدرّجي ومُحسِّن Adam")},
        {"type": "code", "code":
            "  Plain SGD:      w  ←  w − lr · ∂L/∂w\n"
            "\n"
            "  Adam keeps two running averages per weight:\n"
            "      m ← β1·m + (1−β1)·g      (momentum: average direction)\n"
            "      v ← β2·v + (1−β2)·g²     (average squared magnitude)\n"
            "      w ← w − lr · m̂ / (sqrt(v̂) + ε)\n"
            "\n"
            "  Used here: lr = 1e-4, β1 = 0.9, β2 = 0.999,\n"
            "             weight_decay = 1e-4"},
        {"type": "p", "text": L(
            "Adam gives every weight its own effective step size: weights whose gradients are "
            "consistently large take smaller steps, and rarely-updated weights take larger ones. For "
            "fine-tuning — where a pretrained backbone needs tiny adjustments while a brand-new head "
            "needs large ones — that property is exactly what is wanted, which is why Adam is chosen "
            "over plain SGD here. The learning rate 1e-4 is deliberately ten times smaller than the "
            "usual 1e-3: large steps would destroy the ImageNet features we are trying to preserve.",
            "يمنح Adam كل وزن حجم خطوة فعّالًا خاصًا به: فالأوزان ذات التدرّجات الكبيرة باستمرار تأخذ "
            "خطوات أصغر، والأوزان نادرة التحديث تأخذ خطوات أكبر. وفي الضبط الدقيق — حيث تحتاج الشبكة "
            "المُدرَّبة مسبقًا تعديلات ضئيلة بينما يحتاج الرأس الجديد تعديلات كبيرة — فإن هذه الخاصية "
            "هي المطلوبة تمامًا، ولهذا اختير Adam على SGD البسيط هنا. ومعدّل التعلّم 1e-4 أصغر عمدًا "
            "بعشر مرات من المعتاد 1e-3: فالخطوات الكبيرة ستُتلف سمات ImageNet التي نحاول الحفاظ "
            "عليها.")},
        {"type": "h", "text": L("6 · Weight decay (L2 regularization)", "6 · اضمحلال الوزن (تنظيم L2)")},
        {"type": "code", "code":
            "  L_total = L_data  +  λ · Σ w²        with λ = 1e-4\n"
            "\n"
            "  Effect: every step also pulls each weight slightly toward zero,\n"
            "  so the model prefers many small weights over a few huge ones —\n"
            "  a simpler, smoother function that generalizes better."},
        {"type": "h", "text": L("7 · GradCAM", "7 · GradCAM")},
        {"type": "code", "code":
            "  1) A^k = the k-th feature map of layer4's output\n"
            "           (7 × 7 pixels, k = 1…2048)\n"
            "\n"
            "  2) α_k^c = (1 / 49) · Σ_i Σ_j  ∂y^c / ∂A^k_ij\n"
            "           = average the gradient of the class score over the map\n"
            "\n"
            "  3) L^c_GradCAM = ReLU( Σ_k  α_k^c · A^k )\n"
            "\n"
            "  4) upsample the 7 × 7 map to 224 × 224, colorize,\n"
            "     and blend it over the MRI"},
        {"type": "p", "text": L(
            "In words: how much would the Glioma score rise if this feature map got stronger? That "
            "sensitivity becomes the map's weight. Summing all 2048 weighted maps gives a coarse "
            "importance image; ReLU discards the regions that argue *against* the class, keeping only "
            "the positive evidence. The result is 7 × 7 — genuinely coarse — which is why the heatmap "
            "shows a region of interest and never a precise tumor boundary.",
            "بالكلمات: كم سترتفع درجة «دبقي» لو صارت خريطة السمات هذه أقوى؟ تصبح تلك الحساسية وزن "
            "الخريطة. وجمع الخرائط الموزونة الـ2048 يعطي صورة أهمية خشنة؛ ثم تُسقط ReLU المناطق التي "
            "تُحاجّ ضد الفئة مُبقيةً الأدلة الإيجابية فقط. والنتيجة 7×7 — خشنة فعلًا — ولهذا تُظهر "
            "الخريطة الحرارية منطقة اهتمام لا حدودًا دقيقة للورم.")},
        {"type": "h", "text": L("8 · The evaluation metrics", "8 · مقاييس التقييم")},
        {"type": "code", "code":
            "  Accuracy    = (TP + TN) / total\n"
            "                the headline number\n"
            "\n"
            "  Precision   = TP / (TP + FP)\n"
            "                of the ones we flagged, how many were real\n"
            "\n"
            "  Recall      = TP / (TP + FN)          (= sensitivity)\n"
            "                of the real ones, how many we caught\n"
            "\n"
            "  Specificity = TN / (TN + FP)\n"
            "                how well we avoid false alarms\n"
            "\n"
            "  F1          = 2 · (Precision · Recall) / (Precision + Recall)"},
        {"type": "callout", "tone": "warn",
         "title": L("Why accuracy alone is the wrong metric in medicine",
                    "لماذا الدقة وحدها مقياس خاطئ في الطب"),
         "text": L(
            "In a screening setting, missing a tumor (a false negative) is far more harmful than "
            "raising a false alarm (a false positive) — yet accuracy weights them identically. The "
            "clinically meaningful number is recall (sensitivity) per tumor class, read off a "
            "confusion matrix. train.py does compute a confusion matrix and a full per-class "
            "classification report; the API deliberately returns null for those fields rather than "
            "fabricating numbers it does not have.",
            "في سياق المسح، يكون تفويت ورم (سلبية كاذبة) أشد ضررًا بكثير من إطلاق إنذار كاذب (إيجابية "
            "كاذبة) — ومع ذلك تزنهما الدقة بالتساوي. والرقم ذو المعنى السريري هو الاستدعاء "
            "(الحساسية) لكل فئة ورم، ويُقرأ من مصفوفة الالتباس. ويحسب train.py فعلًا مصفوفة التباس "
            "وتقرير تصنيف كاملًا لكل فئة؛ أما الـAPI فيُعيد عمدًا قيمة فارغة لتلك الحقول بدل اختلاق "
            "أرقام لا يملكها.")},
    ],
}
