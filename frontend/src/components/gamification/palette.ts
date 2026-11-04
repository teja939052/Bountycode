// Coddy.tech reverse-engineered gamification palette
// Source: https://coddy.tech/brand/colors
// One brand color: Coddy Blue (#29ABE2). Every other color means something.
// Every entry is { base, light } so components can safely read .base/.light.
// Wrapped in a Proxy so any undefined key falls back to Coddy Blue —
// the app never crashes on a missing CODDY entry.
const _CODDY = {
  // Brand
  blue: { base: "#29ABE2", light: "#DBEAFE" },             // Logo, Bit, links, accents
  blueDark: { base: "#34B4E4", light: "#DBEAFE" },         // Same blue lifted for dark backgrounds

  // Semantic product colors (never decorative)
  streak:   { base: "#E85A18", light: "#F4C4B4" },         // Streak flame, daily streak moments
  score:    { base: "#FCAD00", light: "#FDE6A5" },         // XP, score, coins, gems
  energy:   { base: "#3E39B8", light: "#D6D4EC" },         // Energy bolt, daily limit
  pro:      { base: "#CF7F26", light: "#EAC89C" },         // Coddy Pro / premium features
  success:  { base: "#05B20C", light: "#DFF8DB" },         // Passed tests, done lessons, correct answers
  hearts:   { base: "#FF4B4B", light: "#FFCCCC" },         // Hearts and lives
  streakFreeze: { base: "#69AEFF", light: "#D3E3FF" },     // Frozen streak saving a missed day

  // Bugsy (AI tutor only - never decorative)
  bugsy: { base: "#D31D65", light: "#F4A9C4" },

  // Backgrounds
  white:    { base: "#FFFFFF", light: "#FFFFFF" },
  mist:     { base: "#F1F5F9", light: "#F1F5F9" },         // Cards, secondary surfaces light
  skyWash:  { base: "#DDF4FF", light: "#DDF4FF" },         // Light blue landing sections
  charcoal: { base: "#252627", light: "#252627" },         // Dark theme background
  graphite: { base: "#2D2E2F", light: "#2D2E2F" },         // Cards on dark
  editor:   { base: "#1E1E1E", light: "#1E1E1E" },         // Code editor background

  // Gradients
  skyLight: ["#26A8E4", "#037BFD"],
  skyDark:  ["#072031", "#07314E"],

  // Neutral
  ink:   { base: "#0F172A", light: "#0F172A" },
  slate: { base: "#64748B", light: "#94A3B8" },
} as const;

export const CODDY = new Proxy(_CODDY, {
  get(target, prop) {
    const value = target[prop as keyof typeof target];
    if (value === undefined) {
      return target.blue; // fallback to brand blue
    }
    return value;
  },
});

export type CoddyColor = keyof typeof _CODDY;

export function coddyGradient(color: keyof typeof _CODDY, angle = 135): string {
  const c = CODDY[color];
  return `linear-gradient(${angle}deg, ${c.base} 0%, ${c.base} 55%, ${c.light} 110%)`;
}

export function coddyRadial(color: keyof typeof _CODDY): string {
  const c = CODDY[color];
  return `radial-gradient(circle at 30% 30%, ${c.light}, ${c.base} 60%)`;
}

export function coddyGlow(color: keyof typeof _CODDY, alpha = "80"): string {
  const c = CODDY[color];
  return `0 0 24px -6px ${c.base}${alpha}`;
}

export const CODDY_BLUE = "#29ABE2";
export const CODDY_BLUE_DARK = "#34B4E4";

export const LEVEL_LABELS = [
  { level: 1,  label: "Novice",   color: "slate" },
  { level: 5,  label: "Learner",  color: "blue" },
  { level: 10, label: "Coder",    color: "blue" },
  { level: 15, label: "Engineer", color: "success" },
  { level: 20, label: "Architect",color: "score" },
  { level: 25, label: "Master",   color: "hearts" },
  { level: 30, label: "Grandmaster", color: "slate" },
] as const;

export const LEVEL_THRESHOLDS = [
  0, 100, 300, 600, 1000, 1600, 2400, 3400, 4600, 6000,
  7800, 10000, 12600, 15600, 19200, 23400, 28200, 33800, 40200, 47600,
];

export function getLevelForXP(xp: number): number {
  let level = 1;
  for (let i = 1; i < LEVEL_THRESHOLDS.length; i++) {
    if (xp >= LEVEL_THRESHOLDS[i]) level = i + 1;
    else break;
  }
  return level;
}

export function getXPForLevel(level: number): number {
  return LEVEL_THRESHOLDS[level - 1] ?? 0;
}

export function getLevelLabel(level: number) {
  let entry = LEVEL_LABELS[0];
  for (const e of LEVEL_LABELS) {
    if (level >= e.level) entry = e;
  }
  return entry;
}
