// @ts-nocheck
import useReducedMotion from "./useReducedMotion";
import { type Easing, type Variants } from "framer-motion";
import { motion as motionTokens } from "../design-system/motion";

/** Design tokens store CSS strings ("220ms"); Framer Motion wants seconds. */
function tokenSeconds(value: string): number {
  const n = Number.parseFloat(value);
  return Number.isFinite(n) ? (value.trim().endsWith("ms") ? n / 1000 : n) : 0;
}

/** Tokens name easings ("emphasized"); Framer Motion needs the curve itself. */
function tokenEasing(name: string): Easing {
  return (motionTokens.easings as Record<string, Easing>)[name] ?? motionTokens.easings.standard;
}

export function useMotion() {
  const prefersReduced = useReducedMotion();

  const duration = (key: keyof typeof motionTokens.durations) =>
    prefersReduced ? motionTokens.durations.instant : motionTokens.durations[key];

  const easing = (key: keyof typeof motionTokens.easings) =>
    motionTokens.easings[key];

  const scale = (key: keyof typeof motionTokens.scale) =>
    prefersReduced ? 1 : motionTokens.scale[key];

  const stateTransition = (state: keyof typeof motionTokens.states) => {
    const config = motionTokens.states[state];
    if (prefersReduced) {
      return { duration: 0, easing: "linear" };
    }
    return {
      duration: tokenSeconds(config.duration),
      easing: tokenEasing(config.easing),
    };
  };

  const springTransition = () => {
    if (prefersReduced) {
      return { type: "tween" as const, duration: 0 };
    }
    return {
      type: "spring" as const,
      stiffness: 400,
      damping: 25,
    };
  };

  return {
    duration,
    easing,
    scale,
    stateTransition,
    springTransition,
    prefersReduced,
  };
}

export function getMotionVariants(state: keyof typeof motionTokens.states): Variants {
  const config = motionTokens.states[state];
  const reduced = window.matchMedia(motionTokens.prefersReducedMotion).matches;

  if (reduced) {
    return {
      hidden: { opacity: 1, y: 0 },
      visible: { opacity: 1, y: 0 },
    };
  }

  return {
    hidden: { opacity: 0, y: 12, scale: 0.98 },
    visible: {
      opacity: 1,
      y: 0,
      scale: 1,
      transition: {
        duration: tokenSeconds(config.duration),
        ease: tokenEasing(config.easing),
      },
    },
    exit: {
      opacity: 0,
      y: -8,
      scale: 0.98,
      transition: {
        duration: tokenSeconds(config.duration),
        ease: tokenEasing(config.easing),
      },
    },
  };
}
