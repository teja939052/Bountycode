import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { motion } from "framer-motion";
import useReducedMotion from "../hooks/useReducedMotion";
import {
  Bot, ArrowRight, Building2, Target, Sparkles,
  Brain, MessageSquare, Code,
} from "lucide-react";

const COMPANIES = [
  { id: "google", name: "Google", color: "from-blue-500 to-green-500", icon: "G", focus: "Algorithms + System Design" },
  { id: "amazon", name: "Amazon", color: "from-orange-400 to-yellow-500", icon: "A", focus: "Leadership Principles + Coding" },
  { id: "meta", name: "Meta", color: "from-blue-600 to-indigo-600", icon: "M", focus: "Coding + Product Sense" },
  { id: "microsoft", name: "Microsoft", color: "from-green-500 to-blue-500", icon: "MS", focus: "Problem Solving + Growth Mindset" },
  { id: "tcs", name: "TCS", color: "from-blue-700 to-blue-900", icon: "T", focus: "Aptitude + Programming Basics" },
  { id: "infosys", name: "Infosys", color: "from-blue-500 to-purple-600", icon: "I", focus: "Soft Skills + Aptitude" },
  { id: "wipro", name: "Wipro", color: "from-blue-600 to-cyan-500", icon: "W", focus: "Basic Coding + Communication" },
  { id: "uber", name: "Uber", color: "from-black to-gray-700", icon: "U", focus: "Real-time Systems + Algorithms" },
  { id: "general", name: "General", color: "from-gray-500 to-gray-700", icon: "G", focus: "Mixed Practice" },
];

const INTERVIEW_TYPES = [
  { id: "mixed", name: "Full Simulation", icon: Brain, desc: "Behavioral + Technical + Situational", color: "bg-space-nebula/20 text-cyber-purple" },
  { id: "behavioral", name: "Behavioral Only", icon: MessageSquare, desc: "STAR method, leadership, teamwork", color: "bg-cyber-blue/10 text-cyber-blue" },
  { id: "technical", name: "Technical Only", icon: Code, desc: "Coding concepts, algorithms, design", color: "bg-cyber-green/10 text-cyber-green" },
];

const DIFFICULTIES = [
  { id: "easy", name: "Easy", desc: "Warm-up questions", color: "border-cyber-green/40 text-cyber-green bg-cyber-green/10" },
  { id: "medium", name: "Medium", desc: "Standard interview level", color: "border-cyber-yellow/40 text-cyber-yellow bg-cyber-yellow/10" },
  { id: "hard", name: "Hard", desc: "FAANG-level challenges", color: "border-cyber-red/40 text-cyber-red bg-cyber-red/10" },
];

const ROLES = [
  "Software Engineer", "Senior Software Engineer", "Staff Engineer",
  "Product Manager", "Data Scientist", "UX Designer",
  "DevOps Engineer", "Business Analyst", "Consultant",
];

