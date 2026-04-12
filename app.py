"""
Brain Tumor Detection — Gradio UI
Upload an MRI image to classify it into one of 4 categories.
"""

import os
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import gradio as gr

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


# ─── Inference ────────────────────────────────────────────────────────────────
def predict(image: Image.Image):
    if image is None:
        return {}, "Please upload an MRI image."

    img_tensor = transform(image.convert("RGB")).unsqueeze(0).to(device)

    with torch.no_grad():
        logits = model(img_tensor)
        probs  = torch.softmax(logits, dim=1).squeeze().cpu().tolist()

    label_probs = {CLASSES[i]: round(probs[i], 4) for i in range(4)}

    top_class = max(label_probs, key=label_probs.get)
    top_conf  = label_probs[top_class]
    info      = CLASS_INFO[top_class]

    if top_class == "No Tumor":
        verdict = f"**Result: {top_class}** ({top_conf*100:.1f}% confidence)\n\n{info}"
    else:
        verdict = f"**Result: {top_class} Tumor Detected** ({top_conf*100:.1f}% confidence)\n\n{info}"

    return label_probs, verdict


# ─── UI ───────────────────────────────────────────────────────────────────────
with gr.Blocks(title="Brain Tumor Detection") as demo:
    gr.Markdown(
        """
        # Brain Tumor Detection
        Upload a brain MRI scan to classify it into one of four categories:
        **Glioma**, **Meningioma**, **Pituitary**, or **No Tumor**.

        > Model: ResNet50 fine-tuned on the Kaggle Brain Tumor MRI Dataset (~98.5% test accuracy)
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            image_input = gr.Image(type="pil", label="Upload MRI Image")
            submit_btn  = gr.Button("Analyze", variant="primary")
            gr.Examples(
                examples=[],
                inputs=image_input,
            )

        with gr.Column(scale=1):
            verdict_out = gr.Markdown(label="Diagnosis")
            probs_out   = gr.Label(num_top_classes=4, label="Confidence Scores")

    submit_btn.click(
        fn=predict,
        inputs=image_input,
        outputs=[probs_out, verdict_out],
    )
    image_input.change(
        fn=predict,
        inputs=image_input,
        outputs=[probs_out, verdict_out],
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
