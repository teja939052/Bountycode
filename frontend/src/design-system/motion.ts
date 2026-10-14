// @ts-nocheck
export const motion = {
  durations: {
    instant: "0ms",
    fast: "120ms",
    normal: "220ms",
    slow: "320ms",
    ceremony: "480ms",
    unlock: "700ms",
  },
  easings: {
    standard: "cubic-bezier(0, 0, 0.2, 1)",
    emphasized: "cubic-bezier(0.2, 0, 0, 1)",
    spring: "cubic-bezier(0.34, 1.56, 0.64, 1)",
    decelerate: "cubic-bezier(0, 0, 0.2, 1)",
    anticipate: "cubic-bezier(0.4, 0, 0.2, 1)",
  },
  distances: {
    small: "4px",
    medium: "8px",
    large: "16px",
  },
  scale: {
    press: 0.97,
    hover: 1.02,
    success: 1.05,
    mastery: 1.1,
    boss: 1.15,
  },
  states: {
    idle: {
      duration: "220ms",
      easing: "standard",
      description: "Calm. No motion unless necessary.",
    },
    focus: {
      duration: "220ms",
      easing: "emphasized",
      description: "Attention moves toward the current task.",
    },
    interaction: {
      duration: "120ms",
      easing: "spring",
      description: "Immediate tactile response.",
    },
    success: {
      duration: "320ms",
      easing: "spring",
      description: "Clear positive feedback.",
    },
    failure: {
      duration: "220ms",
      easing: "standard",
      description: "Clear mistake communication.",
    },
    repair: {
      duration: "320ms",
      easing: "emphasized",
      description: "Visual transition into recovery.",
    },
    mastery: {
      duration: "480ms",
      easing: "spring",
      description: "Concept transforms/unlocks.",
    },
    boss: {
      duration: "480ms",
      easing: "emphasized",
      description: "Energy increases.",
    },
    navigation: {
      duration: "220ms",
      easing: "standard",
      description: "Quiet and fast.",
    },
  },
  prefersReducedMotion: "(prefers-reduced-motion: reduce)",
};

export type MotionState = keyof typeof motion.states;
