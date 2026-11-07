import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  Play,
  ArrowRight,
  Target,
  Zap,
  Code2,
  Star,
  Flame,
  GraduationCap,
  Rocket,
  ShieldCheck,
  Brain,
  Puzzle,
  Layers,
  RefreshCw,
  ChevronRight,
} from "lucide-react";

import Button from "../components/ui/Button";
import { Card } from "../components/ui/Card";
import { PageShell } from "../design-system/PageShell";

/* ------------------------------------------------------------------ */
/*  Shared skill map data                                             */
/* ------------------------------------------------------------------ */
type SkillNode = {
  id: string;
  title: string;
  description: string;
  topic: string;
  level: number; // 1-5 difficulty
  xp: number;
  prerequisites: string[]; // skill ids that must be completed first
  x: number; // percentage 0-100
  y: number; // percentage 0-100
  color: string;
  icon: string; // lucide icon name
};

const SKILL_NODES: SkillNode[] = [
  { id: "loops", title: "Loops", description: "Repeat work automatically", topic: "Loops", level: 1, xp: 50, prerequisites: [], x: 12, y: 22, color: "#22c55e", icon: "Play" },
  { id: "nested-loops", title: "Nested Loops", description: "Loops inside loops", topic: "Loops", level: 2, xp: 100, prerequisites: ["loops"], x: 32, y: 22, color: "#22c55e", icon: "Play" },
  { id: "arrays", title: "Arrays", description: "Store lists of data", topic: "Arrays", level: 1, xp: 75, prerequisites: [], x: 30, y: 45, color: "#22c55e", icon: "Code2" },
  { id: "basic-complexity", title: "Basic Complexity", description: "O(n), O(n²) basics", topic: "Basic Complexity", level: 1, xp: 60, prerequisites: [], x: 55, y: 20, color: "#3b82f6", icon: "Zap" },
  {
    id: "basic-complexity-2",
    title: "Nested Complexity",
    description: "O(n²), O(n³)",
    topic: "Basic Complexity",
    level: 2,
    xp: 120,
    prerequisites: ["basic-complexity"],
    x: 70,
    y: 20,
    color: "#3b82f6",
    icon: "Zap",
  },
  {
    id: "sorting",
    title: "Sorting",
    description: "Sort data efficiently",
    topic: "Algorithms",
    level: 3,
    xp: 150,
    prerequisites: ["arrays"],
    x: 70,
    y: 45,
    color: "#3b82f6",
    icon: "Zap",
  },
  {
    id: "searching",
    title: "Searching",
    description: "Find elements fast",
    topic: "Algorithms",
    level: 3,
    xp: 150,
    prerequisites: ["arrays"],
    x: 70,
    y: 65,
    color: "#3b82f6",
    icon: "Zap",
  },
  {
    id: "recursion",
    title: "Recursion",
    description: "Functions that call themselves",
    topic: "Advanced",
    level: 4,
    xp: 200,
    prerequisites: ["nested-loops", "functions"],
    x: 88,
    y: 22,
    color: "#a855f7",
    icon: "Brain",
  },
  {
    id: "dp",
    title: "Dynamic Programming",
    description: "Optimize with memoization",
    topic: "Advanced",
    level: 5,
    xp: 300,
    prerequisites: ["recursion", "arrays"],
    x: 88,
    y: 65,
    color: "#a855f7",
    icon: "Brain",
  },
];

const SKILL_MAP: Record<string, SkillNode> = {};
SKILL_NODES.forEach((q) => {
  SKILL_MAP[q.id] = q;
});

