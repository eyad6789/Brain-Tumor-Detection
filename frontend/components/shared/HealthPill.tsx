"use client";

import { useEffect, useState } from "react";

import { getHealth } from "@/lib/api";
import type { HealthInfo } from "@/lib/types";
import { cn } from "@/lib/utils";

type State =
  | { kind: "loading" }
  | { kind: "ok"; health: HealthInfo }
  | { kind: "degraded"; health: HealthInfo }
  | { kind: "offline" };

export function useHealth(): State {
  const [state, setState] = useState<State>({ kind: "loading" });

  useEffect(() => {
    const ctrl = new AbortController();
    getHealth(ctrl.signal)
      .then((health) =>
        setState({ kind: health.modelLoaded ? "ok" : "degraded", health }),
      )
      .catch(() => {
        if (!ctrl.signal.aborted) setState({ kind: "offline" });
      });
    return () => ctrl.abort();
  }, []);

  return state;
}

const TONE: Record<string, { dot: string; label: string; pulse: boolean }> = {
  loading: { dot: "bg-muted", label: "Connecting…", pulse: true },
  ok: { dot: "bg-safe", label: "Model online", pulse: true },
  degraded: { dot: "bg-alert", label: "Model unavailable", pulse: false },
  offline: { dot: "bg-glioma", label: "API offline", pulse: false },
};

export function HealthPill({ className }: { className?: string }) {
  const state = useHealth();
  const tone = TONE[state.kind];
  const device =
    state.kind === "ok" || state.kind === "degraded" ? state.health.device : null;

  return (
    <span
      className={cn(
        "inline-flex items-center gap-2 rounded-full border border-line bg-surface-2/70 px-3 py-1 text-xs font-medium text-ink",
        className,
      )}
      role="status"
      aria-live="polite"
    >
      <span className="relative flex h-2 w-2">
        {tone.pulse && (
          <span className={cn("absolute inline-flex h-full w-full animate-ping rounded-full opacity-60", tone.dot)} />
        )}
        <span className={cn("relative inline-flex h-2 w-2 rounded-full", tone.dot)} />
      </span>
      {tone.label}
      {device && (
        <span className="data ml-0.5 rounded bg-surface-3 px-1.5 py-0.5 text-[0.65rem] uppercase text-muted">
          {device}
        </span>
      )}
    </span>
  );
}
