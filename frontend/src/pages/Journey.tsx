import { useState, useEffect, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Lock, Check, MapPin, Zap, Sparkles, Trophy, ChevronRight } from "lucide-react";
import { journeyApi } from "../services/api/journey.ts";
import { useToast } from "../components/Toast";
import useTrack from "../hooks/useTrack";

const BUILDING_META = {
  interview_hub: { label: "Interview Hub", icon: "🎤" },
  arena: { label: "Arena", icon: "⚔️" },
  guild_hall: { label: "Guild Hall", icon: "🛡️" },
  dungeon: { label: "Dungeon", icon: "🕳️" },
  showcase: { label: "Showcase", icon: "🏆" },
  merchant: { label: "Merchant", icon: "🛒" },
  collection: { label: "Collection", icon: "📚" },
  pvp: { label: "PvP Arena", icon: "🥊" },
};

const QUEST_POOL = [
  "Solve 2 problems",
  "Open merchant",
  "Complete 1 dungeon",
  "Win 1 battle",
  "Review 1 showcase",
];

function hashRegion(id) {
  let h = 0;
  for (let i = 0; i < id.length; i++) {
    h = (h * 31 + id.charCodeAt(i)) >>> 0;
  }
  return h;
}

function questsForRegion(regionId) {
  const start = hashRegion(regionId) % QUEST_POOL.length;
  return Array.from({ length: 3 }, (_, i) => QUEST_POOL[(start + i) % QUEST_POOL.length]);
}

function generateStars() {
  return Array.from({ length: 42 }, (_, i) => ({
    id: i,
    left: `${(i * 37) % 100}%`,
    top: `${(i * 53 + 7) % 100}%`,
    size: 1 + ((i * 7) % 3),
    delay: `${(i % 8) * 0.7}s`,
    duration: `${2.2 + (i % 5) * 0.6}s`,
  }));
}

