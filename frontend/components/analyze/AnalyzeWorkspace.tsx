"use client";

import { motion } from "motion/react";
import { Crosshair, ScanLine, Loader2, Activity, FileText } from "lucide-react";
import { useCallback, useEffect, useRef, useState } from "react";

import { GradCamViewer } from "@/components/analyze/GradCamViewer";
import { PredictionResult } from "@/components/analyze/PredictionResult";
import { ReportPanel } from "@/components/analyze/ReportPanel";
import { UploadDropzone } from "@/components/analyze/UploadDropzone";
import { DisclaimerBanner } from "@/components/shared/DisclaimerBanner";
import { HealthPill, useHealth } from "@/components/shared/HealthPill";
import { ApiError, predict, report } from "@/lib/api";
import type { AsyncState, PredictResult, ReportResult } from "@/lib/types";
import { cn } from "@/lib/utils";

function errMessage(e: unknown): string {
  if (e instanceof ApiError) return e.message;
  if (e instanceof Error) return e.message;
  return "Something went wrong.";
}

export function AnalyzeWorkspace() {
  const healthState = useHealth();
  const modelLoaded = healthState.kind === "ok";
  const ollamaReady = healthState.kind === "ok" && healthState.health.capabilities.ollama;
  const gradcamReady = healthState.kind === "ok" && healthState.health.capabilities.gradcam;
  const ollamaModel = healthState.kind === "ok" ? healthState.health.ollamaModel : "the local model";

  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [predictState, setPredictState] = useState<AsyncState<PredictResult>>({ status: "idle" });
  const [reportState, setReportState] = useState<AsyncState<ReportResult>>({ status: "idle" });

  const predictAbort = useRef<AbortController | null>(null);
  const reportAbort = useRef<AbortController | null>(null);

  useEffect(() => {
    return () => {
      predictAbort.current?.abort();
      reportAbort.current?.abort();
      if (previewUrl) URL.revokeObjectURL(previewUrl);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const onFile = useCallback(
    (next: File) => {
      setPreviewUrl((prev) => {
        if (prev) URL.revokeObjectURL(prev);
        return URL.createObjectURL(next);
      });
      setFile(next);
      setPredictState({ status: "idle" });
      setReportState({ status: "idle" });
    },
    [],
  );

  const onClear = useCallback(() => {
    predictAbort.current?.abort();
    reportAbort.current?.abort();
    setPreviewUrl((prev) => {
      if (prev) URL.revokeObjectURL(prev);
      return null;
    });
    setFile(null);
    setPredictState({ status: "idle" });
    setReportState({ status: "idle" });
  }, []);

  const runReport = useCallback(
    async (result: PredictResult) => {
      if (!ollamaReady) {
        setReportState({ status: "unavailable" });
        return;
      }
      reportAbort.current?.abort();
      const ctrl = new AbortController();
      reportAbort.current = ctrl;
      setReportState({ status: "loading" });
      try {
        const rep = await report(
          { tumorClass: result.topClass, classes: result.classes },
          ctrl.signal,
        );
        setReportState(
          rep.available ? { status: "success", data: rep } : { status: "unavailable" },
        );
      } catch (e) {
        if (ctrl.signal.aborted) return;
        setReportState({ status: "error", message: errMessage(e) });
      }
    },
    [ollamaReady],
  );

  const analyze = useCallback(async () => {
    if (!file || !modelLoaded) return;
    predictAbort.current?.abort();
    reportAbort.current?.abort();
    const ctrl = new AbortController();
    predictAbort.current = ctrl;
    setPredictState({ status: "loading" });
    setReportState({ status: "idle" });
    try {
      const res = await predict(file, { signal: ctrl.signal });
      if (ctrl.signal.aborted) return;
      setPredictState({ status: "success", data: res });
      runReport(res);
    } catch (e) {
      if (ctrl.signal.aborted) return;
      setPredictState({ status: "error", message: errMessage(e) });
    }
  }, [file, modelLoaded, runReport]);

  const retryReport = useCallback(() => {
    if (predictState.status === "success") runReport(predictState.data);
  }, [predictState, runReport]);

  const scanning = predictState.status === "loading";
  const hasResult = predictState.status === "success";
  const disabledReason = !file
    ? "Upload an MRI scan to analyze"
    : !modelLoaded
      ? healthState.kind === "loading"
        ? "Connecting to the model…"
        : "Model is unavailable — check the API server"
      : null;

  return (
    <div className="grid gap-6 lg:grid-cols-12">
      {/* ── Left rail: input ── */}
      <div className="lg:col-span-5 xl:col-span-4">
        <div className="panel grain relative overflow-hidden p-5 lg:sticky lg:top-24">
          <div className="mb-4 flex items-center justify-between">
            <p className="eyebrow">Input scan</p>
            <HealthPill />
          </div>

          <UploadDropzone
            previewUrl={previewUrl}
            fileName={file?.name ?? null}
            disabled={scanning}
            scanning={scanning}
            onFile={onFile}
            onClear={onClear}
          />

          <button
            type="button"
            onClick={analyze}
            disabled={!file || !modelLoaded || scanning}
            title={disabledReason ?? undefined}
            className={cn(
              "mt-4 inline-flex w-full items-center justify-center gap-2 rounded-xl px-4 py-3 text-sm font-semibold transition-all",
              !file || !modelLoaded || scanning
                ? "cursor-not-allowed bg-surface-3 text-muted"
                : "bg-primary text-bg hover:opacity-90 glow",
            )}
          >
            {scanning ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" /> Analyzing…
              </>
            ) : (
              <>
                <ScanLine className="h-4 w-4" /> Analyze scan
              </>
            )}
          </button>
          {disabledReason && !scanning && (
            <p className="mt-2 text-center text-xs text-muted">{disabledReason}</p>
          )}

          <div className="mt-4 flex flex-wrap gap-2 border-t border-line pt-4">
            <Capability label="GradCAM" on={gradcamReady} icon={<Activity className="h-3 w-3" />} />
            <Capability label="LLM report" on={ollamaReady} icon={<FileText className="h-3 w-3" />} />
          </div>
        </div>
      </div>

      {/* ── Right: results ── */}
      <div className="space-y-6 lg:col-span-7 xl:col-span-8">
        {!hasResult && predictState.status !== "loading" && predictState.status !== "error" ? (
          <EmptyState />
        ) : (
          <>
            <PredictionResult state={predictState} onRetry={analyze} />
            {hasResult && (
              <motion.div
                initial={{ opacity: 0, y: 14 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.1 }}
              >
                <GradCamViewer originalUrl={previewUrl} result={predictState.data} />
              </motion.div>
            )}
            {hasResult && (
              <ReportPanel state={reportState} onRetry={retryReport} model={ollamaModel} />
            )}
          </>
        )}
        <DisclaimerBanner variant="callout" />
      </div>
    </div>
  );
}

function Capability({ label, on, icon }: { label: string; on: boolean; icon: React.ReactNode }) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-xs font-medium",
        on ? "border-safe/30 bg-safe/8 text-safe" : "border-line bg-surface-2 text-muted",
      )}
    >
      {icon}
      {label}
      <span className="data text-[0.6rem] uppercase opacity-70">{on ? "on" : "off"}</span>
    </span>
  );
}

function EmptyState() {
  return (
    <div className="panel flex min-h-[420px] flex-col items-center justify-center gap-4 p-10 text-center">
      <span className="relative grid h-20 w-20 place-items-center rounded-2xl border border-dashed border-line text-primary">
        <Crosshair className="h-10 w-10 opacity-30 animate-pulse-soft" />
        <ScanLine className="absolute h-7 w-7" />
      </span>
      <div>
        <h3 className="font-display text-xl font-semibold tracking-tight text-ink-strong">
          Awaiting a scan
        </h3>
        <p className="mx-auto mt-1.5 max-w-sm text-sm leading-relaxed text-muted">
          Upload a brain MRI on the left and run the analysis. You&apos;ll get a class prediction,
          a GradCAM heatmap, and a local clinical report.
        </p>
      </div>
    </div>
  );
}
