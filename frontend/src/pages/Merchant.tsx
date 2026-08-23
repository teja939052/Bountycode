import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { merchantApi } from "../services/api/merchant.ts";
import useTrack from "../hooks/useTrack";
import {
  Coins, Crown, Sparkles, RefreshCcw, Gift, X, Check, Zap, Flame, Gem, ShoppingBag,
} from "lucide-react";

const TYPE_LABELS = {
  card: "Collectible Card",
  xp_potion: "XP Potion",
  double_xp_token: "Double XP Token",
  avatar: "Avatar",
  border: "Profile Border",
};

const TYPE_STYLES = {
  card: "border-nature-leaf/30 bg-surface-card text-nature-blossom",
  xp_potion: "border-nature-leaf/30 bg-nature-bark text-nature-blossom",
  double_xp_token: "border-amber-500/30 bg-amber-500/10 text-amber-400",
  avatar: "border-nature-leaf/30 bg-surface-card text-nature-blossom",
  border: "border-nature-leaf/30 bg-surface-card text-nature-blossom",
};

function formatMultiplier(value) {
  return value.toFixed(2).replace(/\.?0+$/, "");
}

export default function Merchant() {
  const track = useTrack();
  const [shop, setShop] = useState(null);
  const [prestige, setPrestige] = useState(null);
  const [loading, setLoading] = useState(true);
  const [buying, setBuying] = useState(null);
  const [confirmReset, setConfirmReset] = useState(false);
  const [prestiging, setPrestiging] = useState(false);
  const [toast, setToast] = useState("");

  useEffect(() => {
    Promise.all([merchantApi.getShop(), merchantApi.getPrestige()])
      .then(([shopData, prestigeData]) => {
        setShop(shopData);
        setPrestige(prestigeData);
      })
      .catch((err) => setToast(err.message || "Failed to load the merchant"))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    track("merchant", "open");
  }, [track]);

  useEffect(() => {
    if (!toast) return;
    const t = setTimeout(() => setToast(""), 3500);
    return () => clearTimeout(t);
  }, [toast]);

  const handleBuy = async (item) => {
    if (item.purchased || buying) return;
    setBuying(item.id);
    try {
      const res = await merchantApi.buyItem(item.id);
      track("merchant", "buy", item.price);
      setShop((prev) => ({
        ...prev,
        items: prev.items.map((i) => (i.id === item.id ? { ...i, purchased: true } : i)),
      }));
      if (res.xp_earned > 0) {
        setToast(`+${res.xp_earned} XP earned! Potion down the hatch.`);
      } else {
        setToast(`${item.emoji} ${item.name} added to your collection!`);
      }
    } catch (err) {
      setToast(err.message || "Purchase failed");
    } finally {
      setBuying(null);
    }
  };

  const handlePrestige = async () => {
    setPrestiging(true);
    try {
      const data = await merchantApi.prestige();
      track("prestige", "reset");
      setPrestige(data);
      setConfirmReset(false);
      setToast(`Prestige ${data.level} unlocked! ${data.perks.current.emote} ${data.perks.current.title}`);
    } catch (err) {
      setToast(err.message || "Prestige failed");
      setConfirmReset(false);
    } finally {
      setPrestiging(false);
    }
  };

  const level = prestige?.level ?? 0;
  const nextReq = prestige?.next_requirements;
  const currentPerk = prestige?.perks?.current;
  const nextPerk = prestige?.perks?.next;
  const bonus = prestige?.bonus_multiplier ?? 1;
  const threshold = nextReq?.xp_threshold || 0;
  const totalXp = prestige?.total_xp ?? 0;
  const progress = threshold > 0 ? Math.min(100, Math.round((totalXp / threshold) * 100)) : 100;

  if (loading) {
    return (
      <div className="min-h-screen bg-surface-base text-text-primary flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <Gift className="w-12 h-12 text-nature-blossom animate-bounce" />
          <p className="text-text-muted text-sm">Summoning the merchant...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-surface-base text-text-primary relative overflow-hidden">
      <div className="pointer-events-none absolute -top-32 left-1/2 -translate-x-1/2 w-[600px] h-[400px] rounded-full bg-nature-leaf/10 blur-[120px]" />
      <div className="pointer-events-none absolute bottom-0 right-0 w-[400px] h-[300px] rounded-full bg-[#7BB661]/10 blur-[120px]" />

      <div className="relative max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
          <div>
            <h1 className="text-3xl sm:text-4xl font-display font-bold text-text-primary flex items-center gap-3">
              <Gift className="w-9 h-9 text-nature-blossom" />
              Mystery Merchant
            </h1>
            <p className="text-text-muted mt-1">
              Daily rotating deals{shop?.date ? ` for ${shop.date}` : ""}. New stock every midnight.
            </p>
          </div>
          {shop && (
            <div className="flex items-center gap-2 px-4 py-2 rounded-xl border border-nature-leaf/30 bg-nature-bark self-start sm:self-auto">
              <Coins className="w-5 h-5 text-nature-blossom" />
              <span className="text-nature-blossom font-bold">{shop.coins}</span>
              <span className="text-emerald-500/80 text-xs">coins</span>
            </div>
          )}
        </div>

        <div className="mb-8 rounded-2xl border border-amber-500/30 bg-gradient-to-r from-amber-500/10 via-orange-500/10 to-rose-500/10 px-5 py-3 flex items-center gap-3">
          <Flame className="w-5 h-5 text-amber-400 shrink-0" />
          <p className="text-sm text-amber-600">
            <span className="font-semibold">Gone tomorrow.</span> The shop refreshes at midnight UTC —
            grab today's items before they vanish.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-12">
          {(shop?.items || []).map((item, idx) => (
            <motion.div
              key={item.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.08 }}
              className="relative rounded-2xl border border-nature-leaf/20 bg-white p-5 flex flex-col"
            >
              {item.discount_pct > 0 && (
                <span className="absolute -top-2.5 -right-2 px-2.5 py-1 rounded-lg bg-rose-500 text-text-primary text-[10px] font-bold shadow-lg shadow-rose-500/30">
                  {item.discount_pct}% OFF
                </span>
              )}
              <div className="w-16 h-16 rounded-2xl bg-surface-card border border-nature-leaf/20 flex items-center justify-center text-4xl mb-4">
                {item.emoji}
              </div>
              <h3 className="text-base font-semibold text-text-primary">{item.name}</h3>
              <span className={`mt-2 self-start px-2.5 py-0.5 rounded-full text-[10px] font-mono font-medium border ${TYPE_STYLES[item.type] || "border-nature-leaf/20 text-text-muted"}`}>
                {TYPE_LABELS[item.type] || item.type}
              </span>
              <div className="mt-4 flex items-center gap-2">
                <Coins className="w-4 h-4 text-amber-400" />
                <span className="text-xl font-bold text-amber-600">{item.price}</span>
                {item.discount_pct > 0 && (
                  <span className="text-xs text-text-muted line-through">{item.original_price}</span>
                )}
              </div>
              <button
                onClick={() => handleBuy(item)}
                disabled={item.purchased || !!buying}
                className={`mt-4 w-full flex items-center justify-center gap-2 rounded-xl py-2.5 text-sm font-semibold transition-all ${
                  item.purchased
                    ? "bg-[#E5E0D3] text-text-muted cursor-not-allowed"
                    : "bg-gradient-to-r from-[#4F8F57] to-[#7BB661] text-text-primary hover:opacity-90 disabled:opacity-50"
                }`}
              >
                {item.purchased ? (
                  <>
                    <Check className="w-4 h-4" /> Owned
                  </>
                ) : buying === item.id ? (
                  <>
                    <Zap className="w-4 h-4 animate-pulse" /> Buying...
                  </>
                ) : (
                  <>
                    <ShoppingBag className="w-4 h-4" /> Buy
                  </>
                )}
              </button>
            </motion.div>
          ))}
        </div>

        <motion.section
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="rounded-3xl border border-nature-leaf/20 bg-white p-6 sm:p-8"
        >
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 mb-6">
            <div className="flex items-center gap-4">
              <div
                className="w-16 h-16 rounded-2xl bg-gradient-to-br from-[#EDF5E6] to-[#D9EFCF] border border-nature-leaf/20 flex items-center justify-center text-3xl"
                style={currentPerk ? { borderColor: currentPerk.border, borderWidth: 2 } : undefined}
              >
                {currentPerk ? currentPerk.emote : <Crown className="w-8 h-8 text-nature-blossom" />}
              </div>
              <div>
                <h2 className="text-xl font-bold text-text-primary flex items-center gap-2">
                  <Sparkles className="w-5 h-5 text-nature-blossom" />
                  Prestige
                </h2>
                <p className="text-sm text-text-muted">
                  {level === 0
                    ? "Ascend through XP thresholds to earn permanent bonuses."
                    : `${currentPerk.title} — Prestige ${level}`}
                </p>
              </div>
            </div>
            <span className="self-start lg:self-auto px-3 py-1.5 rounded-xl border border-nature-leaf/30 bg-nature-bark text-nature-blossom text-sm font-bold">
              x{formatMultiplier(bonus)} XP bonus
            </span>
          </div>

          <div className="mb-6">
            <div className="flex items-center justify-between text-xs text-text-muted mb-2">
              <span>{level === 0 ? "Ascend to Prestige 1" : `Progress to Prestige ${nextReq?.level ?? level}`}</span>
              <span className="font-mono">
                {totalXp.toLocaleString()} / {(threshold || 1).toLocaleString()}
              </span>
            </div>
            <div className="h-3 rounded-full bg-[#E5E0D3] overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                transition={{ duration: 0.8, ease: "easeOut" }}
                className="h-full rounded-full bg-gradient-to-r from-[#4F8F57] to-[#7BB661]"
              />
            </div>
            {nextPerk ? (
              <p className="mt-3 text-xs text-text-muted">
                Next:{" "}
                <span className="text-text-secondary font-medium">
                  {nextPerk.emote} {nextPerk.title}
                </span>{" "}
                · x{formatMultiplier(nextPerk.bonus_multiplier)} XP ·{" "}
                <span className="font-medium" style={{ color: nextPerk.border }}>border</span>
              </p>
            ) : (
              <p className="mt-3 text-xs text-amber-400">Max prestige reached. Legendary status achieved.</p>
            )}
          </div>

          <div className="flex flex-col sm:flex-row sm:items-center gap-4">
            <button
              onClick={() => setConfirmReset(true)}
              disabled={!nextReq || prestiging}
              className="flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-[#4F8F57] to-[#7BB661] text-text-primary px-6 py-3 text-sm font-semibold hover:opacity-90 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
            >
              <RefreshCcw className={`w-4 h-4 ${prestiging ? "animate-spin" : ""}`} />
              {level === 0 ? "Start Prestige" : `Prestige to ${nextReq?.level ?? ""}`}
            </button>
            {nextReq && (
              <p className="text-xs text-text-muted">
                Requires{" "}
                <span className="text-text-secondary font-semibold">{nextReq.xp_threshold.toLocaleString()} XP</span>
                {prestige?.xp_needed > 0
                  ? ` — ${prestige.xp_needed.toLocaleString()} XP to go`
                  : " — you're ready!"}
              </p>
            )}
          </div>
        </motion.section>
      </div>

      <AnimatePresence>
        {confirmReset && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-surface-2 backdrop-blur-sm px-4"
            onClick={() => setConfirmReset(false)}
          >
            <motion.div
              initial={{ scale: 0.9, y: 20 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.9, y: 20 }}
              className="w-full max-w-md rounded-3xl border border-nature-leaf/20 bg-white p-6"
              onClick={(e) => e.stopPropagation()}
            >
              <h3 className="text-lg font-bold text-text-primary flex items-center gap-2">
                <Gem className="w-5 h-5 text-nature-blossom" />
                Prestige to Level {nextReq?.level}?
              </h3>
              <p className="mt-3 text-sm text-text-muted leading-relaxed">
                Your XP stays fully intact. You'll unlock the{" "}
                <span className="text-text-primary">{nextPerk?.title}</span> title, a permanent{" "}
                <span className="text-nature-blossom">x{formatMultiplier(nextPerk?.bonus_multiplier ?? 1)} XP bonus</span>,
                and the exclusive {nextPerk?.emote} border.
              </p>
              <div className="mt-6 flex gap-3 justify-end">
                <button
                  onClick={() => setConfirmReset(false)}
                  className="rounded-xl border border-nature-leaf/20 bg-surface-card px-5 py-2.5 text-sm text-text-secondary hover:bg-[#EDEAE0] transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={handlePrestige}
                  disabled={prestiging}
                  className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-[#4F8F57] to-[#7BB661] px-5 py-2.5 text-sm font-semibold text-text-primary hover:opacity-90 disabled:opacity-50 transition-all"
                >
                  {prestiging ? (
                    <>
                      <RefreshCcw className="w-4 h-4 animate-spin" /> Ascending...
                    </>
                  ) : (
                    <>
                      <Crown className="w-4 h-4" /> Ascend
                    </>
                  )}
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {toast && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            className="fixed bottom-6 inset-x-0 mx-auto z-50 w-fit max-w-[90vw] rounded-xl border border-nature-leaf/20 bg-white px-5 py-3 text-sm text-text-primary shadow-xl text-center"
          >
            {toast}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
