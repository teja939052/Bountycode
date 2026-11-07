import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  ArrowRight,
  BarChart3,
  BrainCircuit,
  Check,
  ChevronDown,
  CircleDot,
  Clock3,
  Crosshair,
  Gauge,
  LockKeyhole,
  Radar,
  ShieldCheck,
  Sparkles,
  Target,
  TimerReset,
  Trophy,
  Users,
  Zap,
} from "lucide-react";
import useAuthStore from "../store/authStore";

const TARGETS = [
  { id: "tcs", label: "TCS", mode: "Foundation → Advanced", color: "#20c997" },
  { id: "wipro", label: "Wipro", mode: "WILP / NTH", color: "#7c5cff" },
  { id: "accenture", label: "Accenture", mode: "Campus track", color: "#ff8a3d" },
  { id: "infosys", label: "Infosys", mode: "InfyTQ / coding", color: "#3b82f6" },
];

const ROLES = ["Software Engineer", "QA Engineer", "Data Analyst", "Support Engineer"];

const LOOP = [
  { number: "01", title: "Map the gap", body: "A short server-graded diagnostic measures accuracy, speed and confidence across the skills your target track actually tests.", icon: Radar, color: "#20c997" },
  { number: "02", title: "Build the weak link", body: "Your level path turns weak areas into small missions: learn, retrieve, practise, then revisit after time has passed.", icon: BrainCircuit, color: "#7c5cff" },
  { number: "03", title: "Prove under pressure", body: "Run a versioned company-style OA, review section evidence, and get the next repair mission—not a vague score.", icon: TimerReset, color: "#ff8a3d" },
];

const COMPANY_NOTES = [
  { name: "TCS", detail: "Foundation + Advanced", accent: "#20c997", tag: "75 / 115 min tracks" },
  { name: "Wipro", detail: "WILP / NTH practice", accent: "#7c5cff", tag: "Aptitude + communication" },
  { name: "Accenture", detail: "Campus preparation", accent: "#ff8a3d", tag: "Cognitive + technical" },
];

