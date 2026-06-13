import type { ClassName } from "./types";

// Static per-class copy (mirrors CLASS_INFO in app.py / inference_core.py) so the
// hero and about pages can render it without a network round-trip. The live
// /analyze + /metrics flows use the values returned by the API.
export const CLASS_META: Record<
  ClassName,
  { blurb: string; token: string; tone: "safe" | "alert" }
> = {
  Glioma: {
    blurb:
      "Originates in the glial cells of the brain. Can be benign or malignant; gliomas span a wide range of WHO grades.",
    token: "glioma",
    tone: "alert",
  },
  Meningioma: {
    blurb:
      "Forms on the meninges — the membranes surrounding the brain and spinal cord. Most are slow-growing and benign.",
    token: "meningioma",
    tone: "alert",
  },
  Pituitary: {
    blurb:
      "Grows in the pituitary gland at the base of the brain. The majority are benign (non-cancerous) adenomas.",
    token: "pituitary",
    tone: "alert",
  },
  "No Tumor": {
    blurb: "No brain tumor was detected in this MRI scan by the classifier.",
    token: "notumor",
    tone: "safe",
  },
};

export const DISCLAIMER_SHORT =
  "Educational & research use only — not a medical device and not a substitute for professional diagnosis.";

export const DISCLAIMER_LONG =
  "NeuroScan is an educational and research prototype. Its predictions, heatmaps, and generated reports are produced by an experimental model and must never be used for diagnosis or treatment decisions. Always consult a licensed radiologist or neurologist.";
