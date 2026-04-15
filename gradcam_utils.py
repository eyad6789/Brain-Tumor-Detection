"""
GradCAM Visualization Utility
Generates heatmap overlays showing which regions of an MRI
the ResNet50 model focuses on when making a prediction.

Requires: pip install grad-cam
"""

import numpy as np
from PIL import Image

try:
    from pytorch_grad_cam import GradCAM
    from pytorch_grad_cam.utils.image import show_cam_on_image
    GRADCAM_AVAILABLE = True
except ImportError:
    GRADCAM_AVAILABLE = False


def generate_gradcam(model, image_tensor, original_pil_image):
    """
    Generate a GradCAM heatmap overlay on the original MRI image.

    Args:
        model:             PyTorch ResNet50 model (eval mode)
        image_tensor:      (1, 3, 224, 224) tensor, normalized, on CPU/GPU
        original_pil_image: PIL Image (original, before normalization)

    Returns:
        numpy array (224, 224, 3) uint8 — heatmap blended on MRI,
        or the original image as numpy if grad-cam is not installed.
    """
    if not GRADCAM_AVAILABLE:
        # Fallback: return the original image resized to 224x224
        img = original_pil_image.convert("RGB").resize((224, 224))
        return np.array(img)

    target_layers = [model.layer4[-1]]

    # GradCAM context manager handles hook registration and cleanup
    with GradCAM(model=model, target_layers=target_layers) as cam:
        # targets=None → auto-select the highest-scoring class
        grayscale_cam = cam(
            input_tensor=image_tensor,
            targets=None,
            aug_smooth=True,       # averages across augmented copies for stability
            eigen_smooth=True,     # uses first principal component to reduce noise
        )

    # grayscale_cam shape: (batch, H, W) — take first item
    grayscale_cam = grayscale_cam[0]

    # Prepare the original image as float32 RGB [0,1] at 224×224
    rgb_img = np.array(
        original_pil_image.convert("RGB").resize((224, 224)),
        dtype=np.float32
    ) / 255.0

    # Blend heatmap with original image
    visualization = show_cam_on_image(rgb_img, grayscale_cam, use_rgb=True)
    return visualization  # (224, 224, 3) uint8


def gradcam_available():
    """Return True if pytorch-grad-cam is installed."""
    return GRADCAM_AVAILABLE
