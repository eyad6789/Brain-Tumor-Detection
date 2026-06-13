"""Image upload validation and numpy -> base64 PNG data-URL encoding."""

import base64
import io

import numpy as np
from PIL import Image, UnidentifiedImageError

MAX_UPLOAD_MB = 15
MAX_UPLOAD_BYTES = MAX_UPLOAD_MB * 1024 * 1024
ALLOWED_CONTENT_TYPES = {
    "image/png", "image/jpeg", "image/jpg", "image/webp", "image/bmp",
}


class ImageValidationError(Exception):
    """Raised when an uploaded file is too large or not a decodable image."""

    def __init__(self, code: str, message: str, status: int):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status


def load_upload_image(raw: bytes, content_type: str | None) -> Image.Image:
    """Validate raw upload bytes and return a decoded RGB PIL image.

    Raises ImageValidationError (413 / 415 / 422) on bad input.
    """
    if len(raw) == 0:
        raise ImageValidationError("empty_file", "Uploaded file is empty.", 422)
    if len(raw) > MAX_UPLOAD_BYTES:
        raise ImageValidationError(
            "file_too_large", f"File exceeds the {MAX_UPLOAD_MB} MB limit.", 413
        )
    if content_type and content_type.lower() not in ALLOWED_CONTENT_TYPES:
        raise ImageValidationError(
            "unsupported_type",
            f"Unsupported content type '{content_type}'. Upload a PNG/JPEG/WEBP/BMP image.",
            415,
        )

    # Verify it really is an image, then reopen (verify() leaves the file unusable).
    try:
        Image.open(io.BytesIO(raw)).verify()
        img = Image.open(io.BytesIO(raw))
        return img.convert("RGB")
    except (UnidentifiedImageError, OSError, ValueError):
        raise ImageValidationError(
            "invalid_image", "Could not decode the uploaded file as an image.", 422
        )


def numpy_to_data_url(arr: np.ndarray) -> str:
    """Encode an (H,W,3) uint8 array as a base64 PNG data URL."""
    img = Image.fromarray(np.asarray(arr, dtype="uint8"), "RGB")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64}"
