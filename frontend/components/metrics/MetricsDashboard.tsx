"use client";

import { TriangleAlert } from "lucide-react";
import { useEffect, useState } from "react";

import { ConfusionMatrix } from "@/components/metrics/ConfusionMatrix";
import { LearningCurves } from "@/components/metrics/LearningCurves";
import { PerClassTable } from "@/components/metrics/PerClassTable";
import { StatCard } from "@/components/metrics/StatCard";
import { getMetrics } from "@/lib/api";
import type { AsyncState, ClassName, MetricsInfo } from "@/lib/types";
import { formatPct } from "@/lib/utils";

export function MetricsDashboard() {
  const [state, setState] = useState<AsyncState<MetricsInfo>>({ status: "loading" });

  useEffect(() => {
    const ctrl = new AbortController();
    getMetrics(ctrl.signal)
      .then((data) => setState({ status: "success", data }))
      .catch((e) => {
        if (!ctrl.signal.aborted)
          setState({ status: "error", message: e?.message ?? "Failed to load metrics." });
      });
    return () => ctrl.abort();
  }, []);

  if (state.status === "loading") {
    return (
      <div className="space-y-6">
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {[0, 1, 2, 3].map((i) => (
            <div key={i} className="panel p-5">
              <div className="skeleton h-3 w-20" />
              <div className="skeleton mt-3 h-8 w-24" />
            </div>
          ))}
        </div>
        <div className="skeleton h-64 w-full rounded-2xl" />
      </div>
    );
  }

  if (state.status === "error") {
    return (
      <div className="panel p-6">
        <p className="font-semibold text-glioma">Couldn&apos;t load metrics</p>
        <p className="mt-1 text-sm text-muted">{state.message}</p>
        <p className="mt-2 text-xs text-muted">Make sure the API server is running.</p>
      </div>
    );
  }

  if (state.status !== "success") return null;

  const m = state.data;
  const last = m.epochs[m.epochs.length - 1];
  const labels = m.classes.map((c) => c.name as ClassName);

  return (
    <div className="space-y-6">
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          label="Claimed accuracy"
          value={formatPct(m.claimedAccuracy, 2)}
          sub="best validation epoch"
          caveat={m.accuracyCaveat}
          accent
        />
        <StatCard label="Epochs trained" value={String(m.epochs.length)} sub="early-stopped" />
        <StatCard
          label="Final train acc"
          value={last?.trainAcc != null ? formatPct(last.trainAcc, 1) : "—"}
        />
        <StatCard
          label="Final val loss"
          value={last?.valLoss != null ? last.valLoss.toFixed(3) : "—"}
        />
      </div>

      <div className="flex items-start gap-3 rounded-2xl border border-alert/30 bg-alert/8 p-4">
        <TriangleAlert className="mt-0.5 h-4 w-4 shrink-0 text-alert" />
        <p className="text-sm leading-relaxed text-ink">
          <span className="font-semibold text-alert">Methodology note.</span> {m.accuracyCaveat}
        </p>
      </div>

      <LearningCurves epochs={m.epochs} />

      <div className="grid gap-6 lg:grid-cols-2">
        <ConfusionMatrix matrix={m.confusionMatrix} labels={labels} />
        <PerClassTable classes={m.classes} />
      </div>
    </div>
  );
}
