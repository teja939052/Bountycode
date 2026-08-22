import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import api from "../services/api";
import useReducedMotion from "../hooks/useReducedMotion";
import {
  Code2, Cpu, Network, Database, Globe, Shield, BookOpen,
  Check, Lock, ArrowRight
} from "lucide-react";

const FOUNDATIONS = [
  { id: "arrays", label: "Arrays & Strings", icon: Code2, progress: 100, completed: true },
  { id: "linked-lists", label: "Linked Lists", icon: Code2, progress: 100, completed: true },
  { id: "trees", label: "Trees", icon: Code2, progress: 72, completed: false },
  { id: "graphs", label: "Graphs", icon: Code2, progress: 58, completed: false },
];

const PROBLEM_SOLVER = [
  { id: "dsa-patterns", label: "DSA Patterns", icon: Code2, progress: 72, completed: false, locked: false },
  { id: "dbms", label: "DBMS", icon: Database, progress: 45, completed: false, locked: false },
  { id: "os", label: "Operating Systems", icon: Cpu, progress: 38, completed: false, locked: false },
  { id: "networks", label: "Computer Networks", icon: Network, progress: 52, completed: false, locked: false },
  { id: "system-design", label: "System Design", icon: Network, progress: 0, completed: false, locked: true },
  { id: "web", label: "Web Dev", icon: Globe, progress: 0, completed: false, locked: true },
];

const BUILDER = [
  { id: "projects", label: "Portfolio Projects", icon: Code2, progress: 0, completed: false, locked: true },
  { id: "resume", label: "Resume Studio", icon: BookOpen, progress: 0, completed: false, locked: true },
  { id: "interview", label: "Interview Prep", icon: Shield, progress: 0, completed: false, locked: true },
];

interface SkillData {
  sde_ready?: number;
  foundations?: number;
  problem_solver?: number;
  builder?: number;
}

export default function Prepare() {
  const reduced = useReducedMotion();
  const [skills, setSkills] = useState<SkillData | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const data = await api.gamification.getSkills().catch(() => null);
        if (data) setSkills(data);
      } catch {
        // Use defaults
      }
    })();
  }, []);

  const sdeReady = skills?.sde_ready || 68;

  return (
    <div className="min-h-screen px-4 py-6 md:py-8 page-surface">
      <div className="mx-auto max-w-5xl space-y-8">
        {/* Header */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: -16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45 }}
        >
          <h1 className="text-2xl md:text-3xl font-black text-text-primary">Your SDE Journey</h1>
          <p className="text-sm text-text-muted mt-1">Build skills step by step. Each region must be mastered.</p>
        </motion.div>

        {/* SDE Ready Meter */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="rounded-[16px] p-6 bg-white border border-border shadow-card"
        >
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-lg font-bold text-text-primary">SDE Ready</h2>
            <span className="text-sm font-medium text-primary">{sdeReady}%</span>
          </div>
          <div className="h-3 rounded-full bg-border overflow-hidden">
            <div
              className="h-full rounded-full bg-primary transition-all duration-500 ease-out"
              style={{ width: `${sdeReady}%` }}
            />
          </div>
        </motion.div>

        {/* Journey Tree */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <JourneyRegion
            name="🌱 Foundations"
            subtitle="Core programming patterns"
            progress={100}
            completed={true}
            items={FOUNDATIONS}
            reduced={reduced}
          />

          <JourneyRegion
            name="⚔ Problem Solver"
            subtitle="Algorithms & CS fundamentals"
            progress={72}
            completed={false}
            items={PROBLEM_SOLVER}
            reduced={reduced}
          />

          <JourneyRegion
            name="🔒 Builder"
            subtitle="Projects, resume, and interview mastery"
            progress={0}
            completed={false}
            locked={true}
            items={BUILDER}
            reduced={reduced}
          />
        </motion.div>
      </div>
    </div>
  );
}

function JourneyRegion({
  name,
  subtitle,
  progress,
  completed,
  locked,
  items,
  reduced,
}: {
  name: string;
  subtitle: string;
  progress: number;
  completed: boolean;
  locked?: boolean;
  items: Array<{
    id: string;
    label: string;
    icon: React.ReactNode;
    progress: number;
    completed: boolean;
    locked?: boolean;
  }>;
  reduced: boolean;
}) {
  return (
    <motion.div
      initial={reduced ? {} : { opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="mb-8"
    >
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-3">
          <span className="text-xl">{name.split(" ")[0]}</span>
          <h3 className="text-lg font-bold text-text-primary">{name.split(" ").slice(1).join(" ")}</h3>
        </div>
        <div className="flex items-center gap-2 text-sm">
          {completed && <Check size={14} className="text-primary" />}
          {locked && <Lock size={14} className="text-text-muted" />}
          <span className="text-sm font-medium text-text-primary">{progress}%</span>
        </div>
      </div>
      <p className="text-xs text-text-muted mb-4">{subtitle}</p>

      <div className="grid gap-3 sm:grid-cols-2 md:grid-cols-3">
        {items.map((item) => (
          <div
            key={item.id}
            className={`rounded-[16px] p-4 border transition-all duration-200 ${
              item.locked
                ? "bg-surface-2 border-border opacity-50"
                : "bg-white border-border hover:border-primary/20"
            }`}
          >
            {item.completed ? (
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <item.icon size={18} className="text-primary" />
                  <span className="font-medium text-text-primary">{item.label}</span>
                </div>
                <Check size={14} className="text-primary" />
              </div>
            ) : item.locked ? (
              <div className="flex items-center gap-2">
                <Lock size={18} className="text-text-muted" />
                <span className="font-medium text-text-muted">{item.label}</span>
              </div>
            ) : (
              <Link to={`/modules/${item.id}`} className="flex items-center justify-between group">
                <div className="flex items-center gap-2">
                  <item.icon size={18} className="text-blue" />
                  <span className="font-medium text-text-primary">{item.label}</span>
                </div>
                <ArrowRight size={14} className="text-text-muted group-hover:text-primary transition-colors" />
              </Link>
            )}
            {(item.progress > 0 && !item.locked) && (
              <div className="mt-2 h-1.5 rounded-full bg-border overflow-hidden">
                <div
                  className="h-full rounded-full bg-primary"
                  style={{ width: `${item.progress}%` }}
                />
              </div>
            )}
          </div>
        ))}
      </div>
    </motion.div>
  );
}
