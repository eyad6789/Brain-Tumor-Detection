import { ShieldAlert } from "lucide-react";

import { DISCLAIMER_LONG, DISCLAIMER_SHORT } from "@/lib/constants";
import { cn } from "@/lib/utils";

export function DisclaimerBanner({
  variant = "callout",
  className,
}: {
  variant?: "strip" | "callout";
  className?: string;
}) {
  if (variant === "strip") {
    return (
      <div className="border-b border-line bg-surface-2/60">
        <div className="mx-auto flex max-w-6xl items-center gap-2 px-5 py-2 sm:px-8">
          <ShieldAlert className="h-3.5 w-3.5 shrink-0 text-alert" />
          <p className="text-[0.72rem] leading-tight text-muted">{DISCLAIMER_SHORT}</p>
        </div>
      </div>
    );
  }

  return (
    <div
      className={cn(
        "relative flex items-start gap-3 rounded-2xl border border-alert/30 bg-alert/8 p-4",
        className,
      )}
      role="note"
    >
      <span className="mt-0.5 grid h-8 w-8 shrink-0 place-items-center rounded-lg border border-alert/30 bg-alert/10 text-alert">
        <ShieldAlert className="h-4 w-4" />
      </span>
      <div>
        <p className="eyebrow mb-1 text-alert">Medical disclaimer</p>
        <p className="text-sm leading-relaxed text-ink">{DISCLAIMER_LONG}</p>
      </div>
    </div>
  );
}
