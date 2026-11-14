import { useEffect, useState } from "react";
import api from "../services/api";

type LearningResource = {
  id: string;
  title: string;
  provider: string;
  url: string;
  format?: string[];
  domains?: string[];
  topics?: string[];
  level?: string;
  access?: string;
  rights?: string;
  recommended_use?: string;
  source_type?: string;
};

type ResourceResponse = {
  resources?: LearningResource[];
  total_matches?: number;
  notice?: string;
};

function humanize(value: string) {
  return value.replace(/_/g, " ").replace(/-/g, " ");
}

export default function LearningResourcesPanel({
  domain,
  topic,
}: {
  domain?: string;
  topic: string;
}) {
  const [resources, setResources] = useState<LearningResource[]>([]);
  const [notice, setNotice] = useState("");
  const [loading, setLoading] = useState(true);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    let cancelled = false;
    const params = new URLSearchParams();
    if (domain) params.set("domain", domain);
    if (topic) params.set("topic", topic.replace(/[_-]+/g, " "));
    params.set("limit", "8");

    setLoading(true);
    setFailed(false);
    api.get(`/api/v1/learning-resources?${params.toString()}`)
      .then((response: ResourceResponse) => {
        if (cancelled) return;
        setResources(response?.resources || []);
        setNotice(response?.notice || "");
      })
      .catch(() => {
        if (!cancelled) setFailed(true);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [domain, topic]);

  return (
    <section className="mb-5 rounded-2xl border border-white/10 bg-surface-base/70 p-4">
      <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
        <div>
          <p className="text-[10px] font-mono font-bold uppercase tracking-wider text-brand-sky">Study library</p>
          <h2 className="mt-1 text-base font-bold text-text-primary">Learn from trusted external resources</h2>
          <p className="mt-1 text-xs text-text-secondary">Books, lectures, notes, exercises and official references related to this topic.</p>
        </div>
        <span className="rounded-full border border-white/10 px-2.5 py-1 text-[10px] text-text-secondary">Supplementary</span>
      </div>

      {loading ? (
        <p className="text-xs text-text-secondary">Finding relevant study material…</p>
      ) : failed ? (
        <p className="text-xs text-text-secondary">The resource catalogue is temporarily unavailable. You can continue with the lesson.</p>
      ) : resources.length === 0 ? (
        <p className="text-xs text-text-secondary">No closely matched external resources are indexed for this topic yet. The catalogue is being expanded.</p>
      ) : (
        <div className="space-y-2">
          {resources.map((resource) => (
            <article key={resource.id} className="rounded-xl border border-white/10 bg-white/[0.025] p-3">
              <div className="flex flex-wrap items-start justify-between gap-2">
                <div className="min-w-0">
                  <h3 className="text-sm font-semibold text-text-primary">{resource.title}</h3>
                  <p className="mt-0.5 text-[11px] text-text-secondary">{resource.provider}</p>
                </div>
                <a
                  href={resource.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="shrink-0 rounded-lg border border-brand-sky/30 px-3 py-1.5 text-xs font-semibold text-brand-sky hover:bg-brand-sky/10"
                >
                  Open source ↗
                </a>
              </div>
              {resource.recommended_use && <p className="mt-2 text-xs leading-5 text-text-secondary">{resource.recommended_use}</p>}
              <div className="mt-2 flex flex-wrap gap-1.5">
                {(resource.format || []).slice(0, 4).map((format) => (
                  <span key={format} className="rounded-md bg-white/5 px-2 py-1 text-[10px] text-text-secondary">{humanize(format)}</span>
                ))}
                {resource.access && <span className="rounded-md bg-white/5 px-2 py-1 text-[10px] text-text-secondary">{humanize(resource.access)}</span>}
              </div>
              {resource.rights && <p className="mt-2 text-[10px] leading-4 text-text-secondary">Rights: {resource.rights}</p>}
            </article>
          ))}
        </div>
      )}
      {notice && <p className="mt-3 text-[10px] leading-4 text-text-secondary">{notice}</p>}
      <p className="mt-2 text-[10px] text-text-secondary">Opening or reading an external resource does not award XP or count as mastery. Complete Bountycode practice and assessments to demonstrate your skills.</p>
    </section>
  );
}
