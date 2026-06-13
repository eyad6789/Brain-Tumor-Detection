"use client";

import { motion } from "motion/react";

import type { ClassName } from "@/lib/types";
import { classColorVar, cn, formatPct } from "@/lib/utils";

export function ConfidenceBar({
  name,
  value,
  highlight,
  index,
}: {
  name: ClassName;
  value: number;
  highlight: boolean;
  index: number;
}) {
  const color = classColorVar(name);
  return (
    <div
      role="meter"
      aria-label={name}
      aria-valuenow={Math.round(value * 100)}
      aria-valuemin={0}
      aria-valuemax={100}
      className="space-y-1.5"
    >
      <div className="flex items-baseline justify-between">
        <span className="flex items-center gap-2 text-sm">
          <span className="h-2 w-2 rounded-full" style={{ backgroundColor: color }} />
          <span className={cn("font-medium", highlight ? "text-ink-strong" : "text-muted")}>
            {name}
          </span>
        </span>
        <span
          className={cn("data text-sm tabular-nums", highlight ? "text-ink-strong" : "text-muted")}
        >
          {formatPct(value)}
        </span>
      </div>
      <div className="h-2 overflow-hidden rounded-full bg-surface-3">
        <motion.div
          className="h-full rounded-full"
          style={{
            backgroundColor: color,
            opacity: highlight ? 1 : 0.5,
            boxShadow: highlight ? `0 0 14px ${color}` : "none",
          }}
          initial={{ width: 0 }}
          animate={{ width: `${Math.max(value * 100, 1.5)}%` }}
          transition={{ duration: 0.7, delay: 0.08 * index, ease: [0.16, 1, 0.3, 1] }}
        />
      </div>
    </div>
  );
}
