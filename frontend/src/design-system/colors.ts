export const colors = {
  // ── Base Light System ──
  background: {
    canvas: "#F7FAF7",
    surface: "#FFFFFF",
    surface2: "#F0F7F1",
    mint: "#EAF7ED",
    secondary: "#F0F7F1",
  },

  // ── Primary Green (accent, not background) ──
  brand: {
    primary: "#22C55E",
    dark: "#15803D",
    deep: "#166534",
    darkest: "#14532D",
    soft: "#DCFCE7",
    mint: "#EAF7ED",
    softMint: "#ECFDF5",
  },

  // ── Adventure Palette ──
  adventure: {
    ocean: "#5BA7A0",
    oceanSoft: "#E0F2F1",
    sky: "#8BC9D5",
    skySoft: "#E8F5FA",
    sand: "#E9D6A3",
    sandSoft: "#FDF6EB",
    wood: "#A8754F",
    woodSoft: "#F5EFE8",
  },

  // ── Reward Gold ──
  reward: {
    gold: "#EAB74D",
    goldSoft: "#FFF3D0",
  },

  // ── Text ──
  text: {
    primary: "#17211B",
    secondary: "#68736B",
    muted: "#68736B",
    dim: "#94A3B8",
    inverse: "#FFFFFF",
  },

  border: {
    primary: "#DCE8DE",
    secondary: "#C9D8CC",
    focus: "#22C55E",
  },

  // ── Semantic ──
  semantic: {
    techBlue: "#4A90E2",
    techSoft: "#E8F0FE",
    boss: "#E96A5B",
    bossSoft: "#FDEDEC",
    rare: "#8B6BD9",
    rareSoft: "#F3F0FA",
    xp: "#EAB74D",
    achievement: "#EAB74D",
    info: "#4A90E2",
    locked: "#94A3B8",
    error: "#EF4444",
    success: "#15803D",
    warning: "#F59E0B",
    readiness: "#22C55E",
  },

  shadow: {
    card: "rgba(17, 33, 27, 0.04)",
    elevated: "rgba(17, 33, 27, 0.06)",
    modal: "rgba(17, 33, 27, 0.12)",
    bounty: "rgba(234, 183, 77, 0.25)",
    ocean: "rgba(91, 167, 160, 0.15)",
    color: "rgba(34,197,94,0.08)",
    colorStrong: "rgba(34,197,94,0.15)",
  },

  glass: {
    bg: "rgba(255,255,255,0.7)",
    blur: "18px",
  },
} as const;
