import { useState } from "react";
import { motion } from "framer-motion";
import { ArrowRight, Clock, Target, Briefcase } from "lucide-react";

const ROLES = [
  { id: "sde", name: "Software Development Engineer", icon: "💻", description: "Build systems that scale. Full backend + algorithms + system design.", skills: ["Python/Java/C++", "DSA", "System Design", "APIs", "Databases"], targets: ["Google", "Amazon", "Microsoft", "Meta"], hours: 120, color: "from-blue-500 to-indigo-600" },
  { id: "data_scientist", name: "Data Scientist", icon: "📊", description: "Extract insights from data. Statistics + SQL + Python + storytelling.", skills: ["Python", "SQL", "Statistics", "Data Analysis", "Visualization"], targets: ["Data Scientist", "Analyst", "Product Analyst"], hours: 80, color: "from-emerald-500 to-teal-600" },
  { id: "ml_engineer", name: "Machine Learning Engineer", icon: "🤖", description: "Build and deploy ML systems. From models to production.", skills: ["Python", "ML", "Deep Learning", "LLMs", "RAG", "MLOps"], targets: ["ML Engineer", "Applied Scientist", "AI Engineer"], hours: 150, color: "from-purple-500 to-violet-600" },
  { id: "devops", name: "DevOps / SRE", icon: "⚙️", description: "Keep systems running. Reliability, automation, infrastructure.", skills: ["Linux", "Docker", "Kubernetes", "CI/CD", "Monitoring", "Cloud"], targets: ["DevOps Engineer", "SRE", "Platform Engineer"], hours: 90, color: "from-orange-500 to-red-600" },
  { id: "frontend", name: "Frontend Engineer", icon: "🎨", description: "Build interfaces users love. JavaScript + React + system design.", skills: ["JavaScript", "TypeScript", "React", "HTML/CSS", "APIs", "Testing"], targets: ["Frontend Engineer", "UI Engineer", "Full Stack"], hours: 100, color: "from-pink-500 to-rose-600" },
  { id: "cp", name: "Competitive Programmer", icon: "🏆", description: "Master algorithms for competitions and tough interviews.", skills: ["C++", "Algorithms", "Data Structures", "Math", "Speed"], targets: ["Code Jam", "ICPC", "Top-tier interviews"], hours: 200, color: "from-amber-500 to-yellow-600" },
];

/**
 * Role selection page — choose your career path.
 *
 * Each role maps to a curated path through the 12 worlds.
 * The selected role personalizes the learning journey.
 */
export default function RoleSelect() {
  const [selected, setSelected] = useState<string | null>(null);

  return (
    <div className="min-h-screen bg-gradient-to-b from-[var(--pp-canvas)] to-white">
      <div className="mx-auto max-w-[900px] px-4 py-8">
        {/* Header */}
        <motion.div
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="text-center mb-8"
        >
          <h1 className="text-2xl font-bold text-text-primary">Choose Your Path</h1>
          <p className="text-sm text-text-muted mt-2">
            Select the role you're preparing for. We'll curate your journey through the 12 worlds.
          </p>
        </motion.div>

        {/* Role grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {ROLES.map((role, idx) => (
            <motion.button
              key={role.id}
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: idx * 0.08 }}
              whileHover={{ y: -4, scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setSelected(role.id)}
              className={`relative rounded-2xl border-2 p-5 text-left transition-all overflow-hidden group ${
                selected === role.id
                  ? "border-primary bg-primary/5 shadow-lg ring-2 ring-primary/20"
                  : "border-border bg-white hover:border-primary/30 hover:shadow-md"
              }`}
            >
              {/* Gradient accent */}
              <div className={`absolute top-0 left-0 right-0 h-1 bg-gradient-to-r ${role.color}`} />

              <div className="flex items-start gap-3">
                <span className="text-3xl">{role.icon}</span>
                <div className="flex-1 min-w-0">
                  <h3 className="text-sm font-bold text-text-primary leading-tight">{role.name}</h3>
                  <p className="text-[11px] text-text-muted mt-1 line-clamp-2">{role.description}</p>
                </div>
              </div>

              {/* Skills */}
              <div className="mt-3 flex flex-wrap gap-1">
                {role.skills.slice(0, 4).map((skill) => (
                  <span key={skill} className="text-[10px] bg-zinc-100 text-zinc-600 px-1.5 py-0.5 rounded-full">
                    {skill}
                  </span>
                ))}
                {role.skills.length > 4 && (
                  <span className="text-[10px] text-text-muted">+{role.skills.length - 4}</span>
                )}
              </div>

              {/* Meta */}
              <div className="mt-3 flex items-center gap-3 text-[11px] text-text-muted">
                <span className="flex items-center gap-1">
                  <Clock className="w-3 h-3" /> {role.hours}h
                </span>
                <span className="flex items-center gap-1">
                  <Target className="w-3 h-3" /> {role.targets[0]}
                </span>
              </div>

              {/* Selected indicator */}
              {selected === role.id && (
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  className="absolute top-3 right-3 h-6 w-6 rounded-full bg-primary flex items-center justify-center"
                >
                  <svg className="w-3.5 h-3.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                </motion.div>
              )}
            </motion.button>
          ))}
        </div>

        {/* Continue */}
        {selected && (
          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            className="mt-6 text-center"
          >
            <button
              onClick={() => {
                // Store selected role and navigate to journey
                localStorage.setItem("bountycode_role", selected);
                window.location.href = "/journey";
              }}
              className="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-primary to-primary-dark text-white font-semibold px-8 py-3.5 shadow-lg hover:shadow-xl transition-shadow min-h-[48px]"
            >
              Start Your Journey
              <ArrowRight className="w-4 h-4" />
            </button>
          </motion.div>
        )}
      </div>
    </div>
  );
}