export default function Journey() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [moving, setMoving] = useState(null);
  const [busyQuest, setBusyQuest] = useState(null);
  const [heroHop, setHeroHop] = useState(false);
  const [flash, setFlash] = useState(null);
  const toast = useToast();
  const stars = useMemo(generateStars, []);

  const load = async () => {
    setLoading(true);
    try {
      const res = await journeyApi.get();
      setData(res);
    } catch (err) {
      toast.error(err.message || "Failed to load journey");
    }
    setLoading(false);
  };

  useEffect(() => {
    load();
  }, []);

  const regions = data?.regions || [];
  const current = data?.current_region || null;
  const totalXp = data?.total_xp || 0;
  const nextRegion = data?.next_region || null;
  const progressPercent = data?.progress_percent ?? 0;
  const completedSet = useMemo(
    () => new Set(data?.completed_quests || []),
    [data?.completed_quests]
  );
  const fogCleared = useMemo(
    () => new Set(data?.fog_cleared_regions || []),
    [data?.fog_cleared_regions]
  );
  const unlocked = useMemo(
    () => new Set(regions.filter((r) => totalXp >= r.xp_required).map((r) => r.id)),
    [regions, totalXp]
  );

  const quests = current ? questsForRegion(current.id) : [];

  const scrollToNode = (regionId) => {
    const el = document.getElementById(`journey-node-${regionId}`);
    if (el) el.scrollIntoView({ behavior: "smooth", block: "center" });
  };

  const handleMove = async (region) => {
    setMoving(region.id);
    try {
      const res = await journeyApi.move(region.id);
      setHeroHop(true);
      setTimeout(() => setHeroHop(false), 600);
      setData((d) => ({ ...d, current_region: res.current_region }));
      toast.success(`${res.current_region.emoji} ${res.message}`);
      setTimeout(() => scrollToNode(region.id), 350);
    } catch (err) {
      toast.error(err.message || "Failed to move");
    }
    setMoving(null);
  };

  const handleComplete = async (idx) => {
    if (!current) return;
    setBusyQuest(idx);
    try {
      const res = await journeyApi.completeQuest(current.id, idx);
      setData((d) => ({
        ...d,
        completed_quests: res.completed_quests,
        fog_cleared_regions: res.fog_cleared_regions,
        quests_completed: res.quests_completed,
      }));
      setFlash({
        quest: quests[idx],
        xp: res.xp_gained || 0,
        fog: res.fog_cleared,
        fogRegion: res.fog_cleared_region,
      });
      setTimeout(() => setFlash(null), 1600);
    } catch (err) {
      toast.error(err.message || "Failed to complete quest");
    }
    setBusyQuest(null);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-surface-card flex items-center justify-center">
        <div className="spinner-cyber" />
      </div>
    );
  }

  return (
    <div className="relative min-h-screen bg-surface-card overflow-hidden">
      <style>{`
        @keyframes journeyTwinkle {
          0%, 100% { opacity: 0.15; transform: scale(0.7); }
          50% { opacity: 1; transform: scale(1.15); }
        }
        .journey-star {
          position: absolute;
          border-radius: 9999px;
          background: #A9C88E;
          animation: journeyTwinkle infinite;
        }
        @keyframes journeyMist {
          0%, 100% { opacity: 0.75; }
          50% { opacity: 0.45; }
        }
        .journey-fog {
          animation: journeyMist 3s ease-in-out infinite;
        }
      `}</style>

      <div className="absolute inset-0 bg-gradient-to-b from-[#EDF5E6] via-transparent to-[#F6F3EA]" />
      {stars.map((s) => (
        <div
          key={s.id}
          className="journey-star"
          style={{
            left: s.left,
            top: s.top,
            width: s.size,
            height: s.size,
            animationDelay: s.delay,
            animationDuration: s.duration,
          }}
        />
      ))}

      <div className="relative mx-auto max-w-2xl px-4 py-10">
        <div className="text-center mb-8">
          <motion.div
            initial={{ opacity: 0, y: -16 }}
            animate={{ opacity: 1, y: 0 }}
            className="inline-flex items-center gap-2 text-xs font-mono uppercase tracking-[0.3em] text-nature-blossom mb-2"
          >
            <Sparkles size={14} />
            The Journey
            <Sparkles size={14} />
          </motion.div>
          <h1 className="text-4xl font-bold font-display bg-gradient-to-r from-[#4F8F57] to-[#7BB661] bg-clip-text text-transparent">
            {current ? `${current.emoji} ${current.name}` : "Adventure Map"}
          </h1>
          <div className="flex items-center justify-center gap-4 mt-3 text-sm text-text-muted">
            <span className="flex items-center gap-1.5">
              <Zap size={14} className="text-amber-500" />
              {totalXp.toLocaleString()} XP
            </span>
            <span className="flex items-center gap-1.5">
              <Trophy size={14} className="text-nature-blossom" />
              {data?.quests_completed ?? 0} quests
            </span>
            <span className="flex items-center gap-1.5">
              <MapPin size={14} className="text-nature-blossom" />
              Region {current?.order ?? 1}/8
            </span>
          </div>
        </div>

        {nextRegion && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="rounded-2xl border border-nature-leaf/20 bg-white p-5 mb-10"
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-mono uppercase tracking-wider text-text-muted">
                Progress to {nextRegion.emoji} {nextRegion.name}
              </span>
              <span className="text-xs font-mono text-text-muted">
                {totalXp.toLocaleString()} / {nextRegion.xp_required.toLocaleString()} XP
              </span>
            </div>
            <div className="h-3 rounded-full bg-[#E5E0D3] overflow-hidden border border-[#EDEAE0]">
              <motion.div
                className="h-full rounded-full bg-gradient-to-r from-[#4F8F57] to-[#7BB661] shadow-[0_0_12px_rgba(79,143,87,0.4)]"
                initial={{ width: 0 }}
                animate={{ width: `${progressPercent}%` }}
                transition={{ duration: 0.9, ease: "easeOut" }}
              />
            </div>
            <div className="flex items-center justify-between mt-2">
              <span className="text-xs text-text-muted font-mono">{progressPercent}%</span>
              <span className="text-xs text-text-muted font-mono">
                {nextRegion.xp_required - totalXp > 0
                  ? `${(nextRegion.xp_required - totalXp).toLocaleString()} XP to unlock`
                  : "Unlocked"}
              </span>
            </div>
          </motion.div>
        )}

        <div className="flex flex-col items-center">
          {regions.map((region, index) => {
            const isUnlocked = unlocked.has(region.id);
            const isLocked = !isUnlocked;
            const isCurrent = current?.id === region.id;
            const revealed = isUnlocked || fogCleared.has(region.id);
            const regionDone = completedSet.has(`${region.id}:0`) &&
              completedSet.has(`${region.id}:1`) &&
              completedSet.has(`${region.id}:2`);

            return (
              <div key={region.id} className="flex flex-col items-center w-full">
                <div id={`journey-node-${region.id}`} className="w-full max-w-xl scroll-mt-24">
                  <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true, margin: "-40px" }}
                    transition={{ delay: index * 0.07, duration: 0.45 }}
                    className={`relative rounded-2xl border p-5 transition-all ${
                      isCurrent
                        ? "border-[#4F8F57]/60 bg-surface-card shadow-[0_0_24px_rgba(79,143,87,0.15)]"
                        : isUnlocked
                        ? "border-[#4F8F57]/40 bg-white"
                        : "border-nature-leaf/20 bg-white/70"
                    } ${revealed ? "" : "journey-fog"}`}
                  >
                    {isCurrent && (
                      <div className="pulse-ring absolute inset-0 rounded-2xl text-nature-blossom" />
                    )}

                    <div className="relative flex items-center gap-4">
                      <div className={`relative text-5xl ${revealed ? "" : "opacity-50 grayscale"}`}>
                        {region.emoji}
                      </div>

                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2">
                          <h3 className={`font-semibold text-lg ${revealed ? "text-text-primary" : "text-text-muted"}`}>
                            {region.name}
                          </h3>
                          <span className="text-[10px] font-mono uppercase tracking-wider text-text-muted">
                            R{region.order}
                          </span>
                        </div>

                        {isLocked ? (
                          <div className="flex items-center gap-1.5 mt-1 text-xs text-text-muted font-mono">
                            <Lock size={12} />
                            {region.xp_required.toLocaleString()} XP required
                          </div>
                        ) : regionDone ? (
                          <div className="flex items-center gap-1.5 mt-1 text-xs text-nature-blossom font-mono">
                            <Check size={12} />
                            Region complete
                          </div>
                        ) : (
                          <div className="flex items-center gap-1.5 mt-1 text-xs text-nature-blossom/80 font-mono">
                            <MapPin size={12} />
                            {isCurrent ? "Current position" : "Unlocked"}
                          </div>
                        )}

                        {isUnlocked && (
                          <div className="flex items-center gap-2 mt-2">
                            {region.buildings.map((b) => (
                              <span
                                key={b}
                                title={BUILDING_META[b]?.label}
                                className={`text-base ${isCurrent ? "" : "opacity-60"}`}
                              >
                                {BUILDING_META[b]?.icon}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>

                      <div className="flex flex-col items-end gap-2">
                        {regionDone ? (
                          <span className="flex items-center gap-1 text-xs font-semibold text-nature-blossom bg-nature-bark border border-nature-leaf/30 rounded-xl px-3 py-1.5">
                            <Check size={13} />
                            Done
                          </span>
                        ) : isLocked ? (
                          <span className="flex items-center gap-1 text-xs font-semibold text-text-muted bg-surface-card border border-nature-leaf/20 rounded-xl px-3 py-1.5">
                            <Lock size={13} />
                            Locked
                          </span>
                        ) : isCurrent ? (
                          <span className="flex items-center gap-1 text-xs font-semibold text-nature-blossom bg-surface-card border border-nature-leaf/30 rounded-xl px-3 py-1.5">
                            <MapPin size={13} />
                            Here
                          </span>
                        ) : (
                          <button
                            onClick={() => handleMove(region)}
                            disabled={moving === region.id}
                            className="flex items-center gap-1.5 px-4 py-2 rounded-xl text-sm font-semibold transition-all bg-gradient-to-r from-[#4F8F57] to-[#7BB661] text-white hover:opacity-90 shadow-[0_0_16px_rgba(79,143,87,0.3)] disabled:opacity-60"
                          >
                            {moving === region.id ? (
                              <span className="spinner-border spinner-border-sm" />
                            ) : (
                              <>
                                Enter
                                <ChevronRight size={14} />
                              </>
                            )}
                          </button>
                        )}
                      </div>
                    </div>

                    {isCurrent && (
                      <motion.div
                        layoutId="journey-hero"
                        style={{ x: "-50%" }}
                        className="absolute -top-10 left-1/2 z-10 text-4xl"
                        transition={{ type: "spring", stiffness: 260, damping: 20 }}
                        animate={heroHop ? { y: [0, -18, 0], scale: [1, 1.15, 1] } : { y: 0, scale: 1 }}
                      >
                        <span className="drop-shadow-[0_0_14px_rgba(79,143,87,0.6)]">🧙</span>
                      </motion.div>
                    )}
                  </motion.div>
                </div>

                {index < regions.length - 1 && (
                  <div className="w-px h-10 bg-gradient-to-b from-[#7BB661]/50 to-[#B8D9A8]/50" />
                )}
              </div>
            );
          })}
        </div>

        {current && (
          <>
            <motion.section
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="rounded-2xl border border-nature-leaf/20 bg-white p-5 mt-10"
            >
              <h4 className="flex items-center gap-2 text-sm font-semibold text-text-primary mb-4">
                <Trophy size={15} className="text-amber-400" />
                {current.emoji} {current.name} Buildings
              </h4>
              <div className="flex flex-wrap gap-3">
                {current.buildings.map((b) => {
                  const meta = BUILDING_META[b];
                  return (
                    <div
                      key={b}
                      className="flex items-center gap-2 rounded-xl border border-nature-leaf/30 bg-surface-card px-3 py-2"
                    >
                      <span className="text-xl">{meta?.icon}</span>
                      <span className="text-xs font-semibold text-nature-blossom">{meta?.label}</span>
                    </div>
                  );
                })}
              </div>
            </motion.section>

            <motion.section
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="rounded-2xl border border-nature-leaf/20 bg-white p-5 mt-4 mb-6"
            >
              <div className="flex items-center justify-between mb-4">
                <h4 className="flex items-center gap-2 text-sm font-semibold text-text-primary">
                  <Sparkles size={15} className="text-nature-blossom" />
                  Region Quests
                </h4>
                <span className="text-xs font-mono text-text-muted">
                  {Number(completedSet.has(`${current.id}:0`)) +
                    Number(completedSet.has(`${current.id}:1`)) +
                    Number(completedSet.has(`${current.id}:2`))}
                  /3
                </span>
              </div>
              <div className="flex flex-col gap-2.5">
                {quests.map((quest, idx) => {
                  const done = completedSet.has(`${current.id}:${idx}`);
                  return (
                    <div
                      key={idx}
                      className={`flex items-center justify-between gap-3 rounded-xl border px-4 py-3 transition-all ${
                        done
                          ? "border-nature-leaf/30 bg-[#F0F7EC]"
                          : "border-nature-leaf/20 bg-surface-base"
                      }`}
                    >
                      <div className="flex items-center gap-3 min-w-0">
                        {done ? (
                          <span className="w-6 h-6 flex items-center justify-center rounded-full bg-nature-bark text-nature-blossom">
                            <Check size={14} />
                          </span>
                        ) : (
                          <span className="w-6 h-6 flex items-center justify-center rounded-full bg-[#E5E0D3] text-nature-blossom">
                            <Sparkles size={13} />
                          </span>
                        )}
                        <span className={`text-sm ${done ? "text-nature-blossom line-through" : "text-text-secondary"}`}>
                          {quest}
                        </span>
                      </div>
                      {done ? (
                        <span className="text-xs font-mono text-nature-blossom whitespace-nowrap">
                          Completed
                        </span>
                      ) : (
                        <button
                          onClick={() => handleComplete(idx)}
                          disabled={busyQuest === idx}
                          className="flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-semibold bg-gradient-to-r from-[#4F8F57] to-[#7BB661] text-white hover:opacity-90 disabled:opacity-60 whitespace-nowrap"
                        >
                          {busyQuest === idx ? (
                            <span className="spinner-border spinner-border-sm" />
                          ) : (
                            "Complete"
                          )}
                        </button>
                      )}
                    </div>
                  );
                })}
              </div>
            </motion.section>
          </>
        )}
      </div>

      <AnimatePresence>
        {flash && (
          <motion.div
            className="fixed inset-0 z-50 flex items-center justify-center pointer-events-none"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <div className="absolute inset-0 bg-gradient-to-b from-[#7BB661]/20 via-transparent to-[#B8D9A8]/20" />
            <motion.div
              initial={{ scale: 0.2, opacity: 0, rotate: -12 }}
              animate={{ scale: 1, opacity: 1, rotate: 0 }}
              exit={{ scale: 1.8, opacity: 0 }}
              transition={{ type: "spring", stiffness: 260, damping: 18 }}
              className="relative text-center rounded-3xl border border-nature-leaf/20 bg-white px-10 py-8 shadow-[0_0_60px_rgba(79,143,87,0.25)]"
            >
              <div className="text-6xl mb-3">✨</div>
              <div className="text-text-primary font-bold text-lg">{flash.quest}</div>
              {flash.xp > 0 && (
                <div className="mt-1 text-nature-blossom font-mono font-semibold">+{flash.xp} XP</div>
              )}
              {flash.fog && (
                <div className="mt-2 flex items-center justify-center gap-2 text-sm text-nature-blossom font-mono">
                  <Lock size={13} />
                  Fog cleared — {flash.fogRegion} revealed
                </div>
              )}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
