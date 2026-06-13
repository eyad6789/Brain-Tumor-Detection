import type { Metadata } from "next";

import { MetricsDashboard } from "@/components/metrics/MetricsDashboard";
import { PageHeader } from "@/components/shared/PageHeader";

export const metadata: Metadata = {
  title: "Metrics — NeuroScan",
  description: "Training metrics and model performance for the brain-tumor classifier.",
};

export default function MetricsPage() {
  return (
    <div className="mx-auto max-w-6xl px-5 py-10 sm:px-8">
      <PageHeader
        eyebrow="Model performance"
        title="Training metrics"
        subtitle="Per-epoch learning curves and class metadata from the model's training log. Accuracy figures are reported honestly as 'claimed', with the known methodology caveat."
      />
      <MetricsDashboard />
    </div>
  );
}
