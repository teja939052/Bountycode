const fs = require('fs');

let content = `import { useState, useEffect } from "react";
import {
  ArrowRight,
  Code2,
  Flame,
  Trophy,
  Zap,
  Target,
  Compass,
  BookOpen,
  Code as CodeIcon,
  Zap as ZapIcon,
  Target as TargetIcon,
  Flame as FlameIcon,
  Compass as CompassIcon,
  BookOpen as BookOpenIcon,
} from "lucide-react";
import api from "../services/api";
import { Card, Button, SectionHeader } from "../design-system";
import { PageShell } from "../design-system/PageShell";
import { CelebrationOverlay } from "../components/CelebrationOverlay";

type Badge = {
  id: string;
  name: string;
  description: string;
  icon: string;
  tier: string;
  earned: boolean;
  earnedAt?: string;
};

type PowerUp = {
  id: string;
  name: string;
  description: string;
  cost: number;
  effect: string;
  owned: number;
};

type Challenge = {
  id: string;
  title: string;
  description: string;
  type: string;
  progress: number;
  target: number;
  xpReward: number;
  completed: boolean;
};

type BossBattle = {
  id: number;
  name: string;
  emoji: string;
  topic: string;
  difficulty: string;
  requiredScore: number;
  defeated: boolean;
  defeatedAt?: string;
};

export default function GamificationDashboard() {
  const [profile, setProfile] = useState<any>(null);
  const [badges, setBadges] = useState<any[]>([]);
  const [powerUps, setPowerUps] = useState<any[]>([]);
  const [challenges, setChallenges] = useState<any[]>([]);
  const [tower, setTower] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("overview");
  const [showCelebration, setShowCelebration] = useState(false);
  const [celebrationType, setCelebrationType] = useState("");
  const [celebrationMessage, setCelebrationMessage] = useState("");

  const loadData = async () => {
    setLoading(true);
    try {
      const [profileRes, badgesRes, powerUpsRes, challengesRes, towerRes] =
        await Promise.all([
          api.gamification.getProfile(),
          api.gamification.getAllBadges(),
          api.gamification.getPowerUps(),
          api.gamification.getChallenges(),
          api.gamification.getTower(),
        ]);
        setProfile(profileRes);
        setBadges(badgesRes);
        setPowerUps(powerUpsRes);
        setChallenges(challengesRes);
        setTower(towerRes);
      } catch (e: any) {
        console.error("Failed to load gamification data", e);
      } finally {
        setLoading(false);
      }
    };

  useEffect(() => {
    loadData();
  }, []);

  const claimDailyBonus = async () => {
    try {
      const res = await api.gamification.claimDailyBonus();
      setShowCelebration(true);
      setCelebrationType("bonus");
      setCelebrationMessage(\`Daily bonus completed! +\${res?.reward?.xp || 50} XP\`);
      setLoading(true);
      await loadData();
      setLoading(false);
      setTimeout(() => setShowCelebration(false), 3000);
    } catch (e: any) {
      // Already claimed today
    }
  };

  const claimChallenge = async (challengeId: string) => {
    try {
      await api.gamification.claimChallenge("weekly", challengeId);
      setShowCelebration(true);
      setCelebrationType("challenge");
      setCelebrationMessage("Challenge completed! Reward claimed.");
      setLoading(true);
      await loadData();
      setLoading(false);
      setTimeout(() => setShowCelebration(false), 3000);
    } catch (e: any) {
      // Already claimed or not eligible
    }
  };

  const buyPowerUp = async (powerUpId: string) => {
    try {
      await api.gamification.buyPowerUp(powerUpId);
      setLoading(true);
      await loadData();
      setLoading(false);
    } catch (e: any) {
      // Failed to purchase
    }
  };

  const levelProgress =
    profile &&
    profile.xp_for_current_level !== undefined
      ? Math.min(
          100,
          Math.round(
            ((profile.xp - profile.xp_for_current_level) /
              (profile.xp_to_next_level - profile.xp_for_current_level)) *
              100,
          ),
        )
      : 0;

  const levelLabel =
    profile?.role || profile?.level || "Beginner";

  return (
    <PageShell theme="adventure" className="max-w-7xl mx-auto py-6">
      <div className="mb-6 flex flex-col md:flex-row md:items-end gap-4">
        <div>
          <h1 className="text-3xl font-display font-bold text-ink dark:text-white">
            Gamification Dashboard
          </h1>
          <p className="text-slate-600 dark:text-slate-400 mt-1">
            Track your progress, earn badges, and level up your placement prep.
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            onClick={() => setActiveTab("overview")}
            className={activeTab === "overview" ? "bg-ink text-white" : ""}
          >
            Overview
          </Button>
          <Button
            variant="outline"
            onClick={() => setActiveTab("badges")}
            className={activeTab === "badges" ? "bg-ink text-white" : ""}
          >
            Badges
          </Button>
          <Button
            variant="outline"
            onClick={() => setActiveTab("journey")}
            className={activeTab === "journey" ? "bg-ink text-white" : ""}
          >
            Journey
          </Button>
          <Button
            variant="outline"
            onClick={() => setActiveTab("chests")}
            className={activeTab === "chests" ? "bg-ink text-white" : ""}
          >
            Chests
          </Button>
        </div>
      </div>

      {showCelebration && (
        <CelebrationOverlay
          show={showCelebration}
          type={celebrationType as any}
          message={celebrationMessage}
          onClose={() => setShowCelebration(false)}
        />
      )}

      <div className="mt-6 grid gap-6 md:grid-cols-3 lg:grid-cols-3">
        <Card pad="md">
          <div className="flex items-center justify-between mb-4">
            <div className="flex-1">
              <span className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                Level
              </span>
              <h2 className="text-2xl font-bold text-ink dark:text-white mt-1">
                {profile?.level || 1}
              </h2>
              <p className="text-[10px] font-mono text-brand-500 mt-1">
                {levelLabel}
              </p>
            </div>
            <div className="w-10 h-10 rounded-xl flex items-center justify-center bg-brand-50 dark:bg-brand-900/30">
              <Zap size={20} className="text-brand-500" />
            </div>
          </div>
          <div className="mt-4">
            <div className="flex justify-between text-xs font-mono text-slate-500 mb-1">
              <span>{profile?.xp_for_current_level || 0} XP</span>
              <span>{profile?.xp_to_next_level || 0} XP</span>
            </div>
            <div className="h-2 bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-brand-500 to-brand-600 rounded-full transition-all duration-500"
                style={\`width: \${levelProgress}%\`}
              ></div>
            </div>
          </div>
        </Card>

        <Card pad="md">
          <div className="flex items-center justify-between mb-4">
            <div className="flex-1">
              <span className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                Streak
              </span>
              <h2 className="text-2xl font-bold text-ink dark:text-white mt-1">
                {profile?.streak || 0}
              </h2>
              <p className="text-[10px] font-mono text-orange-500 mt-1">
                {profile?.streak_freezes || 0} freezes
              </p>
            </div>
            <div className="w-10 h-10 rounded-xl flex items-center justify-center bg-orange-50 dark:bg-orange-900/30">
              <Flame size={20} className="text-orange-500" />
            </div>
          </div>
          <div className="mt-3">
            <div className="w-full bg-slate-200 dark:bg-slate-800 rounded-full h-2 overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-orange-400 to-orange-600 rounded-full"
                style={{ width: \`\${Math.min(100, (profile?.streak || 0) / 30) * 100}%\` }}
              ></div>
            </div>
          </div>
        </Card>

        <Card pad="md">
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <span className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                Badges
              </span>
              <h2 className="text-2xl font-bold text-ink dark:text-white mt-1">
                {badges?.filter((b: any) => b.earned).length || 0}
              </h2>
              <p className="text-[10px] font-mono text-amber-500 mt-1">
                {badges?.length || 0} available
              </p>
            </div>
            <div className="w-10 h-10 rounded-xl flex items-center justify-center bg-amber-50 dark:bg-amber-900/30">
              <Star size={20} className="text-amber-500" />
            </div>
          </div>
        </Card>
      </div>

      {activeTab === "streak" && (
        <div className="mt-6 grid gap-6 md:grid-cols-3 lg:grid-cols-3">
          <Card pad="md">
            <SectionHeader eyebrow="Daily Streak" title="Daily Streak" description="Practice daily to maintain your streak and earn bonus XP." />
            <div className="bg-[#0f0f0f] border border-[#2a2a2a] rounded-xl p-4">
              <div className="flex items-center justify-between mb-4">
                <div className="flex-1">
                  <h3 className="font-bold text-text">{currentStep.title}</h3>
                  <p className="text-xs text-[#9a9a9a] mt-2">{currentStep.description}</p>
                </div>
                {currentStep.type === "quiz" && (
                  <Badge
                    state={
                      questionIndex === currentQuestionIndex
                        ? "correct"
                        : currentStep.type === "quiz"
                        ? "neutral"
                        : "neutral"
                    }
                  />
                )}
              </div>
              <div className="bg-[#0f0f0f] border border-[#2a2a2a] rounded-xl p-4 mb-4">
                <div className="font-mono text-sm text-[#e9e9e9] mb-2">{currentStep.code}</div>
                {currentStep.inputPlaceholder && (
                  <textarea
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    rows={4}
                    className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] focus:border-[#ffa116] outline-none font-mono"
                    placeholder={currentStep.starterCode || ""}
                  />
                )}
                {!currentStep.inputPlaceholder && (
                  <input
                    type="text"
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    placeholder="Your answer..."
                    className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] focus:border-[#ffa116] outline-none font-mono"
                  />
                )}
                <div className="flex gap-2 mt-4">
                  <Button variant="outline" disabled={loading} onClick={submitAnswer}>
                    {loading ? <Loader2 size={14} className="mr-2" /> : null} Check Answer
                  </Button>
                  <Button variant="outline" disabled={loading || !code} onClick={() => setCode(currentStep.starterCode || "")}>
                    Reset
                  </Button>
                </div>
                {feedback && (
                  <div className={`mt-3 p-3 rounded-lg ${feedback.is_correct ? "bg-green-500/10 border border-green-500/30 text-green-500" : "bg-red-500/10 border border-red-500/30 text-red-500"}`}>
                    {feedback.message}
                  </div>
                )}
                {error && (
                  <div className="mt-3 p-3 rounded bg-red-500/10 border border-red-500/30 text-red-400 text-sm">{error}</div>
                )}
              </div>
            </div>

            <div className="lg:col-span-5 space-y-6">
              <Card pad="md">
                <SectionHeader eyebrow="Diagnose" title="Your Progress" />
                <div className="flex items-center justify-between mb-4">
                  <span className="text-xs font-semibold text-slate-500 dark:text-slate-400">Overall Progress</span>
                  <span className="text-sm font-bold text-text">{progressPct}%</span>
                </div>
                <div className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded-full h-2">
                  <div
                    className="h-full bg-gradient-to-r from-brand-500 to-brand-600 rounded-full transition-all duration-500"
                    style={{ width: \`\${levelProgress}%\` }}
                  ></div>
                </div>
                <div className="flex justify-between text-xs text-slate-500">
                  <span>{progressCompleted}</span>
                  <span>{lesson.steps.length}</span>
                </div>
              </div>

              <Card pad="md">
                <h3 className="font-bold text-text-primary mb-4">Next Lesson</h3>
                {nextLesson ? (
                  <div className="bg-[#0f0f0f] border border-[#2a2a2a] rounded-xl p-4 mb-4">
                    <div className="flex items-center gap-3 mb-3">
                      <div className={`w-6 h-6 rounded-full flex items-center justify-center font-bold text-xs ${i === 1 ? "bg-brand-500 text-white" : "bg-white dark:bg-slate-800 border border-white/100 text-slate-500 dark:text-gray-500"}`}>
                        {i + 1}
                      </div>
                      <div className="flex-1">
                        <div className="font-bold text-text text-sm">{nextLesson.title}</div>
                        <div className="text-xs text-brand-muted">{nextLesson.description}</div>
                      </div>
                    </div>
                    <Button variant="primary" onClick={() => navigate(\`/coding-academy/${nextLesson.id}\`)}>
                      Start Lesson →
                    </Button>
                  </div>
                ) : (
                  <div className="flex items-center gap-3 p-4 rounded-xl bg-green-50/10 border border-green-50/20 text-green-500">
                    <div className="w-8 h-8 rounded-full flex items-center justify-center text-green-500">
                      🎉
                    </div>
                    <div>
                      <p className="font-bold text-text mb-2">All lessons complete!</p>
                      <p className="text-xs text-green-500">Congratulations on completing all lessons.</p>
                    </div>
                  </div>
                )}
              </Card>
            </div>
          )}
        </PageShell>
  );
}
`;

fs.writeFileSync("D:\\Project-Fremen\\frontend\\src\\pages\\GamificationDashboard.tsx", content);
console.log("Written GamificationDashboard.tsx");