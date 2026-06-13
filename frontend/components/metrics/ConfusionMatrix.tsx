import { Info } from "lucide-react";

import type { ClassName } from "@/lib/types";

export function ConfusionMatrix({
  matrix,
  labels,
}: {
  matrix: number[][] | null;
  labels: ClassName[];
}) {
  if (!matrix) {
    return (
      <div className="panel p-5">
        <h3 className="mb-3 font-display text-base font-semibold tracking-tight text-ink-strong">
          Confusion matrix
        </h3>
        <p className="flex items-start gap-2 rounded-lg border border-line bg-surface-2 px-3 py-2.5 text-sm text-muted">
          <Info className="mt-0.5 h-4 w-4 shrink-0 text-primary" />
          Not available — the training log doesn&apos;t include a confusion matrix. Re-run training
          to generate one. (We don&apos;t fabricate metrics that weren&apos;t recorded.)
        </p>
      </div>
    );
  }

  const short = (l: ClassName) => (l === "No Tumor" ? "None" : l.slice(0, 4));
  const max = Math.max(...matrix.flat(), 1);

  return (
    <div className="panel p-5">
      <h3 className="mb-4 font-display text-base font-semibold tracking-tight text-ink-strong">
        Confusion matrix
      </h3>
      <div className="overflow-x-auto">
        <table className="border-collapse">
          <tbody>
            {matrix.map((row, r) => (
              <tr key={r}>
                <th className="data px-2 py-1 text-right text-[0.65rem] uppercase text-muted">
                  {short(labels[r])}
                </th>
                {row.map((v, c) => {
                  const t = v / max;
                  const onDiag = r === c;
                  return (
                    <td
                      key={c}
                      className="data h-12 w-12 border border-line text-center text-xs tabular-nums"
                      style={{
                        backgroundColor: onDiag
                          ? `color-mix(in srgb, var(--color-primary) ${10 + t * 70}%, transparent)`
                          : `color-mix(in srgb, var(--color-glioma) ${t * 60}%, transparent)`,
                        color: t > 0.5 ? "var(--color-bg)" : "var(--color-ink)",
                      }}
                    >
                      {v}
                    </td>
                  );
                })}
              </tr>
            ))}
            <tr>
              <th />
              {labels.map((l) => (
                <th key={l} className="data px-1 py-1 text-center text-[0.65rem] uppercase text-muted">
                  {short(l)}
                </th>
              ))}
            </tr>
          </tbody>
        </table>
      </div>
      <p className="mt-3 text-xs text-muted">Rows: actual · Columns: predicted</p>
    </div>
  );
}
