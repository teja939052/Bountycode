import { useState, useEffect } from "react";
import api from "../services/api";
import { useJuice } from "../juice/JuiceProvider";

export default function ReferralGamification() {
  const { showXP, play } = useJuice();
  const [referralStatus, setReferralStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const data = await api.referrals?.getStatus?.() || {};
      setReferralStatus(data);
    } catch {
      setReferralStatus(null);
    } finally {
      setLoading(false);
    }
  };

  const handleCopyCode = () => {
    const code = referralStatus?.referral_code || "";
    navigator.clipboard.writeText(code).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  const handleClaimBonus = async () => {
    setLoading(true);
    try {
      const data = await api.referrals?.claimBonus?.() || {};
      setMessage(`🎉 Claimed ${data.bonus_xp} XP bonus! Badge: ${data.badge}`);
      play("levelUp");
      showXP(data.bonus_xp || 0, window.innerWidth / 2, window.innerHeight / 2);
      await loadData();
    } catch (err) {
      setMessage(err.message || "Failed to claim bonus");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-gray-400 text-lg">Loading referrals...</div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">🎁 Referral Gamification</h1>

      {message && (
        <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm">
          {message}
        </div>
      )}

      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl p-6 text-white">
        <h2 className="text-xl font-bold mb-2">Invite Friends, Earn XP!</h2>
        <p className="text-indigo-100 mb-4">
          Share your referral code and earn {referralStatus?.rewards?.referral_bonus_xp || 100} XP for each friend who joins.
          Unlock bonus tiers for even more rewards!
        </p>
        <div className="flex items-center gap-3">
          <div className="bg-white/20 rounded-lg px-4 py-2 font-mono text-lg">
            {referralStatus?.referral_code || "PP------"}
          </div>
          <button
            onClick={handleCopyCode}
            className="px-4 py-2 bg-white/20 text-white rounded-lg text-sm font-medium hover:bg-white/30"
          >
            {copied ? "✓ Copied!" : "Copy Code"}
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white border border-gray-200 rounded-xl p-5 text-center">
          <div className="text-3xl mb-2">👥</div>
          <div className="text-2xl font-bold text-indigo-600">{referralStatus?.total_referrals || 0}</div>
          <div className="text-sm text-gray-500">Total Referrals</div>
        </div>
        <div className="bg-white border border-gray-200 rounded-xl p-5 text-center">
          <div className="text-3xl mb-2">⭐</div>
          <div className="text-2xl font-bold text-amber-600">{referralStatus?.total_xp_earned || 0}</div>
          <div className="text-sm text-gray-500">XP Earned</div>
        </div>
        <div className="bg-white border border-gray-200 rounded-xl p-5 text-center">
          <div className="text-3xl mb-2">🏆</div>
          <div className="text-2xl font-bold text-green-600">{referralStatus?.tier || "none"}</div>
          <div className="text-sm text-gray-500">Current Tier</div>
        </div>
      </div>

      <div className="space-y-4">
        <h2 className="text-lg font-semibold">Referral Tiers</h2>
        {[
          { tier: "tier_1", min: 3, xp: 200, badge: "🦋 Social Butterfly", color: "green" },
          { tier: "tier_2", min: 5, xp: 500, badge: "🌟 Community Leader", color: "blue" },
          { tier: "tier_3", min: 10, xp: 1000, badge: "👑 Referral King", color: "amber" },
        ].map((t) => {
          const isUnlocked = referralStatus?.total_referrals >= t.min;
          const isClaimed = referralStatus?.referral_bonus_claimed?.includes(t.tier);
          return (
            <div
              key={t.tier}
              className={`bg-white border rounded-xl p-4 flex items-center justify-between ${isUnlocked ? "border-green-300" : "border-gray-200 opacity-60"}`}
            >
              <div className="flex items-center gap-3">
                <span className="text-2xl">{isUnlocked ? "✅" : "🔒"}</span>
                <div>
                  <div className="font-semibold">{t.badge}</div>
                  <div className="text-xs text-gray-500">Refer {t.min}+ friends</div>
                </div>
              </div>
              <div className="text-right">
                <div className="font-semibold text-indigo-600">+{t.xp} XP</div>
                {isUnlocked && !isClaimed ? (
                  <button
                    onClick={handleClaimBonus}
                    disabled={loading}
                    className="mt-1 px-3 py-1 bg-green-600 text-white rounded-lg text-xs font-medium hover:bg-green-700"
                  >
                    Claim
                  </button>
                ) : isClaimed ? (
                  <span className="text-xs text-green-600">Claimed ✓</span>
                ) : null}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}