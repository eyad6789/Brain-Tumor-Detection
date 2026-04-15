"""
Brain Tumor Detection — Gradio UI
Upload an MRI image to classify it, visualize tumor regions via GradCAM,
and receive an AI-generated medical report.
"""

import os
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import gradio as gr

from gradcam_utils import generate_gradcam, gradcam_available
from llm_report import generate_medical_report, llm_available

# ─── Config ───────────────────────────────────────────────────────────────────
CLASSES = {0: "Pituitary", 1: "No Tumor", 2: "Meningioma", 3: "Glioma"}
MODEL_PATH = "model_class.pth"
IMG_SIZE = 224

CLASS_INFO = {
    "Pituitary":  "A pituitary tumor grows in the pituitary gland at the base of the brain. Most are benign (non-cancerous).",
    "No Tumor":   "No brain tumor was detected in this MRI scan.",
    "Meningioma": "A meningioma is a tumor that forms on the membranes (meninges) surrounding the brain and spinal cord.",
    "Glioma":     "A glioma is a tumor that originates in the glial cells of the brain. It can be benign or malignant.",
}

# ─── Model ────────────────────────────────────────────────────────────────────
def build_model():
    model = models.resnet50(weights=None)
    in_features = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Dropout(0.5),
        nn.Linear(in_features, 512),
        nn.ReLU(),
        nn.Dropout(0.3),
        nn.Dropout(0.3),
        nn.Linear(512, 4),
    )
    return model


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = build_model()
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Model file '{MODEL_PATH}' not found. "
        "Please run train.py first to train and save the model."
    )
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.to(device)
model.eval()

transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

# ─── Status banners ───────────────────────────────────────────────────────────
_gradcam_status = (
    "GradCAM heatmap enabled."
    if gradcam_available()
    else "GradCAM unavailable — run `pip install grad-cam` to enable heatmaps."
)
_llm_status = (
    "Meditron-7B report enabled (via Ollama)."
    if llm_available()
    else (
        "Meditron report unavailable — start Ollama: `ollama serve` "
        "and pull the model: `ollama pull meditron`."
    )
)


# ─── Inference ────────────────────────────────────────────────────────────────
def predict(image: Image.Image):
    if image is None:
        empty_msg = "Please upload an MRI image."
        return {}, empty_msg, None, empty_msg

    pil_rgb = image.convert("RGB")
    img_tensor = transform(pil_rgb).unsqueeze(0).to(device)

    with torch.no_grad():
        logits = model(img_tensor)
        probs  = torch.softmax(logits, dim=1).squeeze().cpu().tolist()

    label_probs = {CLASSES[i]: round(probs[i], 4) for i in range(4)}
    top_class   = max(label_probs, key=label_probs.get)
    top_conf    = label_probs[top_class]
    info        = CLASS_INFO[top_class]

    if top_class == "No Tumor":
        verdict = f"**Result: {top_class}** ({top_conf*100:.1f}% confidence)\n\n{info}"
    else:
        verdict = f"**Result: {top_class} Tumor Detected** ({top_conf*100:.1f}% confidence)\n\n{info}"

    # GradCAM overlay
    gradcam_img = generate_gradcam(model, img_tensor, pil_rgb)  # numpy (224,224,3)

    # LLM report
    llm_report = generate_medical_report(pil_rgb, top_class, label_probs)

    return label_probs, verdict, gradcam_img, llm_report


# ─── UI ───────────────────────────────────────────────────────────────────────
with gr.Blocks(title="Brain Tumor Detection") as demo:
    gr.Markdown(
        """
        # Brain Tumor Detection & Analysis
        Upload a brain MRI scan to classify it into one of four categories:
        **Glioma**, **Meningioma**, **Pituitary**, or **No Tumor**.

        > Model: ResNet50 fine-tuned on the Kaggle Brain Tumor MRI Dataset (~98.5% test accuracy)
        """
    )

    with gr.Row():
        # ── Left column: input ──────────────────────────────────────────────
        with gr.Column(scale=1):
            image_input = gr.Image(type="pil", label="Upload MRI Image")
            submit_btn  = gr.Button("Analyze", variant="primary")

        # ── Right column: results ───────────────────────────────────────────
        with gr.Column(scale=2):
            verdict_out = gr.Markdown(label="Diagnosis")
            probs_out   = gr.Label(num_top_classes=4, label="Confidence Scores")

            with gr.Row():
                original_out = gr.Image(
                    type="pil",
                    label="Original MRI",
                    height=224,
                )
                gradcam_out  = gr.Image(
                    type="numpy",
                    label="GradCAM — Tumor Region Heatmap",
                    height=224,
                )

            gr.Markdown(
                f"> **Status:** {_gradcam_status}  \n> {_llm_status}"
            )

            llm_out = gr.Markdown(label="AI Medical Report")

    def predict_with_original(image):
        label_probs, verdict, gradcam_img, llm_report = predict(image)
        return label_probs, verdict, image, gradcam_img, llm_report

    submit_btn.click(
        fn=predict_with_original,
        inputs=image_input,
        outputs=[probs_out, verdict_out, original_out, gradcam_out, llm_out],
    )
    image_input.change(
        fn=predict_with_original,
        inputs=image_input,
        outputs=[probs_out, verdict_out, original_out, gradcam_out, llm_out],
    )

    gr.Markdown(
        """
        ---
        **Disclaimer:** This tool is for educational and research purposes only.
        It is not a substitute for professional medical diagnosis.
        """
    )

if __name__ == "__main__":
    demo.launch(share=False, theme=gr.themes.Soft())
