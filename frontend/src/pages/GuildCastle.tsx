import { useState, useEffect, useCallback } from "react";
import { useParams } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { guildCastleApi } from "../services/api/guildCastle.ts";
import useAuthStore from "../store/authStore";
import { Shield, Sword, Coins, Gem, Zap, Crown, Users, ArrowLeft, ArrowRight, RefreshCw } from "lucide-react";

const ZONE_ICONS = {
  outer_wall: "🧱",
  inner_keep: "🏰",
  treasure_vault: "💎",
};

const ZONE_COLORS = {
  outer_wall: "border-amber-500 bg-amber-500/10",
  inner_keep: "border-nature-leaf/30 bg-surface-card",
  treasure_vault: "border-nature-leaf/30 bg-nature-bark",
};

const CASTLE_ZONES = ["outer_wall", "inner_keep", "treasure_vault"];

const ZONE_HP: Record<string, number> = {
  outer_wall: 1000,
  inner_keep: 750,
  treasure_vault: 500,
};

const ZONE_DEFENSE: Record<string, number> = {
  outer_wall: 20,
  inner_keep: 35,
  treasure_vault: 50,
};

const UPGRADES = [
  { name: "Reinforced Walls", effect: "Reduces incoming damage by 15%", cost: 1000, icon: "🧱" },
  { name: "Sharpened Blades", effect: "Increases damage dealt by 20%", cost: 800, icon: "⚔️" },
  { name: "Treasure Guard", effect: "Boosts vault HP by 30%", cost: 1200, icon: "💎" },
  { name: "Rapid Repairs", effect: "HP regenerates 5/turn", cost: 900, icon: "🔧" },
];

