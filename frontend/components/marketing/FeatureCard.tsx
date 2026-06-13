import type { LucideIcon } from "lucide-react";

import { cn } from "@/lib/utils";

export function FeatureCard({
  icon: Icon,
  title,
  description,
  className,
}: {
  icon: LucideIcon;
  title: string;
  description: string;
  className?: string;
}) {
  return (
    <div
      className={cn(
        "group panel p-5 transition-all hover:border-primary/40 hover:-translate-y-0.5",
        className,
      )}
    >
      <span className="grid h-10 w-10 place-items-center rounded-xl border border-line bg-surface-2 text-primary transition-colors group-hover:border-primary/40">
        <Icon className="h-5 w-5" />
      </span>
      <h3 className="mt-4 font-display text-lg font-semibold tracking-tight text-ink-strong">
        {title}
      </h3>
      <p className="mt-1.5 text-sm leading-relaxed text-muted">{description}</p>
    </div>
  );
}
