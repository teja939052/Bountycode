import { useCallback, useEffect, useMemo, useState } from "react";
import {
  ArrowRight,
  BookOpen,
  Compass,
  Flame,
  Target,
  Trophy,
  Zap,
} from "lucide-react";
import api from "../services/api";
import { Card, Button, SectionHeader } from "../design-system";
import { PageShell } from "../design-system/PageShell";
import CelebrationOverlay from "../components/CelebrationOverlay";

type AnyRecord = Record<string, any>;

type BadgeEntry = {
  id: string;
  name: string;
  description: string;
  icon: string;
  earned: boolean;
};

type PowerUpEntry = {
  id: string;
  name: string;
  description: string;
  cost: number;
  icon: string;
  owned: number;
};

type ChallengeEntry = {
  id: string;
  type: "weekly" | "monthly";
  name: string;
  target: number;
  progress: number;
  xpReward: number;
  completed: boolean;
  claimed: boolean;
};

const TABS = [
  { id: "overview", label: "Overview" },
  { id: "badges", label: "Badges" },
  { id: "journey", label: "Journey" },
  { id: "powerups", label: "Power-ups" },
] as const;

type TabId = (typeof TABS)[number]["id"];

/**
 * The gamification API returns some collections as maps keyed by id
 * (`{ badges: { first_interview: {...} } }`). Normalize either shape.
 */
function asList(value: unknown): AnyRecord[] {
  if (Array.isArray(value)) return value.filter((entry) => entry && typeof entry === "object");
  if (value && typeof value === "object") {
    return Object.entries(value as Record<string, unknown>)
      .filter(([, entry]) => entry && typeof entry === "object")
      .map(([id, entry]) => ({ id, ...(entry as AnyRecord) }));
  }
  return [];
}

function badgesOf(raw: unknown): AnyRecord[] {
  if (raw && typeof raw === "object" && "badges" in (raw as AnyRecord)) {
    return asList((raw as AnyRecord).badges);
  }
  return asList(raw);
}

function powerUpsOf(raw: unknown): AnyRecord[] {
  if (raw && typeof raw === "object" && "power_ups" in (raw as AnyRecord)) {
    return asList((raw as AnyRecord).power_ups);
  }
  return asList(raw);
}

function challengesOf(raw: unknown): AnyRecord[] {
  if (!raw || typeof raw !== "object") return [];
  const source = raw as AnyRecord;
  const weekly = (source.weekly || []).map((entry: AnyRecord) => ({ ...entry, type: "weekly" }));
  const monthly = (source.monthly || []).map((entry: AnyRecord) => ({ ...entry, type: "monthly" }));
  return [...weekly, ...monthly];
}

