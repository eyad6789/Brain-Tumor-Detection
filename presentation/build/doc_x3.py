# -*- coding: utf-8 -*-
"""Extra deep-dive sections, part 3 — hands-on testing, roadmap,
commercialization, the live demo script, hard questions, and the file map.
"""
from i18n import L

# ── N · TEST IT YOURSELF ─────────────────────────────────────────────────
TESTING = {
    "id": "testing",
    "title": L("Test It Yourself — a Hands-On Script",
               "جرّبه بنفسك — دليل عملي"),
    "lead": L(
        "Hand this page to a judge and let them break the system on purpose. A team that invites "
        "adversarial testing looks far stronger than one that only demos the happy path.",
        "سلّم هذه الصفحة إلى المُحكِّم ودعه يحاول كسر النظام عمدًا. فالفريق الذي يدعو إلى الاختبار "
        "العدائي يبدو أقوى بكثير من فريق لا يعرض إلا المسار السعيد."),
    "blocks": [
        {"type": "h", "text": L("Step 0 — get it running in three terminals",
                                "الخطوة صفر — شغّله في ثلاث نوافذ طرفية")},
        {"type": "code", "code":
            "# Terminal 1 — the API (run from the repository root)\n"
            "source venv/bin/activate\n"
            "pip install -r backend/requirements.txt\n"
            "uvicorn backend.main:app --port 8000 --reload\n"
            "\n"
            "# Terminal 2 — the web app\n"
            "cd frontend && npm install && npm run dev   # port 3000\n"
            "\n"
            "# Terminal 3 — the optional local LLM\n"
            "ollama serve\n"
            "ollama pull qwen2.5:1.5b-instruct-q4_K_M\n"
            "\n"
            "# ...or the whole stack at once:\n"
            "docker compose up --build"},
        {"type": "h", "text": L("Test 1 — is the system actually alive?",
                                "الاختبار 1 — هل النظام حيّ فعلًا؟")},
        {"type": "code", "code":
            "curl -s http://localhost:8000/api/health | python3 -m json.tool"},
        {"type": "p", "text": L(
            "Expect model_loaded: true, the device (cpu or cuda), and two capability flags. This one "
            "call proves the weights loaded, tells you whether heatmaps and reports will work, and "
            "names the LLM in use. If model_loaded is false, model_error contains the reason in plain "
            "English — the API stays up on purpose so you can read it.",
            "توقّع model_loaded: true، والجهاز (cpu أو cuda)، وعَلمَي قدرة. هذا النداء وحده يثبت "
            "تحميل الأوزان، ويخبرك هل ستعمل الخرائط الحرارية والتقارير، ويسمّي النموذج اللغوي "
            "المستخدَم. وإن كان model_loaded يساوي false فإن model_error يحوي السبب بلغة واضحة — "
            "ويبقى الـAPI عاملًا عمدًا لتستطيع قراءته.")},
        {"type": "h", "text": L("Test 2 — the interactive API documentation",
                                "الاختبار 2 — التوثيق التفاعلي للـAPI")},
        {"type": "p", "text": L(
            "Open http://localhost:8000/docs. FastAPI generates a full OpenAPI page from the Pydantic "
            "schemas, and every endpoint can be executed from the browser with a real file upload. "
            "This is often the single most persuasive thing to show a technical judge, because it "
            "proves the API is typed and self-describing rather than hand-rolled.",
            "افتح http://localhost:8000/docs. يولّد FastAPI صفحة OpenAPI كاملة من مخطّطات Pydantic، "
            "ويمكن تنفيذ كل نقطة نهاية من المتصفح برفع ملف حقيقي. وهذا غالبًا أكثر ما يُقنع "
            "المُحكِّم التقني، لأنه يثبت أن الـAPI مُوصَّف الأنواع ويصف نفسه بدل أن يكون مصنوعًا "
            "يدويًا.")},
        {"type": "h", "text": L("Test 3 — a real prediction from the command line",
                                "الاختبار 3 — تنبؤ حقيقي من سطر الأوامر")},
        {"type": "code", "code":
            "curl -s -X POST http://localhost:8000/api/predict \\\n"
            "     -F 'file=@some_mri.jpg' \\\n"
            "     | python3 -m json.tool\n"
            "\n"
            "# Skip the heatmap to see the raw classification speed:\n"
            "curl -s -X POST \\\n"
            "     'http://localhost:8000/api/predict?gradcam=false' \\\n"
            "     -F 'file=@some_mri.jpg'"},
        {"type": "p", "text": L(
            "Check that the four probabilities sum to 1.0 and that they come back sorted descending. "
            "Run the same image twice: the result must be identical every time, because the "
            "inference transform contains no randomness and the model is in eval() mode.",
            "تحقّق من أن الاحتمالات الأربعة مجموعها 1.0 وأنها تعود مرتَّبة تنازليًا. وشغّل الصورة "
            "نفسها مرتين: يجب أن تكون النتيجة متطابقة في كل مرة، لأن تحويل الاستدلال خالٍ من "
            "العشوائية والنموذج في وضع eval().")},
        {"type": "h", "text": L("Tests 4–9 — try to break it", "الاختبارات 4–9 — حاول كسره")},
        {"type": "table",
         "head": [L("Do this", "افعل هذا"), L("What should happen", "ما ينبغي أن يحدث"),
                  L("What it proves", "ما الذي يُثبته")],
         "rows": [
            [L("Upload a PDF or a .zip renamed to .png",
               "ارفع ملف PDF أو .zip أُعيدت تسميته إلى .png"),
             L("415 unsupported_type, or 422 invalid_image if the MIME header was faked.",
               "415 unsupported_type، أو 422 invalid_image إن زُوّرت ترويسة MIME."),
             L("Validation checks the actual bytes, not the file name.",
               "يفحص التحقّق البايتات الفعلية لا اسم الملف.")],
            [L("Upload a 0-byte file", "ارفع ملفًا بحجم صفر بايت"),
             L("422 empty_file", "422 empty_file"),
             L("Edge cases were thought about, not discovered in the demo.",
               "جرى التفكير في الحالات الحدّية، ولم تُكتشف أثناء العرض.")],
            [L("Upload a 20 MB image", "ارفع صورة بحجم 20 ميغابايت"),
             L("413 file_too_large from the API; the browser blocks it even earlier at 10 MB.",
               "413 file_too_large من الـAPI؛ ويحجبها المتصفح قبل ذلك عند 10 ميغابايت."),
             L("Two layers of defence, and the server-side one is the real one.",
               "طبقتا دفاع، والطبقة على الخادم هي الحقيقية.")],
            [L("Upload a photograph of a cat, a car or a face",
               "ارفع صورة قطة أو سيارة أو وجه"),
             L("It will confidently return one of the four classes — often at high confidence.",
               "سيُعيد بثقة إحدى الفئات الأربع — وغالبًا بثقة عالية."),
             L("The most important limitation in the whole project. The model has only four possible "
               "answers and softmax always normalizes to 1, so it cannot say \"this is not a brain "
               "MRI\". Say this out loud before a judge finds it: it is a known gap, and the fix (an "
               "out-of-distribution detector plus confidence calibration) is item one on the roadmap.",
               "أهم حدٍّ في المشروع كله. فليس أمام النموذج سوى أربع إجابات ممكنة، و softmax يطبّع "
               "دائمًا إلى واحد، فلا يستطيع قول «هذه ليست صورة رنين للدماغ». قل هذا بصوت عالٍ قبل أن "
               "يكتشفه المُحكِّم: فهو ثغرة معروفة، وإصلاحها (كاشف خروج عن التوزيع مع معايرة الثقة) "
               "هو البند الأول في خارطة الطريق.")],
            [L("Stop the backend, then press Analyze",
               "أوقف الخادم ثم اضغط «تحليل»"),
             L("A readable message: \"Could not reach the backend. Make sure the API server is "
               "running.\"",
               "رسالة مقروءة: «تعذّر الوصول إلى الخادم. تأكّد من تشغيل خادم الـAPI.»"),
             L("Network failure is handled as a typed error, not an unhandled exception.",
               "يُعالَج فشل الشبكة كخطأ مُوصَّف النوع لا كاستثناء غير معالَج.")],
            [L("Never start Ollama, then run an analysis",
               "لا تشغّل Ollama أبدًا ثم نفّذ تحليلًا"),
             L("Prediction and heatmap work perfectly; the report panel shows the exact `ollama pull` "
               "command.",
               "يعمل التنبؤ والخريطة الحرارية تمامًا؛ وتعرض لوحة التقرير أمر `ollama pull` بالضبط."),
             L("Optional features degrade instead of taking the app down.",
               "تتراجع الميزات الاختيارية بلطف بدل إسقاط التطبيق.")],
            [L("Upload a new image while an analysis is still running",
               "ارفع صورة جديدة أثناء تشغيل تحليل"),
             L("The old request is aborted; the old result never appears.",
               "يُلغى الطلب القديم؛ ولا تظهر نتيجته أبدًا."),
             L("Race conditions were handled with AbortControllers.",
               "عولجت حالات السباق بمتحكّمات الإلغاء.")],
            [L("Toggle dark/light and the four accent palettes; resize to a phone width",
               "بدّل بين الداكن والفاتح واللوحات الأربع؛ وصغّر النافذة إلى عرض هاتف"),
             L("Instant switching with no flash of the wrong theme, and a responsive layout.",
               "تبديل فوري بلا وميض بالسمة الخاطئة، وتخطيط متجاوب."),
             L("The design system is real, not a screenshot.",
               "نظام التصميم حقيقي لا لقطة شاشة.")],
        ]},
        {"type": "h", "text": L("Test 10 — verify our honesty claim",
                                "الاختبار 10 — تحقّق من ادّعائنا بالصدق")},
        {"type": "code", "code":
            "curl -s http://localhost:8000/api/metrics \\\n"
            "     | python3 -m json.tool | head -20"},
        {"type": "p", "text": L(
            "The response contains claimed_accuracy together with accuracy_caveat — a sentence that "
            "states, in the API itself, that the test set was reused for validation and the figure is "
            "therefore optimistic. confusion_matrix and per_class come back as null, because "
            "model_log.csv does not contain them and the code refuses to invent them. Showing a judge "
            "that your API admits what it does not know is a stronger move than any accuracy number.",
            "تحوي الاستجابة claimed_accuracy مع accuracy_caveat — وهي جملة تنصّ، داخل الـAPI نفسه، "
            "على أن مجموعة الاختبار أُعيد استخدامها للتحقق وأن الرقم متفائل لذلك. وتعود "
            "confusion_matrix و per_class فارغتين، لأن model_log.csv لا يحويهما والشيفرة ترفض "
            "اختلاقهما. وإظهار أن واجهتك البرمجية تعترف بما لا تعرفه أقوى من أي رقم دقة.")},
    ],
}

