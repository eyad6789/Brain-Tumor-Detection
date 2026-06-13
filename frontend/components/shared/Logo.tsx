import { cn } from "@/lib/utils";

/** NeuroScan mark: a reticle frame enclosing a neural node + pulse trace. */
export function Logo({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 32 32" fill="none" className={cn("h-7 w-7", className)} aria-hidden>
      <rect x="2.5" y="2.5" width="27" height="27" rx="8.5" stroke="currentColor" strokeOpacity="0.28" />
      {/* reticle ticks */}
      <path d="M16 3.5v4M16 24.5v4M3.5 16h4M24.5 16h4" stroke="var(--color-primary)" strokeWidth="1.4" strokeLinecap="round" />
      {/* pulse trace */}
      <path
        d="M7 16.5h3l1.6-4 2.2 8 2-5.5 1.5 2.2H25"
        stroke="var(--color-primary)"
        strokeWidth="1.7"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <circle cx="16" cy="16" r="2.4" fill="var(--color-accent)" />
    </svg>
  );
}
