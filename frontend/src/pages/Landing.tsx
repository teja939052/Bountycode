import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import {
  ArrowRight,
  BarChart3,
  Bot,
  Brain,
  CheckCircle,
  ChevronDown,
  Code2,
  Compass,
  Crown,
  DollarSign,
  FileText,
  Flame,
  Layers,
  Mail,
  ScrollText,
  Shield,
  Sparkles,
  Star,
  Sword,
  Target,
  Trophy,
  Zap,
} from "lucide-react";
import StaggerContainer, { StaggerItem } from "../components/motion/StaggerContainer";
import useReducedMotion from "../hooks/useReducedMotion";

const coreFeatures = [
  { icon: Bot, title: "AI Interviewer", desc: "Live mock rounds with sharp feedback and better follow-ups.", color: "text-brand-sky", bg: "from-brand-sky/10 to-brand-sky/5" },
  { icon: Layers, title: "System Design", desc: "Practice trade-offs, scaling calls, and architecture storytelling.", color: "text-brand-lavender", bg: "from-brand-lavender/10 to-brand-lavender/5" },
  { icon: Code2, title: "Coding Battles", desc: "Timed problem solving with hidden judge cases and XP rewards.", color: "text-brand-teal", bg: "from-brand-teal/10 to-brand-teal/5" },
  { icon: FileText, title: "Resume Forge", desc: "Rewrite weak bullets into high-impact, ATS-friendly wins.", color: "text-brand-coral", bg: "from-brand-coral/10 to-brand-coral/5" },
  { icon: Target, title: "ATS Scanner", desc: "See missing keywords before recruiters do.", color: "text-brand-gold", bg: "from-brand-gold/20 to-brand-gold/5" },
  { icon: Brain, title: "Aptitude Arena", desc: "Placement prep drills that feel like a ranked mode.", color: "text-fuchsia-500", bg: "from-fuchsia-500/10 to-fuchsia-500/5" },
  { icon: Mail, title: "Cover Letter AI", desc: "Fast, tailored letters for real applications.", color: "text-rose-500", bg: "from-rose-500/10 to-rose-500/5" },
  { icon: DollarSign, title: "Negotiation Coach", desc: "Scripts and strategy for better offers.", color: "text-emerald-500", bg: "from-emerald-500/10 to-emerald-500/5" },
  { icon: BarChart3, title: "Salary Intel", desc: "Understand your market value before the call.", color: "text-cyan-500", bg: "from-cyan-500/10 to-cyan-500/5" },
];

const factionCards = [
  {
    title: "The Ronin",
    subtitle: "DSA path",
    icon: Sword,
    badge: "Code",
    accent: "from-brand-sky to-cyan-300",
    desc: "Rank up through problem-solving quests, hidden tests, and progressive hints.",
  },
  {
    title: "The Architect",
    subtitle: "System design path",
    icon: Compass,
    badge: "Design",
    accent: "from-brand-lavender to-fuchsia-300",
    desc: "Learn how to explain scale, trade-offs, and architecture like a senior engineer.",
  },
  {
    title: "The Alchemist",
    subtitle: "Career path",
    icon: ScrollText,
    badge: "Career",
    accent: "from-brand-coral to-brand-gold",
    desc: "Turn resumes, cover letters, and negotiation prep into real leverage.",
  },
];

const rewards = [
  { title: "Daily Quest", value: "5 min", note: "Keep the streak alive", icon: Flame },
  { title: "Boss Battle", value: "30 XP", note: "Win the round, win the loot", icon: Crown },
  { title: "Mystery Box", value: "Bonus", note: "Random rewards after wins", icon: Sparkles },
];

const testimonials = [
  { name: "Ananya R.", role: "SDE at Amazon", text: "The interview mode felt like a boss fight. It made me sharper fast.", avatar: "A", tone: "from-brand-coral to-brand-gold" },
  { name: "Rohit K.", role: "TCS NQT Ranker", text: "The aptitude drills were addictive and never felt passive.", avatar: "R", tone: "from-brand-sky to-brand-lavender" },
  { name: "Sarah M.", role: "PM at Meta", text: "The ATS rewrite made my resume feel engineered, not just written.", avatar: "S", tone: "from-brand-teal to-emerald-400" },
];