# ── O · ROADMAP ──────────────────────────────────────────────────────────
ROADMAP = {
    "id": "roadmap",
    "title": L("How We Make It Better — the Roadmap",
               "كيف نجعله أفضل — خارطة الطريق"),
    "lead": L(
        "Ordered by honesty first, capability second, scale third. Every item names the specific "
        "weakness it removes.",
        "مرتَّبة بالصدق أولًا، ثم القدرة، ثم التوسّع. وكل بند يسمّي الضعف المحدَّد الذي يزيله."),
    "blocks": [
        {"type": "h", "text": L("Phase 1 — fix the science (weeks, not months)",
                                "المرحلة 1 — إصلاح العلم (أسابيع لا أشهر)")},
        {"type": "table",
         "head": [L("Item", "البند"), L("The weakness it removes", "الضعف الذي يزيله")],
         "rows": [
            [L("A genuine three-way split, or 5-fold cross-validation",
               "تقسيم ثلاثي حقيقي، أو تحقّق متقاطع خماسي"),
             L("The headline number stops being \"claimed\" and becomes a real, unbiased "
               "generalization estimate. This is the single highest-value change in the project.",
               "يتوقّف الرقم البارز عن كونه «مُعلَنًا» ويصير تقديرًا حقيقيًا غير متحيّز للتعميم. "
               "وهذا أعلى التغييرات قيمةً في المشروع.")],
            [L("Publish the confusion matrix and per-class precision / recall / F1",
               "نشر مصفوفة الالتباس ودقة كل فئة واستدعائها ومقياس F1"),
             L("Accuracy hides the only thing that matters clinically: how many tumors we miss. "
               "train.py already computes these — they just need to reach the API and the dashboard.",
               "تخفي الدقةُ الشيءَ الوحيد المهمّ سريريًا: كم ورمًا نفوّت. وتحسب train.py هذه القيم "
               "أصلًا — وما تحتاجه هو الوصول إلى الـAPI ولوحة المعلومات.")],
            [L("Out-of-distribution detection", "كشف الخروج عن التوزيع"),
             L("Stops the model confidently classifying a photograph of a cat. Practical approaches: "
               "a maximum-softmax-probability threshold, energy scores, or a lightweight \"is this a "
               "brain MRI?\" gate model.",
               "يمنع النموذج من تصنيف صورة قطة بثقة. والمناهج العملية: عتبة لأقصى احتمال softmax، أو "
               "درجات الطاقة، أو نموذج بوابة خفيف يسأل «هل هذه صورة رنين للدماغ؟».")],
            [L("Confidence calibration (temperature scaling)", "معايرة الثقة (قياس الحرارة)"),
             L("Makes \"95%\" mean that the model is right about 95% of the time, instead of being an "
               "arbitrary softmax artifact. Cheap to implement, high credibility payoff.",
               "يجعل «95%» تعني أن النموذج مصيب نحو 95% من المرات، بدل أن تكون أثرًا اعتباطيًا "
               "لـsoftmax. رخيص التنفيذ وعالي المردود في المصداقية.")],
            [L("Automated tests + CI", "اختبارات آلية مع تكامل مستمر"),
             L("The repository currently has none. A handful of pytest cases over load_upload_image, "
               "predict_core's output shape and the four error codes would prevent an entire class of "
               "regression.",
               "لا يحوي المستودع حاليًا أي اختبار. وحفنة من حالات pytest على load_upload_image وشكل "
               "مخرَج predict_core ورموز الخطأ الأربعة ستمنع صنفًا كاملًا من الانتكاسات.")],
        ]},
        {"type": "h", "text": L("Phase 2 — clinical capability", "المرحلة 2 — القدرة السريرية")},
        {"type": "bullets", "items": [
            L("DICOM support — real hospitals do not have JPEGs. Reading DICOM means handling "
              "windowing, slice geometry, patient metadata and de-identification. Without it the tool "
              "cannot touch a real workflow.",
              "دعم DICOM — لا تملك المستشفيات الحقيقية ملفات JPEG. وقراءة DICOM تعني التعامل مع "
              "النوافذ وهندسة الشرائح والبيانات الوصفية للمريض وإزالة المعرّفات. وبدونه لا تستطيع "
              "الأداة ملامسة مسار عمل حقيقي."),
            L("Segmentation with U-Net — move from \"there is a glioma\" to \"here is its outline and "
              "its volume\". This is what actually changes treatment planning, and it is the natural "
              "successor to a GradCAM heatmap.",
              "التجزئة بـU-Net — الانتقال من «يوجد ورم دبقي» إلى «هذا محيطه وهذا حجمه». وهذا ما "
              "يغيّر فعلًا تخطيط العلاج، وهو الخليفة الطبيعي لخريطة GradCAM الحرارية."),
            L("3D volumetric analysis — an MRI is a stack of slices, not one image. A 3D CNN, or "
              "aggregating predictions across a series, uses information a single-slice model throws "
              "away.",
              "التحليل الحجمي ثلاثي الأبعاد — صورة الرنين كومة شرائح لا صورة واحدة. وشبكة التفافية "
              "ثلاثية الأبعاد، أو تجميع التنبؤات عبر السلسلة، تستخدم معلومات يهدرها نموذج الشريحة "
              "الواحدة."),
            L("Multi-dataset validation — evaluate on BraTS, Figshare, and hospital data from a "
              "different scanner. Cross-site accuracy is the only number a clinician will believe.",
              "التحقّق عبر مجموعات متعددة — التقييم على BraTS و Figshare وبيانات مستشفى من جهاز "
              "مختلف. فالدقة عبر المواقع هي الرقم الوحيد الذي سيصدّقه الطبيب."),
            L("Radiologist-in-the-loop feedback — let the reader mark a prediction right or wrong, "
              "and use that stream both as a quality signal and as future training data.",
              "تغذية راجعة من الأخصائي داخل الحلقة — دع القارئ يضع علامة صواب أو خطأ على التنبؤ، "
              "واستخدم ذلك التدفّق إشارةَ جودة وبياناتِ تدريب مستقبلية معًا."),
        ]},
        {"type": "h", "text": L("Phase 3 — product and scale", "المرحلة 3 — المنتج والتوسّع")},
        {"type": "bullets", "items": [
            L("Accounts, roles and an immutable audit log — who analyzed which study, when, and what "
              "the system said. Non-negotiable in any clinical deployment.",
              "حسابات وأدوار وسجلّ تدقيق غير قابل للتعديل — من حلّل أي دراسة ومتى وماذا قال النظام. "
              "وهذا غير قابل للتفاوض في أي نشر سريري."),
            L("Batch and queue processing — a worker queue (Celery or RQ) so a department can submit "
              "a whole day's studies overnight instead of one image at a time.",
              "معالجة دفعية وطوابير — طابور عمّال (Celery أو RQ) ليتمكّن قسم كامل من إرسال دراسات "
              "يوم بأكمله ليلًا بدل صورة واحدة في كل مرة."),
            L("A model registry and versioned checkpoints — replace a 98 MB binary in git with MLflow "
              "or DVC, so every prediction can name the exact model version that produced it.",
              "سجلّ نماذج ونقاط تفتيش مُصدَّرة — استبدال ملف ثنائي بحجم 98 ميغابايت في git بـMLflow "
              "أو DVC، ليتمكّن كل تنبؤ من تسمية إصدار النموذج الذي أنتجه بالضبط."),
            L("Observability — structured logs, Prometheus metrics, and drift monitoring that alerts "
              "when the input distribution shifts away from the training data.",
              "قابلية الرصد — سجلّات مهيكلة ومقاييس Prometheus ومراقبة انحراف تُنذر عند ابتعاد توزيع "
              "المدخلات عن بيانات التدريب."),
            L("PACS / HL7 / FHIR integration — the model has to live inside the radiologist's "
              "existing viewer, not in a separate browser tab. This is usually the real barrier to "
              "adoption, not accuracy.",
              "تكامل مع PACS و HL7 و FHIR — يجب أن يعيش النموذج داخل عارض الأخصائي القائم لا في "
              "لسان متصفح منفصل. وهذا عادةً هو الحاجز الحقيقي أمام التبنّي، لا الدقة."),
            L("Model compression — ONNX export, quantization or a MobileNet/EfficientNet distillation "
              "for edge and mobile deployment.",
              "ضغط النموذج — تصدير إلى ONNX أو تكميم أو تقطير إلى MobileNet/EfficientNet للنشر على "
              "الأجهزة الطرفية والهواتف."),
        ]},
        {"type": "callout", "tone": "info",
         "title": L("How to present the roadmap", "كيف تعرض خارطة الطريق"),
         "text": L(
            "Do not present it as a wish list. Present it as: \"here is the flaw we found in our own "
            "work, here is the exact fix, here is how long it takes, and here is what it unlocks.\" "
            "Judges reward teams that can criticize themselves precisely far more than teams that "
            "claim everything already works.",
            "لا تعرضها قائمة أمنيات، بل اعرضها هكذا: «هذا الخلل الذي وجدناه في عملنا، وهذا الإصلاح "
            "بالضبط، وهذه مدّته، وهذا ما يفتحه». فالمُحكِّمون يكافئون الفرق القادرة على نقد نفسها "
            "بدقة أكثر بكثير من الفرق التي تدّعي أن كل شيء يعمل.")},
    ],
}

