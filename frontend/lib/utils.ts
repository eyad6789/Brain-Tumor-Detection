import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

import type { ClassName } from "./types";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatPct(value: number, digits = 1): string {
  return `${(value * 100).toFixed(digits)}%`;
}

/** Fixed-width mono numeral string, e.g. 0.9842 */
export function formatProb(value: number, digits = 4): string {
  return value.toFixed(digits);
}

const CLASS_TOKEN: Record<ClassName, string> = {
  Glioma: "glioma",
  Meningioma: "meningioma",
  Pituitary: "pituitary",
  "No Tumor": "notumor",
};

/** CSS custom-property reference for a class accent color, e.g. var(--color-glioma) */
export function classColorVar(name: ClassName): string {
  return `var(--color-${CLASS_TOKEN[name]})`;
}
