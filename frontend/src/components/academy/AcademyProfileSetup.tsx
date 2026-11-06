import { useEffect, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { CheckCircle2, ChevronDown, GraduationCap, Save, Target } from "lucide-react";
import api from "../services/api";

const companies = [
  ["tcs", "TCS"], ["infosys", "Infosys"], ["accenture", "Accenture"],
  ["wipro", "Wipro"], ["cognizant", "Cognizant"], ["capgemini", "Capgemini"],
  ["hcltech", "HCLTech"], ["tech_mahindra", "Tech Mahindra"],
];

const initialProfile = {
  target_role: "software_engineer",
  target_companies: ["tcs", "infosys", "accenture"],
  experience_level: "absolute_beginner",
  preferred_language: "cpp",
  daily_minutes: 60,
  placement_date: "",
  learning_preference: "mixed",
  timezone: "Asia/Kolkata",
};

export default function AcademyProfileSetup() {
  const queryClient = useQueryClient();
  const [profile, setProfile] = useState(initialProfile);
  const [saved, setSaved] = useState(false);
  const { data, isLoading } = useQuery({
    queryKey: ["academy", "learner-profile"],
    queryFn: () => api.academy.getProfile(),
    staleTime: 60_000,
  });

  useEffect(() => {
    const existing = (data as any)?.data?.profile;
    if (existing) {
      setProfile({ ...initialProfile, ...existing, placement_date: existing.placement_date || "" });
    }
  }, [data]);

  const mutation = useMutation({
    mutationFn: () => api.academy.saveProfile({
      ...profile,
      placement_date: profile.placement_date || null,
    }),
    onSuccess: async () => {
      setSaved(true);
      await queryClient.invalidateQueries({ queryKey: ["academy", "learner-profile"] });
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

  if (isLoading) return null;

  return (
    <section className="rounded-3xl border border-emerald-200 bg-white p-5 shadow-sm sm:p-6">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="flex items-center gap-2 text-xs font-bold uppercase tracking-[0.16em] text-emerald-700">
            <Target size={14} /> Your learning profile
          </p>
          <h2 className="mt-2 text-xl font-black text-slate-900">Build your placement path around your goal</h2>
          <p className="mt-1 max-w-2xl text-sm text-slate-600">
            These settings will shape your diagnostic, lesson order, daily workload and company practice.
          </p>
        </div>
        <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-800">
          <GraduationCap className="mr-1 inline" size={14} /> Personalization
        </span>
      </div>

      <div className="mt-5 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <label className="text-sm font-semibold text-slate-700">Target role
          <select className="mt-1.5 w-full rounded-xl border border-slate-200 bg-white p-3 font-normal" value={profile.target_role} onChange={(e) => update("target_role", e.target.value)}>
            <option value="software_engineer">Software Engineer / SDE</option>
            <option value="full_stack_developer">Full-stack Developer</option>
            <option value="backend_developer">Backend Developer</option>
            <option value="frontend_developer">Frontend Developer</option>
            <option value="qa_engineer">QA Engineer</option>
            <option value="data_analyst">Data Analyst</option>
            <option value="devops_engineer">DevOps Engineer</option>
            <option value="support_engineer">Support Engineer</option>
            <option value="undecided">I'm exploring</option>
          </select>
        </label>
        <label className="text-sm font-semibold text-slate-700">Current level
          <select className="mt-1.5 w-full rounded-xl border border-slate-200 bg-white p-3 font-normal" value={profile.experience_level} onChange={(e) => update("experience_level", e.target.value)}>
            <option value="absolute_beginner">Starting from zero</option>
            <option value="beginner">Know the basics</option>
            <option value="intermediate">Can solve easy problems</option>
            <option value="advanced">Already placement-ready in some areas</option>
          </select>
        </label>
        <label className="text-sm font-semibold text-slate-700">Preferred coding language
          <select className="mt-1.5 w-full rounded-xl border border-slate-200 bg-white p-3 font-normal" value={profile.preferred_language} onChange={(e) => update("preferred_language", e.target.value)}>
            <option value="cpp">C++</option><option value="java">Java</option><option value="python">Python</option><option value="c">C</option><option value="javascript">JavaScript</option>
          </select>
        </label>
        <label className="text-sm font-semibold text-slate-700">Daily study time
          <select className="mt-1.5 w-full rounded-xl border border-slate-200 bg-white p-3 font-normal" value={profile.daily_minutes} onChange={(e) => update("daily_minutes", Number(e.target.value))}>
            <option value={30}>30 minutes</option><option value={45}>45 minutes</option><option value={60}>1 hour</option><option value={90}>1.5 hours</option><option value={120}>2 hours</option><option value={180}>3 hours</option>
          </select>
        </label>
        <label className="text-sm font-semibold text-slate-700">Expected placement date
          <input type="date" className="mt-1.5 w-full rounded-xl border border-slate-200 bg-white p-3 font-normal" min={new Date().toISOString().slice(0, 10)} value={profile.placement_date} onChange={(e) => update("placement_date", e.target.value)} />
        </label>
        <label className="text-sm font-semibold text-slate-700">Learning style
          <select className="mt-1.5 w-full rounded-xl border border-slate-200 bg-white p-3 font-normal" value={profile.learning_preference} onChange={(e) => update("learning_preference", e.target.value)}>
            <option value="mixed">A mix of everything</option><option value="examples_first">Examples first</option><option value="hands_on">Hands-on practice</option><option value="visual">Visual explanations</option><option value="reading">Detailed reading</option>
          </select>
        </label>
      </div>

      <div className="mt-5">
        <p className="mb-2 text-sm font-semibold text-slate-700">Companies you want to prepare for</p>
        <div className="flex flex-wrap gap-2">
          {companies.map(([id, label]) => (
            <button key={id} type="button" onClick={() => toggleCompany(id)} className={`rounded-full border px-3 py-2 text-sm font-medium transition ${profile.target_companies.includes(id) ? "border-emerald-600 bg-emerald-50 text-emerald-800" : "border-slate-200 bg-white text-slate-600 hover:border-slate-400"}`}>
              {profile.target_companies.includes(id) && <CheckCircle2 className="mr-1 inline" size={14} />}{label}
            </button>
          ))}
        </div>
      </div>

      <div className="mt-5 flex flex-wrap items-center gap-3">
        <button type="button" disabled={mutation.isPending || profile.target_companies.length === 0} onClick={() => mutation.mutate()} className="inline-flex items-center gap-2 rounded-xl bg-emerald-700 px-5 py-3 text-sm font-bold text-white transition hover:bg-emerald-800 disabled:cursor-not-allowed disabled:opacity-50">
          <Save size={16} /> {mutation.isPending ? "Saving..." : "Save my learning profile"}
        </button>
        {saved && <span className="text-sm font-medium text-emerald-700">Profile saved. Your learning path can now use these preferences.</span>}
        {mutation.isError && <span role="alert" className="text-sm text-red-600">Could not save your profile. Please try again.</span>}
      </div>
    </section>
  );
}
