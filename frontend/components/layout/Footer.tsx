import Link from "next/link";
import { Cpu, Lock } from "lucide-react";

import { Logo } from "@/components/shared/Logo";
import { DISCLAIMER_SHORT } from "@/lib/constants";

export function Footer() {
  return (
    <footer className="mt-24 border-t border-line bg-surface/40">
      <div className="mx-auto grid max-w-6xl gap-10 px-5 py-12 sm:px-8 md:grid-cols-[1.4fr_1fr_1fr]">
        <div>
          <div className="flex items-center gap-2.5 text-ink-strong">
            <Logo />
            <span className="font-display text-lg font-semibold tracking-tight">NeuroScan</span>
          </div>
          <p className="mt-3 max-w-xs text-sm leading-relaxed text-muted">
            An explainable brain-tumor MRI classifier — ResNet50, GradCAM heatmaps, and
            local clinical reports. {DISCLAIMER_SHORT}
          </p>
        </div>

        <div>
          <p className="eyebrow mb-3">Pipeline</p>
          <ul className="space-y-2 text-sm text-muted">
            <li>ResNet50 · 4-class</li>
            <li>GradCAM · layer4</li>
            <li>Local LLM report</li>
          </ul>
        </div>

        <div>
          <p className="eyebrow mb-3">Navigate</p>
          <ul className="space-y-2 text-sm text-muted">
            <li><Link href="/analyze" className="transition-colors hover:text-primary">Analyze a scan</Link></li>
            <li><Link href="/metrics" className="transition-colors hover:text-primary">Model metrics</Link></li>
            <li><Link href="/about" className="transition-colors hover:text-primary">How it works</Link></li>
          </ul>
        </div>
      </div>

      <div className="border-t border-line">
        <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-3 px-5 py-4 text-xs text-muted sm:flex-row sm:px-8">
          <p>© {new Date().getFullYear()} NeuroScan · Educational & research prototype</p>
          <div className="flex items-center gap-4">
            <span className="inline-flex items-center gap-1.5">
              <Lock className="h-3.5 w-3.5" /> Runs 100% locally
            </span>
            <span className="inline-flex items-center gap-1.5">
              <Cpu className="h-3.5 w-3.5" /> PyTorch · FastAPI
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
}
