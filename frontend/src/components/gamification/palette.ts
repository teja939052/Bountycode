// Coddy.tech-inspired gamification palette
// Clean, modern design — Coddy Blue primary, no candy/pirate theme
export const CODDY = {
  // Primary brand
  blue: { base: "#2563EB", light: "#DBEAFE", dark: "#1D4ED8" },
  indigo: { base: "#4F46E5", light: "#E0E7FF", dark: "#4338CA" },
  
  // Status / tier colors
  success: { base: "#10B981", light: "#D1FAE5", dark: "#047857" },
  warning: { base: "#F59E0B", light: "#FEF3C7", dark: "#B45309" },
  danger: { base: "#EF4444", light: "#FEE2E2", dark: "#B91C1C" },
  
  // Tier colors for badges / levels
  bronze: { base: "#CD7F32", light: "#F3E5AB", dark: "#8F5A2E" },
  silver: { base: "#C0C0C0", light: "#E9ECEF", dark: "#7F7F7F" },
  gold: { base: "#FFD700", light: "#FEF3C7", dark: "#B8860B" },
  platinum: { base: "#E5E4E2", light: "#F8FAFC", dark: "#71717A" },
  
  // Neutral
  ink: { base: "#0F172A", light: "#F8FAFC", dark: "#020617" },
  slate: { base: "#64748B", light: "#F1F5F9", dark: "#475569" },
} as const;

export type CoddyColor = keyof typeof CODDY;

export function coddyGradient(color: CoddyColor, angle = 135): string {
  const c = CODDY[color];
  return `linear-gradient(${angle}deg, ${c.dark} 0%, ${c.base} 55%, ${c.light} 110%)`;
}

export function coddyRadial(color: CoddyColor): string {
  const c = CODDY[color];
  return `radial-gradient(circle at 30% 30%, ${c.light}, ${c.base} 60%, ${c.dark})`;
}

export function coddyGlow(color: CoddyColor, alpha = "80"): string {
  return `0 0 24px -6px ${CODDY[color].base}${alpha}`;
}

export const CODDY_BLUE_500 = "#2563EB";
export const CODDY_INDIGO_600 = "#4F46E5";

export const LEVEL_LABELS = [
  { level: 1, label: "Novice", color: "slate" },
  { level: 5, label: "Learner", color: "blue" },
  { level: 10, label: "Coder", color: "indigo" },
  { level: 15, label: "Engineer", color: "success" },
  { level: 20, label: "Architect", color: "warning" },
  { level: 25, label: "Master", color: "danger" },
  { level: 30, label: "Grandmaster", color: "platinum" },
] as const;

export function getLevelLabel(level: number) {
  let entry = LEVEL_LABELS[0];
  for (const e of LEVEL_LABELS) {
    if (level >= e.level) entry = e;
  }
  return entry;
}
