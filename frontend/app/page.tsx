import Link from "next/link";
import { Activity, ArrowRight, FileText, Layers, Lock, ScanLine } from "lucide-react";

import { FeatureCard } from "@/components/marketing/FeatureCard";
import { HeroScan } from "@/components/marketing/HeroScan";
import { ClassCard } from "@/components/shared/ClassCard";
import { DisclaimerBanner } from "@/components/shared/DisclaimerBanner";
import { HealthPill } from "@/components/shared/HealthPill";
import { CLASS_ORDER } from "@/lib/types";

const FEATURES = [
  {
    icon: ScanLine,
    title: "ResNet50 classifier",
    description: "Fine-tuned to sort brain MRIs into four classes with calibrated per-class confidence.",
  },
  {
    icon: Activity,
    title: "GradCAM explainability",
    description: "A heatmap over layer4 shows the regions that drove each prediction — not a black box.",
  },
  {
    icon: FileText,
    title: "Local clinical report",
    description: "A local LLM drafts a structured report via Ollama. No API keys, fully offline.",
  },
  {
    icon: Lock,
    title: "100% private",
    description: "Inference, heatmaps, and reports all run locally. Your scans never leave the machine.",
  },
];

const STEPS = [
  { n: "01", title: "Upload", body: "Drop a brain MRI image into the workspace." },
  { n: "02", title: "Classify & explain", body: "Get a prediction, confidence bars, and a GradCAM heatmap." },
  { n: "03", title: "Report", body: "A local model drafts a structured, cautious clinical summary." },
];

export default function Home() {
  return (
    <div className="mx-auto max-w-6xl px-5 sm:px-8">
      {/* Hero */}
      <section className="grid items-center gap-10 py-14 lg:grid-cols-[1.1fr_0.9fr] lg:py-20">
        <div className="animate-fade-up">
          <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-line bg-surface-2/70 px-3 py-1 text-xs text-muted">
            <span className="data uppercase tracking-widest text-primary">Explainable AI</span>
            <span className="h-1 w-1 rounded-full bg-muted" />
            Brain MRI · 4 classes
          </div>
          <h1 className="font-display text-4xl font-semibold leading-[1.05] tracking-tight text-ink-strong sm:text-5xl lg:text-6xl">
            See the tumor.
            <br />
            <span className="text-gradient">And why the model thinks so.</span>
          </h1>
          <p className="mt-5 max-w-xl text-lg leading-relaxed text-muted">
            NeuroScan classifies brain MRI scans, highlights the regions behind each call with
            GradCAM, and drafts a local clinical report — an end-to-end, interpretable pipeline you
            can run entirely offline.
          </p>
          <div className="mt-7 flex flex-wrap items-center gap-3">
            <Link
              href="/analyze"
              className="group inline-flex items-center gap-2 rounded-xl bg-primary px-5 py-3 text-sm font-semibold text-bg transition-all hover:opacity-90 glow"
            >
              Analyze a scan
              <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
            </Link>
            <Link
              href="/about"
              className="inline-flex items-center gap-2 rounded-xl border border-line bg-surface px-5 py-3 text-sm font-semibold text-ink-strong transition-colors hover:border-primary"
            >
              How it works
            </Link>
            <HealthPill className="ml-1" />
          </div>
        </div>
        <div className="animate-fade-up [animation-delay:120ms]">
          <HeroScan />
        </div>
      </section>

      {/* Features */}
      <section className="py-10">
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {FEATURES.map((f) => (
            <FeatureCard key={f.title} {...f} />
          ))}
        </div>
      </section>

      {/* Class showcase */}
      <section className="py-12">
        <div className="mb-6 flex items-end justify-between gap-4">
          <div>
            <p className="eyebrow mb-2">Detected classes</p>
            <h2 className="font-display text-2xl font-semibold tracking-tight text-ink-strong sm:text-3xl">
              Four findings, one scan
            </h2>
          </div>
          <Layers className="hidden h-8 w-8 text-muted sm:block" />
        </div>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {CLASS_ORDER.map((name) => (
            <ClassCard key={name} name={name} />
          ))}
        </div>
      </section>

      {/* How it works */}
      <section className="py-12">
        <p className="eyebrow mb-2">Workflow</p>
        <h2 className="mb-8 font-display text-2xl font-semibold tracking-tight text-ink-strong sm:text-3xl">
          Three steps, fully local
        </h2>
        <div className="grid gap-4 md:grid-cols-3">
          {STEPS.map((s) => (
            <div key={s.n} className="panel relative overflow-hidden p-6">
              <span className="data text-3xl font-semibold text-primary/30">{s.n}</span>
              <h3 className="mt-2 font-display text-lg font-semibold tracking-tight text-ink-strong">
                {s.title}
              </h3>
              <p className="mt-1.5 text-sm leading-relaxed text-muted">{s.body}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Closing CTA + disclaimer */}
      <section className="py-12">
        <div className="panel grain relative overflow-hidden p-8 text-center sm:p-12">
          <h2 className="font-display text-3xl font-semibold tracking-tight text-ink-strong">
            Ready to analyze a scan?
          </h2>
          <p className="mx-auto mt-2 max-w-md text-muted">
            Upload an MRI and get an interpretable result in seconds.
          </p>
          <Link
            href="/analyze"
            className="mt-6 inline-flex items-center gap-2 rounded-xl bg-ink-strong px-6 py-3 text-sm font-semibold text-bg transition-opacity hover:opacity-90"
          >
            Open the workspace <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
        <div className="mt-6">
          <DisclaimerBanner variant="callout" />
        </div>
      </section>
    </div>
  );
}
