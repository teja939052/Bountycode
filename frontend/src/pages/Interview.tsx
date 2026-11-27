import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useStartInterview } from "../hooks/useInterviews";
import api from "../services/api";
import { motion } from "framer-motion";
import useReducedMotion from "../hooks/useReducedMotion";
import {
  Bot, ArrowRight, Building2, Target, Sparkles,
  Brain, MessageSquare, Code,
} from "lucide-react";
import { Card, SectionHeader } from "../design-system/Card";
import { Button } from "../design-system/Button";

const COMPANIES = [
  { id: "google", name: "Google", icon: "G", focus: "Algorithms + System Design" },
  { id: "amazon", name: "Amazon", icon: "A", focus: "Leadership Principles + Coding" },
  { id: "meta", name: "Meta", icon: "M", focus: "Coding + Product Sense" },
  { id: "microsoft", name: "Microsoft", icon: "MS", focus: "Problem Solving + Growth Mindset" },
  { id: "tcs", name: "TCS", icon: "T", focus: "Aptitude + Programming Basics" },
  { id: "infosys", name: "Infosys", icon: "I", focus: "Soft Skills + Aptitude" },
  { id: "wipro", name: "Wipro", icon: "W", focus: "Basic Coding + Communication" },
  { id: "uber", name: "Uber", icon: "U", focus: "Real-time Systems + Algorithms" },
  { id: "general", name: "General", icon: "G", focus: "Mixed Practice" },
];

const INTERVIEW_TYPES = [
  { id: "mixed", name: "Full Simulation", icon: Brain, desc: "Behavioral + Technical + Situational" },
  { id: "behavioral", name: "Behavioral Only", icon: MessageSquare, desc: "STAR method, leadership, teamwork" },
  { id: "technical", name: "Technical Only", icon: Code, desc: "Coding concepts, algorithms, design" },
];

const DIFFICULTIES = [
  { id: "easy", name: "Easy", desc: "Warm-up questions", color: "subject-verbal" },
  { id: "medium", name: "Medium", desc: "Standard interview level", color: "subject-aptitude" },
  { id: "hard", name: "Hard", desc: "FAANG-level challenges", color: "subject-interview" },
];

const ROLES = [
  "Software Engineer", "Senior Software Engineer", "Staff Engineer",
  "Product Manager", "Data Scientist", "UX Designer",
  "DevOps Engineer", "Business Analyst", "Consultant",
];