export default function GamificationDashboard() {
  const [profile, setProfile] = useState<AnyRecord | null>(null);
  const [badgesRaw, setBadgesRaw] = useState<unknown>(null);
  const [powerUpsRaw, setPowerUpsRaw] = useState<unknown>(null);
  const [challengesRaw, setChallengesRaw] = useState<unknown>(null);
  const [tower, setTower] = useState<AnyRecord | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<TabId>("overview");
  const [showCelebration, setShowCelebration] = useState(false);
  const [celebrationMessage, setCelebrationMessage] = useState("");
  const [error, setError] = useState("");

  const loadData = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const [profileRes, badgesRes, powerUpsRes, challengesRes, towerRes] =
        await Promise.all([
          api.gamification.getProfile(),
          api.gamification.getAllBadges(),
          api.gamification.getPowerUps(),
          api.gamification.getChallenges(),
          api.gamification.getTower(),
        ]);
      setProfile(profileRes as AnyRecord);
      setBadgesRaw(badgesRes);
      setPowerUpsRaw(powerUpsRes);
      setChallengesRaw(challengesRes);
      setTower(towerRes as AnyRecord);
    } catch (err) {
      setError((err as { detail?: string })?.detail || "Could not load gamification data.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadData();
  }, [loadData]);

  const earnedBadgeIds = useMemo(() => {
    const ids = profile?.badges;
    return new Set(Array.isArray(ids) ? (ids as string[]) : []);
  }, [profile]);

  const badges: BadgeEntry[] = useMemo(
    () =>
      badgesOf(badgesRaw).map((badge) => ({
        id: String(badge.id),
        name: String(badge.name || badge.id),
        description: String(badge.description || ""),
        icon: String(badge.icon || badge.emoji || "🏅"),
        earned: Boolean(badge.earned) || earnedBadgeIds.has(String(badge.id)),
      })),
    [badgesRaw, earnedBadgeIds]
  );

  const ownedPowerUps = useMemo(() => {
    const owned = (profile?.power_ups || tower?.power_ups || {}) as Record<string, number>;
    return owned;
  }, [profile, tower]);

  const powerUps: PowerUpEntry[] = useMemo(
    () =>
      powerUpsOf(powerUpsRaw).map((entry) => ({
        id: String(entry.id),
        name: String(entry.name || entry.id),
        description: String(entry.description || ""),
        cost: Number(entry.cost || 0),
        icon: String(entry.icon || entry.emoji || "✨"),
        owned: Number(ownedPowerUps[String(entry.id)] || 0),
      })),
    [powerUpsRaw, ownedPowerUps]
  );

  const challenges: ChallengeEntry[] = useMemo(
    () =>
      challengesOf(challengesRaw).map((entry) => ({
        id: String(entry.id),
        type: entry.type as "weekly" | "monthly",
        name: String(entry.name || entry.title || entry.id),
        target: Number(entry.target || 0),
        progress: Number(entry.progress || 0),
        xpReward: Number(entry.xp_reward ?? entry.xpReward ?? 0),
        completed: Boolean(entry.completed),
        claimed: Boolean(entry.claimed),
      })),
    [challengesRaw]
  );

  const xp = Number(profile?.xp || 0);
  const xpForCurrent = Number(profile?.xp_for_current_level || 0);
  const xpRemaining = Number(profile?.xp_to_next_level || 0);
  const levelSpan = xp + xpRemaining - xpForCurrent;
  const levelProgress = levelSpan > 0
    ? Math.min(100, Math.max(0, Math.round(((xp - xpForCurrent) / levelSpan) * 100)))
    : 0;

  const dailyCount = Number(profile?.daily_goal_count || 0);
  const dailyTarget = Number(profile?.daily_goal_target || 5);
  const dailyDone = Boolean(profile?.daily_goal_completed);
  const streak = Number(profile?.streak || 0);
  const earnedCount = badges.filter((badge) => badge.earned).length;

  const celebrate = (message: string) => {
    setCelebrationMessage(message);
    setShowCelebration(true);
    window.setTimeout(() => setShowCelebration(false), 3000);
  };

  const claimDailyBonus = async () => {
    try {
      const res = await api.gamification.claimDailyBonus();
      const reward = Number(res?.reward?.xp || 0);
      celebrate(reward ? `Daily bonus claimed! +${reward} XP` : "Daily bonus claimed!");
      await loadData();
    } catch (err) {
      setError((err as { detail?: string })?.detail || "Daily bonus is not available yet.");
    }
  };

  const claimChallenge = async (challenge: ChallengeEntry) => {
    try {
      await api.gamification.claimChallenge(challenge.type, challenge.id);
      celebrate(`Challenge claimed! +${challenge.xpReward} XP`);
      await loadData();
    } catch (err) {
      setError((err as { detail?: string })?.detail || "That reward is not claimable yet.");
    }
  };

  const buyPowerUp = async (powerUp: PowerUpEntry) => {
    try {
      await api.gamification.buyPowerUp(powerUp.id);
      celebrate(`${powerUp.name} purchased for ${powerUp.cost} coins.`);
      await loadData();
    } catch (err) {
      setError((err as { detail?: string })?.detail || "Not enough coins for that power-up.");
    }
  };

  return (
    <PageShell theme="adventure" className="max-w-7xl mx-auto py-6 px-4">
      <div className="mb-6 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <h1 className="text-3xl font-display font-bold text-text">Gamification</h1>
          <p className="mt-1 text-sm text-text-muted">
            Track your level, streak, badges and rewards.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          {TABS.map((tab) => (
            <Button
              key={tab.id}
              variant={activeTab === tab.id ? "primary" : "outline"}
              size="sm"
              onClick={() => setActiveTab(tab.id)}
            >
              {tab.label}
            </Button>
          ))}
        </div>
      </div>

      {showCelebration && (
        <CelebrationOverlay
          show={showCelebration}
          type="challenge"
          message={celebrationMessage}
          onClose={() => setShowCelebration(false)}
        />
      )}

      {error && (
        <div className="mb-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-600">
          {error}
        </div>
      )}

      {loading ? (
        <p className="py-10 text-center text-sm text-text-muted">Loading your progress…</p>
      ) : (
        <>
          <div className="grid gap-6 md:grid-cols-3">
            <Card pad="md">
              <div className="mb-4 flex items-center justify-between">
                <div>
                  <span className="text-xs font-semibold uppercase tracking-wider text-text-muted">
                    Level
                  </span>
                  <h2 className="mt-1 text-2xl font-bold text-text">
                    {Number(profile?.level || 1)}
                  </h2>
                  <p className="mt-1 text-[11px] font-mono text-primary">
                    {profile?.title_emoji} {profile?.title || "Beginner"}
                  </p>
                </div>
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-[#F4FAEF]">
                  <Zap size={20} className="text-primary" />
                </div>
              </div>
              <div className="flex justify-between text-xs font-mono text-text-muted">
                <span>{xp} XP</span>
                <span>{xpRemaining} XP to next</span>
              </div>
              <div className="mt-2 h-2 overflow-hidden rounded-full bg-[#E8EDE3]">
                <div
                  className="h-full rounded-full bg-primary transition-all duration-500"
                  style={{ width: `${levelProgress}%` }}
                />
              </div>
            </Card>

            <Card pad="md">
              <div className="mb-4 flex items-center justify-between">
                <div>
                  <span className="text-xs font-semibold uppercase tracking-wider text-text-muted">
                    Streak
                  </span>
                  <h2 className="mt-1 text-2xl font-bold text-text">{streak}</h2>
                  <p className="mt-1 text-[11px] font-mono text-orange-500">
                    {Number(profile?.streak_freezes || 0)} freezes
                  </p>
                </div>
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-orange-50">
                  <Flame size={20} className="text-orange-500" />
                </div>
              </div>
              <p className="text-xs text-text-muted">
                Streak multiplier ×{Number(profile?.streak_multiplier || 1)}
              </p>
            </Card>

            <Card pad="md">
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-xs font-semibold uppercase tracking-wider text-text-muted">
                    Badges
                  </span>
                  <h2 className="mt-1 text-2xl font-bold text-text">{earnedCount}</h2>
                  <p className="mt-1 text-[11px] font-mono text-amber-500">
                    {badges.length} available
                  </p>
                </div>
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-50">
                  <Trophy size={20} className="text-amber-500" />
                </div>
              </div>
            </Card>
          </div>

          {activeTab === "overview" && (
            <div className="mt-6 grid gap-6 lg:grid-cols-2">
              <Card>
                <SectionHeader
                  eyebrow="Daily goal"
                  title={`${dailyCount} / ${dailyTarget} today`}
                  description="Complete activities to fill your daily goal and earn bonus XP."
                />
                <div className="h-2 overflow-hidden rounded-full bg-[#E8EDE3]">
                  <div
                    className="h-full rounded-full bg-primary transition-all duration-500"
                    style={{
                      width: `${dailyTarget ? Math.min(100, (dailyCount / dailyTarget) * 100) : 0}%`,
                    }}
                  />
                </div>
                <p className="mt-3 text-xs text-text-muted">
                  {dailyDone ? "Daily goal completed!" : "Keep going to finish today's goal."}
                </p>
              </Card>

              <Card>
                <SectionHeader
                  eyebrow="Rewards"
                  title="Daily bonus"
                  description="Claim once per day for a free XP boost."
                />
                <div className="flex flex-wrap items-center gap-3">
                  <Button onClick={() => void claimDailyBonus()}>Claim daily bonus</Button>
                  <span className="text-xs text-text-muted">
                    {Number(profile?.coins || 0)} coins · {Number(profile?.stars_total || 0)} stars
                  </span>
                </div>
              </Card>
            </div>
          )}

          {activeTab === "badges" && (
            <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {badges.length === 0 ? (
                <Card>
                  <p className="text-sm text-text-muted">No badges are configured yet.</p>
                </Card>
              ) : (
                badges.map((badge) => (
                  <Card key={badge.id} tone={badge.earned ? "mint" : "default"} pad="md">
                    <div className="flex items-start gap-3">
                      <span className="text-2xl" aria-hidden="true">
                        {badge.icon}
                      </span>
                      <div className="min-w-0">
                        <p className="font-bold text-text">{badge.name}</p>
                        <p className="mt-1 text-xs text-text-muted">{badge.description}</p>
                        <p
                          className={`mt-2 text-[11px] font-semibold uppercase tracking-wider ${
                            badge.earned ? "text-primary" : "text-text-muted"
                          }`}
                        >
                          {badge.earned ? "Earned" : "Locked"}
                        </p>
                      </div>
                    </div>
                  </Card>
                ))
              )}
            </div>
          )}

          {activeTab === "journey" && (
            <div className="mt-6 grid gap-6 lg:grid-cols-2">
              <Card>
                <SectionHeader
                  eyebrow="Tower"
                  title={`Tower level ${Number(tower?.level || profile?.level || 1)}`}
                  description="Defeat bosses at every 10th level to climb the tower."
                />
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-xs uppercase tracking-wider text-text-muted">Bosses defeated</p>
                    <p className="mt-1 font-bold text-text">
                      {(tower?.bosses_defeated || []).length}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs uppercase tracking-wider text-text-muted">Coins</p>
                    <p className="mt-1 font-bold text-text">{Number(tower?.coins || 0)}</p>
                  </div>
                </div>
                {tower?.current_boss ? (
                  <div className="mt-4 rounded-lg border border-border p-3">
                    <p className="text-sm font-semibold text-text">
                      Current boss: {tower.current_boss.name || "Boss"}
                    </p>
                    <p className="mt-1 text-xs text-text-muted">
                      {tower.current_boss.topic || "Mixed topics"} · required score{" "}
                      {Number(tower.current_boss.required_score || 0)}
                    </p>
                    <Button
                      className="mt-3"
                      size="sm"
                      variant="outline"
                      onClick={() => {
                        window.location.href = "/tower";
                      }}
                    >
                      Enter boss battle <ArrowRight size={14} className="ml-2" />
                    </Button>
                  </div>
                ) : (
                  <p className="mt-4 text-sm text-text-muted">
                    No boss is waiting right now — keep levelling up.
                  </p>
                )}
              </Card>

              <Card>
                <SectionHeader
                  eyebrow="Challenges"
                  title="Weekly and monthly"
                  description="Complete challenges to earn XP and coins."
                />
                {challenges.length === 0 ? (
                  <p className="text-sm text-text-muted">No challenges assigned yet.</p>
                ) : (
                  <div className="space-y-3">
                    {challenges.map((challenge) => (
                      <div
                        key={`${challenge.type}-${challenge.id}`}
                        className="rounded-lg border border-border p-3"
                      >
                        <div className="flex items-start justify-between gap-3">
                          <div className="min-w-0">
                            <p className="text-sm font-semibold text-text">{challenge.name}</p>
                            <p className="mt-1 text-xs text-text-muted">
                              {challenge.progress} / {challenge.target} ·{" "}
                              {challenge.xpReward} XP · {challenge.type}
                            </p>
                          </div>
                          {challenge.completed && !challenge.claimed && (
                            <Button
                              size="sm"
                              onClick={() => void claimChallenge(challenge)}
                            >
                              Claim
                            </Button>
                          )}
                          {challenge.claimed && (
                            <span className="text-[11px] font-semibold uppercase text-primary">
                              Claimed
                            </span>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </Card>
            </div>
          )}

          {activeTab === "powerups" && (
            <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {powerUps.length === 0 ? (
                <Card>
                  <p className="text-sm text-text-muted">No power-ups are available.</p>
                </Card>
              ) : (
                powerUps.map((powerUp) => (
                  <Card key={powerUp.id} pad="md">
                    <div className="flex items-start gap-3">
                      <span className="text-2xl" aria-hidden="true">
                        {powerUp.icon}
                      </span>
                      <div className="min-w-0 flex-1">
                        <p className="font-bold text-text">{powerUp.name}</p>
                        <p className="mt-1 text-xs text-text-muted">{powerUp.description}</p>
                        <p className="mt-2 text-[11px] font-mono text-text-muted">
                          Owned: {powerUp.owned} · Cost: {powerUp.cost} coins
                        </p>
                        <Button
                          className="mt-3"
                          size="sm"
                          variant="outline"
                          onClick={() => void buyPowerUp(powerUp)}
                        >
                          Buy
                        </Button>
                      </div>
                    </div>
                  </Card>
                ))
              )}
            </div>
          )}

          <div className="mt-8 grid gap-4 sm:grid-cols-3">
            <Card pad="sm" interactive onClick={() => { window.location.href = "/lessons"; }}>
              <div className="flex items-center gap-2 text-sm font-semibold text-text">
                <BookOpen size={16} className="text-primary" /> Lessons
              </div>
            </Card>
            <Card pad="sm" interactive onClick={() => { window.location.href = "/question-bank"; }}>
              <div className="flex items-center gap-2 text-sm font-semibold text-text">
                <Target size={16} className="text-primary" /> Practice
              </div>
            </Card>
            <Card pad="sm" interactive onClick={() => { window.location.href = "/skills"; }}>
              <div className="flex items-center gap-2 text-sm font-semibold text-text">
                <Compass size={16} className="text-primary" /> Skill map
              </div>
            </Card>
          </div>
        </>
      )}
    </PageShell>
  );
}
