import type { Metadata } from "next";

import { AnalyzeWorkspace } from "@/components/analyze/AnalyzeWorkspace";
import { PageHeader } from "@/components/shared/PageHeader";

export const metadata: Metadata = {
  title: "Analyze — NeuroScan",
  description: "Upload a brain MRI to classify it, view a GradCAM heatmap, and get a local report.",
};

export default function AnalyzePage() {
  return (
    <div className="mx-auto max-w-6xl px-5 py-10 sm:px-8">
      <PageHeader
        eyebrow="Workspace"
        title="Analyze an MRI scan"
        subtitle="Upload a brain MRI. The classifier returns a prediction with per-class confidence, a GradCAM heatmap of where it looked, and a locally-generated clinical report."
      />
      <AnalyzeWorkspace />
    </div>
  );
}