# ── P · COMMERCIALIZATION ────────────────────────────────────────────────
BUSINESS = {
    "id": "business",
    "title": L("Commercialization — How This Could Be Sold",
               "التسويق التجاري — كيف يمكن بيع هذا"),
    "lead": L(
        "The honest version: today this is a prototype and it is not sellable. This section sets out "
        "what it would take to change that, who would pay, how much, and in what order.",
        "النسخة الصادقة: هذا اليوم نموذج أولي وغير قابل للبيع. ويعرض هذا القسم ما يلزم لتغيير ذلك، "
        "ومن سيدفع، وكم، وبأي ترتيب."),
    "blocks": [
        {"type": "callout", "tone": "warn",
         "title": L("Start here, always", "ابدأ من هنا دائمًا"),
         "text": L(
            "Software that influences a diagnosis is regulated as a medical device almost everywhere "
            "in the world. Selling this build as a diagnostic tool today would be both unsafe and "
            "illegal. Everything below assumes the regulatory path is walked, not skipped.",
            "البرمجيات التي تؤثّر في التشخيص مُنظَّمة بوصفها جهازًا طبيًا في جميع أنحاء العالم "
            "تقريبًا. وبيع هذا البناء اليوم بوصفه أداة تشخيص سيكون غير آمن وغير قانوني معًا. وكل ما "
            "يلي يفترض سلوك المسار التنظيمي لا تخطّيه.")},
        {"type": "h", "text": L("Who would actually pay", "من الذي سيدفع فعلًا")},
        {"type": "table",
         "head": [L("Segment", "الشريحة"), L("What they buy", "ما الذي يشترونه"),
                  L("Why they buy it", "لماذا يشترونه"),
                  L("Regulatory burden", "العبء التنظيمي")],
         "rows": [
            [L("Universities & medical schools", "الجامعات وكليات الطب"),
             L("A teaching licence for the whole platform.", "رخصة تعليمية للمنصّة كاملةً."),
             L("It teaches CNNs, explainability and MLOps in one working system, in Arabic and "
               "English. No patient data involved.",
               "تُعلِّم الشبكات الالتفافية والتفسير وهندسة تشغيل التعلّم الآلي في نظام واحد عامل، "
               "بالعربية والإنجليزية. وبلا أي بيانات مرضى."),
             L("None — this is sellable now.", "لا شيء — وهذا قابل للبيع الآن.")],
            [L("Radiology research groups", "مجموعات أبحاث الأشعة"),
             L("An on-premise research tool plus support.", "أداة بحثية داخل المؤسسة مع دعم."),
             L("Fully offline, so no ethics-committee fight about sending images to a cloud; open "
               "enough to retrain on their own data.",
               "تعمل بلا اتصال تمامًا، فلا نزاع مع لجنة الأخلاقيات حول إرسال الصور إلى السحابة؛ "
               "ومفتوحة بما يكفي لإعادة التدريب على بياناتهم."),
             L("Low — \"research use only\" labelling.", "منخفض — وسم «للاستخدام البحثي فقط».")],
            [L("Small hospitals & imaging centres", "المستشفيات الصغيرة ومراكز التصوير"),
             L("A triage assistant that pre-sorts the queue.", "مساعد فرز يرتّب الطابور مسبقًا."),
             L("The core economic argument: a radiologist's time. Flagging likely-abnormal studies "
               "first shortens the wait for the patients who need it most.",
               "الحُجّة الاقتصادية الجوهرية: وقت أخصائي الأشعة. فتقديم الدراسات المرجَّح شذوذها "
               "يقصّر الانتظار على المرضى الأشد حاجة."),
             L("High — full medical-device clearance.", "مرتفع — اعتماد كامل كجهاز طبي.")],
            [L("Telemedicine & rural clinics", "الطب عن بُعد والعيادات الريفية"),
             L("An offline second-look on a local machine.", "رأي ثانٍ يعمل بلا اتصال على جهاز محلي."),
             L("Where there is no on-site radiologist and no reliable internet, a fully local model "
               "is not a convenience — it is the only option.",
               "حيث لا أخصائي أشعة في الموقع ولا إنترنت موثوق، لا يكون النموذج المحلي الكامل "
               "رفاهية — بل هو الخيار الوحيد."),
             L("High.", "مرتفع.")],
            [L("Health-tech companies", "شركات التقنية الصحية"),
             L("The explainability layer as a component.", "طبقة التفسير بوصفها مكوّنًا."),
             L("Many teams have a classifier and no GradCAM + report layer. That layer is the "
               "differentiated asset here.",
               "كثير من الفرق لديه مُصنِّف وليس لديه طبقة GradCAM مع التقرير. وتلك الطبقة هي الأصل "
               "المميِّز هنا."),
             L("Depends on their claims.", "يعتمد على ادّعاءاتهم.")],
        ]},
        {"type": "callout", "tone": "good",
         "title": L("The obvious first move", "الخطوة الأولى البديهية"),
         "text": L(
            "Sell the education and research segments first. They need no regulatory clearance, they "
            "can buy this year, and every deployment generates the feedback, the varied data and the "
            "reference customers that a clinical product needs anyway. Revenue while you build the "
            "compliance case is far better than compliance with no revenue.",
            "بِع لشريحتَي التعليم والبحث أولًا. فهما لا تحتاجان اعتمادًا تنظيميًا، وتستطيعان الشراء "
            "هذا العام، وكل نشر يولّد التغذية الراجعة والبيانات المتنوّعة والعملاء المرجعيين التي "
            "يحتاجها المنتج السريري على أي حال. والإيراد أثناء بناء ملف الامتثال أفضل بكثير من "
            "امتثال بلا إيراد.")},
        {"type": "h", "text": L("Three business models", "ثلاثة نماذج أعمال")},
        {"type": "table",
         "head": [L("Model", "النموذج"), L("How it works", "كيف يعمل"),
                  L("Fits", "يناسب"), L("Watch out for", "احذر من")],
         "rows": [
            [L("On-premise licence", "رخصة داخل المؤسسة"),
             L("An annual per-site or per-seat licence for the Docker stack, running on the "
               "customer's own hardware.",
               "رخصة سنوية لكل موقع أو لكل مقعد لحزمة Docker، تعمل على عتاد العميل نفسه."),
             L("Hospitals and universities — the offline architecture is already exactly this "
               "product.",
               "المستشفيات والجامعات — فالمعمارية العاملة بلا اتصال هي بالضبط هذا المنتج أصلًا."),
             L("Support and upgrade logistics across many isolated sites.",
               "لوجستيات الدعم والترقية عبر مواقع معزولة كثيرة.")],
            [L("SaaS / per-study", "خدمة سحابية أو لكل دراسة"),
             L("Hosted, billed per scan analyzed or per monthly tier.",
               "مستضاف، ويُفوتَر لكل صورة تُحلَّل أو بمستويات شهرية."),
             L("Small clinics with no IT department.", "العيادات الصغيرة بلا قسم تقنية معلومات."),
             L("It destroys the privacy story that is currently the strongest selling point. Requires "
               "data-processing agreements and a compliant host.",
               "يهدم حكاية الخصوصية التي هي أقوى نقاط البيع حاليًا. ويتطلّب اتفاقيات معالجة بيانات "
               "ومضيفًا ممتثلًا.")],
            [L("Open core", "نواة مفتوحة"),
             L("The model and API stay open; charge for DICOM/PACS integration, support, audit "
               "logging and validated model updates.",
               "يبقى النموذج والـAPI مفتوحَين؛ ويُتقاضى الثمن على تكامل DICOM و PACS والدعم وسجلّ "
               "التدقيق وتحديثات النماذج المُتحقَّق منها."),
             L("Building credibility and adoption fast in a research community.",
               "بناء المصداقية والتبنّي بسرعة في مجتمع بحثي."),
             L("Requires real discipline about which features are paid.",
               "يتطلّب انضباطًا حقيقيًا في تحديد الميزات المدفوعة.")],
        ]},
        {"type": "h", "text": L("The regulatory path, concretely", "المسار التنظيمي بصورة ملموسة")},
        {"type": "num", "items": [
            L("Classify the product. Software intended to inform a diagnosis is Software as a Medical "
              "Device (SaMD). Under the international IMDRF framework its risk class depends on how "
              "serious the condition is and how much weight the software carries in the decision — "
              "brain tumors are serious, so this is not the lowest class.",
              "صنّف المنتج. فالبرمجيات المعدّة لإفادة التشخيص هي «برمجيات كجهاز طبي» (SaMD). وبحسب "
              "إطار IMDRF الدولي تعتمد فئة خطرها على خطورة الحالة ومقدار وزن البرمجية في القرار — "
              "وأورام الدماغ خطيرة، فهذه ليست أدنى فئة."),
            L("Pick the claim carefully. \"Triage assistant that prioritizes a worklist\" is a far "
              "lighter claim than \"diagnoses brain tumors\", and it is both more honest and far "
              "faster to clear.",
              "اختر الادّعاء بعناية. فـ«مساعد فرز يرتّب قائمة العمل» ادّعاء أخفّ بكثير من «يشخّص "
              "أورام الدماغ»، وهو أصدق وأسرع اعتمادًا معًا."),
            L("Build the quality system. ISO 13485 for the organization and IEC 62304 for the "
              "software lifecycle: documented requirements, risk management (ISO 14971), design "
              "history, and traceability from requirement to test.",
              "ابنِ نظام الجودة. ISO 13485 للمنظّمة و IEC 62304 لدورة حياة البرمجية: متطلّبات "
              "موثَّقة، وإدارة مخاطر (ISO 14971)، وسجلّ تصميم، وتتبّع من المتطلَّب إلى الاختبار."),
            L("Run a real clinical validation study on data the model has never seen, from multiple "
              "sites and scanners, with a radiologist-established ground truth. This is the expensive "
              "part and there is no shortcut around it.",
              "أجرِ دراسة تحقّق سريري حقيقية على بيانات لم يرها النموذج قط، من مواقع وأجهزة متعددة، "
              "بمرجع حقيقة يضعه أخصائي أشعة. وهذا هو الجزء المكلف ولا اختصار حوله."),
            L("Submit to the relevant authority — an FDA 510(k) in the United States, CE marking "
              "under the EU MDR in Europe, or the national health regulator in your own market. In "
              "the Gulf and wider MENA region, an existing FDA or CE clearance usually shortens the "
              "national process considerably.",
              "قدّم إلى الجهة المعنية — تصريح 510(k) من إدارة الغذاء والدواء في الولايات المتحدة، أو "
              "علامة CE بموجب لائحة MDR الأوروبية، أو الجهة الصحية الوطنية في سوقك. وفي الخليج "
              "ومنطقة الشرق الأوسط وشمال أفريقيا عمومًا، يختصر وجود اعتماد FDA أو CE المسارَ الوطني "
              "اختصارًا كبيرًا."),
            L("Commit to post-market surveillance: monitor performance in the field, track drift, and "
              "report incidents. A model is not \"done\" when it ships.",
              "التزم بالمراقبة بعد التسويق: راقب الأداء ميدانيًا، وتتبّع الانحراف، وأبلغ عن الحوادث. "
              "فالنموذج لا «ينتهي» عند إطلاقه."),
        ]},
        {"type": "h", "text": L("What must be built before the first clinical sale",
                                "ما يجب بناؤه قبل أول بيع سريري")},
        {"type": "bullets", "items": [
            L("An unbiased, published validation on unseen multi-site data — this replaces the "
              "\"claimed\" accuracy and is the foundation of every other claim.",
              "تحقّق غير متحيّز ومنشور على بيانات غير مرئية من مواقع متعددة — يحلّ محلّ الدقة "
              "«المُعلَنة» وهو أساس كل ادّعاء آخر."),
            L("DICOM ingestion and de-identification.", "استيعاب DICOM وإزالة المعرّفات."),
            L("Authentication, role-based access and an immutable audit log.",
              "الاستيثاق والوصول القائم على الأدوار وسجلّ تدقيق غير قابل للتعديل."),
            L("Model versioning, so any past prediction can be reproduced exactly.",
              "إصدارات النماذج، ليمكن إعادة إنتاج أي تنبؤ سابق بالضبط."),
            L("Out-of-distribution rejection — a clinical system must be able to say \"I will not "
              "answer this\".",
              "رفض الخارج عن التوزيع — يجب أن يستطيع النظام السريري قول «لن أجيب عن هذا»."),
            L("Automated tests, CI, and a documented release process.",
              "اختبارات آلية وتكامل مستمر وعملية إصدار موثَّقة."),
            L("Professional liability insurance and clear terms of use.",
              "تأمين مسؤولية مهنية وشروط استخدام واضحة."),
        ]},
        {"type": "h", "text": L("Pricing: how to reason about it", "التسعير: كيف نفكّر فيه")},
        {"type": "p", "text": L(
            "Price against the value of the time saved, not against the cost of the servers. The "
            "argument a buyer understands is: how many studies per month, how many minutes of "
            "specialist time each one saves, and what an hour of that specialist's time is worth in "
            "their market. Build the number bottom-up from the customer's own figures during the "
            "meeting — that is far more persuasive than a fixed price list, and far safer than "
            "quoting a market-size statistic you have not personally verified.",
            "سعّر مقابل قيمة الوقت الموفَّر لا مقابل تكلفة الخوادم. فالحُجّة التي يفهمها المشتري "
            "هي: كم دراسة في الشهر، وكم دقيقة من وقت الأخصائي توفّر كلٌّ منها، وكم تساوي ساعة ذلك "
            "الأخصائي في سوقه. وابنِ الرقم تصاعديًا من أرقام العميل نفسه أثناء الاجتماع — فهذا أقنع "
            "بكثير من قائمة أسعار ثابتة، وأسلم بكثير من الاستشهاد بإحصاء لحجم السوق لم تتحقّق منه "
            "بنفسك.")},
        {"type": "callout", "tone": "info",
         "title": L("If a judge asks \"what is the market size?\"",
                    "إن سأل مُحكِّم: «ما حجم السوق؟»"),
         "text": L(
            "Do not quote a number you cannot source. Say instead: \"We size it bottom-up — the "
            "number of imaging centres in our target market, times the studies each performs per "
            "year, times a per-study or per-site price. We would rather show you that arithmetic than "
            "a global figure we did not measure.\" That answer is more credible than a large "
            "number, and it cannot be picked apart.",
            "لا تستشهد برقم لا تستطيع عزوه إلى مصدر. بل قل: «نقيسه تصاعديًا — عدد مراكز التصوير في "
            "سوقنا المستهدف، مضروبًا في عدد الدراسات التي يجريها كلٌّ منها سنويًا، مضروبًا في سعر "
            "لكل دراسة أو لكل موقع. ونفضّل أن نُريكم هذه العملية الحسابية على رقم عالمي لم نقِسه». "
            "وهذا الجواب أجدر بالتصديق من رقم كبير، ولا يمكن تفنيده.")},
        {"type": "h", "text": L("The competitive position, honestly",
                                "الموقع التنافسي بصدق")},
        {"type": "p", "text": L(
            "There are cleared commercial products in neuro-imaging AI, backed by large clinical "
            "validation studies. This project does not compete with them on accuracy or on approval. "
            "Where a small team can genuinely win is a narrower position: fully offline operation for "
            "sites with no reliable internet or no permission to send images anywhere; explainability "
            "as a first-class feature rather than an afterthought; bilingual Arabic/English delivery "
            "for a region most vendors do not localize for; and a price point that a university or a "
            "district hospital can actually approve. Saying this plainly is a strength — a team that "
            "claims to beat a cleared medical device with a hackathon project loses the room.",
            "توجد منتجات تجارية معتمَدة في الذكاء الاصطناعي للتصوير العصبي، مدعومة بدراسات تحقّق "
            "سريري كبيرة. ولا ينافسها هذا المشروع في الدقة ولا في الاعتماد. أما حيث يستطيع فريق "
            "صغير الفوز فعلًا فهو موقع أضيق: التشغيل الكامل بلا اتصال للمواقع التي لا إنترنت موثوقًا "
            "لديها أو لا إذن لديها بإرسال الصور إلى أي مكان؛ والتفسير بوصفه ميزة من الدرجة الأولى لا "
            "فكرة لاحقة؛ والتسليم ثنائي اللغة عربي/إنجليزي لمنطقة لا يوطّن معظم المورّدين لها؛ وسعر "
            "تستطيع جامعة أو مستشفى قضاء اعتماده فعلًا. وقول هذا بصراحة قوّة — فالفريق الذي يدّعي "
            "التفوّق على جهاز طبي معتمَد بمشروع هاكاثون يخسر القاعة.")},
    ],
}