export default function InterviewSelect() {
  const [step, setStep] = useState("company");
  const [selectedCompany, setSelectedCompany] = useState(null);
  const [selectedType, setSelectedType] = useState("mixed");
  const [difficulty, setDifficulty] = useState("medium");
  const [role, setRole] = useState("Software Engineer");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const reduced = useReducedMotion();

  const startInterview = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await api.startInterviewV2(role, selectedCompany, selectedType, difficulty);
      navigate(`/interview/${data.interview_id}`, {
        state: {
          interviewId: data.interview_id,
          question: data.question,
          questionType: data.question_type,
          tips: data.tips,
          jobRole: role,
          company: selectedCompany,
          difficulty: data.difficulty,
          companyStyle: data.company_style,
          totalQuestions: data.total_questions,
        },
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <motion.div
          className="text-center mb-10"
          initial={reduced ? {} : { opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <span className="section-subheader mb-3 block">Simulated Engagement</span>
          <h1 className="section-header text-3xl mb-2">
            <Bot className="text-cyber-blue inline mr-2" size={28} />
            AI Interview <span className="text-cyber-blue">Simulator</span>
          </h1>
          <p className="text-gray-500 font-mono text-sm">
            Company-specific questions with adaptive difficulty
          </p>
        </motion.div>

        {/* Step Indicator */}
        <div className="flex items-center justify-center gap-2 mb-8">
          {["company", "type", "start"].map((s, i) => (
            <div key={s} className="flex items-center gap-2">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-display font-bold ${
                step === s ? "bg-cyber-blue text-space-void" :
                ["company", "type", "start"].indexOf(step) > i ? "bg-cyber-green text-space-void" :
                "bg-space-panel border border-space-border text-gray-500"
              }`}>
                {["company", "type", "start"].indexOf(step) > i ? "✓" : i + 1}
              </div>
              {i < 2 && <div className={`w-12 h-0.5 ${["company", "type", "start"].indexOf(step) > i ? "bg-cyber-green" : "bg-space-border"}`} />}
            </div>
          ))}
        </div>

        {error && (
          <div className="bg-cyber-red/10 border border-cyber-red/20 text-cyber-red px-4 py-3 rounded-lg mb-6 text-center font-mono text-sm">
            {error}
          </div>
        )}

        {/* Step 1: Company Selection */}
        {step === "company" && (
          <motion.div initial={reduced ? {} : { opacity: 0 }} animate={{ opacity: 1 }}>
            <h2 className="font-display font-bold text-white mb-6 flex items-center gap-2">
              <Building2 size={20} className="text-cyber-blue" /> Select Company Style
            </h2>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
              {COMPANIES.map((company, i) => (
                <motion.button
                  key={company.id}
                  onClick={() => setSelectedCompany(company.id)}
                  className={`card text-left transition-all border-2 ${
                    selectedCompany === company.id
                      ? "border-cyber-blue shadow-lg shadow-cyber-blue/10"
                      : "border-transparent hover:border-space-border"
                  }`}
                  initial={reduced ? {} : { opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.05 }}
                  whileHover={reduced ? {} : { scale: 1.02 }}
                  whileTap={reduced ? {} : { scale: 0.98 }}
                >
                  <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${company.color} flex items-center justify-center text-white font-bold text-sm mb-3`}>
                    {company.icon}
                  </div>
                  <p className="font-display font-bold text-white">{company.name}</p>
                  <p className="text-xs font-mono text-gray-500 mt-1">{company.focus}</p>
                </motion.button>
              ))}
            </div>

            <div className="card mb-6">
              <label className="block text-xs font-mono uppercase tracking-wider text-gray-400 mb-2">Target Role</label>
              <div className="flex flex-wrap gap-2">
                {ROLES.map((r) => (
                  <button
                    key={r}
                    onClick={() => setRole(r)}
                    className={`px-3 py-1.5 rounded-full text-xs font-mono transition-colors ${
                      role === r
                        ? "bg-cyber-blue text-space-void"
                        : "bg-space-panel border border-space-border text-gray-400 hover:text-white hover:border-gray-500"
                    }`}
                  >
                    {r}
                  </button>
                ))}
              </div>
            </div>

            <button
              onClick={() => setStep("type")}
              disabled={!selectedCompany}
              className="w-full btn-primary flex items-center justify-center gap-2"
            >
              Next: Interview Type <ArrowRight size={16} />
            </button>
          </motion.div>
        )}

        {/* Step 2: Interview Type + Difficulty */}
        {step === "type" && (
          <motion.div initial={reduced ? {} : { opacity: 0 }} animate={{ opacity: 1 }}>
            <h2 className="font-display font-bold text-white mb-6 flex items-center gap-2">
              <Target size={20} className="text-cyber-blue" /> Mission Configuration
            </h2>

            <div className="card mb-6">
              <h3 className="font-display font-bold text-white text-sm mb-4">Interview Mode</h3>
              <div className="grid sm:grid-cols-3 gap-3">
                {INTERVIEW_TYPES.map((type) => (
                  <button
                    key={type.id}
                    onClick={() => setSelectedType(type.id)}
                    className={`p-4 rounded-xl text-left transition-all border-2 ${
                      selectedType === type.id
                        ? "border-cyber-blue bg-cyber-blue/10"
                        : "border-space-border hover:border-gray-600"
                    }`}
                  >
                    <type.icon size={24} className={`mb-2 ${selectedType === type.id ? "text-cyber-blue" : "text-gray-500"}`} />
                    <p className="font-display font-bold text-white text-sm">{type.name}</p>
                    <p className="text-xs font-mono text-gray-500 mt-1">{type.desc}</p>
                  </button>
                ))}
              </div>
            </div>

            <div className="card mb-6">
              <h3 className="font-display font-bold text-white text-sm mb-4">Threat Level</h3>
              <div className="grid sm:grid-cols-3 gap-3">
                {DIFFICULTIES.map((d) => (
                  <button
                    key={d.id}
                    onClick={() => setDifficulty(d.id)}
                    className={`p-4 rounded-xl text-left transition-all border-2 ${
                      difficulty === d.id
                        ? d.color
                        : "border-space-border hover:border-gray-600"
                    }`}
                  >
                    <p className="font-display font-bold text-sm">{d.name}</p>
                    <p className="text-xs font-mono text-gray-500 mt-1">{d.desc}</p>
                  </button>
                ))}
              </div>
            </div>

            <div className="card mb-6 border-cyber-blue/20 bg-cyber-blue/5">
              <div className="flex items-center gap-2 mb-2">
                <Sparkles size={16} className="text-cyber-blue" />
                <span className="font-display font-bold text-cyber-blue text-sm">Mission Brief</span>
              </div>
              <p className="text-xs font-mono text-gray-400">
                {COMPANIES.find(c => c.id === selectedCompany)?.name} style {INTERVIEW_TYPES.find(t => t.id === selectedType)?.name}
                {" "}for <strong className="text-white">{role}</strong> at <strong className="text-white">{difficulty}</strong> difficulty.
                {selectedCompany === "amazon" && " Heavy behavioral + Leadership Principles focus."}
                {selectedCompany === "google" && " Algorithmic coding + system design emphasis."}
                {selectedCompany === "meta" && " Coding + product sense evaluation."}
                {" 10 questions with follow-ups."}
              </p>
            </div>

            <div className="flex gap-4">
              <button onClick={() => setStep("company")} className="btn-secondary">
                Back
              </button>
              <button
                onClick={startInterview}
                disabled={loading}
                className="flex-1 btn-primary flex items-center justify-center gap-2"
              >
                {loading ? (
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-space-void" />
                ) : (
                  <>
                    Launch Simulation
                    <ArrowRight size={16} />
                  </>
                )}
              </button>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
}
