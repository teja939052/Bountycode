// @ts-nocheck
export function Section({ title, description, children }: { title?: string; description?: string; children: React.ReactNode }) {
  return (
    <section className="rounded-2xl border border-brand-primary/10 bg-white p-5 shadow-soft">
      {title && <h2 className="text-lg font-bold text-text-primary">{title}</h2>}
      {description && <p className="mt-1 text-sm text-text-secondary">{description}</p>}
      <div className="mt-4">{children}</div>
    </section>
  );
}
