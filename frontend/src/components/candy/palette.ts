export const CANDY = {
  strawberry: { base: "#FF6B6B", light: "#FFA3A3", dark: "#E14B4B" },
  grape: { base: "#845EC2", light: "#B39DDB", dark: "#6A45A8" },
  lemon: { base: "#FFC75F", light: "#FFDFA0", dark: "#E0A33A" },
  mint: { base: "#00C9A7", light: "#6BE4CF", dark: "#00A086" },
  blueberry: { base: "#4B7BEC", light: "#93B4F7", dark: "#315BD0" },
  tangerine: { base: "#FF8A5C", light: "#FFB49A", dark: "#E06A3A" },
  cherry: { base: "#FF3F6C", light: "#FF8A9F", dark: "#D81B4B" },
  gold: { base: "#FFD700", light: "#FFE86B", dark: "#E0B400" },
} as const;

export type CandyColor = keyof typeof CANDY;

export function candyGradient(color: CandyColor, angle = 135): string {
  const c = CANDY[color];
  return `linear-gradient(${angle}deg, ${c.dark} 0%, ${c.base} 60%, ${c.light} 135%)`;
}

export function candyRadial(color: CandyColor): string {
  const c = CANDY[color];
  return `radial-gradient(circle at 32% 28%, ${c.light}, ${c.base} 58%, ${c.dark})`;
}

export function candyGlow(color: CandyColor, alpha = "66"): string {
  return `0 12px 30px -8px ${CANDY[color].base}${alpha}`;
}
