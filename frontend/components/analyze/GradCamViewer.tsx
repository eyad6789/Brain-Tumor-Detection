"use client";

import { Columns2, Layers, Info } from "lucide-react";
import { useState } from "react";

import { Ticks } from "@/components/shared/Ticks";
import type { PredictResult } from "@/lib/types";
import { cn } from "@/lib/utils";

type Mode = "split" | "overlay";

export function GradCamViewer({
  originalUrl,
  result,
}: {
  originalUrl: string | null;
  result: PredictResult;
}) {
  const [mode, setMode] = useState<Mode>("split");
  const [opacity, setOpacity] = useState(0.6);

  const hasHeatmap = result.gradcamIsHeatmap && result.gradcamDataUrl;

  return (
    <div className="panel p-5">
      <div className="mb-4 flex items-center justify-between gap-3">
        <div>
          <p className="eyebrow">Explainability</p>
          <h3 className="font-display text-lg font-semibold tracking-tight text-ink-strong">
            GradCAM heatmap
          </h3>
        </div>
        {hasHeatmap && (
          <div className="flex rounded-lg border border-line bg-surface-2 p-0.5">
            <ModeButton active={mode === "split"} onClick={() => setMode("split")} icon={<Columns2 className="h-4 w-4" />} label="Split" />
            <ModeButton active={mode === "overlay"} onClick={() => setMode("overlay")} icon={<Layers className="h-4 w-4" />} label="Overlay" />
          </div>
        )}
      </div>

      {!hasHeatmap ? (
        <div className="space-y-3">
          <Frame label="Original">
            {originalUrl && (
              // eslint-disable-next-line @next/next/no-img-element
              <img src={originalUrl} alt="MRI scan" className="h-full w-full object-contain" />
            )}
          </Frame>
          <p className="flex items-start gap-2 rounded-lg border border-line bg-surface-2 px-3 py-2 text-xs text-muted">
            <Info className="mt-0.5 h-3.5 w-3.5 shrink-0 text-primary" />
            Heatmap unavailable — install <code className="data">grad-cam</code> on the server to enable tumor-region visualization.
          </p>
        </div>
      ) : mode === "split" ? (
        <div className="grid grid-cols-2 gap-3">
          <Frame label="Original">
            {originalUrl && (
              // eslint-disable-next-line @next/next/no-img-element
              <img src={originalUrl} alt="MRI scan" className="h-full w-full object-contain" />
            )}
          </Frame>
          <Frame label="Heatmap" glow>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src={result.gradcamDataUrl!} alt="GradCAM heatmap" className="h-full w-full object-contain" />
          </Frame>
        </div>
      ) : (
        <div className="space-y-3">
          <Frame label={`Overlay · ${Math.round(opacity * 100)}%`} glow>
            {originalUrl && (
              // eslint-disable-next-line @next/next/no-img-element
              <img src={originalUrl} alt="MRI scan" className="absolute inset-0 h-full w-full object-contain" />
            )}
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={result.gradcamDataUrl!}
              alt="GradCAM heatmap overlay"
              className="absolute inset-0 h-full w-full object-contain mix-blend-screen"
              style={{ opacity }}
            />
          </Frame>
          <label className="flex items-center gap-3 text-xs text-muted">
            <span className="data uppercase">Opacity</span>
            <input
              type="range"
              min={0}
              max={1}
              step={0.05}
              value={opacity}
              onChange={(e) => setOpacity(Number(e.target.value))}
              className="h-1.5 flex-1 cursor-pointer appearance-none rounded-full bg-surface-3 accent-[var(--color-primary)]"
              aria-label="Heatmap overlay opacity"
            />
          </label>
        </div>
      )}

      <p className="mt-3 text-xs leading-relaxed text-muted">
        Warm regions show where the model focused (GradCAM on <code className="data">layer4</code>). This indicates attention, not a clinical segmentation.
      </p>
    </div>
  );
}

function ModeButton({
  active,
  onClick,
  icon,
  label,
}: {
  active: boolean;
  onClick: () => void;
  icon: React.ReactNode;
  label: string;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={cn(
        "inline-flex items-center gap-1.5 rounded-md px-2.5 py-1.5 text-xs font-medium transition-colors",
        active ? "bg-surface text-ink-strong shadow-sm" : "text-muted hover:text-ink-strong",
      )}
    >
      {icon}
      {label}
    </button>
  );
}

function Frame({
  label,
  glow,
  children,
}: {
  label: string;
  glow?: boolean;
  children: React.ReactNode;
}) {
  return (
    <figure className="space-y-1.5">
      <div
        className={cn(
          "relative aspect-square overflow-hidden rounded-xl border border-line bg-black/40",
          glow && "glow",
        )}
      >
        <Ticks />
        {children}
      </div>
      <figcaption className="data text-center text-[0.65rem] uppercase tracking-widest text-muted">
        {label}
      </figcaption>
    </figure>
  );
}
