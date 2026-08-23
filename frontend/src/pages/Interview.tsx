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

const COMPANIES = [
  { id: "google", name: "Google", color: "from-nature-blossom to-nature-moss", icon: "G", focus: "Algorithms + System Design" },
  { id: "amazon", name: "Amazon", color: "from-nature-sand to-nature-sun", icon: "A", focus: "Leadership Principles + Coding" },
  { id: "meta", name: "Meta", color: "from-nature-blossom to-nature-sky", icon: "M", focus: "Coding + Product Sense" },
  { id: "microsoft", name: "Microsoft", color: "from-nature-moss to-nature-sky", icon: "MS", focus: "Problem Solving + Growth Mindset" },
  { id: "tcs", name: "TCS", color: "from-nature-sky to-nature-blossom", icon: "T", focus: "Aptitude + Programming Basics" },
  { id: "infosys", name: "Infosys", color: "from-nature-sky to-nature-blossom", icon: "I", focus: "Soft Skills + Aptitude" },
  { id: "wipro", name: "Wipro", color: "from-nature-sky to-nature-moss", icon: "W", focus: "Basic Coding + Communication" },
  { id: "uber", name: "Uber", color: "from-nature-bark to-nature-sand", icon: "U", focus: "Real-time Systems + Algorithms" },
  { id: "general", name: "General", color: "from-nature-bark to-nature-sand", icon: "G", focus: "Mixed Practice" },
];

const INTERVIEW_TYPES = [
  { id: "mixed", name: "Full Simulation", icon: Brain, desc: "Behavioral + Technical + Situational", color: "bg-nature-blossom/10 text-nature-blossom" },
  { id: "behavioral", name: "Behavioral Only", icon: MessageSquare, desc: "STAR method, leadership, teamwork", color: "bg-nature-sky/10 text-nature-sky" },
  { id: "technical", name: "Technical Only", icon: Code, desc: "Coding concepts, algorithms, design", color: "bg-nature-moss/10 text-nature-moss" },
];

