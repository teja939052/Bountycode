export const colors = {
  // ── Base (Golden Hour — warm dark canvas) ──
  background: {
    canvas: "#0F172A",
    surface: "#334155",
    surfaceHover: "#475569",
  },
  border: {
    primary: "#475569",
    soft: "#334155",
    focus: "#F97316",
  },
  text: {
    primary: "#F8FAFC",
    secondary: "#CBD5E1",
    muted: "#94A3B8",
    dim: "#64748B",
    inverse: "#0F172A",
  },

  // ── Primary brand (vibrant orange — energetic) ──
  brand: {
    primary: "#F97316",
    dark: "#EA580C",
    deep: "#C2410C",
    soft: "rgba(249, 115, 22, 0.10)",
    softer: "rgba(249, 115, 22, 0.05)",
    glow: "rgba(249, 115, 22, 0.25)",
    text: "#FFFFFF",
  },

  // ── Subject accent colors ──
  subject: {
    coding: { DEFAULT: "#06B6D4", soft: "rgba(6, 182, 212, 0.10)", glow: "rgba(6, 182, 212, 0.25)" },
    aptitude: { DEFAULT: "#F59E0B", soft: "rgba(245, 158, 11, 0.10)", glow: "rgba(245, 158, 11, 0.25)" },
    reasoning: { DEFAULT: "#EC4899", soft: "rgba(236, 72, 153, 0.10)", glow: "rgba(236, 72, 153, 0.25)" },
    verbal: { DEFAULT: "#10B981", soft: "rgba(16, 185, 129, 0.10)", glow: "rgba(16, 185, 129, 0.25)" },
    interview: { DEFAULT: "#8B5CF6", soft: "rgba(139, 92, 246, 0.10)", glow: "rgba(139, 92, 246, 0.25)" },
    boss: { DEFAULT: "#EF4444", soft: "rgba(239, 68, 68, 0.10)", glow: "rgba(239, 68, 68, 0.25)" },
  },

  // ── Semantic ──
  semantic: {
    success: { DEFAULT: "#22C55E", soft: "rgba(34, 197, 94, 0.10)", text: "#86EFAC" },
    warning: { DEFAULT: "#F59E0B", soft: "rgba(245, 158, 11, 0.10)", text: "#FCD34D" },
    error: { DEFAULT: "#EF4444", soft: "rgba(239, 68, 68, 0.10)", text: "#FCA5A5" },
    info: { DEFAULT: "#3B82F6", soft: "rgba(59, 130, 246, 0.10)", text: "#93C5FD" },
  },

  shadow: {
    card: "rgba(15, 23, 42, 0.15)",
    cardHover: "rgba(15, 23, 42, 0.25)",
    primary: "rgba(249, 115, 22, 0.25)",
    primaryLg: "rgba(249, 115, 22, 0.35)",
    modal: "rgba(15, 23, 42, 0.35)",
    coding: "rgba(6, 182, 212, 0.15)",
    aptitude: "rgba(245, 158, 11, 0.15)",
    reasoning: "rgba(236, 72, 153, 0.15)",
    verbal: "rgba(16, 185, 129, 0.15)",
    boss: "rgba(239, 68, 68, 0.15)",
    bounty: "rgba(245, 158, 11, 0.25)",
  },

  glass: {
    bg: "rgba(17, 24, 39, 0.6)",
    blur: "18px",
  },
} as const;