# ── Q · THE DEMO SCRIPT ──────────────────────────────────────────────────
DEMO = {
    "id": "demo",
    "title": L("The Live Demo Script, Minute by Minute",
               "نص العرض الحيّ دقيقةً بدقيقة"),
    "lead": L(
        "A five-minute plan that shows the strongest things first and never leaves dead air while "
        "something loads.",
        "خطة من خمس دقائق تعرض أقوى ما لديك أولًا ولا تترك فراغًا صامتًا أثناء تحميل أي شيء."),
    "blocks": [
        {"type": "h", "text": L("Before you start", "قبل أن تبدأ")},
        {"type": "bullets", "items": [
            L("Have everything already running and warm: backend, frontend, and Ollama with the model "
              "pulled. Run one throwaway analysis first so the model is loaded into memory — never "
              "let the judges watch a cold start.",
              "اجعل كل شيء يعمل ومُسخَّنًا مسبقًا: الخادم والواجهة و Ollama مع تنزيل النموذج. ونفّذ "
              "تحليلًا تجريبيًا واحدًا أولًا ليُحمَّل النموذج في الذاكرة — ولا تدع المُحكِّمين "
              "يشاهدون إقلاعًا باردًا أبدًا."),
            L("Have three images ready in a folder: a clear tumor case, a No Tumor case, and one "
              "non-MRI photograph for the honesty moment.",
              "جهّز ثلاث صور في مجلد: حالة ورم واضحة، وحالة بلا ورم، وصورة واحدة ليست رنينًا "
              "للحظة الصدق."),
            L("Open two browser tabs in advance: the app, and http://localhost:8000/docs.",
              "افتح لسانَي متصفح مسبقًا: التطبيق، و http://localhost:8000/docs."),
            L("Decide who speaks. One person drives the screen, one person talks. Never both.",
              "حدّدوا من يتكلّم. شخص يقود الشاشة وشخص يتكلّم. ولا يفعل الاثنان الأمرين معًا."),
        ]},
        {"type": "h", "text": L("Minute 0:00–0:40 — the problem",
                                "الدقيقة 0:00–0:40 — المشكلة")},
        {"type": "p", "text": L(
            "Landing page on screen. \"Reading a brain MRI needs a specialist, and in many hospitals "
            "there are far more scans than specialists. AI can help triage — but no doctor will trust "
            "a program that just prints a word and a percentage. So we built the part that makes it "
            "trustworthy.\"",
            "صفحة الهبوط على الشاشة. «قراءة صورة رنين الدماغ تحتاج أخصائيًا، وفي كثير من المستشفيات "
            "عدد الصور أكبر بكثير من عدد الأخصائيين. يستطيع الذكاء الاصطناعي المساعدة في الفرز — "
            "لكن لن يثق طبيب ببرنامج يطبع كلمة ونسبة فقط. لذا بنينا الجزء الذي يجعله جديرًا "
            "بالثقة.»")},
        {"type": "h", "text": L("Minute 0:40–2:00 — the live analysis",
                                "الدقيقة 0:40–2:00 — التحليل الحيّ")},
        {"type": "p", "text": L(
            "Drag in the tumor image and press Analyze. While the prediction appears, narrate: \"the "
            "image is resized to 224 by 224 and normalized, then a fine-tuned ResNet50 — 50 layers, "
            "about 24 million parameters — produces four scores that softmax turns into "
            "probabilities.\" Point at the four bars. Then switch the GradCAM viewer between Split and "
            "Overlay and drag the opacity slider: \"this is the model showing us where it looked. If "
            "the heat were on the image border or on a text label instead of the lesion, we would "
            "know not to trust this prediction — that check is impossible with a bare classifier.\"",
            "اسحب صورة الورم واضغط «تحليل». وأثناء ظهور التنبؤ اروِ: «تُحجَّم الصورة إلى 224×224 "
            "وتُطبَّع، ثم تُنتج ResNet50 مضبوطة — 50 طبقة ونحو 24 مليون معامل — أربع درجات يحوّلها "
            "softmax إلى احتمالات». وأشِر إلى الأشرطة الأربعة. ثم بدّل عارض GradCAM بين «مُقسَّم» "
            "و«تراكب» واسحب منزلق الشفافية: «هذا هو النموذج يُرينا أين نظر. فلو كانت الحرارة على "
            "حافة الصورة أو على مُلصَق نصّي بدل الآفة، لعرفنا ألا نثق بهذا التنبؤ — وهذا الفحص "
            "مستحيل مع مُصنِّف مجرّد».")},
        {"type": "h", "text": L("Minute 2:00–3:00 — the report and the privacy point",
                                "الدقيقة 2:00–3:00 — التقرير ونقطة الخصوصية")},
        {"type": "p", "text": L(
            "The report panel is generating. Use the wait deliberately: \"this is a language model "
            "running on this laptop. No internet, no API key, nothing sent anywhere — which for "
            "medical images is not a feature, it is a requirement. It receives the class and the four "
            "probabilities and writes five fixed sections.\" Then read the Recommended Next Steps and "
            "the Disclaimer aloud.",
            "لوحة التقرير تولّد الآن. استثمر الانتظار عمدًا: «هذا نموذج لغوي يعمل على هذا الحاسوب. "
            "بلا إنترنت ولا مفتاح API ولا إرسال شيء إلى أي مكان — وهذا في الصور الطبية ليس ميزة بل "
            "شرط. يتلقّى الفئة والاحتمالات الأربعة ويكتب خمسة أقسام ثابتة». ثم اقرأ بصوت مسموع "
            "«الخطوات التالية المقترحة» و«إخلاء المسؤولية».")},
        {"type": "h", "text": L("Minute 3:00–3:40 — the honesty moment (do not skip this)",
                                "الدقيقة 3:00–3:40 — لحظة الصدق (لا تتخطّها)")},
        {"type": "p", "text": L(
            "Go to /metrics. \"Our best validation accuracy was 99.39%. We label it 'claimed', and "
            "the API itself returns the reason: in that training run the test set was reused for "
            "validation, which is data leakage, so the number is optimistic. Fixing the evaluation is "
            "the first item on our roadmap.\" Optionally upload the non-MRI photograph: \"and here is "
            "the second limitation — the model has only four possible answers, so it cannot say "
            "'this is not a brain MRI'. Out-of-distribution detection is item two.\" This is the "
            "moment that separates you from every other team.",
            "انتقل إلى /metrics. «أفضل دقة تحقق لدينا كانت 99.39%. ونصفها بأنها «مُعلَنة»، ويُعيد "
            "الـAPI نفسه السبب: ففي ذلك التدريب أُعيد استخدام مجموعة الاختبار للتحقق، وهذا تسريب "
            "بيانات، فالرقم متفائل. وإصلاح التقييم هو البند الأول في خارطة طريقنا». واختياريًا ارفع "
            "الصورة التي ليست رنينًا: «وهذا هو الحدّ الثاني — ليس أمام النموذج سوى أربع إجابات "
            "ممكنة، فلا يستطيع قول «هذه ليست صورة رنين للدماغ». وكشف الخروج عن التوزيع هو البند "
            "الثاني». وهذه هي اللحظة التي تفصلكم عن كل فريق آخر.")},
        {"type": "h", "text": L("Minute 3:40–4:30 — that it is a real system",
                                "الدقيقة 3:40–4:30 — أنه نظام حقيقي")},
        {"type": "p", "text": L(
            "Switch to the /docs tab. \"This is not a notebook. It is a typed REST API with automatic "
            "OpenAPI documentation, upload validation with real HTTP status codes, a threadpool and a "
            "lock so concurrent GradCAM requests cannot corrupt each other, and three Docker "
            "containers behind nginx. Any hospital system could call this endpoint.\" Toggle the theme "
            "once on the way back — it takes a second and it lands.",
            "انتقل إلى لسان /docs. «هذا ليس دفتر ملاحظات. إنه واجهة REST مُوصَّفة الأنواع بتوثيق "
            "OpenAPI تلقائي، وتحقّق من الملفات المرفوعة برموز HTTP حقيقية، ومجمع خيوط وقفل يمنعان "
            "طلبات GradCAM المتزامنة من إفساد بعضها، وثلاث حاويات Docker خلف nginx. وأي نظام مستشفى "
            "يستطيع مناداة هذه النقطة». وبدّل السمة مرة واحدة في طريق العودة — تستغرق ثانية "
            "وتترك أثرًا.")},
        {"type": "h", "text": L("Minute 4:30–5:00 — the close",
                                "الدقيقة 4:30–5:00 — الختام")},
        {"type": "p", "text": L(
            "\"To summarize: a fine-tuned ResNet50 classifies the scan, GradCAM shows where it "
            "looked, and a local language model explains what it found — all offline, all on your own "
            "machine. Today it is an educational prototype and we say so on every screen. The path to "
            "something clinically useful is: fix the evaluation, add out-of-distribution rejection, "
            "add DICOM, and validate on multi-site data. Thank you — what would you like us to break "
            "for you?\"",
            "«خلاصة القول: تُصنِّف ResNet50 مضبوطة الصورة، ويُظهر GradCAM أين نظرت، ويشرح نموذج لغوي "
            "محلي ما وجدته — كل ذلك بلا اتصال وعلى جهازك أنت. وهو اليوم نموذج تعليمي ونقول ذلك على "
            "كل شاشة. والطريق إلى شيء مفيد سريريًا هو: إصلاح التقييم، وإضافة رفض الخارج عن "
            "التوزيع، وإضافة DICOM، والتحقّق على بيانات متعددة المواقع. شكرًا لكم — ما الذي تودّون "
            "منّا كسره أمامكم؟»")},
        {"type": "callout", "tone": "warn",
         "title": L("If something breaks live", "إن انكسر شيء أثناء العرض"),
         "text": L(
            "Do not apologize twice and do not start debugging on stage. Say what happened, say why "
            "the system is designed to survive it, and move on: \"Ollama isn't responding — notice "
            "the app didn't crash, it's telling us exactly which command to run. That's the graceful "
            "degradation we built in.\" A failure you narrate calmly is a demonstration; a failure "
            "you panic over is a failure.",
            "لا تعتذر مرتين ولا تبدأ التنقيح على المنصّة. قل ما حدث، وقل لماذا صُمِّم النظام "
            "للنجاة منه، ثم امضِ: «لا يستجيب Ollama — لاحظوا أن التطبيق لم ينهر، بل يخبرنا بالأمر "
            "المطلوب تشغيله بالضبط. هذا هو التراجع الآمن الذي بنيناه». فالإخفاق الذي ترويه بهدوء "
            "استعراضٌ للقدرة، والإخفاق الذي تفزع منه إخفاق.")},
    ],
}