export default function GuildCastle() {
  const { guildId } = useParams();
  const user = useAuthStore((s) => s.user);
  const [castle, setCastle] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [action, setAction] = useState(null);
  const [actionMsg, setActionMsg] = useState("");
  const [activeZone, setActiveZone] = useState("outer_wall");

  const loadCastle = useCallback(async () => {
    if (!guildId) return;
    try {
      const c = await guildCastleApi.get(guildId);
      setCastle(c);
    } catch (e) {
      setError(e.message || "Could not load castle");
    } finally {
      setLoading(false);
    }
  }, [guildId]);

  useEffect(() => {
    loadCastle();
  }, [loadCastle]);

  const handleDefend = async (zone) => {
    setAction("defending");
    setError("");
    try {
      const res = await guildCastleApi.defend(guildId, zone);
      setActionMsg(res.message);
      setCastle((prev) => prev ? {
        ...prev,
        zones: { ...prev.zones, [zone]: { ...prev.zones[zone], hp: res.hp_remaining } },
      } : prev);
      setTimeout(() => setActionMsg(""), 3000);
    } catch (e) {
      setError(e.message || "Defend failed");
    } finally {
      setAction(null);
    }
  };

  const handleAttack = async (zone) => {
    setAction("attacking");
    setError("");
    try {
      const res = await guildCastleApi.attack(guildId, zone);
      setActionMsg(res.message);
      setCastle((prev) => prev ? {
        ...prev,
        zones: { ...prev.zones, [zone]: { ...prev.zones[zone], hp: res.hp_remaining } },
      } : prev);
      setTimeout(() => setActionMsg(""), 3000);
    } catch (e) {
      setError(e.message || "Attack failed");
    } finally {
      setAction(null);
    }
  };

  const handleUpgrade = async (upgradeId) => {
    setAction("upgrading");
    setError("");
    try {
      const res = await guildCastleApi.upgrade(guildId, upgradeId);
      setActionMsg(res.message);
      setTimeout(() => setActionMsg(""), 3000);
    } catch (e) {
      setError(e.message || "Upgrade failed");
    } finally {
      setAction(null);
    }
  };

  const handleDailyBonus = async () => {
    setAction("claiming");
    try {
      const res = await guildCastleApi.dailyBonus(guildId);
      setActionMsg(res.message);
      setTimeout(() => setActionMsg(""), 3000);
    } catch (e) {
      setError(e.message || "Bonus claim failed");
    } finally {
      setAction(null);
    }
  };

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-surface-base text-text-primary">
        <div className="animate-pulse text-nature-blossom">Loading Castle...</div>
      </div>
    );
  }

  if (!castle) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-surface-base text-text-primary">
        <p className="text-text-muted">No castle found for this guild.</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-surface-base text-text-primary px-4 py-8">
      <div className="max-w-5xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold">🏰 Guild Castle</h1>
          <p className="text-text-muted mt-2">
            Defend your guild's castle. Attack rivals. Earn rewards.
          </p>
          {castle && (
            <p className="text-sm text-nature-blossom mt-1">
              Guild: {castle.guild_name || guildId}
            </p>
          )}
        </div>

        {error && (
          <p className="text-center text-amber-400 text-sm mb-4 bg-amber-500/10 border border-amber-500/30 rounded-lg py-2 px-4 max-w-md mx-auto">
            {error}
          </p>
        )}

        {actionMsg && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-4 bg-green-500/10 border border-green-500/30 rounded-lg py-2 text-green-700 text-sm"
          >
            {actionMsg}
          </motion.div>
        )}

        {/* Castle Zones */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          {CASTLE_ZONES.map((zone) => {
            const zoneData = castle.zones?.[zone] || {};
            const hp = zoneData.hp || 0;
            const maxHp = zoneData.max_hp || ZONE_HP[zone];
            const defense = zoneData.defense || ZONE_DEFENSE[zone];
            const hpPercent = (hp / maxHp) * 100;
            const isCritical = hpPercent < 30;

            return (
              <motion.div
                key={zone}
                className={`rounded-2xl border-2 p-5 ${ZONE_COLORS[zone]} ${isCritical ? 'animate-pulse border-red-500' : ''}`}
              >
                <div className="text-3xl mb-2">{ZONE_ICONS[zone]}</div>
                <h3 className="font-bold text-text-primary capitalize">
                  {zone.replace('_', ' ')}
                </h3>
                <div className="mt-3 mb-2">
                  <div className="flex justify-between text-xs mb-1">
                    <span className="text-text-muted">HP</span>
                    <span className={isCritical ? "text-red-400" : "text-text-secondary"}>
                      {hp} / {maxHp}
                    </span>
                  </div>
                  <div className="h-2 bg-[#E5E0D3] rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full transition-all ${
                        isCritical ? 'bg-red-500' : hpPercent > 50 ? 'bg-green-500' : 'bg-amber-500'
                      }`}
                      style={{ width: `${hpPercent}%` }}
                    />
                  </div>
                </div>
                <p className="text-xs text-text-muted mb-3">Defense: {defense}</p>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleDefend(zone)}
                    disabled={action === "defending"}
                    className="flex-1 rounded-lg bg-nature-leaf px-3 py-2 text-xs font-bold text-white hover:bg-nature-moss disabled:opacity-50"
                  >
                    {action === "defending" ? "..." : "🛡️ Defend"}
                  </button>
                  <button
                    onClick={() => handleAttack(zone)}
                    disabled={action === "attacking"}
                    className="flex-1 rounded-lg bg-rose-600 px-3 py-2 text-xs font-bold text-white hover:bg-rose-500 disabled:opacity-50"
                  >
                    {action === "attacking" ? "..." : "⚔️ Attack"}
                  </button>
                </div>
              </motion.div>
            );
          })}
        </div>

        {/* Upgrades */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8 bg-white border border-nature-leaf/20 rounded-2xl p-6"
        >
          <h2 className="text-xl font-bold text-text-primary mb-4 flex items-center gap-2">
            <Crown className="h-5 w-5 text-amber-400" />
            Castle Upgrades
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {UPGRADES.map((upgrade, idx) => {
              const id = upgrade.name;
              const level = castle?.upgrades?.[id] || 0;
              const canAfford = castle?.resources?.coins >= upgrade.cost;
              return (
                <div
                  key={id}
                  className="rounded-xl border border-nature-leaf/20 bg-surface-card p-4"
                >
                  <h3 className="font-bold text-text-primary">{upgrade.name}</h3>
                  <p className="text-sm text-text-muted mt-1">{upgrade.effect}</p>
                  <div className="flex items-center justify-between mt-3">
                    <span className="text-xs text-text-muted">Level {level}</span>
                    <button
                      onClick={() => handleUpgrade(id)}
                      disabled={!canAfford || action === "upgrading"}
                      className="rounded-lg bg-amber-600 px-3 py-1 text-xs font-bold text-white hover:bg-amber-500 disabled:opacity-50"
                    >
                      {action === "upgrading" ? "..." : `${upgrade.cost} 🪙`}
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </motion.div>

        {/* Daily Bonus */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8 bg-gradient-to-r from-[#EDF5E6] to-[#D9EFCF] border border-nature-leaf/30 rounded-2xl p-6 text-center"
        >
          <h2 className="text-xl font-bold text-nature-blossom mb-2">Daily Castle Bonus</h2>
          <p className="text-sm text-text-muted mb-4">+30 XP, +15 coins daily for castle activity</p>
          <button
            onClick={handleDailyBonus}
            disabled={action === "claiming"}
            className="rounded-xl bg-green-600 px-6 py-3 font-bold text-white hover:bg-green-500 disabled:opacity-50"
          >
            {action === "claiming" ? "Claiming..." : "Claim Daily Bonus"}
          </button>
        </motion.div>

        {/* Guild Resources */}
        <div className="flex justify-center gap-6 mb-8">
          <div className="text-center">
            <div className="text-2xl font-bold text-amber-400">{castle.resources?.coins || 0}</div>
            <div className="text-xs text-text-muted">Guild Coins</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-nature-blossom">{castle.resources?.gems || 0}</div>
            <div className="text-xs text-text-muted">Guild Gems</div>
          </div>
        </div>
      </div>
    </div>
  );
}