/* ------------------------------------------------------------------ */
/*  Helpers                                                           */
/* ------------------------------------------------------------------ */
const getCompletedSkills = (): string[] => {
  try {
    const raw = localStorage.getItem("bounty_completed_skills");
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
};

const saveCompletedSkills = (ids: string[]) => {
  localStorage.setItem("bounty_completed_skills", JSON.stringify([...new Set(ids)]));
};

const isCompleted = (id: string, completed: string[]) => completed.includes(id);
const canUnlock = (id: string, completed: string[]) => {
  const skill = SKILL_MAP[id];
  if (!skill) return false;
  return skill.prerequisites.every((p) => completed.includes(p));
};

/* ------------------------------------------------------------------ */
/*  Sub-components                                                    */
/* ------------------------------------------------------------------ */
function SkillNodeItem({ skill }: { skill: SkillNode }) {
  const [completed, setCompleted] = useState<boolean>(isCompleted(skill.id, getCompletedSkills()));
  const isCurrent = canUnlock(skill.id, getCompletedSkills());

  const getStatus = () => {
    if (completed) return "completed";
    if (isCurrent) return "current";
    return "locked";
  };

  const toggle = async () => {
    if (getStatus() === "locked") return;
    const next = !completed;
    setCompleted(next);
    const updated = getCompletedSkills();
    if (next) {
      saveCompletedSkills([...updated, skill.id]);
    } else {
      setCompleted(false);
      saveCompletedSkills(updated.filter((id) => id !== skill.id));
    }
  };

  const status = getStatus();

  return (
    <div
      className={"group cursor-pointer flex flex-col items-center justify-center w-[90px] h-[100px] " + (status === "completed" ? "ring-2 ring-brand-500/50 ring-offset-2 rounded-full bg-[#0f0f0f]" : status === "current" ? "bg-[#16161a] border border-[#ffa116]" : "bg-[#16161a] border border-[#2a2a2a] opacity-50")}
      style={{
        left: skill.x + "%",
        top: skill.y + "%",
      }}
      onClick={() => toggle()}
      title={skill.title + " (" + skill.xp + " XP)"}
    >
      <div className="w-10 h-10 rounded-full flex items-center justify-center text-white text-xl mb-1 bg-[#0f0f0f] border border-[#2a2a2a]">
        <span style={{ fontSize: "16px" }}>{skill.icon}</span>
      </div>
      <div className="text-[9px] font-bold text-[#e9e9e9] text-center leading-tight leading-[1.1]">{skill.title}</div>
      <div className="w-2 h-2 rounded-full bg-[#4ade80] mt-1" style={{ display: completed ? "block" : "none" }} />
    </div>
  );
}

export default function Landing() {
  const navigate = useNavigate();
  const [selectedSkill, setSelectedSkill] = useState<string | null>(null);
  const [completed, setCompleted] = useState<string[]>(getCompletedSkills());

  const handleSkillClick = (id: string) => {
    setSelectedSkill(id);
    navigate("/learning/" + id);
  };

  return (
    <PageShell theme="adventure" className="min-h-screen relative">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-b from-[#0f172a] via-[#0f172a] to-[#1e1a3a] pointer-events-none" />
      <div className="absolute inset-0 opacity-10" style={{ backgroundImage: "radial-gradient(circle at 20% 20%, rgba(99, 102, 241, 0.15), transparent 60%)" }} />

      {/* Navbar */}
      <div className="relative z-20 flex items-center justify-between px-6 py-4">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-brand-500 flex items-center justify-center">
            <Code2 className="w-5 h-5 text-white" />
          </div>
          <span className="text-xl font-bold text-text-primary">Bountycode</span>
        </div>
        <div className="flex gap-3">
          <Button variant="outline" size="sm">
            Login
          </Button>
          <Button variant="primary" size="sm">
            Join Free
          </Button>
        </div>
      </div>

      <main className="relative z-10 px-6 py-8">
        {/* Hero */}
        <section className="flex flex-col md:flex-row items-center gap-12 mb-16">
          <div className="flex-1 md:w-1/2">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-500/20 text-brand-500 text-xs font-bold uppercase tracking-wider mb-3">
              Start Your Journey
            </div>
            <h1 className="text-5xl font-bold text-ink dark:text-white mb-4 leading-tight">
              Build real programming<br />
              <span className="text-brand-500">mental models</span>
            </h1>
            <p className="text-text-muted text-lg mb-6">
              Master loops, arrays, complexity and more through trace, predict, build & repair.
            </p>
            <div className="flex gap-3">
              <Button variant="primary" onClick={() => navigate("/learning")}
                className="px-8 py-3 text-lg"
              >
                Start Coding <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
              <Button variant="outline">
                Browse Lessons
              </Button>
            </div>
            <div className="mt-6 flex items-center gap-4 text-sm text-text-muted">
              <div className="flex items-center gap-1">
                <Star className="w-4 h-4 text-[#fbbf24]" />
                <span>10,000+ students learning</span>
              </div>
              <div className="flex items-center gap-1">
                <Flame className="w-4 h-4 text-orange-500" />
                <span>2,400 active students</span>
              </div>
            </div>
          </div>
          <div className="flex-1 md:w-1/2 relative">
            <div className="relative w-full aspect-square">
              {/* Skill Map SVG */}
              <svg
                width="100%"
                height="100%"
                viewBox="0 0 100 100"
                className="w-full h-[500px]"
              >
{/* Connection Lines */}
                {SKILL_NODES.map((skill) => {
                  const deps = skill.prerequisites.map((id) => SKILL_MAP[id]).filter(Boolean);
                  return deps.map((parent) => (
                    <line
                      key={parent.id + "-" + skill.id}
                      x1={parent.x}
                      y1={parent.y}
                      x2={skill.x}
                      y2={skill.y}
                      stroke={completed.includes(parent.id) ? "#22c55e" : "#2a2a2a"}
                      strokeWidth={completed.includes(parent.id) ? 3 : 1}
                      opacity={completed.includes(parent.id) ? 0.8 : 0.3}
                    />
                  ));
                })}
                {/* Nodes */}
                {SKILL_NODES.map((skill) => {
                  const isComplete = completed.includes(skill.id);
                  const isUnlocked = canUnlock(skill.id, completed);
                  const status = isComplete ? "completed" : isUnlocked ? "current" : "locked";
                  return (
                    <div
                      key={skill.id}
                      className={`skill-node ${status}`}
                      style={{
                        left: skill.x + "%",
                        top: skill.y + "%",
                      }}
                      onClick={() => setSelectedSkill(skill.id)}
                    >
                      <div
                        className="w-8 h-8 rounded-full flex items-center justify-center mx-auto mb-1 "
                        style={{
                          backgroundColor: isComplete ? "#4ade80" : isUnlocked ? "#ffa116" : "#16161a",
                          color: isComplete || isUnlocked ? "#0f0f0f" : "#9a9a9a",
                          border: isComplete || isUnlocked ? "none" : "1px solid #2a2a2a",
                        }}
                      >
                        <span style={{ fontSize: "10px" }}>{skill.icon}</span>
                      </div>
                      <div className="w-[70px] text-xs text-center">
                        <span className="block font-bold text-[10px] text-[#e9e9e9]">{skill.title}</span>
                        <span className="block text-[9px] text-[#9a9a9a]">0%</span>
                      </div>
                    </div>
                  );
                })}
              </svg>
            </div>
          </div>
        </section>

      {/* Stats Section */}
      <section className="mt-16">
        <div className="grid grid-cols-3 gap-6">
          {[
            { label: "Problems Solved", value: "12,847" },
            { label: "Total XP", value: "45,320" },
            { label: "Weeks to Job Ready", value: "12" },
          ].map((stat) => (
            <Card key={stat.label} className="text-center bg-[#0f0f0f] border border-[#2a2a2a] p-4">
              <div className="text-2xl font-bold text-text mb-1">{stat.value}</div>
              <p className="text-sm text-text-muted">{stat.label}</p>
            </Card>
          ))}
        </div>
      </section>
    </main>
  </PageShell>
  );
}