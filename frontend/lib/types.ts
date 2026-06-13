// Shared TypeScript types. The wire format from FastAPI is snake_case; lib/api.ts
// is the single seam that maps it to the camelCase shapes below.

export type ClassName = "Pituitary" | "No Tumor" | "Meningioma" | "Glioma";

// Canonical, fixed class order (model index order). Never reorder.
export const CLASS_ORDER: ClassName[] = ["Pituitary", "No Tumor", "Meningioma", "Glioma"];

export interface ClassScore {
  name: ClassName;
  confidence: number; // 0–1
}

export interface HealthInfo {
  status: string;
  modelLoaded: boolean;
  modelError: string | null;
  device: string;
  capabilities: { gradcam: boolean; ollama: boolean };
  ollamaModel: string;
  classes: ClassName[];
}

export interface PredictResult {
  topClass: ClassName;
  confidence: number; // 0–1 for the top class
  classes: ClassScore[]; // sorted descending (display order)
  verdictMarkdown: string;
  gradcamDataUrl: string | null; // data:image/png;base64,... or null
  gradcamIsHeatmap: boolean; // false => fallback (grad-cam missing / skipped)
}

export interface ReportResult {
  reportMarkdown: string;
  available: boolean;
}

export interface EpochRow {
  epoch: number;
  trainLoss: number | null;
  trainAcc: number | null;
  valLoss: number | null;
  valAcc: number | null;
  lr: number | null;
}

export interface ClassMeta {
  name: ClassName;
  index: number;
  description: string;
}

export interface MetricsInfo {
  claimedAccuracy: number;
  accuracyCaveat: string;
  epochs: EpochRow[];
  confusionMatrix: number[][] | null;
  perClass: Array<Record<string, unknown>> | null;
  classes: ClassMeta[];
}

export type AsyncState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; message: string }
  | { status: "unavailable"; message?: string };
