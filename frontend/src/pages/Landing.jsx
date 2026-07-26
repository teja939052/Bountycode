import { Link } from "react-router-dom";
import { useState, lazy, Suspense } from "react";
import { useNavigate } from "react-router-dom";
import { Bot, FileText, Target, Brain, Mail, DollarSign, Layers, Building2, Code, BarChart3, CheckCircle, ArrowRight, Star, ChevronDown, Zap, Rocket, Shield, Terminal, Play, Sparkles, Compass, Sword, Flame } from "lucide-react";
import { motion } from "framer-motion";
import useReducedMotion from "../hooks/useReducedMotion";
import StaggerContainer, { StaggerItem } from "../components/motion/StaggerContainer";
import ErrorBoundary from "../components/ErrorBoundary";

const Hero3D = lazy(() => import("../components/hero/Hero3D"));

function Hero3DFallback() {
  return (
    <div className="w-full h-full flex items-center justify-center">
      <div className="w-40 h-40 rounded-full bg-cyber-blue/20 blur-3xl animate-pulse" />
    </div>
  );
}

const features = [
  { icon: Bot, title: "AI Interviewer", desc: "Mock interviews with real-time feedback.", color: "bg-cyber-blue/10 text-cyber-blue border-cyber-blue/20" },
  { icon: Layers, title: "System Design", desc: "System design with AI evaluation.", color: "bg-cyber-purple/10 text-cyber-purple border-cyber-purple/20" },
  { icon: Code, title: "Coding Challenges", desc: "Timed problems with hyperdrive testing.", color: "bg-cyber-green/10 text-cyber-green border-cyber-green/20" },
  { icon: Building2, title: "Company Intel", desc: "FAANG guides & behavioral questions.", color: "bg-cyber-blue/10 text-cyan-400 border-cyan-400/20" },
  { icon: FileText, title: "Hull Builder", desc: "ATS-optimized resume generation.", color: "bg-cyber-green/10 text-emerald-400 border-emerald-400/20" },
  { icon: Target, title: "Hull Scanner", desc: "Match resume to job descriptions.", color: "bg-cyber-amber/10 text-cyber-amber border-cyber-amber/20" },
  { icon: Brain, title: "Aptitude Tests", desc: "Quant, logical, verbal MCQs.", color: "bg-cyber-purple/10 text-fuchsia-400 border-fuchsia-400/20" },
  { icon: Mail, title: "Cover Letter", desc: "AI-generated cover letters.", color: "bg-pink-500/10 text-pink-400 border-pink-400/20" },
  { icon: BarChart3, title: "Salary Intel", desc: "Know your market worth.", color: "bg-cyber-green/10 text-lime-400 border-lime-400/20" },
  { icon: DollarSign, title: "Negotiation AI", desc: "Scripts & tips to negotiate.", color: "bg-cyber-amber/10 text-yellow-400 border-yellow-400/20" },
];

const testimonials = [
  { name: "Ananya R.", role: "SDE at Amazon", text: "The AI interview mock was brutal — in a good way. Landed my Amazon offer after 2 weeks of daily practice.", avatar: "A", color: "from-orange-400 to-red-500" },
  { name: "Rohit K.", role: "TCS NQT Rank 3", text: "The aptitude section is exactly like TCS NQT. Practiced 200+ questions, scored 92% in the actual test.", avatar: "R", color: "from-cyber-blue to-indigo-500" },
  { name: "Sarah M.", role: "PM at Meta", text: "The ATS optimizer rewrote my resume. Went from 0 callbacks to 6 interviews in one week.", avatar: "S", color: "from-cyber-purple to-pink-500" },
  { name: "Vikram P.", role: "SDE at Google", text: "System design AI caught 'single point of failure' — something no human interviewer told me.", avatar: "V", color: "from-cyber-green to-emerald-500" },
  { name: "Priya S.", role: "Placed at Infosys", text: "30-day streak, went from struggling with percentages to acing every quant section.", avatar: "P", color: "from-yellow-400 to-cyber-amber" },
  { name: "Marcus T.", role: "Senior Eng at Uber", text: "Negotiation coach helped me ask for $15K more. The scripts are gold.", avatar: "M", color: "from-cyan-400 to-cyber-blue" },
];

