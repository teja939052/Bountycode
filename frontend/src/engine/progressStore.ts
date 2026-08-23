/**
 * progressStore — lightweight local persistence for mission progress.
 * Frontend-only; the engine stays pure. Keys are namespaced and versioned.
 */

const KEY_PREFIX = "bc.progress.v1.";

export interface MissionProgressEntry {
  mastery: number;
  completedAt: string;
}

export type WorldProgress = Record<string, MissionProgressEntry>;

export function saveMissionProgress(
  worldId: string,
  missionId: string,
  mastery: number
): void {
  try {
    const key = KEY_PREFIX + worldId;
    const raw = localStorage.getItem(key);
    const data: WorldProgress = raw ? JSON.parse(raw) : {};
    data[missionId] = {
      mastery: Math.max(0, Math.min(100, Math.round(mastery))),
      completedAt: new Date().toISOString(),
    };
    localStorage.setItem(key, JSON.stringify(data));
  } catch {
    // storage unavailable (private mode etc.) — progress stays session-only
  }
}

export function getWorldProgress(worldId: string): WorldProgress {
  try {
    const raw = localStorage.getItem(KEY_PREFIX + worldId);
    return raw ? (JSON.parse(raw) as WorldProgress) : {};
  } catch {
    return {};
  }
}
