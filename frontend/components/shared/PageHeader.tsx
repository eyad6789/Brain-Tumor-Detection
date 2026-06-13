export function PageHeader({
  eyebrow,
  title,
  subtitle,
}: {
  eyebrow: string;
  title: string;
  subtitle?: string;
}) {
  return (
    <div className="mb-8 max-w-2xl animate-fade-up">
      <p className="eyebrow mb-2">{eyebrow}</p>
      <h1 className="font-display text-3xl font-semibold tracking-tight text-ink-strong sm:text-4xl">
        {title}
      </h1>
      {subtitle && <p className="mt-3 text-base leading-relaxed text-muted">{subtitle}</p>}
    </div>
  );
}