export default function InterviewSelect() {
  const [step, setStep] = useState("company");
  const [selectedCompany, setSelectedCompany] = useState<string | null>(null);
  const [selectedType, setSelectedType] = useState("mixed");
  const [difficulty, setDifficulty] = useState("medium");
  const [role, setRole] = useState("Software Engineer");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const reduced = useReducedMotion();

  const { mutate: startInterview, isPending: startLoading } = useStartInterview();

  const handleStartInterview = async () => {
    setStep("company");
  };

  return (
    <div className="min-h-screen bg-canvas py-6 px-3 sm:px-4">
      <div className="max-w-4xl mx-auto">
        <motion.div
          className="text-center mb-6"
          initial={reduced ? {} : { opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <span className="inline-block mb-2 px-2 py-0.5 rounded-full text-xs font-bold tracking-wider text-primary bg-primary/10 border border-primary/20 uppercase">
            AI Interview Simulator
          </span>
          <h1 className="mt-2 text-3xl font-black tracking-tight text-text">
            <Bot className="text-primary inline mr-2" size={28} />
            AI Interview Simulator
          </h1>
          <p className="mt-2 text-sm text-text-secondary font-mono">
            Company-specific questions with adaptive difficulty
          </p>
        </motion.div>

        {/* Step Indicator */}
        <div className="flex items-center justify-center gap-2 mb-6">
          {["company", "type", "start"].map((s, i) => (
            <div key={s} className="flex items-center gap-2">
              <div className={`w-10 h-10 rounded-full flex items-center justify-center text-xs font-display font-bold transition-all ${
                step === s
                  ? "bg-primary text-primary-text shadow-primary"
                  : ["company", "type", "start"].indexOf(step) > i
                    ? "bg-subject-verbal text-white"
                    : "bg-surface border border-border text-text-muted"
              }`}>
                {["company", "type", "start"].indexOf(step) > i ? "✓" : i + 1}
              </div>
              {i < 2 && <div className={`w-10 h-0.5 ${["company", "type", "start"].indexOf(step) > i ? "bg-primary" : "bg-border/30"}`} />}
            </div>
          ))}
        </div>

        {error && (
          <div className="mb-6 p-4 rounded-xl border border-subject-boss/30 bg-subject-boss/5 text-subject-boss text-sm font-medium text-center">
            {error}
          </div>
        )}

        {/* Step 1: Company Selection */}
        {step === "company" && (
          <motion.div initial={reduced ? {} : { opacity: 0 }} animate={{ opacity: 1 }}>
            <h2 className="mb-4 text-lg font-black text-text flex items-center gap-2">
              <Building2 size={20} className="text-primary" /> Select Company Style
            </h2>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3 mb-6">
              {COMPANIES.map((company, i) => (
                <motion.button
                  key={company.id}
                  onClick={() => setSelectedCompany(company.id)}
                  className={`text-left transition-all border border-border rounded-xl p-4 ${
                    selectedCompany === company.id
                      ? "bg-primary/10 border-primary/50 shadow-primary"
                      : "hover:bg-surfaceHover hover:border-primary/30"
                  }`}
                  initial={reduced ? {} : { opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.05 }}
                  whileHover={reduced ? {} : { scale: 1.02 }}
                  whileTap={reduced ? {} : { scale: 0.98 }}
                >
                  <div className={`w-12 h-12 rounded-xl bg-surfaceHover flex items-center justify-center text-text-primary font-bold text-sm mb-3`}>
                    {company.icon}
                  </div>
                  <p className="font-display font-bold text-text">{company.name}</p>
                  <p className="text-[10px] font-mono text-text-muted mt-1">{company.focus}</p>
                </motion.button>
              ))}
            </div>

            <Card pad="md" className="mb-6">
              <div className="flex items-center gap-2 mb-2">
                <label className="text-[10px] font-bold uppercase tracking-wider text-text-muted">Target Role</label>
              </div>
              <div className="flex flex-wrap gap-2">
                {ROLES.map((r) => (
                  <button
                    key={r}
                    onClick={() => setRole(r)}
                    className={`px-3 py-1.5 rounded-xl text-xs font-medium transition-colors ${
                      role === r
                        ? "bg-primary text-primary-text shadow-primary"
                        : "border border-border/30 bg-surfaceHover text-text-secondary hover:bg-surfaceHover hover:border-primary/50"
                    }`}
                  >
                    {r}
                  </button>
                ))}
              </div>
            </Card>

            <Button
              variant="primary"
              onClick={() => setStep("type")}
              disabled={!selectedCompany}
              className="w-full text-sm font-bold shadow-primary"
            >
              Next: Interview Type <ArrowRight size={16} />
            </Button>
          </motion.div>
        )}

        {/* Step 2: Interview Type + Difficulty */}
        {step === "type" && (
          <motion.div initial={reduced ? {} : { opacity: 0 }} animate={{ opacity: 1 }}>
            <h2 className="mb-4 text-lg font-black text-text flex items-center gap-2">
              <Target size={20} className="text-primary" /> Mission Configuration
            </h2>

            <Card pad="md" className="mb-6">
              <h3 className="text-xs font-bold uppercase tracking-wider text-text-muted mb-3">Interview Mode</h3>
              <div className="grid sm:grid-cols-3 gap-3">
                {INTERVIEW_TYPES.map((type) => (
                  <button
                    key={type.id}
                    onClick={() => setSelectedType(type.id)}
                    className={`p-4 rounded-xl text-left transition-all border border-border/50 ${
                      selectedType === type.id
                        ? "bg-primary/10 border-primary/50 shadow-primary"
                        : "hover:bg-surfaceHover hover:border-primary/30"
                    }`}
                  >
                    <type.icon size={24} className={`mb-2 ${selectedType === type.id ? "text-primary" : "text-text-muted"}`} />
                    <p className="font-bold text-sm text-text">{type.name}</p>
                    <p className="text-[10px] font-mono text-text-muted mt-1">{type.desc}</p>
                  </button>
                ))}
              </div>
            </Card>

            <Card pad="md" className="mb-6">
              <h3 className="text-xs font-bold uppercase tracking-wider text-text-muted mb-3">Difficulty</h3>
              <div className="grid sm:grid-cols-3 gap-3">
                {DIFFICULTIES.map((d) => (
                  <button
                    key={d.id}
                    onClick={() => setDifficulty(d.id)}
                    className={`p-4 rounded-xl text-left transition-all border border-border/50 ${
                      difficulty === d.id
                        ? `bg-${d.color}/10 border-${d.color}/50 shadow-${d.color}`
                        : "hover:bg-surfaceHover hover:border-primary/30"
                    }`}
                  >
                    <p className="font-bold text-sm text-text">{d.name}</p>
                    <p className="text-[10px] font-mono text-text-muted mt-1">{d.desc}</p>
                  </button>
                ))}
              </div>
            </Card>

            <Card pad="md" tone="interview" className="mb-6">
              <div className="flex items-center gap-2 mb-2">
                <Sparkles size={16} className="text-primary" />
                <span className="text-xs font-bold uppercase tracking-wider text-primary">Mission Brief</span>
              </div>
              <p className="text-xs font-mono text-text-secondary leading-relaxed">
                {COMPANIES.find(c => c.id === selectedCompany)?.name} style {INTERVIEW_TYPES.find(t => t.id === selectedType)?.name}
                {" "}for <strong className="text-text">{role}</strong> at <strong className="text-text">{difficulty}</strong> difficulty.
                {selectedCompany === "amazon" && " Heavy behavioral + Leadership Principles focus."}
                {selectedCompany === "google" && " Algorithmic coding + system design emphasis."}
                {selectedCompany === "meta" && " Coding + product sense evaluation."}
                {" 20 questions with follow-ups."}
              </p>
            </Card>

            <div className="flex gap-2">
              <Button variant="outline" onClick={() => setStep("company")} size="md">
                Back
              </Button>
              <Button
                variant="primary"
                onClick={() => startInterview({ jobRole: role, company: selectedCompany, interviewType: selectedType, difficulty })}
                disabled={startLoading}
                className="flex-1 text-sm font-bold shadow-primary"
              >
                {startLoading ? (
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white/40" />
                ) : (
                  <>
                    Launch Simulation
                    <ArrowRight size={16} />
                  </>
                )}
              </Button>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
}