# ── R · HARD QUESTIONS ───────────────────────────────────────────────────
HARD_QA = {
    "id": "hardqa",
    "title": L("Hard Questions a Technical Judge Will Ask",
               "أسئلة صعبة سيطرحها مُحكِّم تقني"),
    "lead": L(
        "The uncomfortable ones. Each answer is short enough to say out loud and true enough to "
        "survive a follow-up.",
        "الأسئلة المُحرِجة. وكل إجابة قصيرة بما يكفي لقولها شفهيًا وصادقة بما يكفي للصمود أمام سؤال "
        "متابعة."),
    "blocks": [
        {"type": "kv", "pairs": [
            [L("Your model can't say \"I don't know.\" Isn't that dangerous?",
               "نموذجكم لا يستطيع قول «لا أعرف». أليس هذا خطيرًا؟"),
             L("Yes, and it is our most important known limitation. Softmax always normalizes to 1 "
               "across exactly four options, so the model will confidently classify a photograph of a "
               "car. The fix is a two-part one — an out-of-distribution gate plus temperature "
               "calibration — and it is the top item on our roadmap. In the meantime the app is "
               "labelled educational on every screen and never presents a result as a diagnosis.",
               "نعم، وهو أهم حدٍّ معروف لدينا. إذ يطبّع softmax دائمًا إلى واحد عبر أربعة خيارات "
               "بالضبط، فسيصنّف النموذج صورة سيارة بثقة. والإصلاح من جزأين — بوابة للخروج عن "
               "التوزيع مع معايرة الحرارة — وهو البند الأول في خارطة طريقنا. وفي الأثناء يُوسَم "
               "التطبيق بأنه تعليمي على كل شاشة ولا يقدّم نتيجة بوصفها تشخيصًا أبدًا.")],
            [L("How do you know the model isn't cheating on a dataset artifact?",
               "كيف تعرفون أن النموذج لا يغشّ معتمدًا على أثر في البيانات؟"),
             L("We do not know it for certain, and that is exactly why GradCAM is in the product "
               "rather than in an appendix. If the heat consistently landed on borders, text overlays "
               "or scanner artifacts instead of the lesion, we would see it immediately. It is a "
               "qualitative check, not a proof — a proper proof needs evaluation on data from a "
               "different scanner and site.",
               "لا نعرف ذلك يقينًا، ولهذا بالضبط يوجد GradCAM في المنتج لا في ملحق. فلو استقرّت "
               "الحرارة باستمرار على الحدود أو النصوص المتراكبة أو تشويش الجهاز بدل الآفة لرأينا "
               "ذلك فورًا. وهو فحص نوعي لا برهان — والبرهان الصحيح يحتاج تقييمًا على بيانات من جهاز "
               "وموقع مختلفين.")],
            [L("99% on a public Kaggle dataset — so what?",
               "‏99% على مجموعة عامة من Kaggle — وماذا في ذلك؟"),
             L("Agreed, and we do not lead with it. Our headline claim is the explainability pipeline "
               "and the engineering, not the accuracy number. The accuracy is labelled 'claimed' "
               "precisely because we know a single-source benchmark proves very little about "
               "real-world generalization.",
               "متّفقون، ولا نصدّر به. فادّعاؤنا الرئيسي هو خط التفسير والهندسة، لا رقم الدقة. وقد "
               "وُصِف الرقم بأنه «مُعلَن» تحديدًا لأننا نعرف أن معيارًا من مصدر واحد لا يثبت شيئًا "
               "يُذكر عن التعميم في الواقع.")],
            [L("What is the false-negative rate for glioma specifically?",
               "ما معدّل السلبية الكاذبة للورم الدبقي تحديدًا؟"),
             L("We do not currently publish it, and we will not guess. train.py computes a confusion "
               "matrix and a per-class report, but the shipped model_log.csv does not contain them, "
               "so the API deliberately returns null instead of a fabricated matrix. Surfacing "
               "per-class recall is on the phase-1 roadmap, and clinically it matters far more than "
               "accuracy.",
               "لا ننشره حاليًا ولن نخمّنه. فـtrain.py يحسب مصفوفة التباس وتقريرًا لكل فئة، لكن "
               "model_log.csv المُسلَّم لا يحويهما، فيُعيد الـAPI عمدًا قيمة فارغة بدل مصفوفة مختلقة. "
               "وإظهار استدعاء كل فئة مدرَج في المرحلة الأولى من خارطة الطريق، وهو سريريًا أهمّ "
               "بكثير من الدقة.")],
            [L("Why is a 98 MB binary committed to git?",
               "لماذا أُودِع ملف ثنائي بحجم 98 ميغابايت في git؟"),
             L("For demo convenience — anyone who clones the repository can run it immediately with "
               "no download step. It is the wrong answer at production scale; a model registry "
               "(MLflow) or Git LFS is on the roadmap, together with versioned checkpoints so any "
               "past prediction can be reproduced.",
               "لأجل يُسر العرض — فمن يستنسخ المستودع يستطيع تشغيله فورًا بلا خطوة تنزيل. وهو الجواب "
               "الخاطئ على نطاق الإنتاج؛ وسجلّ النماذج (MLflow) أو Git LFS مدرَج في خارطة الطريق، مع "
               "نقاط تفتيش مُصدَّرة ليمكن إعادة إنتاج أي تنبؤ سابق.")],
            [L("There are no tests. Why should I trust this code?",
               "لا توجد اختبارات. لماذا أثق بهذه الشيفرة؟"),
             L("That is a fair criticism and we do not dispute it — no automated tests exist yet. "
               "What does exist is defensive design: strict checkpoint loading that refuses to "
               "half-load a head, server-side validation with real HTTP codes, an inference lock, and "
               "graceful degradation. Tests are the first item in the engineering roadmap, and the "
               "obvious first cases are the four upload error codes and the shape of predict_core's "
               "output.",
               "نقد عادل ولا نجادل فيه — فلا توجد اختبارات آلية بعد. والموجود هو تصميم دفاعي: تحميل "
               "صارم لملف الأوزان يرفض تحميل الرأس نصفيًا، وتحقّق على الخادم برموز HTTP حقيقية، وقفل "
               "استدلال، وتراجع آمن. والاختبارات هي البند الأول في خارطة الطريق الهندسية، وأوضح "
               "حالاتها الأولى رموز أخطاء الرفع الأربعة وشكل مخرَج predict_core.")],
            [L("Why does the LLM report matter if the model never sees the image?",
               "لماذا يهمّ تقرير النموذج اللغوي إن كان النموذج لا يرى الصورة أصلًا؟"),
             L("Because it is a communication layer, and we describe it as exactly that. It converts "
               "four numbers into structured clinical language a non-specialist can act on. It adds "
               "no diagnostic information and we never claim it does — anything else would be "
               "dishonest.",
               "لأنه طبقة تواصل، ونصفه بذلك بالضبط. فهو يحوّل أربعة أرقام إلى لغة سريرية منظَّمة "
               "يستطيع غير المختص التصرّف بناءً عليها. ولا يضيف معلومة تشخيصية ولا ندّعي ذلك أبدًا — "
               "وأي وصف آخر سيكون غير صادق.")],
            [L("A small quantized model writing medical text — can't it hallucinate?",
               "نموذج صغير مُكمَّم يكتب نصًّا طبيًا — ألا يمكن أن يهلوس؟"),
             L("Yes. We mitigate it with a low temperature (0.3), a rigid five-section template, a "
               "230-word ceiling, a system prompt that mandates a disclaimer, and by giving it "
               "nothing to invent from beyond the class and four probabilities. Mitigation is not "
               "elimination — which is why the report is framed as an explanation, never as advice, "
               "and why a larger medical model (meditron) can be swapped in through one environment "
               "variable.",
               "نعم. ونخفّف ذلك بحرارة منخفضة (0.3)، وقالب صارم من خمسة أقسام، وسقف 230 كلمة، وموجِّه "
               "نظام يفرض إخلاء مسؤولية، وبألا نعطيه ما يختلق منه سوى الفئة والاحتمالات الأربعة. "
               "والتخفيف ليس إزالة — ولهذا يُقدَّم التقرير بوصفه شرحًا لا نصيحة أبدًا، ولهذا يمكن "
               "استبدال نموذج طبي أكبر (meditron) عبر متغيّر بيئة واحد.")],
            [L("Why two front-ends? Isn't that duplicated code?",
               "لماذا واجهتان؟ أليس هذا تكرارًا للشيفرة؟"),
             L("The UI code is duplicated; the model code is not. Both front-ends import "
               "inference_core.py, which is the single source of truth for the architecture, the "
               "preprocessing and the class order. Gradio stays as a zero-setup fallback demo; the "
               "Next.js app is the product.",
               "شيفرة الواجهة مكرَّرة، أما شيفرة النموذج فلا. فكلتا الواجهتين تستوردان "
               "inference_core.py، وهو المصدر الوحيد للحقيقة في المعمارية والمعالجة المسبقة وترتيب "
               "الفئات. وتبقى Gradio عرضًا احتياطيًا بلا إعداد؛ وتطبيق Next.js هو المنتج.")],
            [L("What happens if two users upload at the same time?",
               "ماذا يحدث إن رفع مستخدمان في اللحظة نفسها؟"),
             L("They are serialized by INFERENCE_LOCK, because GradCAM registers backward hooks on "
               "the shared model object and two concurrent calls would interleave them. The heavy "
               "work runs in a threadpool so the async event loop stays responsive. It is correct but "
               "it is not horizontally scalable inside one process — the production answer is "
               "multiple workers or a dedicated inference server, which is on the roadmap.",
               "تُسلسَل بواسطة INFERENCE_LOCK، لأن GradCAM يسجّل خطّافات خلفية على كائن النموذج "
               "المشترك ونداءان متزامنان سيتداخلان. ويعمل الجزء الثقيل في مجمع خيوط فتبقى حلقة "
               "الأحداث اللاتزامنية مستجيبة. وهذا صحيح لكنه غير قابل للتوسّع أفقيًا داخل عملية "
               "واحدة — والجواب الإنتاجي عمّال متعددون أو خادم استدلال مخصّص، وهو مدرَج في خارطة "
               "الطريق.")],
            [L("Could I retrain this on my own hospital's data?",
               "هل أستطيع إعادة تدريب هذا على بيانات مستشفاي؟"),
             L("Yes — that is what train.py is for. Arrange the images in folders named glioma, "
               "meningioma, notumor and pituitary, then run it with --train_dir and --test_dir. Two "
               "warnings: keep the class index order identical, and note that train.py's head "
               "includes a BatchNorm the shipped checkpoint does not, so it produces a new, "
               "deliberately separate model rather than an update to the existing one.",
               "نعم — ولهذا وُجد train.py. رتّب الصور في مجلدات باسم glioma و meningioma و notumor و "
               "pituitary، ثم شغّله بـ--train_dir و--test_dir. مع تحذيرين: حافظ على ترتيب فهارس "
               "الفئات كما هو، ولاحظ أن رأس train.py يتضمّن BatchNorm لا يوجد في ملف الأوزان "
               "المُسلَّم، فينتج نموذجًا جديدًا منفصلًا عمدًا لا تحديثًا للقائم.")],
            [L("What is genuinely novel here?", "ما الجديد فعلًا هنا؟"),
             L("Not the classifier — fine-tuning ResNet50 on this dataset is a well-trodden exercise, "
               "and we would rather say so than pretend otherwise. What is uncommon is the "
               "combination shipped as one coherent product: classification, visual explanation and a "
               "fully local language-model report, behind a typed API, in a deployable container "
               "stack, with the system's own limitations published inside the API response. Most "
               "projects at this level ship one of those four.",
               "ليس المُصنِّف — فضبط ResNet50 على هذه المجموعة تمرين مطروق، ونفضّل قول ذلك على "
               "التظاهر بغيره. أما غير المألوف فهو التركيبة المُسلَّمة منتجًا واحدًا متماسكًا: "
               "تصنيف، وتفسير بصري، وتقرير بنموذج لغوي محلي بالكامل، خلف واجهة مُوصَّفة الأنواع، في "
               "حزمة حاويات قابلة للنشر، مع نشر حدود النظام داخل استجابة الـAPI نفسها. ومعظم "
               "المشاريع في هذا المستوى تُسلِّم واحدة من هذه الأربع.")],
        ]},
    ],
}