const DIFFICULTIES = [
  { id: "easy", name: "Easy", desc: "Warm-up questions", color: "border-nature-moss/40 text-nature-moss bg-nature-moss/10" },
  { id: "medium", name: "Medium", desc: "Standard interview level", color: "border-nature-sun/40 text-nature-sun bg-nature-sun/10" },
  { id: "hard", name: "Hard", desc: "FAANG-level challenges", color: "border-nature-blossom/40 text-nature-blossom bg-nature-blossom/10" },
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

  const { mutate: startInterview, isPending: startLoading } = useStartInterview();

  const handleStartInterview = async () => {
    setStep("company");
  };

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <motion.div
          className="text-center mb-10"
          initial={reduced ? {} : { opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
           <span className="nature-chip mb-3 block">Simulated Engagement</span>
           <h1 className="nature-section-header text-3xl mb-2">
             <Bot className="text-nature-blossom inline mr-2" size={28} />
             AI Interview <span className="text-nature-blossom">Simulator</span>
           </h1>
           <p className="text-text-secondary font-mono text-sm">
             Company-specific questions with adaptive difficulty
           </p>
        </motion.div>

        {/* Step Indicator */}
        <div className="flex items-center justify-center gap-2 mb-8">
           {["company", "type", "start"].map((s, i) => (
             <div key={s} className="flex items-center gap-2">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-display font-bold ${
                  step === s ? "bg-nature-blossom text-nature-ink" :
                  ["company", "type", "start"].indexOf(step) > i ? "bg-nature-moss text-text-primary" :
                  "bg-nature-stone border border-nature-leaf/30 text-text-muted"
                }`}>
                  {["company", "type", "start"].indexOf(step) > i ? "✓" : i + 1}
                </div>
                {i < 2 && <div className={`w-12 h-0.5 ${["company", "type", "start"].indexOf(step) > i ? "bg-nature-moss" : "bg-nature-leaf/20"}`} />}
             </div>
           ))}
        </div>

        {error && (
          <div className="bg-brand-accent/10 border border-brand-accent/20 text-brand-accent px-4 py-3 rounded-lg mb-6 text-center font-mono text-sm">
            {error}
          </div>
        )}

        {/* Step 1: Company Selection */}
        {step === "company" && (
          <motion.div initial={reduced ? {} : { opacity: 0 }} animate={{ opacity: 1 }}>
             <h2 className="nature-section-header text-xl mb-6 flex items-center gap-2">
               <Building2 size={20} className="text-nature-blossom" /> Select Company Style
             </h2>
             <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
               {COMPANIES.map((company, i) => (
                 <motion.button
                   key={company.id}
                   onClick={() => setSelectedCompany(company.id)}
                   className={`nature-card text-left transition-all border-2 ${
                     selectedCompany === company.id
                       ? "border-nature-blossom shadow-[0_0_30px_rgba(139,188,168,0.3)]"
                       : "border-transparent hover:border-nature-leaf/30"
                   }`}
                   initial={reduced ? {} : { opacity: 0, y: 20 }}
                   animate={{ opacity: 1, y: 0 }}
                   transition={{ delay: i * 0.05 }}
                   whileHover={reduced ? {} : { scale: 1.02 }}
                   whileTap={reduced ? {} : { scale: 0.98 }}
                 >
                   <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${company.color} flex items-center justify-center text-text-primary font-bold text-sm mb-3`}>
                     {company.icon}
                   </div>
                   <p className="font-display font-bold text-text-primary">{company.name}</p>
                   <p className="text-xs font-mono text-text-muted mt-1">{company.focus}</p>
                 </motion.button>
               ))}
             </div>

             <div className="nature-card mb-6 p-4">
               <label className="block text-xs font-mono uppercase tracking-wider text-text-muted mb-2">Target Role</label>
              <div className="flex flex-wrap gap-2">
                 {ROLES.map((r) => (
                   <button
                     key={r}
                     onClick={() => setRole(r)}
                     className={`px-3 py-1.5 rounded-full text-xs font-mono transition-colors ${
                       role === r
                         ? "bg-nature-blossom text-nature-ink"
                         : "bg-nature-stone border border-nature-leaf/30 text-text-muted hover:text-text-primary hover:border-nature-leaf/50"
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
              className="w-full nature-btn flex items-center justify-center gap-2"
            >
              Next: Interview Type <ArrowRight size={16} />
            </button>
          </motion.div>
        )}

        {/* Step 2: Interview Type + Difficulty */}
        {step === "type" && (
          <motion.div initial={reduced ? {} : { opacity: 0 }} animate={{ opacity: 1 }}>
             <h2 className="nature-section-header text-xl mb-6 flex items-center gap-2">
               <Target size={20} className="text-nature-blossom" /> Mission Configuration
             </h2>

             <div className="nature-card mb-6 p-4">
               <h3 className="nature-section-header text-sm mb-4">Interview Mode</h3>
               <div className="grid sm:grid-cols-3 gap-3">
                 {INTERVIEW_TYPES.map((type) => (
                   <button
                     key={type.id}
                     onClick={() => setSelectedType(type.id)}
                     className={`p-4 rounded-xl text-left transition-all border-2 ${
                       selectedType === type.id
                         ? "border-nature-blossom bg-nature-blossom/10"
                         : "border-nature-leaf/20 hover:border-nature-leaf/40"
                     }`}
                   >
                     <type.icon size={24} className={`mb-2 ${selectedType === type.id ? "text-nature-blossom" : "text-text-muted"}`} />
                     <p className="font-display font-bold text-text-primary text-sm">{type.name}</p>
                     <p className="text-xs font-mono text-text-muted mt-1">{type.desc}</p>
                   </button>
                 ))}
               </div>
             </div>

             <div className="nature-card mb-6 p-4">
               <h3 className="nature-section-header text-sm mb-4">Threat Level</h3>
               <div className="grid sm:grid-cols-3 gap-3">
                 {DIFFICULTIES.map((d) => (
                   <button
                     key={d.id}
                     onClick={() => setDifficulty(d.id)}
                     className={`p-4 rounded-xl text-left transition-all border-2 ${
                       difficulty === d.id
                         ? d.color
                         : "border-nature-leaf/20 hover:border-nature-leaf/40"
                     }`}
                   >
                     <p className="font-display font-bold text-sm text-text-primary">{d.name}</p>
                     <p className="text-xs font-mono text-text-muted mt-1">{d.desc}</p>
                   </button>
                 ))}
               </div>
             </div>

             <div className="nature-card mb-6 p-4 border-nature-blossom/30 bg-nature-blossom/5">
               <div className="flex items-center gap-2 mb-2">
                 <Sparkles size={16} className="text-nature-blossom" />
                 <span className="nature-section-header text-sm">Mission Brief</span>
               </div>
               <p className="text-xs font-mono text-text-muted">
                 {COMPANIES.find(c => c.id === selectedCompany)?.name} style {INTERVIEW_TYPES.find(t => t.id === selectedType)?.name}
                 {" "}for <strong className="text-nature-blossom">{role}</strong> at <strong className="text-nature-blossom">{difficulty}</strong> difficulty.
                 {selectedCompany === "amazon" && " Heavy behavioral + Leadership Principles focus."}
                 {selectedCompany === "google" && " Algorithmic coding + system design emphasis."}
                 {selectedCompany === "meta" && " Coding + product sense evaluation."}
                 {" 20 questions with follow-ups."}
               </p>
             </div>

             <div className="flex gap-4">
               <button onClick={() => setStep("company")} className="nature-btn-ghost">
                 Back
               </button>
               <button
                 onClick={() => startInterview({ jobRole: role, company: selectedCompany, interviewType: selectedType, difficulty })}
                 disabled={startLoading}
                 className="flex-1 nature-btn"
               >
                 {startLoading ? (
                   <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-nature-ink" />
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
