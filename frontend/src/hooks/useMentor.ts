// @ts-nocheck
import { useMemo } from "react";
import type { MentorMood } from "../design-system/Mentor";

export interface MentorLine {
  mood: MentorMood;
  message: string;
}

export interface UseMentorOptions {
  phase:
    | "idle"
    | "loading"
    | "intro"
    | "active"
    | "correcting"
    | "repair"
    | "success"
    | "mastery"
    | "boss"
    | "stuck"
    | "complete";
  context?: Record<string, unknown>;
  mistakeCount?: number;
  idleSeconds?: number;
  /** backend-derived mentor line from journey state */
  backendMentor?: { mood: MentorMood; message: string; phase: string };
}

const LINES: Record<UseMentorOptions["phase"], MentorLine> = {
  idle: {
    mood: "thinking",
    message: "Whenever you're ready — this path waits for no one, but it also never rushes you.",
  },
  loading: {
    mood: "thinking",
    message: "I'm pulling up your next challenge. Breathe; clarity is loading.",
  },
  intro: {
    mood: "briefing",
    message: "This step is small on purpose. Focus on one move at a time.",
  },
  active: {
    mood: "explaining",
    message: "Try the smallest possible change first. If it feels big, it probably is.",
  },
  correcting: {
    mood: "correcting",
    message: "Close, but not quite. Look at the exact piece the checker flagged.",
  },
  repair: {
    mood: "encouraging",
    message: "This misconception is common. Repair is just proof you're learning.",
  },
  success: {
    mood: "proud",
    message: "Nice. That move shows you actually understand it.",
  },
  mastery: {
    mood: "celebrating",
    message: "You don't just remember this anymore — you can use it under pressure.",
  },
  boss: {
    mood: "serious",
    message: "This one combines everything we've built. Stay systematic.",
  },
  stuck: {
    mood: "stuck",
    message: "Step back for ten seconds. The answer is usually the simpler move you overlooked.",
  },
  complete: {
    mood: "handoff",
    message: "That's a solid stop. Rest, then pick up the next thread.",
  },
};

export function useMentor({ phase, mistakeCount, idleSeconds, backendMentor }: UseMentorOptions) {
  if (backendMentor) {
    return backendMentor;
  }

  const shouldStuck = mistakeCount && mistakeCount >= 3;
  const shouldIdle = idleSeconds && idleSeconds >= 25;

  const effectivePhase = shouldStuck
    ? "stuck"
    : shouldIdle
      ? "stuck"
      : phase === "active" && mistakeCount && mistakeCount >= 2
        ? "stuck"
        : phase;

  const line = useMemo(() => LINES[effectivePhase] || LINES.idle, [effectivePhase]);

  if (effectivePhase === "stuck" && shouldStuck) {
    return {
      mood: "stuck" as const,
      message:
        mistakeCount && mistakeCount >= 4
          ? "You've hit this edge case twice. Try stating the rule out loud before coding it."
          : "This is the exact gap we planned to repair. One hint: simplify the condition.",
    };
  }

  if (effectivePhase === "stuck" && shouldIdle) {
    return {
      mood: "stuck" as const,
      message: "Still there. Try naming the smallest valid input and working from there.",
    };
  }

  return line;
}