function ReadinessCockpit({ target, role }: { target: typeof TARGETS[number]; role: string }) {
  return (
    <div className="relative mx-auto w-full max-w-[560px]">
      <div className="absolute -inset-5 rounded-[2.5rem] bg-[#20c997]/10 blur-3xl" aria-hidden="true" />
      <div className="relative overflow-hidden rounded-[2rem] border border-white/10 bg-[#111816] p-4 text-white shadow-[0_30px_100px_rgba(8,27,21,0.3)] sm:p-5">
        <div className="flex items-center justify-between border-b border-white/10 pb-4">
          <div className="flex items-center gap-2.5"><div className="flex h-8 w-8 items-center justify-center rounded-xl bg-[#20c997] text-[#07110e]"><Crosshair size={16} /></div><div><p className="font-mono text-[9px] uppercase tracking-[0.2em] text-white/45">Bountycode / cockpit</p><p className="text-sm font-black">{target.label} readiness system</p></div></div>
          <span className="rounded-full border border-[#20c997]/30 bg-[#20c997]/10 px-2.5 py-1 font-mono text-[9px] font-bold text-[#6af0c4]">LIVE PLAN</span>
        </div>
        <div className="mt-5 grid gap-3 sm:grid-cols-[1.1fr_.9fr]">
          <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-4">
            <div className="flex items-start justify-between"><div><p className="font-mono text-[9px] uppercase tracking-[0.18em] text-white/45">Current mission</p><h3 className="mt-1 text-xl font-black">Repair logical reasoning</h3><p className="mt-1 text-xs text-white/50">For {role} · {target.mode}</p></div><div className="rounded-xl bg-[#ff8a3d]/15 p-2 text-[#ffad7b]"><Target size={17} /></div></div>
            <div className="mt-5 h-2 overflow-hidden rounded-full bg-white/10"><div className="h-full w-[68%] rounded-full bg-gradient-to-r from-[#20c997] to-[#ffcc66]" /></div>
            <div className="mt-2 flex justify-between font-mono text-[9px] text-white/45"><span>Evidence collected</span><span>68%</span></div>
            <div className="mt-5 flex items-center gap-2 text-xs text-white/65"><Check size={14} className="text-[#20c997]" /> 3 lessons completed <span className="text-white/20">·</span> <Clock3 size={13} className="text-[#ffcc66]" /> 18 min</div>
          </div>
          <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-4"><p className="font-mono text-[9px] uppercase tracking-[0.18em] text-white/45">Readiness signal</p><div className="mt-3 flex items-center gap-4"><div className="relative flex h-20 w-20 items-center justify-center rounded-full" style={{ background: "conic-gradient(#20c997 0 71%, rgba(255,255,255,.08) 71% 100%)" }}><div className="flex h-[62px] w-[62px] items-center justify-center rounded-full bg-[#111816]"><span className="text-xl font-black">71</span></div></div><div><p className="text-sm font-black text-[#6af0c4]">Building</p><p className="mt-1 text-[11px] leading-4 text-white/50">Timed mock unlocks after two more proof checks.</p></div></div><div className="mt-5 flex items-center gap-2 rounded-xl bg-[#20c997]/10 p-2.5 text-[10px] font-semibold text-[#a6f7dc]"><ShieldCheck size={13} /> Evidence, not streaks, moves the signal.</div></div>
        </div>
        <div className="mt-3 grid grid-cols-3 gap-2"><div className="rounded-xl bg-white/[0.04] p-3"><p className="font-mono text-[9px] text-white/40">ACCURACY</p><p className="mt-1 text-lg font-black">74%</p></div><div className="rounded-xl bg-white/[0.04] p-3"><p className="font-mono text-[9px] text-white/40">CONFIDENCE</p><p className="mt-1 text-lg font-black">61%</p></div><div className="rounded-xl bg-white/[0.04] p-3"><p className="font-mono text-[9px] text-white/40">NEXT CHECK</p><p className="mt-1 text-lg font-black">2 days</p></div></div>
      </div>
    </div>
  );
}

function TargetPicker({ target, setTarget, role, setRole }: { target: typeof TARGETS[number]; setTarget: (target: typeof TARGETS[number]) => void; role: string; setRole: (role: string) => void }) {
  return (
    <div className="rounded-[1.5rem] border border-[#d8e7df] bg-white p-3 shadow-[0_15px_45px_rgba(10,55,38,0.08)] sm:p-4">
      <div className="grid gap-3 lg:grid-cols-[1fr_1fr_auto] lg:items-end">
        <label className="block"><span className="mb-1.5 block font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-[#567064]">I’m preparing for</span><div className="relative"><select value={target.id} onChange={(event) => setTarget(TARGETS.find((item) => item.id === event.target.value) || TARGETS[0])} className="w-full appearance-none rounded-xl border border-[#d8e7df] bg-[#f6fbf8] px-3.5 py-3 text-sm font-bold text-[#10241c] outline-none focus:border-[#20a77d]"><option value="tcs">TCS</option><option value="wipro">Wipro</option><option value="accenture">Accenture</option><option value="infosys">Infosys</option></select><ChevronDown size={16} className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-[#567064]" /></div></label>
        <label className="block"><span className="mb-1.5 block font-mono text-[9px] font-bold uppercase tracking-[0.16em] text-[#567064]">Target role</span><div className="relative"><select value={role} onChange={(event) => setRole(event.target.value)} className="w-full appearance-none rounded-xl border border-[#d8e7df] bg-[#f6fbf8] px-3.5 py-3 text-sm font-bold text-[#10241c] outline-none focus:border-[#20a77d]">{ROLES.map((item) => <option key={item}>{item}</option>)}</select><ChevronDown size={16} className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-[#567064]" /></div></label>
        <Link to={`/register?company=${target.id}&role=${encodeURIComponent(role)}`} className="inline-flex min-h-[46px] items-center justify-center gap-2 rounded-xl bg-[#10241c] px-5 py-3 text-sm font-black text-white transition hover:-translate-y-0.5 hover:bg-[#1a3a2b]">Build my path <ArrowRight size={16} /></Link>
      </div>
      <div className="mt-3 flex flex-wrap items-center gap-x-4 gap-y-2 border-t border-[#edf3ef] pt-3 text-[10px] font-semibold text-[#567064]"><span className="flex items-center gap-1.5"><CircleDot size={12} className="text-[#20a77d]" /> No credit card</span><span className="flex items-center gap-1.5"><ShieldCheck size={12} className="text-[#20a77d]" /> Server-graded baseline</span><span className="flex items-center gap-1.5"><LockKeyhole size={12} className="text-[#20a77d]" /> Your data stays yours</span></div>
    </div>
  );
}

export default function Landing() {
  const { user } = useAuthStore();
  const [target, setTarget] = useState(TARGETS[0]);
  const [role, setRole] = useState(ROLES[0]);
  const [activeLoop, setActiveLoop] = useState(0);
  const cta = user ? "/academy" : `/register?company=${target.id}&role=${encodeURIComponent(role)}`;
  const selectedNote = useMemo(() => COMPANY_NOTES.find((item) => item.name === target.label) || COMPANY_NOTES[0], [target]);

  return (
    <main className="min-h-screen overflow-hidden bg-[#f5faf7] text-[#10241c] selection:bg-[#20c997]/25">
      <nav className="relative z-20 mx-auto flex max-w-7xl items-center justify-between px-5 py-5 sm:px-8 lg:px-10"><Link to="/" className="flex items-center gap-2.5"><div className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#10241c] text-[#6af0c4]"><Crosshair size={19} /></div><span className="text-lg font-black tracking-tight">bounty<span className="text-[#20a77d]">code</span><span className="ml-1.5 rounded-full bg-[#e4f5ed] px-2 py-0.5 align-middle font-mono text-[8px] uppercase tracking-widest text-[#16845f]">readiness OS</span></span></Link><div className="hidden items-center gap-7 text-sm font-semibold text-[#567064] md:flex"><a href="#system" className="transition hover:text-[#10241c]">The system</a><a href="#tracks" className="transition hover:text-[#10241c]">Company tracks</a><a href="#proof" className="transition hover:text-[#10241c]">Why it works</a></div><div className="flex items-center gap-3"><Link to="/login" className="hidden text-sm font-bold text-[#567064] sm:inline">Log in</Link><Link to={cta} className="inline-flex items-center gap-1.5 rounded-full bg-[#10241c] px-4 py-2.5 text-xs font-black text-white transition hover:bg-[#1a3a2b]">{user ? "Open cockpit" : "Start free"}<ArrowRight size={14} /></Link></div></nav>

      <section className="relative mx-auto max-w-7xl px-5 pb-16 pt-8 sm:px-8 sm:pb-24 sm:pt-14 lg:px-10 lg:pb-28"><div className="pointer-events-none absolute -right-40 top-0 h-[500px] w-[500px] rounded-full bg-[#b7f1dc]/50 blur-3xl" /><div className="pointer-events-none absolute -left-32 top-40 h-[350px] w-[350px] rounded-full bg-[#ffe2c7]/45 blur-3xl" /><div className="relative grid items-center gap-12 lg:grid-cols-[.92fr_1.08fr] lg:gap-16"><motion.div initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: .65 }}><div className="inline-flex items-center gap-2 rounded-full border border-[#b9e7d2] bg-white/70 px-3 py-1.5 font-mono text-[10px] font-bold uppercase tracking-[0.16em] text-[#16845f]"><span className="h-1.5 w-1.5 animate-pulse rounded-full bg-[#20c997]" /> The anti-chaos placement system</div><h1 className="mt-6 max-w-2xl text-[3.1rem] font-black leading-[.98] tracking-[-0.06em] text-[#10241c] sm:text-6xl lg:text-[5.6rem]">Know what to learn.<br /><span className="text-[#20a77d]">Prove you’re ready.</span></h1><p className="mt-6 max-w-xl text-base leading-7 text-[#567064] sm:text-lg">Bountycode turns scattered placement prep into one living system for service-based company roles: choose a target, expose the gap, repair it, and rehearse the real assessment.</p><div className="mt-8"><TargetPicker target={target} setTarget={setTarget} role={role} setRole={setRole} /></div><p className="mt-4 flex items-center gap-2 text-xs font-semibold text-[#567064]"><Sparkles size={14} className="text-[#ff8a3d]" /> Built for students who are tired of guessing what “placement ready” means.</p></motion.div><motion.div initial={{ opacity: 0, scale: .96 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: .8, delay: .12 }}><ReadinessCockpit target={target} role={role} /></motion.div></div></section>

      <section id="system" className="border-y border-[#dcebe3] bg-white/70 px-5 py-16 sm:px-8 sm:py-24 lg:px-10"><div className="mx-auto max-w-7xl"><div className="grid gap-8 lg:grid-cols-[.7fr_1.3fr] lg:items-end"><div><p className="font-mono text-[10px] font-bold uppercase tracking-[0.2em] text-[#20a77d]">One system, four signals</p><h2 className="mt-3 max-w-md text-3xl font-black tracking-[-0.04em] sm:text-5xl">Your next task should never be a mystery.</h2></div><p className="max-w-xl text-sm leading-6 text-[#567064] lg:justify-self-end">The platform separates activity from readiness. Lessons, diagnostics, company mocks and repair missions all feed the same explainable learner model.</p></div><div className="mt-10 grid gap-3 lg:grid-cols-3">{LOOP.map((item, index) => { const Icon = item.icon; const active = activeLoop === index; return <button type="button" key={item.number} onClick={() => setActiveLoop(index)} className={`group rounded-[1.5rem] border p-5 text-left transition-all ${active ? "border-[#10241c] bg-[#10241c] text-white shadow-xl shadow-[#10241c]/10" : "border-[#dcebe3] bg-white hover:-translate-y-1 hover:border-[#9adfc3]"}`}><div className="flex items-start justify-between"><span className={`font-mono text-xs font-bold ${active ? "text-[#6af0c4]" : "text-[#20a77d]"}`}>{item.number}</span><span className="rounded-xl p-2" style={{ backgroundColor: active ? `${item.color}30` : `${item.color}15`, color: active ? "white" : item.color }}><Icon size={18} /></span></div><h3 className="mt-8 text-xl font-black">{item.title}</h3><p className={`mt-2 text-sm leading-6 ${active ? "text-white/60" : "text-[#567064]"}`}>{item.body}</p><span className={`mt-6 inline-flex items-center gap-1.5 text-xs font-black ${active ? "text-[#6af0c4]" : "text-[#10241c]"}`}>How this works <ArrowRight size={13} className="transition group-hover:translate-x-1" /></span></button>; })}</div></div></section>

      <section id="tracks" className="bg-[#10241c] px-5 py-16 text-white sm:px-8 sm:py-24 lg:px-10"><div className="mx-auto max-w-7xl"><div className="flex flex-col justify-between gap-6 md:flex-row md:items-end"><div><p className="font-mono text-[10px] font-bold uppercase tracking-[0.2em] text-[#6af0c4]">Company-aware, not company-obsessed</p><h2 className="mt-3 max-w-2xl text-3xl font-black tracking-[-0.04em] sm:text-5xl">Prepare for the pattern.<br /><span className="text-[#6af0c4]">Stay ready for the variation.</span></h2></div><p className="max-w-sm text-sm leading-6 text-white/55">Every company track is a dated simulation with a provenance note. Your current invitation remains the source of truth.</p></div><div className="mt-10 grid gap-3 md:grid-cols-3">{COMPANY_NOTES.map((item) => <div key={item.name} className={`rounded-[1.5rem] border p-5 transition ${item.name === selectedNote.name ? "border-white/35 bg-white/10" : "border-white/10 bg-white/[0.03]"}`}><div className="flex items-center justify-between"><div className="flex items-center gap-2.5"><div className="h-2.5 w-2.5 rounded-full" style={{ backgroundColor: item.accent }} /><h3 className="text-lg font-black">{item.name}</h3></div>{item.name === selectedNote.name && <span className="font-mono text-[9px] font-bold uppercase tracking-widest text-[#6af0c4]">Selected</span>}</div><p className="mt-7 text-sm font-semibold text-white/80">{item.detail}</p><div className="mt-4 flex items-center gap-2 text-xs text-white/45"><Gauge size={13} style={{ color: item.accent }} /> {item.tag}</div></div>)}</div><div className="mt-8 flex flex-wrap items-center justify-between gap-4 rounded-2xl border border-white/10 bg-white/[0.04] p-4"><p className="flex items-center gap-2 text-xs font-semibold text-white/65"><ShieldCheck size={15} className="text-[#6af0c4]" /> No universal cutoff claims. No fake certainty. Just a better feedback loop.</p><Link to={cta} className="inline-flex items-center gap-2 rounded-xl bg-[#6af0c4] px-4 py-2.5 text-xs font-black text-[#10241c]">See my path <ArrowRight size={14} /></Link></div></div></section>

      <section id="proof" className="px-5 py-16 sm:px-8 sm:py-24 lg:px-10"><div className="mx-auto max-w-7xl"><div className="grid gap-10 lg:grid-cols-[.8fr_1.2fr] lg:items-start"><div><p className="font-mono text-[10px] font-bold uppercase tracking-[0.2em] text-[#20a77d]">The Bountycode difference</p><h2 className="mt-3 text-3xl font-black tracking-[-0.04em] sm:text-5xl">Less noise.<br />More signal.</h2><p className="mt-5 max-w-md text-sm leading-6 text-[#567064]">Gamification keeps the journey alive. Evidence keeps it honest. The result is a platform that can tell you not only what to do next, but why.</p><Link to={cta} className="mt-7 inline-flex items-center gap-2 rounded-xl bg-[#10241c] px-5 py-3 text-sm font-black text-white">Start with a baseline <ArrowRight size={15} /></Link></div><div className="grid gap-3 sm:grid-cols-2"><div className="rounded-[1.5rem] border border-[#dcebe3] bg-white p-5"><BarChart3 className="text-[#20a77d]" size={21} /><h3 className="mt-6 text-lg font-black">The skill graph follows evidence</h3><p className="mt-2 text-sm leading-6 text-[#567064]">Accuracy, response time, confidence and recency combine into a readable readiness signal.</p></div><div className="rounded-[1.5rem] border border-[#dcebe3] bg-white p-5"><Zap className="text-[#ff8a3d]" size={21} /><h3 className="mt-6 text-lg font-black">The next mission is actionable</h3><p className="mt-2 text-sm leading-6 text-[#567064]">Weak areas become focused lessons, practice, revision and reassessment—not an endless content feed.</p></div><div className="rounded-[1.5rem] border border-[#dcebe3] bg-white p-5"><Trophy className="text-[#7c5cff]" size={21} /><h3 className="mt-6 text-lg font-black">Levels mean demonstrated progress</h3><p className="mt-2 text-sm leading-6 text-[#567064]">XP and streaks are motivation. Repeated success across varied questions unlocks the next stage.</p></div><div className="rounded-[1.5rem] border border-[#dcebe3] bg-white p-5"><Users className="text-[#20a77d]" size={21} /><h3 className="mt-6 text-lg font-black">Built for the real starting line</h3><p className="mt-2 text-sm leading-6 text-[#567064]">A low-cost path for students who need structure, access and confidence before they need polish.</p></div></div></div></div></section>

      <section className="px-5 pb-16 sm:px-8 sm:pb-24 lg:px-10"><div className="relative mx-auto max-w-7xl overflow-hidden rounded-[2rem] bg-[#d9f6e9] px-6 py-12 sm:px-12 sm:py-16"><div className="pointer-events-none absolute -right-16 -top-20 h-72 w-72 rounded-full border-[40px] border-[#20c997]/20" /><div className="relative max-w-2xl"><p className="font-mono text-[10px] font-bold uppercase tracking-[0.2em] text-[#16845f]">Your first move</p><h2 className="mt-3 text-3xl font-black tracking-[-0.04em] sm:text-5xl">Stop asking “what should I study?”</h2><p className="mt-4 max-w-xl text-sm leading-6 text-[#45675a]">Tell us the company and role. We’ll turn the uncertainty into a starting point you can see, measure and improve.</p><Link to={cta} className="mt-7 inline-flex items-center gap-2 rounded-xl bg-[#10241c] px-5 py-3.5 text-sm font-black text-white shadow-xl shadow-[#10241c]/15 transition hover:-translate-y-0.5 hover:bg-[#1a3a2b]">Build my readiness path <ArrowRight size={16} /></Link></div></div></section>

      <footer className="border-t border-[#dcebe3] px-5 py-7 sm:px-8 lg:px-10"><div className="mx-auto flex max-w-7xl flex-col justify-between gap-4 text-xs text-[#567064] sm:flex-row sm:items-center"><p className="font-semibold">bountycode · placement preparation with a point of view</p><div className="flex gap-5"><Link to="/privacy" className="hover:text-[#10241c]">Privacy</Link><Link to="/terms" className="hover:text-[#10241c]">Terms</Link><Link to="/login" className="hover:text-[#10241c]">Log in</Link></div></div></footer>
    </main>
  );
}
