// Typed API client — the single seam between the snake_case FastAPI wire format
// and the camelCase TypeScript types used across the app.

import type {
  ClassName,
  ClassScore,
  HealthInfo,
  MetricsInfo,
  PredictResult,
  ReportResult,
} from "./types";

const BASE = process.env.NEXT_PUBLIC_API_BASE ?? "/api";

export class ApiError extends Error {
  code: string;
  status: number;
  constructor(status: number, code: string, message: string) {
    super(message);
    this.name = "ApiError";
    this.code = code;
    this.status = status;
  }
}

async function parseError(res: Response): Promise<ApiError> {
  let code = "http_error";
  let message = `Request failed (${res.status})`;
  try {
    const body = await res.json();
    if (body?.error) {
      code = body.error.code ?? code;
      message = body.error.message ?? message;
    } else if (body?.detail) {
      code = "validation_error";
      message =
        typeof body.detail === "string" ? body.detail : JSON.stringify(body.detail);
    }
  } catch {
    /* non-JSON error body */
  }
  return new ApiError(res.status, code, message);
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let res: Response;
  try {
    res = await fetch(`${BASE}${path}`, {
      ...init,
      headers: { Accept: "application/json", ...(init?.headers ?? {}) },
    });
  } catch {
    throw new ApiError(
      0,
      "network_error",
      "Could not reach the backend. Make sure the API server is running.",
    );
  }
  if (!res.ok) throw await parseError(res);
  return (await res.json()) as T;
}

export async function getHealth(signal?: AbortSignal): Promise<HealthInfo> {
  const d = await request<Record<string, unknown>>("/health", { signal });
  return {
    status: String(d.status),
    modelLoaded: Boolean(d.model_loaded),
    modelError: (d.model_error as string | null) ?? null,
    device: String(d.device),
    capabilities: {
      gradcam: Boolean(d.gradcam_available),
      ollama: Boolean(d.ollama_available),
    },
    ollamaModel: String(d.ollama_model ?? "local model"),
    classes: d.classes as ClassName[],
  };
}

export async function predict(
  file: File,
  opts?: { gradcam?: boolean; signal?: AbortSignal },
): Promise<PredictResult> {
  const form = new FormData();
  form.append("file", file);
  const query = opts?.gradcam === false ? "?gradcam=false" : "";
  // NOTE: do not set Content-Type — the browser sets the multipart boundary.
  const d = await request<Record<string, unknown>>(`/predict${query}`, {
    method: "POST",
    body: form,
    signal: opts?.signal,
  });
  const probabilities = (d.probabilities as Array<{ label: ClassName; prob: number }>) ?? [];
  return {
    topClass: d.top_class as ClassName,
    confidence: Number(d.confidence),
    classes: probabilities.map((p) => ({ name: p.label, confidence: p.prob })),
    verdictMarkdown: String(d.verdict_markdown),
    gradcamDataUrl: (d.gradcam_data_url as string | null) ?? null,
    gradcamIsHeatmap: Boolean(d.gradcam_is_heatmap),
  };
}

export async function report(
  input: { tumorClass: ClassName; classes: ClassScore[] },
  signal?: AbortSignal,
): Promise<ReportResult> {
  const confidence_scores: Record<string, number> = {};
  for (const c of input.classes) confidence_scores[c.name] = c.confidence;
  const d = await request<Record<string, unknown>>("/report", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tumor_class: input.tumorClass, confidence_scores }),
    signal,
  });
  return {
    reportMarkdown: String(d.report_markdown),
    available: Boolean(d.available),
  };
}

export async function getMetrics(signal?: AbortSignal): Promise<MetricsInfo> {
  const d = await request<Record<string, unknown>>("/metrics", { signal });
  const epochs = (d.epochs as Array<Record<string, number | null>>) ?? [];
  const classes = (d.classes as Array<Record<string, unknown>>) ?? [];
  return {
    claimedAccuracy: Number(d.claimed_accuracy),
    accuracyCaveat: String(d.accuracy_caveat),
    epochs: epochs.map((e) => ({
      epoch: Number(e.epoch),
      trainLoss: e.train_loss ?? null,
      trainAcc: e.train_acc ?? null,
      valLoss: e.val_loss ?? null,
      valAcc: e.val_acc ?? null,
      lr: e.lr ?? null,
    })),
    confusionMatrix: (d.confusion_matrix as number[][] | null) ?? null,
    perClass: (d.per_class as Array<Record<string, unknown>> | null) ?? null,
    classes: classes.map((c) => ({
      name: c.name as ClassName,
      index: Number(c.index),
      description: String(c.description),
    })),
  };
}
