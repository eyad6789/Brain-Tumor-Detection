import type { Metadata } from "next";
import { Activity, FileText, Layers, ScanLine, TriangleAlert } from "lucide-react";

import { DisclaimerBanner } from "@/components/shared/DisclaimerBanner";
import { PageHeader } from "@/components/shared/PageHeader";

export const metadata: Metadata = {
  title: "About — NeuroScan",
  description: "How the brain-tumor classifier, GradCAM heatmaps, and local report work — and its limitations.",
};

const PIPELINE = ["Resize 224²", "ToTensor", "Normalize (ImageNet)", "ResNet50", "Softmax · 4"];

export default function AboutPage() {
  return (
    <div className="mx-auto max-w-4xl px-5 py-10 sm:px-8">
      <PageHeader
        eyebrow="Under the hood"
        title="How NeuroScan works"
        subtitle="An interpretable pipeline: a fine-tuned CNN for classification, GradCAM for visual explanation, and a local language model for a plain-language report."
      />

      <div className="space-y-6">
        <Section
          icon={ScanLine}
          title="The model"
          body="A ResNet50 pretrained on ImageNet, fine-tuned on the Kaggle Brain Tumor MRI dataset. Early convolutional blocks are frozen; the deeper blocks and a custom classifier head are trained to separate four classes. Inputs are resized to 224×224 and normalized with ImageNet statistics before a softmax produces per-class probabilities."
        >
          <div className="mt-4 flex flex-wrap items-center gap-2">
            {PIPELINE.map((step, i) => (
              <span key={step} className="flex items-center gap-2">
                <span className="data rounded-lg border border-line bg-surface-2 px-2.5 py-1 text-xs text-ink">
                  {step}
                </span>
                {i < PIPELINE.length - 1 && <span className="text-muted">→</span>}
              </span>
            ))}
          </div>
        </Section>

        <Section
          icon={Activity}
          title="GradCAM explainability"
          body="Gradient-weighted Class Activation Mapping inspects the final convolutional block (layer4) to produce a heatmap of the regions most responsible for the prediction. Warmer areas are where the model focused. Augmentation- and eigen-smoothing reduce noise. Treat the heatmap as a window into the model's attention — it is not a clinical segmentation of the tumor."
        />

        <Section
          icon={FileText}
          title="The local clinical report"
          body="When Ollama is running with a local language model (qwen2.5:3b by default; configurable via OLLAMA_MODEL), NeuroScan drafts a structured report — diagnosis summary, condition background, heatmap interpretation, next steps, and a disclaimer. It runs fully offline with no API keys. The model is text-only — it reasons over the classification and confidences, not the pixels. If Ollama isn't available, the rest of the app keeps working and the report panel shows setup instructions."
        />

        <Section
          icon={Layers}
          title="The four classes"
          body="Pituitary, No Tumor, Meningioma, and Glioma — in a fixed index order used consistently across the model, the API, and this UI."
        />

        {/* Limitations / honesty */}
        <div className="panel border-alert/30 p-6">
          <div className="flex items-center gap-2.5">
            <span className="grid h-9 w-9 place-items-center rounded-xl border border-alert/30 bg-alert/10 text-alert">
              <TriangleAlert className="h-4.5 w-4.5" />
            </span>
            <h2 className="font-display text-xl font-semibold tracking-tight text-ink-strong">
              Limitations &amp; honesty
            </h2>
          </div>
          <ul className="mt-4 space-y-3 text-sm leading-relaxed text-ink">
            <li className="flex gap-2.5">
              <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-alert" />
              The headline accuracy is reported as <strong>claimed</strong>, not validated. In the
              original training run the test set was reused for validation/early-stopping, which
              leaks information and makes the figure optimistic.
            </li>
            <li className="flex gap-2.5">
              <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-alert" />
              The model was trained on a specific public dataset and may not generalize to scans from
              other scanners, sequences, or populations.
            </li>
            <li className="flex gap-2.5">
              <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-alert" />
              This is a research and educational prototype — <strong>not a medical device</strong> and
              not validated for clinical use.
            </li>
          </ul>
        </div>

        <DisclaimerBanner variant="callout" />
      </div>
    </div>
  );
}

function Section({
  icon: Icon,
  title,
  body,
  children,
}: {
  icon: React.ComponentType<{ className?: string }>;
  title: string;
  body: string;
  children?: React.ReactNode;
}) {
  return (
    <section className="panel p-6">
      <div className="flex items-center gap-2.5">
        <span className="grid h-9 w-9 place-items-center rounded-xl border border-line bg-surface-2 text-primary">
          <Icon className="h-4.5 w-4.5" />
        </span>
        <h2 className="font-display text-xl font-semibold tracking-tight text-ink-strong">{title}</h2>
      </div>
      <p className="mt-3 text-sm leading-relaxed text-muted">{body}</p>
      {children}
    </section>
  );
}
