import { useState, useEffect, useCallback, type ReactNode } from "react";
import { useSearchParams } from "react-router-dom";
import { Calendar, Building2, Search, X, Target, GraduationCap, Clock, ArrowRight, Sparkles, Lightbulb, Link2 } from "lucide-react";
import api from "../services/api";

type Company = {
  id: string;
  name: string;
  type: string;
  tier: string;
  calendar_window: string;
  calendar_months: string[];
  roles: string[];
  what_they_ask: string[];
  interview_process: string[];
  focus_areas: string[];
  prepare_from_us: string[];
  tips: string;
  tags: string[];
};

type CalEvent = { title: string; kind: string; companies: string[]; note: string };
type CalendarData = Record<string, CalEvent[]>;

// Maps a focus area to a concrete lesson label + the live PlacementPro page to practice it.
const FOCUS_LESSON_MAP: Record<string, { label: string; route: string }> = {
  dsa: { label: "Arrays, Strings & Recursion", route: "/coding-challenge" },
  "data structures": { label: "Linked Lists, Trees, Graphs", route: "/question-bank" },
  algorithms: { label: "DP, Greedy & Graph algorithms", route: "/question-bank" },
  aptitude: { label: "Quant & Logical (NQT pattern)", route: "/aptitude" },
  quant: { label: "Arithmetic, Percentages & Ratios", route: "/aptitude" },
  logical: { label: "Series, Puzzles & Arrangements", route: "/aptitude" },
  verbal: { label: "Reading Comp & Para Jumbles", route: "/aptitude" },
  "system design": { label: "System Design Fundamentals", route: "/system-design" },
  behavioral: { label: "STAR + Leadership Principles", route: "/interview" },
  hr: { label: "HR & Salary Discussion", route: "/salary-negotiation" },
  sql: { label: "DBMS & Query Practice", route: "/compiler" },
  dbms: { label: "DBMS & Query Practice", route: "/compiler" },
  oop: { label: "OOP & Design Patterns", route: "/coding-challenge" },
  coding: { label: "Coding Challenges", route: "/coding-challenge" },
  "computer networks": { label: "Networks Deep Dive", route: "/question-bank" },
  "operating systems": { label: "OS Concepts", route: "/question-bank" },
};

const KIND_COLORS: Record<string, string> = {
  Drive: "bg-cyber-blue/15 text-cyber-blue border-cyber-blue/30",
  Internship: "bg-cyber-green/15 text-cyber-green border-cyber-green/30",
  Exam: "bg-purple-500/15 text-purple-300 border-purple-500/30",
  Hackathon: "bg-amber-500/15 text-amber-300 border-amber-500/30",
  "Off-campus": "bg-pink-500/15 text-pink-300 border-pink-500/30",
  Results: "bg-emerald-500/15 text-emerald-300 border-emerald-500/30",
  "Pre-placement Talk": "bg-sky-500/15 text-sky-300 border-sky-500/30",
  deadline: "bg-red-500/15 text-red-300 border-red-500/30",
  "Open Role": "bg-indigo-500/15 text-indigo-300 border-indigo-500/30",
  Referral: "bg-teal-500/15 text-teal-300 border-teal-500/30",
};

// Novel, differentiated things job seekers actually pay for (beyond a flat subscription).
const PREMIUM_IDEAS: { title: string; desc: string; price: string }[] = [
  { title: "Interview Guarantee", desc: "Buy the prep bundle; if you don't land an offer in 90 days, get your money back.", price: "from $99" },
  { title: "1:1 Human Mock Interviews", desc: "Book senior engineers from your target company for a live, recorded mock.", price: "$19/session" },
  { title: "Resume Rewrite by Ex-Recruiters", desc: "A human rewrites your resume against the exact rubric the company uses.", price: "$29" },
  { title: "Referral Marketplace", desc: "Get matched to employees who can refer you and track the referral to offer.", price: "$15" },
  { title: "Salary Negotiation Concierge", desc: "An expert reviews your offer letter and coaches the negotiation live.", price: "$25" },
  { title: "Reverse-Interview Question Pack", desc: "Smart questions to ask each company that signal you're already an insider.", price: "Pro" },
  { title: "OA Simulators", desc: "Replicate HackerRank/Codeforces/SHL assessment environments with the same timers.", price: "Pro" },
  { title: "Company Insider AMAs", desc: "Live monthly sessions with employees who share what got them hired.", price: "$9/session" },
  { title: "Offer Comparison & Equity 101", desc: "Decode competing offers, RSUs, and base-vs-equity tradeoffs side by side.", price: "$15" },
  { title: "AI Interviewer Voice Mode", desc: "Speak your answers out loud; the AI grills you like a real panel, with tone feedback.", price: "Pro" },
];

