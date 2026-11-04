// Coddy.tech reverse-engineered gamification palette
// Source: https://coddy.tech/brand/colors
// One brand color: Coddy Blue. Every other color means something.
export const CODDY = {
  // Brand
  blue: { base: "#29ABE2", dark: "#34B4E4" },            // Logo, Bit, links, accents
  blueDark: "#0077FF",                                   // Button blue (web light)
  blueShadow: "#005DC8",                                 // Pressed edge
  blueDeep: "#007ACCC",                                  // Secondary buttons/links
  blueDarkTheme: "#1B78A0",                              // Button blue dark theme

  // Semantic product colors (never decorative)
  streak: { base: "#E85A18", light: "#F4C4B4" },         // Streak flame, daily streak moments
  score: { base: "#FCAD00", light: "#FDE6A5" },          // XP, score, coins, gems
  energy: { base: "#3E39B8", light: "#D6D4EC" },         // Energy bolt, daily limit
  pro: { base: "#CF7F26", light: "#EAC89C" },            // Coddy Pro / premium
  success: { base: "#05B20C", light: "#DFF8DB" },        // Passed tests, done lessons, correct answers
  hearts: { base: "#FF4B4B", light: "#FFCCCC" },         // Hearts and lives
  streakFreeze: { base: "#69AEFF", light: "#D3E3FF" },   // Frozen streak

  // Bugsy (AI tutor only - never decorative)
  bugsy: { base: "#D31D65", light: "#F4A9C4" },

  // Backgrounds
  white: "#FFFFFF",
  mist: "#F1F5F9",                                       // Cards, secondary surfaces light
  skyWash: "#DDF4FF",                                    // Light blue landing sections
  charcoal: "#252627",                                   // Dark theme bg
  graphite: "#2D2E2F",                                   // Cards on dark
  editor: "#1E1E1E",                                     // Code editor bg

  // Gradients
  skyLight: ["#26A8E4", "#037BFD"],
  skyDark: ["#072031", "#07314E"],

  // Neutral
  ink: "#0F172A",
  slate: "#64748B",
} as const;

export type CoddyColor = keyof typeof CODDY;

export function coddyGradient(color: keyof Omit<typeof CODDY, "skyLight" | "skyDark" | "ink" | "slate">, angle = 135): string {
  const c = CODDY[color as keyof typeof CODDY];
  const base = typeof c === "string" ? c : c.base;
  const light = typeof c === "string" ? c : c.light;
  return `linear-gradient(${angle}deg, ${base} 0%, ${base} 55%, ${light || base} 110%)`;
}

export function coddyRadial(color: keyof Omit<typeof CODDY, "skyLight" | "skyDark" | "ink" | "slate">): string {
  const c = CODDY[color as keyof typeof CODDY];
  const base = typeof c === "string" ? c : c.base;
  const light = typeof c === "string" ? c : c.light;
  return `radial-gradient(circle at 30% 30%, ${light || base}, ${base} 60%)`;
}

export function coddyGlow(color: keyof Omit<typeof CODDY, "skyLight" | "skyDark" | "ink" | "slate">, alpha = "80"): string {
  const c = CODDY[color as keyof typeof CODDY];
  const base = typeof c === "string" ? c : c.base;
  return `0 0 24px -6px ${base}${alpha}`;
}

export const CODDY_BLUE = "#29ABE2";
export const CODDY_BLUE_DARK = "#34B4E4";

export const LEVEL_LABELS = [
  { level: 1, label: "Novice", color: "slate" },
  { level: 5, label: "Learner", color: "blue" },
  { level: 10, label: "Coder", color: "blue" },
  { level: 15, label: "Engineer", color: "success" },
  { level: 20, label: "Architect", color: "score" },
  { level: 25, label: "Master", color: "hearts" },
  { level: 30, label: "Grandmaster", color: "slate" },
] as const;

export function getLevelLabel(level: number) {
  let entry = LEVEL_LABELS[0];
  for (const e of LEVEL_LABELS) {
    if (level >= e.level) entry = e;
  }
  return entry;
}