# ── S · FILE MAP ─────────────────────────────────────────────────────────
FILEMAP = {
    "id": "filemap",
    "title": L("Appendix — File-by-File Code Map", "ملحق — خريطة الشيفرة ملفًا ملفًا"),
    "lead": L(
        "Every file that matters, what it contains, and what depends on it.",
        "كل ملف ذي أهمية، وما يحويه، وما الذي يعتمد عليه."),
    "blocks": [
        {"type": "h", "text": L("Root — the model core", "الجذر — نواة النموذج")},
        {"type": "table",
         "head": [L("File", "الملف"), L("Contents", "المحتوى")],
         "rows": [
            [L("inference_core.py", "inference_core.py"),
             L("The single source of truth: CLASSES, CLASS_INFO, TRANSFORM, build_model(), "
               "pick_device(), load_model(), build_verdict(), predict_core(). Import-safe — importing "
               "it does not load the weights.",
               "المصدر الوحيد للحقيقة: CLASSES و CLASS_INFO و TRANSFORM و build_model() و "
               "pick_device() و load_model() و build_verdict() و predict_core(). وآمن عند "
               "الاستيراد — فاستيراده لا يحمّل الأوزان.")],
            [L("gradcam_utils.py", "gradcam_utils.py"),
             L("generate_gradcam() and gradcam_available(). Targets model.layer4[-1]; enables "
               "aug_smooth and eigen_smooth; falls back to the resized original if grad-cam is "
               "absent.",
               "‏generate_gradcam() و gradcam_available(). تستهدف model.layer4[-1]؛ وتفعّل aug_smooth "
               "و eigen_smooth؛ وتتراجع إلى الأصل المُحجَّم إن غاب grad-cam.")],
            [L("llm_report.py", "llm_report.py"),
             L("The system and user prompts, the Ollama call, _strip_code_fence(), current_model(), "
               "and llm_available() — which checks not only that the server responds but that the "
               "configured model is actually pulled.",
               "موجِّها النظام والمستخدم، ونداء Ollama، و _strip_code_fence()، و current_model()، و "
               "llm_available() — التي تتحقّق لا من استجابة الخادم فحسب بل من أن النموذج المُهيَّأ "
               "منزَّل فعلًا.")],
            [L("train.py", "train.py"),
             L("The improved training script: BrainTumorDataset, the augmentation pipeline, a head "
               "with BatchNorm1d(512), Adam + weight decay + label smoothing + ReduceLROnPlateau, "
               "early stopping, and the learning-curve and confusion-matrix plots.",
               "سكربت التدريب المحسَّن: BrainTumorDataset، وخط زيادة البيانات، ورأس فيه "
               "BatchNorm1d(512)، و Adam مع اضمحلال الوزن وتنعيم التسميات و ReduceLROnPlateau، "
               "وإيقاف مبكر، ورسما منحنيات التعلّم ومصفوفة الالتباس.")],
            [L("app.py", "app.py"),
             L("The legacy Gradio UI on port 7860. Still works standalone, but loads the weights at "
               "import time — which is precisely the fragility the FastAPI lifespan handler fixes.",
               "واجهة Gradio القديمة على المنفذ 7860. ما زالت تعمل مستقلة، لكنها تحمّل الأوزان عند "
               "الاستيراد — وهي بالضبط الهشاشة التي يعالجها معالج lifespan في FastAPI.")],
            [L("download_dataset.py", "download_dataset.py"),
             L("Fetches the Kaggle dataset via kagglehub — no API key file needed.",
               "يجلب مجموعة Kaggle عبر kagglehub — بلا حاجة إلى ملف مفتاح API.")],
            [L("model_class.pth · model_log.csv", "model_class.pth · model_log.csv"),
             L("The 98 MB trained weights and the 7-epoch training log.",
               "الأوزان المدرَّبة بحجم 98 ميغابايت وسجلّ التدريب لسبع حقب.")],
            [L("brain-tumor.ipynb", "brain-tumor.ipynb"),
             L("The original 2.8 MB TensorFlow/Keras notebook — the project's v0, kept as history.",
               "دفتر TensorFlow/Keras الأصلي بحجم 2.8 ميغابايت — النسخة صفر للمشروع، محفوظة "
               "للتاريخ.")],
        ]},
        {"type": "h", "text": L("backend/ — the API", "backend/ — واجهة البرمجة")},
        {"type": "table",
         "head": [L("File", "الملف"), L("Contents", "المحتوى")],
         "rows": [
            [L("main.py", "main.py"),
             L("The FastAPI app: the lifespan model loader, CORS, INFERENCE_LOCK, the 30-second "
               "Ollama availability cache, the uniform error envelope, and the four routes.",
               "تطبيق FastAPI: مُحمِّل النموذج في lifespan، و CORS، و INFERENCE_LOCK، وذاكرة توفّر "
               "Ollama المؤقتة لثلاثين ثانية، وغلاف الخطأ الموحَّد، والمسارات الأربعة.")],
            [L("schemas.py", "schemas.py"),
             L("The Pydantic wire contract: ClassProb, HealthResponse, PredictResponse, "
               "ReportRequest (with a validator that rejects unknown class names), ReportResponse, "
               "EpochRow, ClassMeta, MetricsResponse.",
               "عقد الشبكة بـPydantic: ClassProb و HealthResponse و PredictResponse و ReportRequest "
               "(مع مُتحقِّق يرفض أسماء الفئات المجهولة) و ReportResponse و EpochRow و ClassMeta و "
               "MetricsResponse.")],
            [L("imaging.py", "imaging.py"),
             L("MAX_UPLOAD_MB = 15, the MIME allow-list, ImageValidationError, load_upload_image() "
               "and numpy_to_data_url().",
               "‏MAX_UPLOAD_MB = 15، وقائمة سماح MIME، و ImageValidationError، و load_upload_image() "
               "و numpy_to_data_url().")],
            [L("metrics.py", "metrics.py"),
             L("Parses model_log.csv, computes the best validation accuracy, attaches the honest "
               "ACCURACY_CAVEAT, and returns null for the confusion matrix and per-class metrics "
               "rather than fabricating them.",
               "يحلّل model_log.csv، ويحسب أفضل دقة تحقق، ويرفق ACCURACY_CAVEAT الصادق، ويُعيد قيمة "
               "فارغة لمصفوفة الالتباس ومقاييس الفئات بدل اختلاقها.")],
        ]},
        {"type": "h", "text": L("Deployment and documentation", "النشر والتوثيق")},
        {"type": "table",
         "head": [L("File", "الملف"), L("Contents", "المحتوى")],
         "rows": [
            [L("Dockerfile.backend", "Dockerfile.backend"),
             L("python:3.12-slim, libgomp1 and libglib2.0-0, CPU-pinned torch 2.6.0 / torchvision "
               "0.21.0, and the opencv-headless swap that makes grad-cam importable in a slim image.",
               "‏python:3.12-slim، و libgomp1 و libglib2.0-0، و torch 2.6.0 مع torchvision 0.21.0 "
               "مثبَّتين للمعالج، واستبدال opencv بالنسخة بلا واجهة ليصير grad-cam قابلًا "
               "للاستيراد في صورة نحيلة.")],
            [L("docker-compose.yml", "docker-compose.yml"),
             L("Three services — backend (127.0.0.1:8110), frontend (127.0.0.1:3040), ollama "
               "(internal only) — with health checks, restart policies and Ollama memory tuning.",
               "ثلاث خدمات — الخادم ‏(127.0.0.1:8110)، والواجهة ‏(127.0.0.1:3040)، و Ollama (داخلية "
               "فقط) — مع فحوص صحة وسياسات إعادة تشغيل وضبط لذاكرة Ollama.")],
            [L("CLAUDE.md · frontend/AGENTS.md", "CLAUDE.md · frontend/AGENTS.md"),
             L("The project's hard rules for any contributor, human or AI: fixed class order, the "
               "intentional duplicate Dropout, the \"claimed accuracy\" framing, and the do-not-read "
               "list.",
               "قواعد المشروع الصارمة لأي مساهم، إنسانًا كان أو ذكاءً اصطناعيًا: ترتيب الفئات "
               "الثابت، وتكرار Dropout المقصود، وصياغة «الدقة المُعلَنة»، وقائمة «لا تُقرأ».")],
            [L("presentation/", "presentation/"),
             L("This documentation package. All text lives in one bilingual data structure "
               "(build/doc_data.py plus doc_x1–x3), rendered to HTML, DOCX, PPTX and PDF in both "
               "languages, so the English and Arabic editions can never drift apart.",
               "هذه الحزمة التوثيقية. ويعيش النص كله في بنية بيانات ثنائية اللغة واحدة "
               "(build/doc_data.py مع doc_x1 إلى x3)، تُعرَض إلى HTML و DOCX و PPTX و PDF باللغتين، "
               "فلا تتباعد النسختان الإنجليزية والعربية أبدًا.")],
        ]},
    ],
}
