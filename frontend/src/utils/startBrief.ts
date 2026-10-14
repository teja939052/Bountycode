// @ts-nocheck
export type StartTrack = "placement" | "learn" | "explore";
export type StartIntent = "diagnostic" | "explore";

export interface StartBrief {
  track: StartTrack;
  goal?: string;
  company?: string;
  role?: string;
  language?: string;
  intent?: StartIntent;
  daily_minutes?: number;
  prep_level?: string;
}

export const START_BRIEF_KEY = "bountycode.start_brief";

export function getStartBrief(): StartBrief | null {
  try {
    const raw = localStorage.getItem(START_BRIEF_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    if (!parsed || typeof parsed !== "object" || !parsed.track) return null;
    return parsed as StartBrief;
  } catch {
    return null;
  }
}

export function setStartBrief(brief: StartBrief): void {
  localStorage.setItem(START_BRIEF_KEY, JSON.stringify(brief));
  if (brief.goal) localStorage.setItem("bountycode.goal", brief.goal);
  if (brief.company) localStorage.setItem("bountycode.target", brief.company);
}

export function clearStartBrief(): void {
  localStorage.removeItem(START_BRIEF_KEY);
}

export function briefToOnboardingPayload(brief: StartBrief): Record<string, unknown> {
  const company = brief.company && brief.company !== "Not decided" && brief.company !== "Generic prep"
    ? brief.company
    : undefined;
  const role = brief.role && brief.role !== "Not sure yet" ? brief.role : undefined;
  const language = brief.language && brief.language !== "unsure" ? brief.language : undefined;
  return {
    target_companies: company ? [company] : [],
    target_company: company,
    target_role: role,
    language,
    daily_minutes: brief.daily_minutes,
    prep_level: brief.prep_level,
  };
}
