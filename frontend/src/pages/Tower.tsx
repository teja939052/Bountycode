import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import { useGamificationData } from "../hooks/useGamificationData";
import { useGamificationState } from "../hooks/useGamificationState";
import ShipJourney from "../components/tower/ForestJourney";
import CharacterWorld from "../components/tower/CrewShip";
import DailyLoginCalendar from "../components/DailyLoginCalendar";
import {
  Flame,
  Trophy,
  Zap,
  Star,
  Coins,
  Snowflake,
  ArrowRight,
  Target,
  Swords,
} from "lucide-react";
import DiamondsBar from "../components/XPBar";
import api from "../services/api";

export default function Tower() {
  const { tower, forest, challenges, leaderboard, streakStatus, combo, dailyLogin, isLoading } =
    useGamificationData();
  const { profile, startup, optimisticPreview } = useGamificationState();

  // Truth layer: prefer backend-owned profile/startup, then tower fallback.
  const level = optimisticPreview?.level ?? profile?.level ?? startup?.level ?? tower?.level ?? 1;
  const diamonds = optimisticPreview?.diamonds ?? profile?.diamonds ?? startup?.diamonds ?? tower?.diamonds ?? 0;
  const xpToNext = profile?.xp_to_next ?? tower?.xp_to_next ?? 100;
  const coins = optimisticPreview?.coins ?? profile?.coins ?? startup?.coins ?? tower?.coins ?? 0;
  const streak = optimisticPreview?.streak ?? profile?.streak ?? streakStatus?.streak ?? startup?.streak ?? 0;
  const streakFreezes = profile?.streak_freezes ?? tower?.streak_freezes ?? startup?.streak_freezes ?? 0;
  const stars = optimisticPreview?.stars ?? profile?.stars_total ?? (tower as any)?.stars_total ?? 0;
  const bossesDefeated = Array.isArray((tower as any)?.bosses_defeated)
    ? ((tower as any).bosses_defeated as number[])
    : typeof (tower as any)?.bosses_beaten === "number"
      ? Array.from({ length: (tower as any).bosses_beaten as number }, (_, i) => i + 1)
      : [];
  const currentBoss = (tower as any)?.boss_level ?? null;
  const title = profile?.title ?? "Seedling";
  const titleEmoji = profile?.title_emoji ?? "🌱";
  const levelColor = profile?.color;
  const currentCombo = combo?.current_combo ?? 0;
  const comboMultiplier = combo?.multiplier ?? 1;
  const loginStreak = dailyLogin?.streak ?? 0;

  const xpPct = xpToNext > 0 ? Math.min(100, Math.round((diamonds / xpToNext) * 100)) : 0;

  if (isLoading && !tower && !profile) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-primary-600" />
      </div>
    );
  }

  return (
    <div className="min-h-screen py-6 px-3 sm:py-8 sm:px-4 max-w-6xl mx-auto space-y-5">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -16 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div className="flex items-center gap-3">
          <Link
            to="/levels"
            className="inline-flex items-center gap-2 text-sm text-gray-500 hover:text-gray-700"
          >
            ← Level Map
          </Link>
        </div>
        <div className="flex items-center gap-3">
          <div
            className="h-11 w-11 rounded-2xl flex items-center justify-center text-2xl"
            style={
              levelColor
                ? {
                    background: `linear-gradient(135deg, ${levelColor.from}30, ${levelColor.to}20)`,
                    border: `1px solid ${levelColor.from}50`,
                    boxShadow: `0 0 24px ${levelColor.glow}`,
                  }
                : {
                    background: 'linear-gradient(135deg, rgba(99,102,241,0.18), rgba(139,92,246,0.18))',
                    border: '1px solid rgba(99,102,241,0.25)',
                    boxShadow: '0 0 24px rgba(99,102,241,0.18)',
                  }
            }
          >
            {titleEmoji}
          </div>
          <div>
            <h1 className="text-xl font-bold text-text-primary dark:text-white tracking-tight">The Crow’s Nest</h1>
            <p className="text-xs text-gray-500 font-mono">Level {level} · {title} · {diamonds.toLocaleString()} Diamonds</p>
          </div>
        </div>
      </motion.div>

      {/* Diamonds Progress Ring + Level */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="gamification-card rounded-3xl p-5 sm:p-6"
      >
        <div className="flex flex-col sm:flex-row items-center gap-5">
          <DiamondsBar diamonds={diamonds} showLevel={true} variant="ring" />
          <div className="flex-1 w-full">
            <div className="flex items-end justify-between mb-2">
              <div>
                <p className="text-xs font-mono uppercase tracking-widest text-gray-500 mb-1">Level Progress</p>
                <p className="text-3xl font-black text-text-primary dark:text-white tracking-tight">{xpPct}%</p>
              </div>
              <p className="text-xs text-gray-500 font-mono">
                {xpToNext - diamonds > 0 ? `${(xpToNext - diamonds).toLocaleString()} Diamonds to Level ${level + 1}` : "Max level reached!"}
              </p>
            </div>
            <div className="h-3 bg-gray-200/60 dark:bg-gray-800 rounded-full overflow-hidden">
              <motion.div
                className="h-full rounded-full"
                style={{ background: 'linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899)' }}
                initial={{ width: 0 }}
                animate={{ width: `${xpPct}%` }}
                transition={{ duration: 0.9, ease: 'easeOut' }}
              />
            </div>
          </div>
        </div>
      </motion.div>

      {/* Stats Row */}
      <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
        {[
          { icon: Flame, label: "Streak", value: `${streak}d`, color: "text-orange-500", bg: "bg-orange-500/10" },
          { icon: Coins, label: "Coins", value: coins, color: "text-yellow-600", bg: "bg-yellow-500/10" },
          { icon: Star, label: "Stars", value: stars, color: "text-amber-500", bg: "bg-amber-400/10" },
          { icon: Snowflake, label: "Freezes", value: streakFreezes, color: "text-sky-500", bg: "bg-sky-500/10" },
          { icon: Swords, label: "Bosses", value: bossesDefeated.length, color: "text-rose-500", bg: "bg-rose-500/10" },
        ].map((s, i) => (
          <motion.div
            key={s.label}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.04 }}
            className={`stat-card gamification-card rounded-2xl p-3 text-center cursor-default`}
          >
            <div className={`w-9 h-9 rounded-xl ${s.bg} flex items-center justify-center mx-auto mb-1.5`}>
              <s.icon size={18} className={s.color} />
            </div>
            <div className="text-lg font-black text-text-primary dark:text-white">{s.value}</div>
            <div className="text-[10px] text-gray-500 uppercase tracking-wider font-medium">{s.label}</div>
          </motion.div>
        ))}
      </div>

      {/* Combo + Login Row */}
      <div className="grid grid-cols-2 gap-3">
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="gamification-card rounded-2xl p-4"
        >
          <p className="text-[10px] font-mono uppercase tracking-widest text-indigo-400 mb-1">Combo</p>
          <div className="flex items-end gap-2">
            <span className="text-3xl font-black text-text-primary">{currentCombo}x</span>
            <span className="text-sm text-indigo-300 mb-1 font-mono">x{comboMultiplier.toFixed(2)}</span>
          </div>
          <p className="text-[10px] text-gray-500 mt-1">Rapid activities multiply Diamonds</p>
        </motion.div>
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="gamification-card rounded-2xl p-4"
        >
          <p className="text-[10px] font-mono uppercase tracking-widest text-yellow-300 mb-1">Daily Login</p>
          <div className="flex items-end gap-2">
            <span className="text-3xl font-black text-text-primary">{loginStreak}</span>
            <span className="text-sm text-yellow-300 mb-1 font-mono">days</span>
          </div>
          <p className="text-[10px] text-gray-500 mt-1">Claim your escalating rewards</p>
        </motion.div>
      </div>

      {/* Boss Battle */}
      {currentBoss && !bossesDefeated.includes(currentBoss) && (
        <motion.div
          initial={{ opacity: 0, scale: 0.96 }}
          animate={{ opacity: 1, scale: 1 }}
          className="gamification-border-gradient rounded-2xl p-5"
          style={{ background: 'linear-gradient(135deg, rgba(239,68,68,0.12), rgba(185,28,28,0.08))' }}
        >
          <div className="flex items-center gap-4">
            <div className="text-4xl">🏴‍☠️</div>
            <div className="flex-1">
              <h3 className="font-bold text-red-400">Boss Island — Level {currentBoss}</h3>
              <p className="text-sm text-gray-400">Conquer this island to unlock the next fleet!</p>
            </div>
            <button className="btn-glow px-5 py-2.5 rounded-xl bg-red-500 text-white font-bold hover:bg-red-600 transition-colors">
              Fight!
            </button>
          </div>
        </motion.div>
      )}

      {/* Ship's Journey */}
      <ShipJourney forest={forest} level={level} />

      {/* Crew & Ship */}
      <CharacterWorld level={level} forest={forest} />

      {/* Daily Login Calendar */}
      {dailyLogin?.calendar && dailyLogin.calendar.length > 0 && (
        <DailyLoginCalendar
          calendar={dailyLogin.calendar}
          streak={dailyLogin.streak ?? 0}
          onClaim={async () => {
            await api.gamification.claimDailyLogin();
          }}
        />
      )}

      {/* Challenges */}
      {challenges?.challenges && challenges.challenges.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="gamification-card rounded-2xl p-5"
        >
          <h3 className="text-sm font-bold text-gray-200 mb-4 flex items-center gap-2">
            <Target size={16} className="text-indigo-400" /> Challenges
          </h3>
          <div className="space-y-3">
            {challenges.challenges.slice(0, 3).map((c) => (
              <div key={c.id} className="flex items-center gap-3 p-3 rounded-xl bg-white/[0.04] border border-white/5 hover:border-white/10 transition-colors">
                <span className="text-xl">{c.completed ? "✅" : "⬜"}</span>
                <div className="flex-1">
                  <div className="text-sm font-semibold text-gray-200">{c.title}</div>
                  <div className="text-xs text-gray-500">{c.description}</div>
                </div>
                {c.reward_xp && (
                  <span className="text-xs text-amber-400 font-mono font-bold">+{c.reward_xp} Diamonds</span>
                )}
              </div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Leaderboard */}
      {leaderboard?.entries && leaderboard.entries.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="gamification-card rounded-2xl p-5"
        >
          <h3 className="text-sm font-bold text-gray-200 mb-4 flex items-center gap-2">
            <Trophy size={16} className="text-amber-400" /> Leaderboard
          </h3>
          <div className="space-y-2">
            {leaderboard.entries.slice(0, 5).map((entry, i) => (
              <div key={i} className="flex items-center gap-3 p-2.5 rounded-xl hover:bg-white/[0.04] transition-colors">
                <span className="w-7 text-center text-sm font-black">
                  {i === 0 ? "🥇" : i === 1 ? "🥈" : i === 2 ? "🥉" : `#${i + 1}`}
                </span>
                <span className="flex-1 text-sm text-gray-300 font-medium">{entry.name || `User ${entry.user_id?.slice(-4)}`}</span>
                <span className="text-xs text-amber-400 font-mono font-bold">{entry.diamonds} Diamonds</span>
              </div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Quick Actions */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { to: "/problem-of-the-day", label: "Daily Problem", icon: Zap },
          { to: "/question-bank", label: "Practice", icon: Target },
          { to: "/daily-challenge", label: "Daily Challenge", icon: Flame },
          { to: "/leaderboard", label: "Leaderboard", icon: Trophy },
        ].map((link) => (
          <Link
            key={link.to}
            to={link.to}
            className="stat-card gamification-card flex items-center gap-2.5 p-3.5 rounded-2xl group"
          >
            <div className="w-9 h-9 rounded-xl bg-indigo-500/10 flex items-center justify-center text-indigo-600 group-hover:scale-110 transition-transform">
              <link.icon size={18} />
            </div>
            <span className="text-sm font-bold text-text-primary dark:text-white">{link.label}</span>
            <ArrowRight size={14} className="ml-auto text-gray-400 group-hover:translate-x-0.5 transition-transform" />
          </Link>
        ))}
      </div>
    </div>
  );
}
