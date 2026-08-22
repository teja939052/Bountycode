import { useState, useEffect, useRef, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { luckyWheelApi } from "../services/api/luckyWheel.ts";

const FALLBACK_REWARDS = [
  { id: "xp_100", label: "100 XP", emoji: "✨", weight: 30 },
  { id: "coins_50", label: "50 Coins", emoji: "🪙", weight: 25 },
  { id: "xp_200", label: "200 XP", emoji: "⚡", weight: 15 },
  { id: "rare_card", label: "Rare Card", emoji: "🃏", weight: 10 },
  { id: "double_xp", label: "Double XP (24h)", emoji: "🔥", weight: 8 },
  { id: "merchant_ticket", label: "Merchant Ticket", emoji: "🎫", weight: 7 },
  { id: "epic_chest", label: "Epic Chest", emoji: "🧰", weight: 3 },
  { id: "legendary_skin", label: "Legendary Skin", emoji: "👑", weight: 2 },
];

const SEGMENT_COLORS = ["#10b981", "#334155", "#059669", "#1e293b", "#0d9488", "#475569", "#047857", "#1e293b"];

const WHEEL_SIZE = 320;

function fmtCountdown(totalSeconds) {
  const h = Math.floor(totalSeconds / 3600);
  const m = Math.floor((totalSeconds % 3600) / 60);
  const s = totalSeconds % 60;
  return h + "h " + m.toString().padStart(2, "0") + "m " + s.toString().padStart(2, "0") + "s";
}

export default function LuckyWheel() {
  const [rewards, setRewards] = useState(FALLBACK_REWARDS);
  const [canSpin, setCanSpin] = useState(true);
  const [lastReward, setLastReward] = useState(null);
  const [remaining, setRemaining] = useState(0);
  const [stats, setStats] = useState({ total_spins: 0, best_reward: null, reward_counts: {} });
  const [spinning, setSpinning] = useState(false);
  const [rotation, setRotation] = useState(0);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const timerRef = useRef(null);

  const loadAll = useCallback(async () => {
    try {
      const [state, st] = await Promise.all([luckyWheelApi.state(), luckyWheelApi.stats()]);
      if (state.rewards && state.rewards.length === 8) setRewards(state.rewards);
      setCanSpin(state.can_spin);
      setLastReward(state.last_reward);
      setRemaining(state.remaining_in_24h_seconds || 0);
      setStats(st);
    } catch (e) {
      setError(e.message || "Could not load wheel state");
    }
  }, []);

  useEffect(() => {
    loadAll();
  }, [loadAll]);

  useEffect(() => {
    if (!canSpin && remaining > 0) {
      timerRef.current = setInterval(() => {
        setRemaining((r) => Math.max(0, r - 1));
      }, 1000);
      return () => clearInterval(timerRef.current);
    }
  }, [canSpin, remaining > 0]);

  const gradient = rewards
    .map((r, i) => SEGMENT_COLORS[i % SEGMENT_COLORS.length] + " " + i * 45 + "deg " + (i + 1) * 45 + "deg")
    .join(", ");

  const spin = async () => {
    if (!canSpin || spinning) return;
    setSpinning(true);
    setError("");
    setResult(null);
    try {
      const res = await luckyWheelApi.spin();
      const idx = rewards.findIndex((r) => r.label === res.reward);
      const target = 360 * 5 - (idx >= 0 ? idx * 45 + 22.5 : 0);
      setRotation((prev) => prev + (target - (prev % 360)) + 360 * 5);
      setTimeout(() => {
        setResult({ reward: res.reward, message: res.message });
        setCanSpin(false);
        setLastReward(res.reward);
        luckyWheelApi.stats().then((s) => setStats(s)).catch(() => {});
      }, 3200);
    } catch (e) {
      if (e.status === 429) {
        setCanSpin(false);
        setError(e.message || "Come back tomorrow — wheel resets daily");
      } else {
        setError(e.message || "Spin failed. Try again.");
      }
    } finally {
      setSpinning(false);
    }
  };

  return (
    <div className="min-h-screen bg-surface-base text-text-primary px-4 py-8">
      <div className="max-w-5xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold">{"🎡 Daily Lucky Wheel"}</h1>
          <p className="text-text-muted mt-2">
            One free spin every day. Stack XP, coins, cards and rare loot.
          </p>
        </div>

        {error && (
          <p className="text-center text-amber-400 text-sm mb-4 bg-amber-500/10 border border-amber-500/30 rounded-lg py-2 px-4 max-w-md mx-auto">
            {error}
          </p>
        )}

        <div className="grid md:grid-cols-5 gap-8 items-start">
          {/* Wheel */}
          <div className="md:col-span-3 flex flex-col items-center">
            <div className="relative" style={{ width: WHEEL_SIZE, height: WHEEL_SIZE }}>
              {/* Pointer */}
              <div className="absolute left-1/2 -translate-x-1/2 -top-3 z-20">
                <div className="w-0 h-0 border-l-[14px] border-r-[14px] border-t-[24px] border-l-transparent border-r-transparent border-t-amber-400 drop-shadow-lg" />
              </div>

              {/* Rotating wheel */}
              <div
                className="absolute inset-0 rounded-full border-[6px] border-nature-leaf/20 shadow-[0_0_40px_rgba(79,143,87,0.25)]"
                style={{
                  background: "conic-gradient(from 0deg, " + gradient + ")",
                  transition: spinning ? "transform 3.2s cubic-bezier(0.16, 1, 0.3, 1)" : "none",
                  transform: "rotate(" + rotation + "deg)",
                }}
              >
                {rewards.map((r, i) => (
                  <div
                    key={r.id}
                    className="absolute inset-0 flex items-center justify-center"
                    style={{ transform: "rotate(" + i * 45 + "deg)" }}
                  >
                    <div
                      className="text-center"
                      style={{ transform: "translateY(" + -WHEEL_SIZE * 0.36 + "px)" }}
                    >
                      <span className="block text-xl leading-tight drop-shadow">{r.emoji}</span>
                      <span className="block text-[9px] font-semibold text-white/95 leading-tight px-1">
                        {r.label}
                      </span>
                    </div>
                  </div>
                ))}

                {/* Hub + spin button */}
                <div className="absolute inset-0 flex items-center justify-center">
                  <button
                    onClick={spin}
                    disabled={!canSpin || spinning}
                    className={"w-24 h-24 rounded-full flex items-center justify-center text-sm font-bold tracking-wide shadow-xl transition border-4 " + (canSpin && !spinning ? "bg-emerald-500 hover:bg-emerald-400 text-emerald-950 border-white/20 animate-pulse" : "bg-[#E5E0D3] text-text-muted border-nature-leaf/30 cursor-not-allowed")}
                  >
                    {spinning ? "Spinning..." : canSpin ? "SPIN" : "Done"}
                  </button>
                </div>
              </div>
            </div>

            {/* Spin status */}
            <div className="mt-8 text-center">
              <p className="text-sm font-semibold">
                Spins today: <span className="text-nature-blossom">{canSpin ? "1/1" : "0/1"}</span>
              </p>
              {!canSpin && remaining > 0 && (
                <p className="text-text-muted text-sm mt-1">
                  {"Come back tomorrow — wheel resets daily · "}
                  <span className="text-amber-600 font-mono">{fmtCountdown(remaining)}</span>
                </p>
              )}
              {!canSpin && remaining === 0 && (
                <p className="text-text-muted text-sm mt-1">{"Come back tomorrow — wheel resets daily"}</p>
              )}
              {lastReward && (
                <p className="text-text-muted text-sm mt-1">Last reward: {lastReward}</p>
              )}
            </div>
          </div>

          {/* Reward legend + stats */}
          <div className="md:col-span-2 space-y-6">
            <div className="bg-white border border-nature-leaf/20 rounded-2xl p-5">
              <h2 className="text-sm font-bold text-text-secondary uppercase tracking-wider mb-3">
                Rewards
              </h2>
              <ul className="space-y-2">
                {rewards.map((r) => (
                  <li key={r.id} className="flex items-center justify-between text-sm">
                    <span className="flex items-center gap-2">
                      <span>{r.emoji}</span>
                      <span className="text-text-secondary">{r.label}</span>
                    </span>
                    <span className="text-text-muted text-xs">{r.weight}%</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="bg-white border border-nature-leaf/20 rounded-2xl p-5">
              <h2 className="text-sm font-bold text-text-secondary uppercase tracking-wider mb-3">
                Your Stats
              </h2>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-surface-card rounded-xl p-3 text-center">
                  <p className="text-2xl font-bold text-nature-blossom">{stats.total_spins}</p>
                  <p className="text-xs text-text-muted">Total spins</p>
                </div>
                <div className="bg-surface-card rounded-xl p-3 text-center">
                  <p className="text-2xl font-bold text-amber-600 truncate">
                    {stats.best_reward ? stats.best_reward.replace(" (24h)", "") : "—"}
                  </p>
                  <p className="text-xs text-text-muted">Best reward</p>
                </div>
              </div>
              {stats.total_spins > 0 && Object.keys(stats.reward_counts || {}).length > 0 && (
                <ul className="mt-4 space-y-1.5">
                  {(Object.entries(stats.reward_counts) as [string, number][])
                    .sort((a, b) => b[1] - a[1])
                    .map(([label, count]) => (
                      <li key={label} className="flex justify-between text-sm">
                        <span className="text-text-secondary">{label}</span>
                        <span className="text-text-muted">{count}{"×"}</span>
                      </li>
                    ))}
                </ul>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Result celebration */}
      <AnimatePresence>
        {result && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm"
            onClick={() => setResult(null)}
          >
            <motion.div
              initial={{ scale: 0.5, y: 40 }}
              animate={{ scale: 1, y: 0 }}
              transition={{ type: "spring", damping: 12 }}
              className="bg-white border border-nature-leaf/30 rounded-3xl p-10 text-center max-w-sm w-full mx-4 shadow-[0_0_60px_rgba(79,143,87,0.25)]"
              onClick={(e) => e.stopPropagation()}
            >
              <motion.div
                animate={{ scale: [1, 1.35, 1], rotate: [0, -8, 8, 0] }}
                transition={{ duration: 0.8, repeat: 2 }}
                className="text-6xl mb-4"
              >
                {rewards.find((r) => r.label === result.reward)?.emoji || "🎉"}
              </motion.div>
              {["✨", "🎊", "🎉", "💫"].map((s, i) => (
                <motion.span
                  key={i}
                  className="absolute text-2xl"
                  style={{ left: 20 + i * 18 + "%", top: "12%" }}
                  initial={{ y: 0, opacity: 1 }}
                  animate={{ y: -90, opacity: 0 }}
                  transition={{ duration: 1.1, repeat: Infinity, delay: i * 0.15 }}
                >
                  {s}
                </motion.span>
              ))}
              <h3 className="text-2xl font-bold text-nature-blossom mb-2">You won!</h3>
              <p className="text-lg font-semibold text-text-primary">{result.reward}</p>
              <p className="text-text-muted text-sm mt-2">{result.message}</p>
              <button
                onClick={() => setResult(null)}
                className="mt-6 w-full bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded-xl py-3 transition"
              >
                Awesome
              </button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
