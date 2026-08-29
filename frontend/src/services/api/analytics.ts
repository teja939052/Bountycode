import { requestWithRetry as request } from "./request.ts";

/**
 * Learning loop analytics.
 *
 * Tracks every step of the student's journey through a lesson.
 * These events power the product metrics that matter:
 *   - lesson_started, discovery_completed, hint_used
 *   - build_attempted, build_failed, build_passed
 *   - transfer_attempted, mastery_achieved
 *   - boss_started, boss_passed, next_level_started
 */
export const analyticsApi = {
  track(event: string, properties: Record<string, unknown> = {}) {
    return request("/api/v1/analytics/track", {
      method: "POST",
      body: JSON.stringify({ event, properties, timestamp: new Date().toISOString() }),
    }).catch(() => null); // analytics should never break the app
  },

  // Learning loop events
  lessonStarted(lessonId: string, worldId: string) {
    return this.track("lesson_started", { lesson_id: lessonId, world_id: worldId });
  },
  discoveryCompleted(lessonId: string) {
    return this.track("discovery_completed", { lesson_id: lessonId });
  },
  hintUsed(lessonId: string, hintIndex: number) {
    return this.track("hint_used", { lesson_id: lessonId, hint_index: hintIndex });
  },
  buildAttempted(lessonId: string, code: string) {
    return this.track("build_attempted", { lesson_id: lessonId, code_length: code.length });
  },
  buildFailed(lessonId: string, attempt: number) {
    return this.track("build_failed", { lesson_id: lessonId, attempt });
  },
  buildPassed(lessonId: string, attempts: number) {
    return this.track("build_passed", { lesson_id: lessonId, attempts });
  },
  transferAttempted(lessonId: string) {
    return this.track("transfer_attempted", { lesson_id: lessonId });
  },
  masteryAchieved(lessonId: string, worldId: string, xp: number) {
    return this.track("mastery_achieved", { lesson_id: lessonId, world_id: worldId, xp });
  },
  bossStarted(lessonId: string) {
    return this.track("boss_started", { lesson_id: lessonId });
  },
  bossPassed(lessonId: string, attempts: number) {
    return this.track("boss_passed", { lesson_id: lessonId, attempts });
  },
  nextLevelStarted(lessonId: string) {
    return this.track("next_level_started", { lesson_id: lessonId });
  },
};

export default analyticsApi;
