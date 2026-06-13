import { CLASS_META } from "@/lib/constants";
import type { ClassName } from "@/lib/types";
import { classColorVar } from "@/lib/utils";

export function ClassCard({ name }: { name: ClassName }) {
  const meta = CLASS_META[name];
  const color = classColorVar(name);
  return (
    <div className="panel relative overflow-hidden p-5">
      <span
        className="absolute inset-x-0 top-0 h-0.5"
        style={{ backgroundColor: color }}
        aria-hidden
      />
      <div className="flex items-center gap-2.5">
        <span className="h-2.5 w-2.5 rounded-full" style={{ backgroundColor: color }} />
        <h3 className="font-display text-base font-semibold tracking-tight text-ink-strong">
          {name}
        </h3>
        {meta.tone === "safe" && (
          <span className="data ml-auto rounded bg-safe/10 px-1.5 py-0.5 text-[0.6rem] uppercase text-safe">
            negative
          </span>
        )}
      </div>
      <p className="mt-2 text-sm leading-relaxed text-muted">{meta.blurb}</p>
    </div>
  );
}
