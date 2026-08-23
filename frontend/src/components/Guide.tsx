import { ReactNode } from "react";
import { Leaf, CheckCircle, Play, Trophy, Clock, Zap } from "lucide-react";

type GuideState = {
  state: "welcome" | "learning" | "practice" | "quiz" | "complete";
  channel?: string;
  moduleIndex?: number;
  completedModules?: string[];
  streak?: number;
  xpEarned?: number;
  bountiesClaimed?: string[];
};

type GuideAction =
  | { type: "advance"; label: string; onClick: () => void }
  | { type: "complete"; label: string; onClick: () => void }
  | { type: "claim"; label: string; onClick: () => void };

const STATE_CONFIG: Record<
  GuideState["state"],
  { title: string; subtitle: string; action: GuideAction; icon: ReactNode }
> = {
  welcome: {
    title: "Welcome aboard! 👋",
    subtitle: "I'm your First Mate, here to guide your learning journey. We'll start with Python fundamentals, then move into DSA, system design, and beyond.",
    action: {
      type: "advance",
      label: "Start Lesson →",
      onClick: () => {},
    },
    icon: <Leaf size={24} className="text-primary" />,
  },
  learning: {
    title: "Learning Time 📖",
    subtitle: "Read the introduction below, then we'll practice together. Take your time — there's no rush!",
    action: {
      type: "advance",
      label: "Mark Complete →",
      onClick: () => {},
    },
    icon: <BookOpen size={24} className="text-primary" />,
  },
  practice: {
    title: "Practice Time ⚔",
    subtitle: "Write code in the editor below. Don't worry if you get stuck — I'm here to help. Try your best!",
    action: {
      type: "advance",
      label: "Start Quiz →",
      onClick: () => {},
    },
    icon: <Zap size={24} className="text-primary" />,
  },
  quiz: {
    title: "Quiz Time 📝",
    subtitle: "A few quick questions to check your understanding. This will help solidify what you've learned.",
    action: {
      type: "complete",
      label: "Submit →",
      onClick: () => {},
    },
    icon: <CheckCircle size={24} className="text-success" />,
  },
  complete: {
    title: "Mission Complete! 🎉",
    subtitle: "Great job finishing this module! You earned some XP and a bounty. Ready for the next one?",
    action: {
      type: "claim",
      label: "Claim Bounty →",
      onClick: () => {},
    },
    icon: <Trophy size={24} className="text-gold" />,
  },
};

export function Guide({ state }: { state: GuideState }) {
  const config = STATE_CONFIG[state.state] || STATE_CONFIG.welcome;

  return (
    <div className="fixed bottom-0 left-1/2 -translate-x-1/2 w-full max-w-md bg-white border-t border-border shadow-2xl p-6 rounded-2xl transform transition-all duration-300 ease-out">
      <div className="flex items-center gap-3 mb-4">
        {config.icon}
        <div>
          <h3 className="font-medium text-text-primary">{config.title}</h3>
          <p className="text-text-muted text-sm">{config.subtitle}</p>
        </div>
      </div>

      {config.action.type === "advance" && (
        <button
          onClick={config.action.onClick}
          className="w-full btn-primary py-3 text-sm font-medium mt-4 hover:bg-primary-dark transition-colors"
        >
          {config.action.label}
        </button>
      )}

      {config.action.type === "complete" && (
        <button
          onClick={config.action.onClick}
          className="w-full btn-primary py-3 text-sm font-medium mt-4 hover:bg-primary-dark transition-colors"
        >
          {config.action.label}
        </button>
      )}

      {config.action.type === "claim" && (
        <button
          onClick={config.action.onClick}
          className="w-full btn-primary py-3 text-sm font-medium mt-4 hover:bg-primary-dark transition-colors"
        >
          {config.action.label}
        </button>
      )}
    </div>
  );
}