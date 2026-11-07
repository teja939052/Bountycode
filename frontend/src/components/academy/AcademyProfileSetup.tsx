import { useEffect, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { ArrowLeft, ArrowRight, CheckCircle2, ClipboardCheck, GraduationCap, Save, ShieldCheck, Target } from "lucide-react";
import api from "../../services/api";

const companies = [
  ["tcs", "TCS"], ["infosys", "Infosys"], ["accenture", "Accenture"],
  ["wipro", "Wipro"], ["cognizant", "Cognizant"], ["capgemini", "Capgemini"],
  ["hcltech", "HCLTech"], ["tech_mahindra", "Tech Mahindra"],
] as const;

const tracks = [
  ["service_company_core", "Service-company core", "A balanced foundation for multiple employers"],
  ["tcs_foundation", "TCS Foundation", "Numerical, verbal and reasoning readiness"],
  ["tcs_advanced", "TCS Advanced", "Advanced aptitude, reasoning and coding"],
  ["infosys_infytq", "Infosys InfyTQ", "Programming, DBMS/SQL, aptitude and OOP/DSA"],
  ["hackwithinfy", "HackWithInfy", "Timed competitive-coding endurance"],
  ["wipro", "Wipro WILP / NTH", "Verbal, analytical, quantitative and writing practice"],
  ["accenture", "Accenture campus", "Cognitive, technical, coding and communication"],
  ["cognizant", "Cognizant GenC", "Communication, aptitude and role-based technical skills"],
] as const;

const initialProfile = {
  target_role: "software_engineer",
  target_companies: ["tcs", "infosys", "accenture"],
  assessment_track: "service_company_core",
  assessment_date: "",
  experience_level: "absolute_beginner",
  preferred_language: "cpp",
  daily_minutes: 60,
  weekly_days: 5,
  device_type: "laptop",
  local_runtime_available: true,
  accessibility_needs: "",
  placement_date: "",
  learning_preference: "mixed",
  timezone: "Asia/Kolkata",
};

const steps = [
  { title: "Choose the mission", detail: "Company, role and assessment" },
  { title: "Set your reality", detail: "Level, time and environment" },
  { title: "Make it sustainable", detail: "Learning style and access" },
];

export default function AcademyProfileSetup() {
  const queryClient = useQueryClient();
  const [profile, setProfile] = useState(initialProfile);
  const [step, setStep] = useState(0);
  const [saved, setSaved] = useState(false);
  const { data, isLoading, isError, refetch, isFetching } = useQuery({
    queryKey: ["academy", "learner-profile"],
    queryFn: () => api.academy.getProfile(),
    staleTime: 60_000,
    retry: 1,
  });

  useEffect(() => {
    const existing = (data as any)?.profile;
    if (existing) {
      setProfile({ ...initialProfile, ...existing, assessment_date: existing.assessment_date || "", placement_date: existing.placement_date || "" });
    }
  }, [data]);

  const mutation = useMutation({
    mutationFn: () => api.academy.saveProfile({
      ...profile,
      assessment_date: profile.assessment_date || null,
      placement_date: profile.placement_date || null,
    }),
    onSuccess: async () => {
      setSaved(true);
      await Promise.all([
        queryClient.invalidateQueries({ queryKey: ["academy", "learner-profile"] }),
        queryClient.invalidateQueries({ queryKey: ["academy", "plan"] }),
        queryClient.invalidateQueries({ queryKey: ["journey"] }),
      ]);
    },
  });

  const update = (key: string, value: any) => {
    setSaved(false);
    setProfile((current) => ({ ...current, [key]: value }));
  };
  const toggleCompany = (id: string) => {
    const next = profile.target_companies.includes(id)
      ? profile.target_companies.filter((company) => company !== id)
      : [...profile.target_companies, id];
    update("target_companies", next);
  };
  const canContinue = step === 0 ? profile.target_companies.length > 0 && Boolean(profile.target_role) : true;

  if (isLoading) return null;
  if (isError) return (
    <section className="rounded-3xl border border-amber-200 bg-white p-5 shadow-sm sm:p-6" aria-live="polite">
      <p className="font-bold text-slate-900">Your learning profile could not load</p>
      <p className="mt-1 text-sm text-slate-600">Your saved preferences have not been changed. Retry before editing so an existing profile is not accidentally replaced.</p>
      <button type="button" onClick={() => void refetch()} disabled={isFetching} className="mt-3 inline-flex min-h-10 items-center rounded-xl bg-emerald-700 px-4 py-2 text-sm font-semibold text-white disabled:opacity-60">{isFetching ? "Retrying…" : "Retry profile load"}</button>
    </section>
  );

  return (
    <section className="rounded-3xl border border-emerald-200 bg-white p-5 shadow-sm sm:p-6">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="flex items-center gap-2 text-xs font-bold uppercase tracking-[0.16em] text-emerald-700"><Target size={14} /> Placement onboarding</p>
          <h2 className="mt-2 text-xl font-black text-slate-900">Build a preparation system around your actual goal</h2>
          <p className="mt-1 max-w-2xl text-sm text-slate-600">We use these signals to choose levels, diagnostic coverage, daily workload, revision and employer-style mocks. Your self-report is a starting hypothesis; assessments update the plan.</p>
        </div>
        <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-800"><GraduationCap className="mr-1 inline" size={14} /> Personalization</span>
      </div>

      <div className="mt-5 grid gap-2 sm:grid-cols-3" aria-label="Onboarding steps">
        {steps.map((item, index) => (
          <button key={item.title} type="button" onClick={() => index <= step && setStep(index)} className={`rounded-2xl border p-3 text-left transition ${index === step ? "border-emerald-500 bg-emerald-50" : index < step ? "border-emerald-200 bg-white" : "border-slate-200 bg-slate-50"}`}>
            <span className="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-emerald-700">{index < step ? <CheckCircle2 size={13} /> : `0${index + 1}`} {item.title}</span>
            <span className="mt-1 block text-xs text-slate-500">{item.detail}</span>
          </button>
        ))}
      </div>

      {step === 0 && (
        <div className="mt-5 space-y-5">
          <div className="grid gap-4 sm:grid-cols-2">
            <label className="text-sm font-semibold text-slate-700">Target role
              <select className="mt-1.5 w-full rounded-xl border border-slate-200 bg-white p-3 font-normal" value={profile.target_role} onChange={(e) => update("target_role", e.target.value)}>
                <option value="software_engineer">Software Engineer / SDE</option><option value="full_stack_developer">Full-stack Developer</option><option value="backend_developer">Backend Developer</option><option value="frontend_developer">Frontend Developer</option><option value="qa_engineer">QA Engineer</option><option value="data_analyst">Data Analyst</option><option value="devops_engineer">DevOps Engineer</option><option value="support_engineer">Support Engineer</option><option value="undecided">I'm exploring</option>
              </select>
            </label>
            <label className="text-sm font-semibold text-slate-700">Preparation track
              <select className="mt-1.5 w-full rounded-xl border border-slate-200 bg-white p-3 font-normal" value={profile.assessment_track} onChange={(e) => update("assessment_track", e.target.value)}>
                {tracks.map(([id, label]) => <option key={id} value={id}>{label}</option>)}
              </select>
            </label>
          </div>
          <div>
            <p className="mb-2 text-sm font-semibold text-slate-700">Which employers are you targeting?</p>
            <div className="flex flex-wrap gap-2">{companies.map(([id, label]) => <button key={id} type="button" onClick={() => toggleCompany(id)} className={`rounded-full border px-3 py-2 text-sm font-medium transition ${profile.target_companies.includes(id) ? "border-emerald-600 bg-emerald-50 text-emerald-800" : "border-slate-200 bg-white text-slate-600 hover:border-slate-400"}`}>{profile.target_companies.includes(id) && <CheckCircle2 className="mr-1 inline" size={14} />}{label}</button>)}</div>
            <p className="mt-2 text-xs text-slate-500">Select more than one if you need a shared foundation. The assessment track controls the emphasis; the current official invitation remains the source of truth.</p>
          </div>
          <div className="grid gap-4 sm:grid-cols-2">
            <label className="text-sm font-semibold text-slate-700">Assessment date, if known<input type="date" className="mt-1.5 w-full rounded-xl border border-slate-200 bg-white p-3 font-normal" min={new Date().toISOString().slice(0, 10)} value={profile.assessment_date} onChange={(e) => update("assessment_date", e.target.value)} /></label>
            <label className="text-sm font-semibold text-slate-700">Expected placement season<input type="date" className="mt-1.5 w-full rounded-xl border border-slate-200 bg-white p-3 font-normal" min={new Date().toISOString().slice(0, 10)} value={profile.placement_date} onChange={(e) => update("placement_date", e.target.value)} /></label>
          </div>
        </div>
      )}

      {step === 1 && (
        <div className="mt-5 space-y-5">
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <label className="text-sm font-semibold text-slate-700">Current level<select className="mt-1.5 w-full rounded-xl border border-slate-200 bg-white p-3 font-normal" value={profile.experience_level} onChange={(e) => update("experience_level", e.target.value)}><option value="absolute_beginner">Starting from zero</option><option value="beginner">Know the basics</option><option value="intermediate">Can solve easy problems</option><option value="advanced">Placement-ready in some areas</option></select></label>
            <label className="text-sm font-semibold text-slate-700">Preferred language<select className="mt-1.5 w-full rounded-xl border border-slate-200 bg-white p-3 font-normal" value={profile.preferred_language} onChange={(e) => update("preferred_language", e.target.value)}><option value="cpp">C++</option><option value="java">Java</option><option value="python">Python</option><option value="c">C</option><option value="javascript">JavaScript</option></select></label>
            <label className="text-sm font-semibold text-slate-700">Minutes per study day<select className="mt-1.5 w-full rounded-xl border border-slate-200 bg-white p-3 font-normal" value={profile.daily_minutes} onChange={(e) => update("daily_minutes", Number(e.target.value))}><option value={30}>30</option><option value={45}>45</option><option value={60}>60</option><option value={90}>90</option><option value={120}>120</option><option value={180}>180</option></select></label>
            <label className="text-sm font-semibold text-slate-700">Study days per week<select className="mt-1.5 w-full rounded-xl border border-slate-200 bg-white p-3 font-normal" value={profile.weekly_days} onChange={(e) => update("weekly_days", Number(e.target.value))}>{[1, 2, 3, 4, 5, 6, 7].map((day) => <option key={day} value={day}>{day} days</option>)}</select></label>
          </div>
          <div className="rounded-2xl border border-sky-200 bg-sky-50 p-4"><p className="flex items-center gap-2 text-sm font-bold text-sky-900"><ClipboardCheck size={16} /> Your diagnostic will overrule guesses</p><p className="mt-1 text-sm text-sky-800">We will test aptitude, reasoning, verbal, programming, SQL and core CS, then re-test weak skills after practice. Points and streaks never substitute for evidence.</p></div>
          <label className="text-sm font-semibold text-slate-700">Primary study device<select className="mt-1.5 w-full rounded-xl border border-slate-200 bg-white p-3 font-normal" value={profile.device_type} onChange={(e) => update("device_type", e.target.value)}><option value="laptop">Laptop</option><option value="desktop">Desktop</option><option value="mobile_only">Mobile only for now</option></select></label>
          <label className="flex items-center gap-3 rounded-xl border border-slate-200 p-3 text-sm text-slate-700"><input type="checkbox" checked={profile.local_runtime_available} onChange={(e) => update("local_runtime_available", e.target.checked)} /> I can run code locally when an optional coding runtime is useful</label>
        </div>
      )}

      {step === 2 && (
        <div className="mt-5 space-y-5">
          <div className="grid gap-4 sm:grid-cols-2">
            <label className="text-sm font-semibold text-slate-700">How should lessons feel?<select className="mt-1.5 w-full rounded-xl border border-slate-200 bg-white p-3 font-normal" value={profile.learning_preference} onChange={(e) => update("learning_preference", e.target.value)}><option value="mixed">A mix of explanation and practice</option><option value="examples_first">Examples first</option><option value="hands_on">Hands-on practice</option><option value="visual">Visual explanations</option><option value="reading">Detailed reading</option></select></label>
            <label className="text-sm font-semibold text-slate-700">Accessibility or study needs (optional)<input className="mt-1.5 w-full rounded-xl border border-slate-200 bg-white p-3 font-normal" maxLength={240} value={profile.accessibility_needs} onChange={(e) => update("accessibility_needs", e.target.value)} placeholder="e.g. larger text, low bandwidth, screen reader" /></label>
          </div>
          <div className="grid gap-3 sm:grid-cols-3"><div className="rounded-2xl bg-emerald-50 p-4"><ShieldCheck className="text-emerald-700" size={18} /><p className="mt-2 text-sm font-bold text-slate-900">Transparent</p><p className="mt-1 text-xs text-slate-600">Every next task will explain why it was selected.</p></div><div className="rounded-2xl bg-indigo-50 p-4"><Target className="text-indigo-700" size={18} /><p className="mt-2 text-sm font-bold text-slate-900">Evidence-led</p><p className="mt-1 text-xs text-slate-600">Mastery needs repeated success and delayed review.</p></div><div className="rounded-2xl bg-amber-50 p-4"><GraduationCap className="text-amber-700" size={18} /><p className="mt-2 text-sm font-bold text-slate-900">Low-cost</p><p className="mt-1 text-xs text-slate-600">Core preparation works without AI or a paid compiler.</p></div></div>
        </div>
      )}

      <div className="mt-6 flex flex-wrap items-center justify-between gap-3 border-t border-slate-100 pt-4">
        <button type="button" onClick={() => setStep((current) => Math.max(0, current - 1))} disabled={step === 0} className="inline-flex min-h-11 items-center gap-2 rounded-xl border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-700 disabled:invisible"><ArrowLeft size={15} /> Back</button>
        <div className="flex flex-wrap items-center gap-3">
          {step < steps.length - 1 ? <button type="button" disabled={!canContinue} onClick={() => setStep((current) => Math.min(steps.length - 1, current + 1))} className="inline-flex min-h-11 items-center gap-2 rounded-xl bg-emerald-700 px-5 py-3 text-sm font-bold text-white disabled:cursor-not-allowed disabled:opacity-50">Continue <ArrowRight size={15} /></button> : <button type="button" disabled={mutation.isPending || profile.target_companies.length === 0} onClick={() => mutation.mutate()} className="inline-flex min-h-11 items-center gap-2 rounded-xl bg-emerald-700 px-5 py-3 text-sm font-bold text-white transition hover:bg-emerald-800 disabled:cursor-not-allowed disabled:opacity-50"><Save size={16} /> {mutation.isPending ? "Saving your path…" : "Save and build my path"}</button>}
          {saved && <span className="text-sm font-medium text-emerald-700">Saved. Your diagnostic and plan are now aligned.</span>}
          {mutation.isError && <span role="alert" className="text-sm text-red-600">Could not save your profile. Please try again.</span>}
        </div>
      </div>
    </section>
  );
}
