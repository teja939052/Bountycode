import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Building2, ArrowRight, Target as TargetIcon } from "lucide-react";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";

// V3 §5 — Company pages are TARGET PACKS, not mini-LMS.
// Selecting a pack sets the Journey target (role+company) via the
// existing onboarding/company-track APIs, then drops back to /journey.
const PACKS: Record<string, Array<{ id: string; name: string; desc: string }>> = {
  tcs: [
    { id: "tcs-nqt", name: "TCS NQT", desc: "General preparation" },
    { id: "tcs-digital", name: "TCS Digital", desc: "Advanced preparation" },
    { id: "tcs-prime", name: "TCS Prime", desc: "Elite preparation" },
  ],
  infosys: [
    { id: "infosys-se", name: "Infosys SE", desc: "General preparation" },
    { id: "infosys-dse", name: "Infosys DSE", desc: "Advanced preparation" },
  ],
  wipro: [{ id: "wipro-nlth", name: "Wipro NLTH", desc: "General preparation" }],
  cognizant: [{ id: "cognizant-genc", name: "Cognizant GenC", desc: "General preparation" }],
  capgemini: [{ id: "capgemini", name: "Capgemini", desc: "General preparation" }],
  amazon: [{ id: "amazon-sde", name: "Amazon SDE", desc: "DSA-heavy preparation" }],
  google: [{ id: "google-swe", name: "Google SWE", desc: "DSA-heavy preparation" }],
};

const COMPANIES = Object.keys(PACKS);

export default function Target() {
  const navigate = useNavigate();
  const [company, setCompany] = useState("tcs");
  const [readiness, setReadiness] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState<string | null>(null);

  useEffect(() => {
    let alive = true;
    (async () => {
      setLoading(true);
      try {
        const data = await (api as any).adaptive?.getReadinessScore?.(company);
        if (alive) setReadiness(data);
      } catch {
        if (alive) setReadiness(null);
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => { alive = false; };
  }, [company]);

  const startPack = async (packId: string) => {
    setSaving(packId);
    try {
      // Persist target via existing onboarding API; fall back to localStorage.
      await (api as any).onboarding?.completeStep?.({
        target_company: company, target_pack: packId,
      }).catch(() => {});
      localStorage.setItem("bountycode.target", JSON.stringify({ company, pack: packId }));
    } finally {
      setSaving(null);
      navigate("/journey");
    }
  };

  const score = readiness?.overall_readiness ?? readiness?.overall ?? null;
  const skills: Array<{ skill_id: string; score: number }> =
    readiness?.target_readiness?.skills ?? [];

  return (
    <div className="min-h-screen px-4 py-6 md:py-8 pb-24 md:pb-8">
      <div className="mx-auto max-w-3xl space-y-6">
        <div className="rounded-2xl border border-border bg-white p-5 shadow-card">
          <p className="text-[10px] font-mono uppercase tracking-widest text-primary mb-1 flex items-center gap-2">
            <Building2 size={12} /> Target
          </p>
          <h1 className="font-display text-2xl font-black text-text-primary">
            {company.toUpperCase()}
          </h1>
          <p className="text-xs text-text-muted font-mono mt-1">Choose your target pack — one Journey, reordered for this target.</p>
          <div className="mt-3 flex flex-wrap gap-2">
            {COMPANIES.map((c) => (
              <button
                key={c}
                onClick={() => setCompany(c)}
                className={`rounded-full border px-3 py-1.5 text-xs font-mono ${c === company ? "border-primary/50 bg-primary/10 text-primary" : "border-black/10 text-text-secondary"}`}
              >
                {c.toUpperCase()}
              </button>
            ))}
          </div>
        </div>

        {(PACKS[company] ?? []).map((p) => (
          <div key={p.id} className="rounded-2xl border border-border bg-white p-5 shadow-card flex items-center justify-between gap-4">
            <div>
              <p className="font-display font-bold text-text-primary">{p.name}</p>
              <p className="text-xs text-text-muted font-mono">{p.desc}</p>
            </div>
            <button
              onClick={() => startPack(p.id)}
              disabled={saving === p.id}
              className="btn-primary text-sm inline-flex items-center gap-2"
            >
              {saving === p.id ? <Spinner size={14} /> : <>Start <ArrowRight size={14} /></>}
            </button>
          </div>
        ))}

        <div className="rounded-2xl border border-border bg-white p-5 shadow-card">
          <h2 className="section-header text-lg mb-2 flex items-center gap-2">
            <TargetIcon size={18} className="text-primary" />
            {company.toUpperCase()} readiness {score != null ? `— ${Math.round(score)}%` : ""}
          </h2>
          {loading ? <Spinner /> : skills.length === 0 ? (
            <p className="text-xs text-text-muted font-mono">No evidence yet — your first mission will generate it. <Link to="/journey" className="text-primary">Enter Journey →</Link></p>
          ) : (
            <div className="space-y-2">
              {skills.slice(0, 6).map((s) => (
                <div key={s.skill_id} className="flex items-center gap-3">
                  <span className="w-40 truncate font-mono text-xs text-text-secondary capitalize">{s.skill_id.split(".").pop()}</span>
                  <div className="h-2 flex-1 rounded-full bg-black/5 overflow-hidden">
                    <div className="h-full rounded-full bg-primary" style={{ width: `${Math.round(s.score)}%` }} />
                  </div>
                  <span className="font-mono text-xs w-10 text-right">{Math.round(s.score)}%</span>
                </div>
              ))}
              <Link to="/journey" className="btn-secondary text-xs inline-flex items-center gap-2 mt-3">
                Enter Journey <ArrowRight size={12} />
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
