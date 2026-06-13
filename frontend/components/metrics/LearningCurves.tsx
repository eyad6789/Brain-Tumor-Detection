"use client";

import type { EpochRow } from "@/lib/types";

type Series = { label: string; color: string; data: (number | null)[] };

function buildPath(
  data: (number | null)[],
  xFor: (i: number) => number,
  yFor: (v: number) => number,
): string {
  let d = "";
  let pen = false;
  data.forEach((v, i) => {
    if (v == null) {
      pen = false;
      return;
    }
    d += `${pen ? "L" : "M"}${xFor(i).toFixed(1)} ${yFor(v).toFixed(1)} `;
    pen = true;
  });
  return d.trim();
}

function Chart({
  title,
  epochs,
  series,
  yMin,
  yMax,
  fmtY,
}: {
  title: string;
  epochs: number[];
  series: Series[];
  yMin: number;
  yMax: number;
  fmtY: (v: number) => string;
}) {
  const W = 360;
  const H = 210;
  const padL = 40;
  const padR = 14;
  const padT = 14;
  const padB = 30;
  const plotW = W - padL - padR;
  const plotH = H - padT - padB;
  const n = epochs.length;

  const xFor = (i: number) => padL + (n <= 1 ? plotW / 2 : (i / (n - 1)) * plotW);
  const yFor = (v: number) => padT + (1 - (v - yMin) / (yMax - yMin || 1)) * plotH;
  const gridLines = [0, 0.25, 0.5, 0.75, 1].map((t) => yMin + t * (yMax - yMin));

  return (
    <div className="panel p-5">
      <div className="mb-3 flex items-center justify-between">
        <h3 className="font-display text-base font-semibold tracking-tight text-ink-strong">{title}</h3>
        <div className="flex gap-3">
          {series.map((s) => (
            <span key={s.label} className="flex items-center gap-1.5 text-xs text-muted">
              <span className="h-2 w-3 rounded-full" style={{ backgroundColor: s.color }} />
              {s.label}
            </span>
          ))}
        </div>
      </div>
      <svg viewBox={`0 0 ${W} ${H}`} className="h-auto w-full" role="img" aria-label={title}>
        {gridLines.map((g, i) => (
          <g key={i}>
            <line
              x1={padL}
              x2={W - padR}
              y1={yFor(g)}
              y2={yFor(g)}
              stroke="var(--color-line)"
              strokeWidth={1}
            />
            <text x={padL - 6} y={yFor(g) + 3} textAnchor="end" className="data" fontSize="8" fill="var(--color-muted)">
              {fmtY(g)}
            </text>
          </g>
        ))}
        {epochs.map((e, i) => (
          <text
            key={i}
            x={xFor(i)}
            y={H - padB + 14}
            textAnchor="middle"
            className="data"
            fontSize="8"
            fill="var(--color-muted)"
          >
            {e}
          </text>
        ))}
        {series.map((s) => (
          <g key={s.label}>
            <path d={buildPath(s.data, xFor, yFor)} fill="none" stroke={s.color} strokeWidth={2} strokeLinejoin="round" strokeLinecap="round" />
            {s.data.map((v, i) =>
              v == null ? null : (
                <circle key={i} cx={xFor(i)} cy={yFor(v)} r={2.5} fill="var(--color-surface)" stroke={s.color} strokeWidth={1.5} />
              ),
            )}
          </g>
        ))}
      </svg>
    </div>
  );
}

export function LearningCurves({ epochs }: { epochs: EpochRow[] }) {
  if (epochs.length < 2) {
    return (
      <div className="panel p-6 text-sm text-muted">Not enough epochs logged to plot learning curves.</div>
    );
  }

  const xs = epochs.map((e) => e.epoch);
  const trainAcc = epochs.map((e) => e.trainAcc);
  const valAcc = epochs.map((e) => e.valAcc);
  const trainLoss = epochs.map((e) => e.trainLoss);
  const valLoss = epochs.map((e) => e.valLoss);

  const accVals = [...trainAcc, ...valAcc].filter((v): v is number => v != null);
  const lossVals = [...trainLoss, ...valLoss].filter((v): v is number => v != null);
  const accMin = accVals.length ? Math.max(0, Math.min(...accVals) - 0.05) : 0;
  const lossMax = lossVals.length ? Math.max(...lossVals) * 1.15 : 1;

  return (
    <div className="grid gap-5 md:grid-cols-2">
      <Chart
        title="Accuracy"
        epochs={xs}
        yMin={accMin}
        yMax={1}
        fmtY={(v) => `${Math.round(v * 100)}%`}
        series={[
          { label: "Train", color: "var(--color-muted)", data: trainAcc },
          { label: "Validation", color: "var(--color-primary)", data: valAcc },
        ]}
      />
      <Chart
        title="Loss"
        epochs={xs}
        yMin={0}
        yMax={lossMax}
        fmtY={(v) => v.toFixed(2)}
        series={[
          { label: "Train", color: "var(--color-muted)", data: trainLoss },
          { label: "Validation", color: "var(--color-accent)", data: valLoss },
        ]}
      />
    </div>
  );
}