function premiumOffersFor(c: Company): { title: string; desc: string; price: string }[] {
  return [
    { title: `1:1 Mock Interview — ${c.name}`, desc: "60-min live mock of their exact rounds, recorded with feedback.", price: "$19" },
    { title: `${c.name} Resume Rewrite`, desc: "Ex-recruiter tailors your resume to ${c.name}'s hiring rubric.", price: "$29" },
    { title: `${c.name} Question Bank`, desc: "Company-specific problems + leaked OA patterns, updated weekly.", price: "Pro" },
    { title: `Referral Assist — ${c.name}`, desc: "Matched to an employee who can refer you into the pipeline.", price: "$15" },
    { title: `Offer Negotiation — ${c.name}`, desc: "Expert coaches your specific ${c.name} offer letter.", price: "$25" },
  ];
}

export default function PlacementCalendar() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [view, setView] = useState<"calendar" | "companies" | "ideas">("calendar");
  const [calendar, setCalendar] = useState<CalendarData>({});
  const [companies, setCompanies] = useState<Company[]>([]);
  const [filters, setFilters] = useState<{ types: string[]; tiers: string[]; months: string[] }>({ types: [], tiers: [], months: [] });
  const [selected, setSelected] = useState<Company | null>(null);
  const [q, setQ] = useState("");
  const [type, setType] = useState("");
  const [tier, setTier] = useState("");
  const [month, setMonth] = useState("");
  const [activeMonth, setActiveMonth] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [checked, setChecked] = useState<Record<string, boolean>>({});
  const [progressMap, setProgressMap] = useState<Record<string, { done: number; total: number }>>({});

  const loadCalendar = useCallback(async () => {
    try {
      const res = await api.companyDirectory.getCalendar();
      setCalendar(res.calendar || {});
    } catch {}
  }, []);

  const loadFilters = useCallback(async () => {
    try {
      const res = await api.companyDirectory.getFilters();
      setFilters({ types: res.types || [], tiers: res.tiers || [], months: res.months || [] });
    } catch {}
  }, []);

  const loadCompanies = useCallback(async () => {
    setLoading(true);
    try {
      const res = await api.companyDirectory.getCompanies({ q, type, tier, month });
      setCompanies(res.companies || []);
    } catch {}
    setLoading(false);
  }, [q, type, tier, month]);

  const openCompany = useCallback(async (idOrName: string) => {
    setLoading(true);
    let id = idOrName;
    try {
      const res = await api.companyDirectory.getCompany(idOrName);
      if (res && res.id) {
        id = res.id;
      } else {
        const sres = await api.companyDirectory.search(idOrName);
        const hit = (sres.companies || [])[0];
        if (!hit) { setLoading(false); return; }
        id = hit.id;
      }
    } catch {
      try {
        const sres = await api.companyDirectory.search(idOrName);
        const hit = (sres.companies || [])[0];
        if (!hit) { setLoading(false); return; }
        id = hit.id;
      } catch { setLoading(false); return; }
    }
    try {
      const full = await api.companyDirectory.getCompany(id);
      if (!full || !full.id) { setLoading(false); return; }
      setSelected(full);
      setSearchParams({ company: full.id });
      let progress: string[] = [];
      try {
        const p = await api.companyDirectory.getProgress(full.id);
        progress = p.completed || [];
      } catch {}
      const init: Record<string, boolean> = {};
      (full.focus_areas || []).forEach((f: string) => {
        if (progress.includes(f)) init[`${full.id}:${f}`] = true;
      });
      setChecked(init);
      setProgressMap((m) => ({ ...m, [full.id]: { done: progress.length, total: (full.focus_areas || []).length } }));
    } catch {}
    setLoading(false);
  }, [setSearchParams]);

  const closeCompany = useCallback(() => {
    setSelected(null);
    setSearchParams({});
  }, [setSearchParams]);

  useEffect(() => { loadCalendar(); loadFilters(); }, [loadCalendar, loadFilters]);
  useEffect(() => {
    if (view === "companies") loadCompanies();
  }, [view, loadCompanies]);

  // Deep-link: open a company if shared via ?company=<id>
  useEffect(() => {
    const id = searchParams.get("company");
    if (id && (!selected || selected.id !== id)) openCompany(id);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchParams]);

  const lessonFor = (area: string) => {
    const key = area.toLowerCase();
    const match = Object.keys(FOCUS_LESSON_MAP).find((k) => key.includes(k));
    return match ? FOCUS_LESSON_MAP[match] : null;
  };

  const months = Object.keys(calendar).sort();

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-8">
          <span className="section-subheader block mb-2">2026 – 2027 Hiring Season</span>
          <h1 className="section-header text-4xl mb-2">Placement & Internship <span className="text-cyber-blue">Calendar</span></h1>
          <p className="text-gray-400 font-mono text-sm">140+ companies, what they ask, how to prepare, and when they hire.</p>
        </div>

        <div className="flex justify-center gap-2 mb-8 flex-wrap">
          <button onClick={() => setView("calendar")} className={view === "calendar" ? "btn-primary" : "btn-secondary"}>
            <Calendar size={16} /> Calendar
          </button>
          <button onClick={() => setView("companies")} className={view === "companies" ? "btn-primary" : "btn-secondary"}>
            <Building2 size={16} /> Companies ({companies.length || "140+"})
          </button>
          <button onClick={() => setView("ideas")} className={view === "ideas" ? "btn-primary" : "btn-secondary"}>
            <Lightbulb size={16} /> What job seekers pay for
          </button>
        </div>

        {view === "calendar" && (
          <div>
            <div className="flex flex-wrap gap-2 justify-center mb-6">
              <button onClick={() => setActiveMonth(null)} className={!activeMonth ? "btn-primary" : "btn-secondary"}>All months</button>
              {months.map((m) => (
                <button key={m} onClick={() => setActiveMonth(activeMonth === m ? null : m)}
                  className={activeMonth === m ? "btn-primary" : "btn-secondary"}>{m}</button>
              ))}
            </div>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {(activeMonth ? [activeMonth] : months).map((m) => (
                <div key={m} className="card">
                  <h3 className="font-display font-bold text-text-primary text-lg mb-3 flex items-center gap-2">
                    <Clock size={16} className="text-cyber-blue" /> {m}
                  </h3>
                  <div className="space-y-3">
                    {(calendar[m] || []).map((ev, i) => (
                      <div key={i} className="rounded-lg border border-space-border bg-space-panel/60 p-3">
                        <div className="flex items-center justify-between mb-1">
                          <span className="font-mono text-xs text-text-primary">{ev.title}</span>
                          <span className={`text-[10px] px-2 py-0.5 rounded-full border ${KIND_COLORS[ev.kind] || "border-gray-500/30 text-gray-400"}`}>{ev.kind}</span>
                        </div>
                        <div className="flex flex-wrap gap-1 mb-1">
                          {ev.companies.map((c) => (
                            <button key={c} onClick={() => openCompany(c)} className="text-[11px] text-cyber-blue hover:underline">{c}</button>
                          ))}
                        </div>
                        <p className="text-[11px] text-gray-500 font-mono">{ev.note}</p>
                      </div>
                    ))}
                    {(!calendar[m] || calendar[m].length === 0) && <p className="text-xs text-gray-600">No tracked events.</p>}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {view === "companies" && (
          <div>
            <div className="flex flex-col md:flex-row gap-2 mb-6">
              <div className="flex items-center gap-2 flex-1 bg-space-panel border border-space-border rounded-lg px-3">
                <Search size={16} className="text-gray-500" />
                <input value={q} onChange={(e) => setQ(e.target.value)} onKeyDown={(e) => e.key === "Enter" && loadCompanies()} placeholder="Search company, role, skill…"
                  className="flex-1 bg-transparent py-2 text-sm text-gray-200 focus:outline-none" />
              </div>
              <select value={type} onChange={(e) => setType(e.target.value)} className="bg-space-panel border border-space-border rounded-lg px-3 py-2 text-sm text-gray-200">
                <option value="">All types</option>
                {filters.types.map((t) => <option key={t} value={t}>{t}</option>)}
              </select>
              <select value={tier} onChange={(e) => setTier(e.target.value)} className="bg-space-panel border border-space-border rounded-lg px-3 py-2 text-sm text-gray-200">
                <option value="">All tiers</option>
                {filters.tiers.map((t) => <option key={t} value={t}>{t}</option>)}
              </select>
              <select value={month} onChange={(e) => setMonth(e.target.value)} className="bg-space-panel border border-space-border rounded-lg px-3 py-2 text-sm text-gray-200">
                <option value="">All months</option>
                {filters.months.map((m) => <option key={m} value={m}>{m}</option>)}
              </select>
              <button onClick={loadCompanies} className="btn-primary">{loading ? "…" : "Search"}</button>
            </div>

            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {companies.map((c) => (
                <button key={c.id} onClick={() => openCompany(c.id)} className="card text-left hover:border-cyber-blue/50 transition-colors">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-display font-bold text-text-primary">{c.name}</h3>
                    <span className="text-[10px] px-2 py-0.5 rounded-full border border-space-border text-gray-400">{c.tier}</span>
                  </div>
                  <p className="text-xs text-gray-500 font-mono mb-2">{c.type} · {c.calendar_window}</p>
                  <div className="flex flex-wrap gap-1">
                    {c.focus_areas.slice(0, 4).map((f) => (
                      <span key={f} className="text-[10px] px-2 py-0.5 rounded-full bg-cyber-blue/10 text-cyber-blue">{f}</span>
                    ))}
                  </div>
                  {progressMap[c.id] && progressMap[c.id].total > 0 && (
                    <p className="text-[10px] mt-2 text-cyber-green font-mono">
                      ✓ {progressMap[c.id].done}/{progressMap[c.id].total} prepared
                    </p>
                  )}
                </button>
              ))}
            </div>
            {companies.length === 0 && !loading && (
              <p className="text-center text-gray-500 mt-10">No companies match. Try clearing filters.</p>
            )}
          </div>
        )}

        {view === "ideas" && (
          <div className="max-w-4xl mx-auto">
            <p className="text-center text-gray-400 text-sm mb-6">Unique, high-intent things job seekers gladly pay for — beyond a flat subscription. Each is a leverage point for ARR.</p>
            <div className="grid sm:grid-cols-2 gap-4">
              {PREMIUM_IDEAS.map((idea) => (
                <div key={idea.title} className="card">
                  <div className="flex items-start justify-between gap-2">
                    <h3 className="font-display font-bold text-text-primary flex items-center gap-2"><Sparkles size={14} className="text-cyber-green" /> {idea.title}</h3>
                    <span className="text-[11px] px-2 py-0.5 rounded-full bg-cyber-green/10 text-cyber-green whitespace-nowrap">{idea.price}</span>
                  </div>
                  <p className="text-xs text-gray-400 mt-2 font-mono">{idea.desc}</p>
                </div>
              ))}
            </div>
            <div className="text-center mt-8">
              <a href="/pricing" className="btn-primary inline-flex items-center gap-2"><ArrowRight size={16} /> See Pro & Bundles</a>
            </div>
          </div>
        )}
      </div>

      {selected && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-surface-2" onClick={closeCompany}>
          <div className="card max-w-2xl w-full max-h-[88vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
              <div className="sticky top-0 bg-space-panel/95 backdrop-blur flex items-start justify-between mb-4 p-4 -m-4 mb-4 border-b border-space-border">
              <div>
                <h2 className="font-display font-bold text-2xl text-text-primary">{selected.name}</h2>
                <p className="text-xs text-gray-500 font-mono">{selected.type} · {selected.tier} · {selected.calendar_window}</p>
                <div className="flex items-center gap-1 mt-1 text-[11px] text-gray-500">
                  <Link2 size={11} /> Shareable: <span className="text-cyber-blue">/placement-calendar?company={selected.id}</span>
                </div>
              </div>
              <button onClick={closeCompany} className="text-gray-400 hover:text-white"><X size={20} /></button>
            </div>

            <Section icon={<Target size={14} className="text-cyber-blue" />} title="What they ask">
              <ul className="space-y-1">
                {selected.what_they_ask.map((w, i) => <li key={i} className="text-sm text-gray-300 font-mono flex gap-2"><span className="text-cyber-blue">▹</span>{w}</li>)}
              </ul>
            </Section>

            <Section icon={<Clock size={14} className="text-cyber-green" />} title="How the interview goes">
              <ol className="space-y-1">
                {selected.interview_process.map((r, i) => <li key={i} className="text-sm text-gray-300 font-mono">{i + 1}. {r}</li>)}
              </ol>
            </Section>

            <Section icon={<GraduationCap size={14} className="text-purple-300" />} title="Free prep checklist (A → Z)">
              <div className="space-y-1">
                {selected.focus_areas.map((f) => {
                  const lesson = lessonFor(f);
                  const key = `${selected.id}:${f}`;
                  if (!lesson) return <div key={f} className="text-sm text-gray-300 font-mono">• {f}</div>;
                  return (
                    <label key={f} className="flex items-center gap-2 text-sm text-gray-300 font-mono cursor-pointer">
                      <input type="checkbox" checked={!!checked[key]}
                        onChange={() => setChecked((c) => {
                          const next = { ...c, [key]: !c[key] };
                          const completed = (selected.focus_areas || []).filter((fa: string) => next[`${selected.id}:${fa}`]);
                          api.companyDirectory.saveProgress(selected.id, completed).catch(() => {});
                          return next;
                        })} className="accent-cyber-blue" />
                      <span className={checked[key] ? "line-through text-gray-500" : ""}>{f} →</span>
                      <a href={lesson.route} className="text-cyber-blue hover:underline inline-flex items-center gap-1">{lesson.label} <ArrowRight size={10} /></a>
                    </label>
                  );
                })}
              </div>
            </Section>

            <Section icon={<Sparkles size={14} className="text-cyber-green" />} title={`Go Pro to unlock — ${selected.name} prep`}>
              <div className="space-y-2">
                {premiumOffersFor(selected).map((o) => (
                  <div key={o.title} className="flex items-center justify-between gap-2 rounded-lg border border-space-border bg-space-panel/60 p-2">
                    <div>
                      <p className="text-sm text-text-primary">{o.title}</p>
                      <p className="text-[11px] text-gray-500 font-mono">{o.desc}</p>
                    </div>
                    <a href="/pricing" className="text-[11px] px-2 py-1 rounded-full bg-cyber-green/10 text-cyber-green border border-cyber-green/30 hover:bg-cyber-green/20 whitespace-nowrap">{o.price}</a>
                  </div>
                ))}
              </div>
            </Section>

            <div className="mt-4 p-3 rounded-lg bg-cyber-green/10 border border-cyber-green/20">
              <p className="text-xs text-cyber-green font-mono">💡 {selected.tips}</p>
            </div>

            <a href="/referral" className="block mt-3 p-3 rounded-lg bg-cyber-blue/10 border border-cyber-blue/30 hover:bg-cyber-blue/20 transition-colors">
              <p className="text-sm text-cyber-blue font-display font-bold flex items-center gap-2"><Link2 size={14} /> Invite a friend — you both get 1 month Pro free</p>
              <p className="text-[11px] text-gray-400 font-mono mt-1">Turn your prep into a streak. Share your referral link and unlock Pro features for free.</p>
            </a>
            <div className="mt-3 flex flex-wrap gap-1">
              {selected.roles.map((r) => <span key={r} className="text-[10px] px-2 py-0.5 rounded-full bg-space-panel text-gray-400">{r}</span>)}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function Section({ icon, title, children }: { icon: ReactNode; title: string; children: ReactNode }) {
  return (
    <div className="mb-4">
      <h4 className="font-display font-bold text-sm text-text-primary mb-2 flex items-center gap-2">{icon} {title}</h4>
      {children}
    </div>
  );
}
