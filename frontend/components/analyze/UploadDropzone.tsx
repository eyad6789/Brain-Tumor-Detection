"use client";

import { ImageUp, Trash2, Crosshair } from "lucide-react";
import { useCallback, useRef, useState } from "react";

import { Ticks } from "@/components/shared/Ticks";
import { cn } from "@/lib/utils";

const ACCEPT = ["image/png", "image/jpeg", "image/webp", "image/bmp"];
const MAX_MB = 10;

export function UploadDropzone({
  previewUrl,
  fileName,
  disabled,
  scanning,
  onFile,
  onClear,
}: {
  previewUrl: string | null;
  fileName: string | null;
  disabled?: boolean;
  scanning?: boolean;
  onFile: (file: File) => void;
  onClear: () => void;
}) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const validateAndSend = useCallback(
    (file: File | undefined) => {
      if (!file) return;
      if (!ACCEPT.includes(file.type)) {
        setError("Unsupported file. Upload a PNG, JPEG, WEBP, or BMP image.");
        return;
      }
      if (file.size > MAX_MB * 1024 * 1024) {
        setError(`Image is too large (max ${MAX_MB} MB).`);
        return;
      }
      setError(null);
      onFile(file);
    },
    [onFile],
  );

  return (
    <div className="space-y-3">
      <div
        onDragOver={(e) => {
          e.preventDefault();
          if (!disabled) setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragging(false);
          if (!disabled) validateAndSend(e.dataTransfer.files?.[0]);
        }}
        className={cn(
          "group relative aspect-square w-full overflow-hidden rounded-2xl border transition-colors",
          previewUrl ? "border-line bg-black/40" : "border-dashed bg-surface-2",
          dragging ? "border-primary bg-primary-soft/40" : "border-line",
        )}
      >
        <Ticks />

        {previewUrl ? (
          <>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={previewUrl}
              alt="Uploaded MRI preview"
              className="h-full w-full object-contain"
            />
            {scanning && (
              <>
                <div className="pointer-events-none absolute inset-x-0 top-0 h-[3px] animate-scan bg-[var(--scan-color)] shadow-[0_0_18px_var(--scan-color)]" />
                <div className="pointer-events-none absolute inset-0 bg-gradient-to-b from-transparent via-[var(--scan-color)]/5 to-transparent" />
              </>
            )}
            <div className="absolute inset-x-0 bottom-0 flex items-center justify-between gap-2 bg-gradient-to-t from-black/70 to-transparent p-2.5">
              <span className="data truncate text-xs text-white/80">{fileName}</span>
              <div className="flex gap-1.5">
                <button
                  type="button"
                  onClick={() => inputRef.current?.click()}
                  disabled={disabled}
                  className="rounded-md bg-white/15 px-2 py-1 text-xs font-medium text-white backdrop-blur transition-colors hover:bg-white/25"
                >
                  Replace
                </button>
                <button
                  type="button"
                  onClick={onClear}
                  aria-label="Remove image"
                  className="grid h-7 w-7 place-items-center rounded-md bg-white/15 text-white backdrop-blur transition-colors hover:bg-glioma/80"
                >
                  <Trash2 className="h-3.5 w-3.5" />
                </button>
              </div>
            </div>
          </>
        ) : (
          <button
            type="button"
            onClick={() => inputRef.current?.click()}
            disabled={disabled}
            className="flex h-full w-full flex-col items-center justify-center gap-3 p-6 text-center disabled:cursor-not-allowed"
          >
            <span className="relative grid h-14 w-14 place-items-center rounded-2xl border border-line bg-surface text-primary transition-transform group-hover:scale-105">
              <Crosshair className="absolute h-7 w-7 opacity-20" />
              <ImageUp className="h-6 w-6" />
            </span>
            <span className="space-y-1">
              <span className="block text-sm font-semibold text-ink-strong">
                Drop an MRI scan, or click to browse
              </span>
              <span className="block text-xs text-muted">
                PNG · JPEG · WEBP · BMP — up to {MAX_MB} MB
              </span>
            </span>
          </button>
        )}

        <input
          ref={inputRef}
          type="file"
          accept={ACCEPT.join(",")}
          className="sr-only"
          onChange={(e) => validateAndSend(e.target.files?.[0])}
        />
      </div>

      {error && (
        <p className="rounded-lg border border-glioma/30 bg-glioma/8 px-3 py-2 text-xs text-glioma" role="alert">
          {error}
        </p>
      )}
    </div>
  );
}
