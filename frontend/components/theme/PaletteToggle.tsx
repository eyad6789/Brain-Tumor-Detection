"use client";

import { useEffect, useState } from "react";

import { cn } from "@/lib/utils";
import { PALETTES, usePalette } from "@/components/theme/PaletteProvider";

export function PaletteToggle({ className }: { className?: string }) {
  const { palette, setPalette } = usePalette();
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);

  return (
    <div
      role="group"
      aria-label="Color palette"
      className={cn(
        "flex items-center gap-1.5 rounded-lg border border-line bg-surface-2 px-2 py-1.5",
        className,
      )}
    >
      {PALETTES.map((p) => {
        const active = mounted && palette === p.id;
        return (
          <button
            key={p.id}
            type="button"
            aria-label={`${p.label} palette`}
            aria-pressed={active}
            title={p.label}
            onClick={() => setPalette(p.id)}
            className={cn(
              "h-4 w-4 rounded-full ring-2 ring-offset-1 ring-offset-surface-2 transition-transform hover:scale-110",
              active ? "ring-ink-strong" : "ring-transparent",
            )}
            style={{
              backgroundImage: `linear-gradient(135deg, ${p.swatch[0]} 0%, ${p.swatch[1]} 100%)`,
            }}
          />
        );
      })}
    </div>
  );
}