const steps = [
  { step: "01", title: "Initialize Systems", desc: "Create a free account. No credit card needed.", icon: Terminal },
  { step: "02", title: "Engage Hyperdrive", desc: "AI interviews, aptitude tests, resume optimization — all systems online.", icon: Rocket },
  { step: "03", title: "Achieve Orbit Lock", desc: "Walk into interviews confident. Land the job.", icon: Shield },
];

export default function Landing() {
  const reduced = useReducedMotion();
  const [showDemo, setShowDemo] = useState(false);
  const navigate = useNavigate();

  const handleGetStarted = () => {
    navigate("/register");
  };

  const handleQuickStart = () => {
    navigate("/problems");
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-space-void via-space-titanium to-space-void" />
        <div className="absolute inset-0 opacity-20">
          <ErrorBoundary fallback={<Hero3DFallback />}>
            <Suspense fallback={<Hero3DFallback />}>
              <Hero3D />
            </Suspense>
          </ErrorBoundary>
        </div>

        {/* Radial glow */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-cyber-blue/5 rounded-full blur-3xl" />

        <div className="relative max-w-7xl mx-auto px-4 py-28 md:py-36 text-center">
          <motion.div
            initial={reduced ? {} : { opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="mb-6"
          >
            <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-cyber-blue/10 border border-cyber-blue/20 text-cyber-blue text-xs font-mono uppercase tracking-widest">
              <span className="status-online" />
              Systems Online — v2.0
            </span>
          </motion.div>

          <motion.h1
            className="text-4xl md:text-6xl lg:text-7xl font-display font-black text-white mb-6 leading-tight"
            initial={reduced ? {} : { opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            Navigate Your
            <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyber-blue via-cyan-300 to-cyber-purple glow-blue">
              Career Orbit
            </span>
          </motion.h1>

          <motion.p
            className="text-lg md:text-xl text-gray-400 mb-10 max-w-2xl mx-auto font-body"
            initial={reduced ? {} : { opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            AI-powered mock interviews, ATS-optimized resumes, aptitude drills, and
            real-time diagnostics — your all-in-one command deck.
          </motion.p>

          <motion.div
            className="flex flex-col sm:flex-row gap-4 justify-center"
            initial={reduced ? {} : { opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.6 }}
          >
            <Link to="/register" className="inline-block">
              <span className="btn-primary inline-flex items-center justify-center gap-2 text-base px-8 py-4">
                Launch Mission <ArrowRight size={20} />
              </span>
            </Link>
            <Link to="/login" className="inline-block">
              <span className="btn-secondary inline-flex items-center justify-center gap-2 text-base px-8 py-4">
                Access Command Deck
              </span>
            </Link>
          </motion.div>

          <motion.p
            className="text-gray-500 mt-6 text-xs font-mono"
            initial={reduced ? {} : { opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8 }}
          >
            Free tier · No credit card · Monthly resets
          </motion.p>
        </div>

        <motion.div
          className="absolute bottom-6 left-1/2 -translate-x-1/2"
          animate={reduced ? {} : { y: [0, 8, 0] }}
          transition={{ duration: 1.5, repeat: Infinity }}
        >
          <ChevronDown size={24} className="text-cyber-blue/40" />
        </motion.div>
      </section>

      {/* Features Grid */}
      <section className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <motion.div
            className="text-center mb-16"
            initial={reduced ? {} : { opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <span className="section-subheader mb-3 block">System Modules</span>
            <h2 className="section-header text-3xl">
              Full <span className="text-cyber-blue">Arsenal</span> Online
            </h2>
          </motion.div>

          <StaggerContainer className="grid md:grid-cols-3 lg:grid-cols-4 gap-4">
            {features.map((f) => (
              <StaggerItem key={f.title}>
                <motion.div
                  whileHover={reduced ? {} : { y: -4, scale: 1.02 }}
                  className="card text-center h-full group hover:border-cyber-blue/30"
                >
                  <div className={`w-14 h-14 ${f.color} border rounded-xl flex items-center justify-center mx-auto mb-4 group-hover:shadow-cyber-blue transition-shadow`}>
                    <f.icon size={28} />
                  </div>
                  <h3 className="font-display font-bold text-white text-sm mb-2">{f.title}</h3>
                  <p className="text-gray-500 text-xs font-mono">{f.desc}</p>
                </motion.div>
              </StaggerItem>
            ))}
          </StaggerContainer>
        </div>
      </section>

      {/* Global Coverage */}
      <section className="py-20 px-4 bg-space-panel/50">
        <div className="max-w-6xl mx-auto">
          <motion.div
            className="text-center mb-16"
            initial={reduced ? {} : { opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <span className="section-subheader mb-3 block">Global Coverage</span>
            <h2 className="section-header text-3xl">
              Built for <span className="text-cyber-purple">Every</span> Orbit
            </h2>
          </motion.div>

          <div className="grid md:grid-cols-2 gap-6">
            <motion.div
              initial={reduced ? {} : { opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="card"
            >
              <h3 className="font-display font-bold mb-4 text-cyber-blue flex items-center gap-2">
                <Rocket size={18} /> Campus Placements (India)
              </h3>
              <ul className="space-y-3">
                {[
                  "Quantitative aptitude (percentages, time/work, speed/distance)",
                  "Logical reasoning (series, coding-decoding, puzzles)",
                  "Verbal ability (grammar, vocabulary, comprehension)",
                  "Technical MCQs for TCS, Infosys, Wipro & more",
                  "Data interpretation (charts, graphs, tables)",
                ].map((f) => (
                  <li key={f} className="flex items-start gap-2 text-gray-400 text-sm">
                    <CheckCircle size={14} className="text-cyber-green shrink-0 mt-0.5" />
                    {f}
                  </li>
                ))}
              </ul>
            </motion.div>

            <motion.div
              initial={reduced ? {} : { opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="card"
            >
              <h3 className="font-display font-bold mb-4 text-cyber-purple flex items-center gap-2">
                <Shield size={18} /> Job Seekers (US & Global)
              </h3>
              <ul className="space-y-3">
                {[
                  "Behavioral interview practice with STAR method feedback",
                  "Resume ATS optimization for applicant tracking systems",
                  "Cover letter generation tailored to job descriptions",
                  "LinkedIn profile optimization",
                  "Salary negotiation coaching with scripts",
                ].map((f) => (
                  <li key={f} className="flex items-start gap-2 text-gray-400 text-sm">
                    <CheckCircle size={14} className="text-cyber-green shrink-0 mt-0.5" />
                    {f}
                  </li>
                ))}
              </ul>
            </motion.div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto">
          <motion.div
            className="text-center mb-16"
            initial={reduced ? {} : { opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <span className="section-subheader mb-3 block">Mission Protocol</span>
            <h2 className="section-header text-3xl">How It Works</h2>
          </motion.div>

          <StaggerContainer className="space-y-8">
            {steps.map((item) => (
              <StaggerItem key={item.step}>
                <motion.div
                  whileHover={reduced ? {} : { x: 8 }}
                  className="flex items-center gap-6 card group"
                >
                  <div className="w-16 h-16 bg-cyber-blue/10 border border-cyber-blue/30 rounded-xl flex items-center justify-center shrink-0 group-hover:shadow-cyber-blue transition-shadow">
                    <item.icon size={28} className="text-cyber-blue" />
                  </div>
                  <div>
                    <div className="text-[10px] font-mono text-cyber-blue/60 tracking-widest mb-1">
                      STEP {item.step}
                    </div>
                    <h3 className="text-lg font-display font-bold text-white">{item.title}</h3>
                    <p className="text-gray-500 text-sm font-mono">{item.desc}</p>
                  </div>
                </motion.div>
              </StaggerItem>
            ))}
          </StaggerContainer>
        </div>
      </section>

      {/* Social Proof */}
      <section className="relative py-24 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-space-titanium via-space-panel to-space-titanium" />
        <div className="absolute inset-0">
          <div className="absolute top-0 left-0 w-96 h-96 bg-cyber-blue/5 rounded-full blur-3xl -translate-x-1/2 -translate-y-1/2" />
          <div className="absolute bottom-0 right-0 w-96 h-96 bg-cyber-purple/5 rounded-full blur-3xl translate-x-1/2 translate-y-1/2" />
        </div>

        <div className="relative max-w-7xl mx-auto text-center">
          <motion.div
            className="mb-16"
            initial={reduced ? {} : { opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <span className="section-subheader mb-3 block">Telemetry</span>
            <h2 className="section-header text-3xl md:text-4xl mb-4">
              Real <span className="text-cyber-green glow-green">Results</span>
            </h2>
            <p className="text-gray-500 text-lg max-w-xl mx-auto font-mono text-sm">
              Join thousands who navigated their career orbit with PlacementPro.
            </p>
          </motion.div>

          <StaggerContainer className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {testimonials.map((t) => (
              <StaggerItem key={t.name}>
                <motion.div
                  whileHover={reduced ? {} : { y: -4 }}
                  className="glass-card rounded-xl p-5 text-left h-full"
                >
                  <div className="flex items-center gap-0.5 mb-3">
                    {[...Array(5)].map((_, i) => (
                      <Star key={i} size={12} className="text-cyber-amber" fill="currentColor" />
                    ))}
                  </div>
                  <p className="text-gray-300 mb-4 leading-relaxed text-sm font-mono">"{t.text}"</p>
                  <div className="flex items-center gap-3">
                    <div className={`w-9 h-9 rounded-full bg-gradient-to-br ${t.color} flex items-center justify-center text-white font-bold text-xs shrink-0`}>
                      {t.avatar}
                    </div>
                    <div>
                      <p className="font-display font-bold text-white text-sm">{t.name}</p>
                      <p className="text-gray-500 text-[10px] font-mono uppercase tracking-wider">{t.role}</p>
                    </div>
                  </div>
                </motion.div>
              </StaggerItem>
            ))}
          </StaggerContainer>

          <motion.div
            className="mt-12 sm:mt-16 grid grid-cols-1 sm:grid-cols-3 gap-6 sm:gap-8 max-w-2xl mx-auto"
            initial={reduced ? {} : { opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.3 }}
          >
            {[
              { num: "2,400+", label: "Cadets Placed" },
              { num: "15,000+", label: "Missions Completed" },
              { num: "4.9/5", label: "Rating" },
            ].map((s) => (
              <div key={s.label} className="text-center">
                <div className="text-2xl md:text-3xl font-display font-black text-white">{s.num}</div>
                <div className="text-gray-500 text-[10px] font-mono uppercase tracking-widest mt-1">{s.label}</div>
              </div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Company Logos */}
      <section className="py-12 px-4 border-b border-space-border">
        <p className="text-center text-[10px] font-mono text-gray-500 uppercase tracking-widest mb-6">Cadets placed at</p>
        <div className="flex overflow-hidden">
          <motion.div
            className="flex gap-12 items-center whitespace-nowrap"
            animate={reduced ? {} : { x: ["0%", "-50%"] }}
            transition={{ duration: 25, repeat: Infinity, ease: "linear" }}
          >
            {["Amazon", "Google", "Microsoft", "Meta", "TCS", "Infosys", "Wipro", "Uber", "Apple", "Flipkart", "Amazon", "Google", "Microsoft", "Meta", "TCS", "Infosys", "Wipro", "Uber", "Apple", "Flipkart"].map((c, i) => (
              <span key={i} className="text-lg font-display font-bold text-gray-700">{c}</span>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Pricing */}
      <section className="py-20 px-4" id="pricing">
        <div className="max-w-5xl mx-auto">
          <motion.div
            className="text-center mb-12"
            initial={reduced ? {} : { opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <span className="section-subheader mb-3 block">Mission Tiers</span>
            <h2 className="section-header text-3xl mb-4">Command Clearance</h2>
            <p className="text-gray-500 font-mono text-sm">
              Start free. Upgrade when ready. Cancel anytime.
            </p>
          </motion.div>

          <StaggerContainer className="grid md:grid-cols-3 gap-6">
            {/* Free */}
            <StaggerItem>
              <motion.div whileHover={reduced ? {} : { y: -4 }} className="card h-full flex flex-col">
                <h3 className="font-display font-bold text-white text-lg mb-2">Cadet</h3>
                <p className="text-4xl font-display font-black text-white mb-1">$0</p>
                <p className="text-gray-500 text-xs font-mono mb-6">Resets monthly</p>
                <ul className="space-y-3 mb-8 flex-1">
                  {["3 AI interviews/month", "3 resume reviews/month", "5 aptitude tests/month", "3 cover letters/month", "ATS score check", "Basic feedback"].map((f) => (
                    <li key={f} className="flex items-center gap-2 text-gray-400 text-sm">
                      <CheckCircle size={14} className="text-cyber-green shrink-0" />
                      {f}
                    </li>
                  ))}
                </ul>
                <Link to="/register" className="block text-center btn-secondary">Enlist</Link>
              </motion.div>
            </StaggerItem>

            {/* Pro */}
            <StaggerItem>
              <motion.div whileHover={reduced ? {} : { y: -4 }} className="card-glow border-2 border-cyber-blue/40 relative h-full flex flex-col">
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-cyber-blue text-space-void px-3 py-1 rounded-full text-[10px] font-display font-bold uppercase tracking-wider">
                  Commander
                </div>
                <h3 className="font-display font-bold text-white text-lg mb-2">Pro</h3>
                <p className="text-4xl font-display font-black text-white mb-1">
                  $19<span className="text-base font-normal text-gray-500">/mo</span>
                </p>
                <p className="text-gray-500 text-xs font-mono mb-6">Billed monthly · Cancel anytime</p>
                <ul className="space-y-3 mb-8 flex-1">
                  {["Unlimited AI interviews", "Unlimited resume reviews", "Unlimited aptitude tests", "Unlimited cover letters", "ATS optimization", "PDF/DOCX export", "Detailed feedback", "Priority support"].map((f) => (
                    <li key={f} className="flex items-center gap-2 text-gray-400 text-sm">
                      <CheckCircle size={14} className="text-cyber-green shrink-0" />
                      {f}
                    </li>
                  ))}
                </ul>
                <Link to="/register" className="block text-center btn-primary">Upgrade to Pro</Link>
              </motion.div>
            </StaggerItem>

            {/* Lifetime */}
            <StaggerItem>
              <motion.div whileHover={reduced ? {} : { y: -4 }} className="card-pro h-full flex flex-col">
                <h3 className="font-display font-bold text-white text-lg mb-2">Admiral</h3>
                <p className="text-4xl font-display font-black text-white mb-1">$39</p>
                <p className="text-gray-500 text-xs font-mono mb-6">One-time payment · Lifetime</p>
                <ul className="space-y-3 mb-8 flex-1">
                  {["Everything in Pro", "One-time payment", "Lifetime access", "All future updates", "Priority support"].map((f) => (
                    <li key={f} className="flex items-center gap-2 text-gray-400 text-sm">
                      <CheckCircle size={14} className="text-cyber-green shrink-0" />
                      {f}
                    </li>
                  ))}
                </ul>
                <Link to="/register" className="block text-center btn-pro">Get Lifetime</Link>
              </motion.div>
            </StaggerItem>
          </StaggerContainer>
        </div>
      </section>

      {/* CTA */}
      <section className="relative py-20 px-4 text-center overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-cyber-blue/5 via-cyber-purple/5 to-cyber-blue/5" />
        <div className="absolute inset-0 cyber-grid opacity-30" />
        <motion.div
          className="relative"
          initial={reduced ? {} : { opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
        >
          <h2 className="text-3xl md:text-4xl font-display font-black text-white mb-6">
            Ready for <span className="text-cyber-blue glow-blue">Launch</span>?
          </h2>
          <p className="text-gray-400 mb-8 max-w-xl mx-auto font-mono text-sm">
            Join thousands of cadets who achieved orbit lock with PlacementPro.
          </p>
          <Link to="/register" className="inline-block">
            <span className="btn-primary inline-flex items-center gap-2 text-base px-8 py-4">
              <Zap size={20} /> Initialize Mission
            </span>
          </Link>
        </motion.div>
      </section>
    </div>
  );
}
