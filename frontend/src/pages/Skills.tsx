import ReadinessHeatmap from "./ReadinessHeatmap";

// V3 §4 — SKILLS is the Capability Graph: ONE profile, multiple targets.
// Reuses the canonical readiness/evidence engine (no parallel truth path).
export default function Skills() {
  return <ReadinessHeatmap />;
}