const steps = [
  { step: "01", title: "Choose your class", desc: "Pick a prep path or combine them like a true grind legend.", icon: Sparkles },
  { step: "02", title: "Clear quests", desc: "Earn XP by solving problems, training, and shipping better answers.", icon: Trophy },
  { step: "03", title: "Beat the boss", desc: "Ace the interview, negotiate harder, and walk away with the win.", icon: Shield },
];

export default function Landing() {
  const reduced = useReducedMotion();
  const navigate = useNavigate();

  const handleGetStarted = () => navigate("/register");
  const handleQuickStart = () => navigate("/problems");

  return (
    <div className="min-h-screen">
      <section className="px-4 pt-6 md:pt-10">
        <div className="mx-auto max-w-7xl">
          <div className="hero-shell overflow-hidden">
            <div className="absolute inset-0">
              <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(72,149,239,0.22),transparent_28%),radial-gradient(circle_at_top_right,rgba(124,109,175,0.18),transparent_24%),radial-gradient(circle_at_bottom_left,rgba(42,157,143,0.16),transparent_26%)]" />
              <div className="absolute inset-0 bg-[linear-gradient(135deg,rgba(255,255,255,0.06)_0%,transparent_42%,rgba(255,255,255,0.03)_100%)]" />
            </div>

            <div className="relative grid gap-8 px-5 py-8 md:px-10 md:py-12 lg:grid-cols-[1.08fr_0.92fr] lg:items-center">
              <div className="relative z-10">
                <motion.div
                  initial={reduced ? {} : { opacity: 0, y: 14 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5 }}
                  className="mb-5 flex flex-wrap gap-3"
                >
                  <span className="section-kicker border-white/10 bg-white/10 text-white">
                    <span className="h-2 w-2 rounded-full bg-emerald-400 shadow-[0_0_18px_rgba(74,222,128,0.9)]" />
                    New-era prep platform
                  </span>
                  <span className="quest-chip border-white/10 bg-white/10 text-white">
                    Monthly free resets
                  </span>
                </motion.div>

                <motion.h1
                  className="max-w-3xl text-4xl font-black leading-[1.02] tracking-tight text-white md:text-6xl lg:text-7xl"
                  initial={reduced ? {} : { opacity: 0, y: 24 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 0.05 }}
                >
                  Turn placement prep into a{" "}
                  <span className="bg-gradient-to-r from-brand-sky via-cyan-200 to-brand-gold bg-clip-text text-transparent">
                    game worth playing
                  </span>
                </motion.h1>

                <motion.p
                  className="mt-6 max-w-2xl text-base leading-7 text-slate-200 md:text-lg"
                  initial={reduced ? {} : { opacity: 0, y: 18 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 0.14 }}
                >
                  PlacementPro blends anime-style progression, fantasy-house energy, and savage interview coaching into one
                  addictive learning arena for students and job seekers.
                </motion.p>

                <motion.div
                  className="mt-8 flex flex-col gap-3 sm:flex-row"
                  initial={reduced ? {} : { opacity: 0, y: 18 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 0.22 }}
                >
                  <Link to="/free-trial" className="inline-flex items-center justify-center gap-2 rounded-2xl bg-gradient-to-r from-emerald-400 via-teal-400 to-cyan-400 px-8 py-4 text-base font-bold text-gray-900 shadow-lg shadow-emerald-400/30 transition-all hover:scale-105 hover:shadow-emerald-400/50">
                    <Sparkles size={18} />
                    Start Coding Free
                  </Link>
                  <button onClick={handleGetStarted} className="btn-primary inline-flex items-center justify-center gap-2 px-8 py-4 text-base">
                    Start Free <ArrowRight size={18} />
                  </button>
                  <button onClick={handleQuickStart} className="inline-flex items-center justify-center gap-2 rounded-2xl border border-white/20 bg-white/10 px-8 py-4 text-base font-semibold text-white transition-all hover:bg-white/20">
                    Quick Practice <Zap size={18} />
                  </button>
                </motion.div>

                <motion.div
                  className="mt-8 grid gap-3 grid-cols-2 lg:grid-cols-4"
                  initial={reduced ? {} : { opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 0.3 }}
                >
                  {[
                    { value: "15+", label: "core modules" },
                    { value: "4", label: "learning lanes" },
                    { value: "1", label: "daily arena" },
                    { value: "100%", label: "game flow" },
                  ].map((item) => (
                    <div key={item.label} className="rounded-2xl border border-white/10 bg-white/10 px-4 py-4 text-left backdrop-blur-md">
                      <div className="text-2xl font-display font-black text-white">{item.value}</div>
                      <div className="mt-1 text-[10px] font-mono uppercase tracking-[0.28em] text-slate-300">{item.label}</div>
                    </div>
                  ))}
                </motion.div>
              </div>

              <div className="relative z-10">
                <motion.div
                  initial={reduced ? {} : { opacity: 0, x: 20, rotate: 2 }}
                  animate={{ opacity: 1, x: 0, rotate: 0 }}
                  transition={{ duration: 0.7, delay: 0.1 }}
                  className="grid gap-4"
                >
                  <div className="faction-card p-5 md:p-6">
                    <div className="relative z-10">
                      <div className="flex items-start justify-between gap-4">
                        <div>
                          <div className="text-[10px] font-mono uppercase tracking-[0.32em] text-slate-300">Featured path</div>
                          <h2 className="mt-2 text-2xl font-display font-black text-white">Choose your class</h2>
                        </div>
                        <div className="rounded-full border border-white/20 bg-white/10 px-3 py-1 text-[10px] font-mono uppercase tracking-[0.22em] text-slate-200">
                          Live meta
                        </div>
                      </div>

                      <div className="mt-5 grid gap-3">
                        {factionCards.map((card) => (
                          <div key={card.title} className="rounded-2xl border border-white/10 bg-white/10 p-4 backdrop-blur-sm transition-transform hover:-translate-y-1">
                            <div className="flex items-start gap-4">
                              <div className={`flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br ${card.accent} text-white shadow-lg`}>
                                <card.icon size={24} />
                              </div>
                              <div className="min-w-0 flex-1">
                                <div className="flex items-center gap-2">
                                  <span className="rounded-full border border-white/20 bg-white/10 px-2 py-1 text-[10px] font-mono uppercase tracking-[0.22em] text-slate-200">{card.badge}</span>
                                  <span className="text-[10px] font-mono uppercase tracking-[0.22em] text-slate-400">{card.subtitle}</span>
                                </div>
                                <h3 className="mt-2 text-lg font-display font-bold text-white">{card.title}</h3>
                                <p className="mt-1 text-sm leading-6 text-slate-300">{card.desc}</p>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>

                  <div className="grid gap-3 sm:grid-cols-3">
                    {rewards.map((item) => (
                      <div key={item.title} className="rounded-2xl border border-white/10 bg-white/10 p-4 text-white backdrop-blur-md">
                        <div className="flex items-center justify-between">
                          <item.icon size={18} className="text-cyan-200" />
                          <span className="text-[10px] font-mono uppercase tracking-[0.28em] text-slate-300">{item.title}</span>
                        </div>
                        <div className="mt-4 text-2xl font-display font-black">{item.value}</div>
                        <p className="mt-1 text-sm text-slate-300">{item.note}</p>
                      </div>
                    ))}
                  </div>
                </motion.div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="px-4 py-16 md:py-24">
        <div className="mx-auto max-w-7xl">
          <div className="mb-10 flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
            <div>
              <span className="section-kicker">Core modules</span>
              <h2 className="mt-4 text-3xl font-black tracking-tight text-text-primary md:text-4xl">
                A full arsenal, tuned like a game loop
              </h2>
            </div>
            <p className="max-w-xl text-sm leading-6 text-text-muted">
              Every module is designed around momentum, streaks, and clear feedback, so users always know what to do next.
            </p>
          </div>

          <StaggerContainer className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {coreFeatures.map((feature) => (
              <StaggerItem key={feature.title}>
                <div className="arena-card h-full p-5">
                  <div className={`mb-4 flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br ${feature.bg}`}>
                    <feature.icon size={24} className={feature.color} />
                  </div>
                  <h3 className="text-lg font-display font-bold text-text-primary">{feature.title}</h3>
                  <p className="mt-2 text-sm leading-6 text-text-muted">{feature.desc}</p>
                </div>
              </StaggerItem>
            ))}
          </StaggerContainer>
        </div>
      </section>

      <section className="px-4 py-16 md:py-24">
        <div className="mx-auto max-w-7xl">
          <div className="grid gap-6 lg:grid-cols-[1fr_0.85fr]">
            <div className="arena-card p-6 md:p-8">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <span className="section-kicker">How it works</span>
                  <h2 className="mt-4 text-3xl font-black tracking-tight text-text-primary">
                    Built to feel like progression, not homework
                  </h2>
                </div>
                <div className="hidden rounded-2xl bg-brand-sky/10 px-4 py-3 text-right md:block">
                  <div className="text-sm font-display font-bold text-brand-sky">+XP on every win</div>
                  <div className="text-[10px] font-mono uppercase tracking-[0.24em] text-text-light">Streaks, badges, quests</div>
                </div>
              </div>

              <div className="mt-8 grid gap-4">
                {steps.map((step) => (
                  <div key={step.step} className="flex items-start gap-4 rounded-2xl border border-gray-100 bg-white/80 p-4">
                    <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-brand-sky/10 text-brand-sky">
                      <step.icon size={24} />
                    </div>
                    <div className="min-w-0">
                      <div className="text-[10px] font-mono uppercase tracking-[0.28em] text-brand-sky/70">Step {step.step}</div>
                      <h3 className="mt-1 text-lg font-display font-bold text-text-primary">{step.title}</h3>
                      <p className="mt-1 text-sm leading-6 text-text-muted">{step.desc}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="grid gap-4">
              <div className="arena-card p-6">
                <div className="flex items-center gap-3">
                  <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-brand-gold-pale text-brand-gold">
                    <Flame size={22} />
                  </div>
                  <div>
                    <div className="text-[10px] font-mono uppercase tracking-[0.28em] text-text-light">Retention hooks</div>
                    <h3 className="mt-1 text-xl font-display font-bold text-text-primary">The stuff that keeps users coming back</h3>
                  </div>
                </div>

                <div className="mt-5 space-y-3">
                  {[
                    "Mystery boxes after wins",
                    "Daily quests with clean XP rewards",
                    "Boss battles, streak freezes, and comeback bonuses",
                    "Savage feedback that feels memorable, not generic",
                  ].map((item) => (
                    <div key={item} className="flex items-start gap-2 text-sm text-text-muted">
                      <CheckCircle size={14} className="mt-1 shrink-0 text-brand-teal" />
                      <span>{item}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="arena-card p-6">
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <div className="text-[10px] font-mono uppercase tracking-[0.28em] text-text-light">Built for two worlds</div>
                    <h3 className="mt-1 text-xl font-display font-bold text-text-primary">Campus placements and global interviews</h3>
                  </div>
                  <Crown className="text-brand-coral" size={22} />
                </div>
                <div className="mt-5 grid gap-3 sm:grid-cols-2">
                  {[
                    "Quant, reasoning, verbal, and technical drills for campus hiring",
                    "Behavioral, system design, resume, and salary prep for global roles",
                  ].map((item) => (
                    <div key={item} className="rounded-2xl border border-gray-100 bg-white/80 p-4 text-sm leading-6 text-text-muted">
                      {item}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="px-4 py-16 md:py-24">
        <div className="mx-auto max-w-7xl">
          <div className="mb-10 text-center">
            <span className="section-kicker">Player feedback</span>
            <h2 className="mt-4 text-3xl font-black tracking-tight text-text-primary md:text-4xl">
              Real users, real wins
            </h2>
            <p className="mx-auto mt-3 max-w-2xl text-sm leading-6 text-text-muted">
              Keep the tone vivid, keep the progress visible, and people keep playing. That is the retention engine.
            </p>
          </div>

          <StaggerContainer className="grid gap-4 md:grid-cols-3">
            {testimonials.map((item) => (
              <StaggerItem key={item.name}>
                <div className="arena-card h-full p-5">
                  <div className="mb-4 flex items-center gap-1">
                    {Array.from({ length: 5 }).map((_, index) => (
                      <Star key={index} size={12} className="text-brand-gold" fill="currentColor" />
                    ))}
                  </div>
                  <p className="text-sm leading-7 text-text-muted">"{item.text}"</p>
                  <div className="mt-5 flex items-center gap-3">
                    <div className={`flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br ${item.tone} text-sm font-bold text-white`}>
                      {item.avatar}
                    </div>
                    <div>
                      <div className="text-sm font-display font-bold text-text-primary">{item.name}</div>
                      <div className="text-[10px] font-mono uppercase tracking-[0.24em] text-text-light">{item.role}</div>
                    </div>
                  </div>
                </div>
              </StaggerItem>
            ))}
          </StaggerContainer>
        </div>
      </section>

      <section className="px-4 py-16 md:py-24">
        <div className="mx-auto max-w-5xl">
          <div className="text-center">
            <span className="section-kicker">Pricing</span>
            <h2 className="mt-4 text-3xl font-black tracking-tight text-text-primary md:text-4xl">Simple tiers. Strong hooks.</h2>
            <p className="mt-3 text-sm leading-6 text-text-muted">
              Start free, upgrade when the grind gets serious, or lock in lifetime once you know it is your platform.
            </p>
          </div>

          <div className="mt-10 grid gap-5 lg:grid-cols-3">
            <PricingCard
              title="Cadet"
              price="$0"
              subtitle="Monthly reset"
              features={["3 interviews/month", "3 resume reviews/month", "5 aptitude tests/month", "3 cover letters/month", "Basic feedback"]}
              cta="Enlist"
              to="/register"
            />
            <PricingCard
              featured
              title="Commander"
              price="$19"
              subtitle="Per month"
              features={["Unlimited interviews", "Unlimited resumes", "Unlimited aptitude", "ATS optimization", "Priority support"]}
              cta="Upgrade"
              to="/register"
            />
            <PricingCard
              title="Admiral"
              price="$39"
              subtitle="One-time lifetime"
              features={["Everything in Pro", "Lifetime access", "All future updates", "Priority support", "Best value"]}
              cta="Go lifetime"
              to="/register"
            />
          </div>
        </div>
      </section>

      <section className="px-4 pb-20 pt-10">
        <div className="mx-auto max-w-5xl">
          <div className="faction-card px-6 py-10 text-center md:px-10">
            <div className="relative z-10">
              <div className="section-kicker border-white/10 bg-white/10 text-white mx-auto justify-center">
                Final CTA
              </div>
              <h2 className="mt-4 text-3xl font-black tracking-tight text-white md:text-5xl">
                Ready to level up the way people learn?
              </h2>
              <p className="mx-auto mt-4 max-w-2xl text-sm leading-7 text-slate-300 md:text-base">
                Build the most addictive learning hub in the room. Give students visible progress, strong feedback, and a brand they remember.
              </p>
              <div className="mt-8 flex flex-col justify-center gap-3 sm:flex-row">
                <button onClick={handleGetStarted} className="btn-primary inline-flex items-center justify-center gap-2 px-8 py-4 text-base">
                  Launch Mission <ArrowRight size={18} />
                </button>
                <Link to="/pricing" className="inline-flex items-center justify-center gap-2 rounded-2xl border border-white/20 bg-white/10 px-8 py-4 text-base font-semibold text-white transition-all hover:bg-white/20">
                  View Tiers <ChevronDown size={18} />
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

function PricingCard({ title, price, subtitle, features, cta, to, featured = false }) {
  return (
    <div className={`arena-card flex h-full flex-col p-6 ${featured ? "border-brand-sky/30 shadow-soft-lg" : ""}`}>
      {featured && (
        <div className="mb-4 inline-flex w-fit items-center rounded-full border border-brand-sky/20 bg-brand-sky/10 px-3 py-1 text-[10px] font-mono uppercase tracking-[0.24em] text-brand-sky">
          Most popular
        </div>
      )}
      <h3 className="text-xl font-display font-bold text-text-primary">{title}</h3>
      <div className="mt-3 flex items-end gap-2">
        <div className="text-4xl font-black text-text-primary">{price}</div>
        <div className="pb-1 text-xs font-mono uppercase tracking-[0.24em] text-text-light">{subtitle}</div>
      </div>
      <div className="mt-6 flex-1 space-y-3">
        {features.map((item) => (
          <div key={item} className="flex items-start gap-2 text-sm text-text-muted">
            <CheckCircle size={14} className="mt-1 shrink-0 text-brand-teal" />
            <span>{item}</span>
          </div>
        ))}
      </div>
      <Link to={to} className={featured ? "btn-primary mt-6 text-center" : "btn-secondary mt-6 text-center"}>
        {cta}
      </Link>
    </div>
  );
}
