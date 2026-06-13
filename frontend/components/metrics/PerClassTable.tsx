import type { ClassMeta, ClassName } from "@/lib/types";
import { classColorVar } from "@/lib/utils";

export function PerClassTable({ classes }: { classes: ClassMeta[] }) {
  return (
    <div className="panel overflow-hidden">
      <div className="border-b border-line p-5 pb-3">
        <h3 className="font-display text-base font-semibold tracking-tight text-ink-strong">
          Classes
        </h3>
        <p className="mt-1 text-xs text-muted">Fixed model index order.</p>
      </div>
      <ul className="divide-y divide-line">
        {classes.map((c) => (
          <li key={c.name} className="flex items-start gap-3 p-4">
            <span
              className="mt-1 h-2.5 w-2.5 shrink-0 rounded-full"
              style={{ backgroundColor: classColorVar(c.name as ClassName) }}
            />
            <div className="min-w-0 flex-1">
              <div className="flex items-center gap-2">
                <span className="font-medium text-ink-strong">{c.name}</span>
                <span className="data rounded bg-surface-3 px-1.5 py-0.5 text-[0.6rem] text-muted">
                  idx {c.index}
                </span>
              </div>
              <p className="mt-0.5 text-sm leading-relaxed text-muted">{c.description}</p>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
