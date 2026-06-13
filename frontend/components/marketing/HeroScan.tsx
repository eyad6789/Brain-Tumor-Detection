import { Ticks } from "@/components/shared/Ticks";

const BARS = [
  { label: "No Tumor", token: "notumor", w: 96 },
  { label: "Glioma", token: "glioma", w: 18 },
  { label: "Meningioma", token: "meningioma", w: 9 },
  { label: "Pituitary", token: "pituitary", w: 5 },
];

/** Decorative "instrument readout" shown in the hero. Pure CSS/SVG. */
export function HeroScan() {
  return (
    <div className="panel glass relative overflow-hidden p-4 grain">
      <Ticks />
      <div className="mb-3 flex items-center justify-between px-1">
        <span className="eyebrow">Live readout</span>
        <span className="data inline-flex items-center gap-1.5 text-[0.65rem] text-muted">
          <span className="h-1.5 w-1.5 rounded-full bg-safe" /> ResNet50
        </span>
      </div>

      {/* Faux scan window */}
      <div className="relative aspect-[5/4] overflow-hidden rounded-xl border border-line bg-[radial-gradient(circle_at_50%_45%,#1b2740_0%,#0a0f1c_70%)]">
        <Ticks />
        {/* crosshair */}
        <div className="absolute inset-0 grid place-items-center">
          <svg viewBox="0 0 200 160" className="h-full w-full opacity-90">
            <defs>
              <radialGradient id="lesion" cx="58%" cy="42%" r="22%">
                <stop offset="0%" stopColor="var(--color-primary)" stopOpacity="0.85" />
                <stop offset="100%" stopColor="var(--color-primary)" stopOpacity="0" />
              </radialGradient>
            </defs>
            {/* brain-ish contour */}
            <path
              d="M100 24c34 0 60 24 60 56 0 30-26 56-60 56S40 110 40 80c0-32 26-56 60-56z"
              fill="none"
              stroke="var(--color-line-strong)"
              strokeWidth="1.2"
              opacity="0.6"
            />
            <path
              d="M100 40c22 0 40 18 40 40s-18 40-40 40"
              fill="none"
              stroke="var(--color-line)"
              strokeWidth="1"
              opacity="0.5"
            />
            <circle cx="116" cy="68" r="30" fill="url(#lesion)" />
            <line x1="100" y1="10" x2="100" y2="150" stroke="var(--color-primary)" strokeWidth="0.5" opacity="0.3" />
            <line x1="20" y1="80" x2="180" y2="80" stroke="var(--color-primary)" strokeWidth="0.5" opacity="0.3" />
          </svg>
        </div>
        {/* scanline */}
        <div className="pointer-events-none absolute inset-x-0 top-0 h-[3px] animate-scan bg-[var(--scan-color)] shadow-[0_0_18px_var(--scan-color)]" />
      </div>

      {/* readout bars */}
      <div className="mt-4 space-y-2.5 px-1">
        {BARS.map((b) => (
          <div key={b.label} className="space-y-1">
            <div className="flex justify-between text-[0.7rem]">
              <span className="text-muted">{b.label}</span>
              <span className="data text-ink-strong">{b.w}%</span>
            </div>
            <div className="h-1.5 overflow-hidden rounded-full bg-surface-3">
              <div
                className="h-full rounded-full"
                style={{ width: `${b.w}%`, backgroundColor: `var(--color-${b.token})` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
