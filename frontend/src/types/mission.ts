/**
 * Mission view types (V4 internal wiring).
 *
 * These are VIEWS over the canonical systems — not a new state model:
 * - identity/progress  → journey_engine.build_journey_state  (GET /api/v1/journey/state)
 * - daily plan          → study_engine.get_today              (GET /api/v1/study/today)
 * - completion sink     → study_engine.record_activity        (POST /api/v1/study/activity)
 * - repair/retest       → repair_service + question_store     (GET/POST /api/v1/repair/*)
 * - rewards             → gamification.record_practice (sole XP writer)
 *
 * No new collections, no new XP paths, no question content in Mongo.
 */

export type MissionKind =
  | "lesson"
  | "repair"
  | "retest"
  | "practice"
  | "assessment"
  | "interview"
  | "review";

export type MissionStepType =
  | "discover"
  | "manipulate"
  | "predict"
  | "recognize"
  | "build"
  | "practice"
  | "break"
  | "debug"
  | "prove";

export interface Mission {
  id: string;
  kind: MissionKind;
  title: string;
  description: string;
  /** Canonical skill id (e.g. "coding.sliding_window") when known. */
  skill_id?: string;
  estimated_minutes: number;
  /** Authoritative reward quoted by the backend (display only — awarded by record_practice). */
  xp_reward?: number;
  /** Existing route that actually runs this mission (lesson/problem/mock/…). */
  to: string;
  to_label: string;
  status: "available" | "in_progress" | "completed";
}

export interface MissionStep {
  type: MissionStepType;
  label: string;
  detail: string;
  /** Existing destination route, or null for in-shell actions. */
  to: string | null;
  to_label?: string;
}

export interface ActivityResult {
  recorded: boolean;
  activity_type: string;
  skill_id?: string | null;
  passed: boolean;
  score: number;
  diamonds: number;
  xp_awarded?: number;
  xp_applied?: boolean;
  mastery_before?: number | null;
  mastery_after?: number | null;
  diagnosis_codes?: string[];
}

function num(v: unknown, fallback: number): number {
  const n = typeof v === "number" ? v : Number(v);
  return Number.isFinite(n) ? n : fallback;
}

function str(v: unknown, fallback = ""): string {
  return typeof v === "string" && v.length > 0 ? v : fallback;
}

/** Backend-decided next action → Mission view. Never hardcodes progression. */
export function missionFromJourneyNext(next: Record<string, unknown> | null | undefined): Mission {
  // Unwrap the journey/state envelope: {success, data: {today: {next}, next_action}}.
  const root = next ?? {};
  const data = (root["data"] as Record<string, unknown> | undefined) ?? root;
  const today = (data["today"] as Record<string, unknown> | undefined) ?? {};
  const n = ((today["next"] ?? data["next"] ?? data["next_action"] ?? {}) as Record<string, unknown>);
  const type = str(n["type"], "learn");
  const kind: MissionKind =
    type === "repair" || type === "mastery_repair" ? "repair"
    : type === "review" ? "review"
    : type === "assessment" || type === "mock" ? "assessment"
    : type === "interview" ? "interview"
    : type === "practice" ? "practice"
    : "lesson";

  const world = str(n["world"]);
  const town = str(n["town"]);
  const level = str(n["level"]) || str(n["target_level"]);
  const skillId = str(n["skill_id"]) || str(n["canonical_skill"]);

  let to = "/practice";
  let toLabel = "Open practice";
  if (kind === "lesson" && level) {
    to = `/lesson/${encodeURIComponent(level)}`;
    toLabel = "Open lesson";
  } else if (kind === "repair" && skillId) {
    to = `/mission/retest:${encodeURIComponent(skillId)}`;
    toLabel = "Start repair retest";
  } else if (kind === "review") {
    to = "/skills";
    toLabel = "Review due cards";
  } else if (kind === "assessment") {
    to = "/mock-oa";
    toLabel = "Start assessment";
  } else if (kind === "interview") {
    to = "/interview";
    toLabel = "Start interview";
  } else if (world && town && level) {
    to = "/journey";
    toLabel = "Open in Journey map";
  }

  return {
    id: "next",
    kind,
    title: str(n["title"], "Continue your journey"),
    description: str(n["description"], str(n["reason"], "Picked by your Journey engine.")),
    skill_id: skillId || undefined,
    estimated_minutes: num(n["estimated_minutes"], 20),
    xp_reward: num(n["xp_reward"], 0) || undefined,
    to,
    to_label: toLabel,
    status: "available",
  };
}

