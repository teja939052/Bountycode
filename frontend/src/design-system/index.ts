export * from "./colors";
export * from "./typography";
export * from "./spacing";
export * from "./radii";
export * from "./shadows";
export * from "./motion";
export * from "./breakpoints";

// V2 components
export { AmbientNature } from "./AmbientNature";
export type { NatureDensity } from "./AmbientNature";
export { PageShell } from "./PageShell";
export type { PageTheme } from "./PageShell";
export { Mentor, MentorAvatar } from "./Mentor";
export type { MentorMood } from "./Mentor";
export { MasteryBar, ReadinessRing, TreasureBadge } from "./Progress";
export { IslandNode, PathConnector, BountyCard } from "./JourneyMap";
export type { NodeState, IslandNodeProps, BountyCardProps } from "./JourneyMap";

import { colors } from "./colors";
import { typography } from "./typography";
import { spacing } from "./spacing";
import { radii } from "./radii";
import { shadows } from "./shadows";
import { motion } from "./motion";
import { breakpoints } from "./breakpoints";

export const designSystem = {
  colors,
  typography,
  spacing,
  radii,
  shadows,
  motion,
  breakpoints,
};