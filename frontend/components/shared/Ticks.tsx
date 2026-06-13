import { cn } from "@/lib/utils";

/** Corner reticle ticks — instrument framing for panels. Parent must be relative. */
export function Ticks({ className }: { className?: string }) {
  return (
    <span aria-hidden className={cn("ticks pointer-events-none absolute inset-0", className)}>
      <span />
      <span />
      <span />
      <span />
    </span>
  );
}