/** Repair-service mission → Mission view (retest runs verified-only). */
export function missionFromRepairMission(m: Record<string, unknown>): Mission {
  const id = str(m["mission_id"] ?? m["id"], "repair");
  const weaknesses = Array.isArray(m["weaknesses"]) ? (m["weaknesses"] as unknown[]) : [];
  const skill = str(weaknesses[0], str(m["skill"], ""));
  return {
    id: `repair:${id}`,
    kind: "repair",
    title: str(m["title"], skill ? `Repair ${skill}` : "Repair mission"),
    description: str(m["description"], "Targeted repair, then a verified retest to prove it."),
    skill_id: skill || undefined,
    estimated_minutes: 20,
    to: skill ? `/mission/retest:${encodeURIComponent(skill)}` : "/skills",
    to_label: "Start repair retest",
    status: "available",
  };
}

/**
 * Universal step checklist for a mission.
 * Steps name the lesson-engine stages (discover → … → prove); each step
 * deep-links to the existing engine that runs it — the shell renders no
 * content of its own.
 */
export function stepsForMission(mission: Mission): MissionStep[] {
  switch (mission.kind) {
    case "lesson":
      return [
        { type: "discover", label: "Discover", detail: "Meet the concept in context.", to: mission.to, to_label: mission.to_label },
        { type: "manipulate", label: "Manipulate", detail: "Change inputs, watch what happens.", to: mission.to, to_label: mission.to_label },
        { type: "predict", label: "Predict", detail: "Guess the output before running.", to: mission.to, to_label: mission.to_label },
        { type: "build", label: "Build", detail: "Solve it yourself.", to: mission.to, to_label: mission.to_label },
        { type: "prove", label: "Prove", detail: "Timed check that feeds readiness.", to: mission.to, to_label: mission.to_label },
      ];
    case "repair":
    case "retest":
      return [
        { type: "recognize", label: "Diagnose", detail: "See exactly which sub-skill failed.", to: "/skills", to_label: "View diagnosis" },
        { type: "build", label: "Repair", detail: "3 targeted exercises on the weakness.", to: mission.to, to_label: mission.to_label },
        { type: "prove", label: "Retest", detail: "Verified-only retest, ≥80% to advance.", to: mission.to, to_label: mission.to_label },
      ];
    case "assessment":
      return [
        { type: "build", label: "Attempt", detail: "Timed, server-authoritative sections.", to: mission.to, to_label: mission.to_label },
        { type: "prove", label: "Diagnosis", detail: "Scorecard → weakness → repair path.", to: "/skills", to_label: "View results" },
      ];
    case "interview":
      return [
        { type: "build", label: "Answer", detail: "Rubric-scored session.", to: mission.to, to_label: mission.to_label },
        { type: "prove", label: "Feedback", detail: "Competency-level diagnosis.", to: mission.to, to_label: mission.to_label },
      ];
    case "review":
      return [
        { type: "recognize", label: "Recall", detail: "Spaced-repetition due cards.", to: mission.to, to_label: mission.to_label },
        { type: "prove", label: "Retain", detail: "Lock it back into mastery.", to: mission.to, to_label: mission.to_label },
      ];
    default:
      return [
        { type: "practice", label: "Practice", detail: "Unordered reps on this pattern.", to: mission.to, to_label: mission.to_label },
        { type: "prove", label: "Prove", detail: "Show mastery, move the needle.", to: "/skills", to_label: "Check mastery" },
      ];
  }
}

export function starsForScore(score: number): number {
  if (score >= 90) return 5;
  if (score >= 80) return 4;
  if (score >= 70) return 3;
  if (score >= 60) return 2;
  return 1;
}
