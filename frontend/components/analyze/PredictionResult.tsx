"use client";

import { motion } from "motion/react";
import { CircleCheck, RotateCw, TriangleAlert } from "lucide-react";

import { ConfidenceBar } from "@/components/analyze/ConfidenceBar";
import { Ticks } from "@/components/shared/Ticks";
import { CLASS_META } from "@/lib/constants";
import type { AsyncState, PredictResult } from "@/lib/types";
import { cn, formatPct } from "@/lib/utils";

export function PredictionResult({
  state,
  onRetry,
}: {
  state: AsyncState<PredictResult>;
  onRetry: () => void;
}) {
  if (state.status === "loading") {
    return (
      <div className="panel relative space-y-4 p-5">
        <div className="skeleton h-7 w-2/3" />
        <div className="space-y-3 pt-2">
          {[0, 1, 2, 3].map((i) => (
            <div key={i} className="space-y-1.5">
              <div className="skeleton h-3 w-24" />
              <div className="skeleton h-2 w-full" />
            </div>
          ))}
        </div>
        <p className="data text-xs text-muted">Running inference…</p>
      </div>
    );
  }

  if (state.status === "error") {
    return (
      <div className="panel space-y-3 p-5">
        <p className="font-semibold text-glioma">Analysis failed</p>
        <p className="text-sm text-muted">{state.message}</p>
        <button
          type="button"
          onClick={onRetry}
          className="inline-flex items-center gap-2 rounded-lg border border-line bg-surface-2 px-3 py-2 text-sm font-medium text-ink-strong transition-colors hover:border-primary"
        >
          <RotateCw className="h-4 w-4" /> Retry
        </button>
      </div>
    );
  }

  if (state.status !== "success") return null;

  const result = state.data;
  const safe = result.topClass === "No Tumor";
  const meta = CLASS_META[result.topClass];
  const ordered = [...result.classes].sort((a, b) => b.confidence - a.confidence);

  return (
    <motion.div
      initial={{ opacity: 0, y: 14 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
      className="panel relative overflow-hidden p-5"
      aria-live="polite"
    >
      <Ticks />
      <div className="flex items-start gap-4">
        <span
          className={cn(
            "grid h-12 w-12 shrink-0 place-items-center rounded-xl border",
            safe ? "border-safe/30 bg-safe/10 text-safe" : "border-alert/30 bg-alert/10 text-alert",
          )}
        >
          {safe ? <CircleCheck className="h-6 w-6" /> : <TriangleAlert className="h-6 w-6" />}
        </span>
        <div className="min-w-0 flex-1">
          <p className="eyebrow">Primary finding</p>
          <h3 className="font-display text-2xl font-semibold tracking-tight text-ink-strong">
            {safe ? "No Tumor Detected" : `${result.topClass} Detected`}
          </h3>
          <p className="mt-1 text-sm leading-relaxed text-muted">{meta.blurb}</p>
        </div>
        <div className="shrink-0 text-right">
          <p className="eyebrow">Confidence</p>
          <p className={cn("data text-2xl font-semibold tabular-nums", safe ? "text-safe" : "text-alert")}>
            {formatPct(result.confidence)}
          </p>
        </div>
      </div>

      <div className="mt-5 space-y-3 border-t border-line pt-4">
        {ordered.map((c, i) => (
          <ConfidenceBar
            key={c.name}
            name={c.name}
            value={c.confidence}
            highlight={c.name === result.topClass}
            index={i}
          />
        ))}
      </div>
    </motion.div>
  );
}
