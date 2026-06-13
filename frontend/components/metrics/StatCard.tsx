import { Info } from "lucide-react";

import { Ticks } from "@/components/shared/Ticks";
import { cn } from "@/lib/utils";

export function StatCard({
  label,
  value,
  sub,
  caveat,
  accent,
}: {
  label: string;
  value: string;
  sub?: string;
  caveat?: string;
  accent?: boolean;
}) {
  return (
    <div className="panel relative overflow-hidden p-5">
      <Ticks />
      <div className="flex items-center gap-1.5">
        <p className="eyebrow">{label}</p>
        {caveat && (
          <span title={caveat} className="cursor-help text-muted" aria-label={caveat}>
            <Info className="h-3 w-3" />
          </span>
        )}
      </div>
      <p
        className={cn(
          "data mt-2 text-3xl font-semibold tracking-tight tabular-nums",
          accent ? "text-primary" : "text-ink-strong",
        )}
      >
        {value}
      </p>
      {sub && <p className="mt-1 text-xs text-muted">{sub}</p>}
    </div>
  );
}
