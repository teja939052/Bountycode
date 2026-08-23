import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { referralSystemApi } from "../services/api/referralSystem.ts";
import useAuthStore from "../store/authStore";
import { Share2, Copy, Users, Gift, Trophy, Link2, CheckCircle } from "lucide-react";

export default function Referral() {
  const user = useAuthStore((s) => s.user);
  const [referralData, setReferralData] = useState(null);
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);
  const [processing, setProcessing] = useState(false);

  const loadData = useCallback(async () => {
    try {
      const [refData, lb] = await Promise.all([
        referralSystemApi.generateCode(),
        referralSystemApi.leaderboard(10),
      ]);
      setReferralData(refData);
      setLeaderboard(lb.leaderboard || []);
    } catch (e) {
      setError(e.message || "Could not load referral data");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const copyCode = async () => {
    if (referralData?.referral_url) {
      await navigator.clipboard.writeText(referralData.referral_url);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const shareInvite = () => {
    if (referralData?.referral_url) {
      if (navigator.share) {
        navigator.share({
          title: "Join PlacementPro — Free Placement Prep",
          text: "Use my referral code to get 50 bonus XP + 25 coins!",
          url: referralData.referral_url,
        }).catch(() => {});
      } else {
        copyCode();
      }
    }
  };

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-surface-base text-text-primary">
        <div className="animate-pulse text-nature-blossom">Loading referrals...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-surface-base text-text-primary px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold">🎁 Referral System</h1>
          <p className="text-text-muted mt-2">
            Invite friends, earn XP and coins. Both you and your friend win!
          </p>
        </div>

        {error && (
          <p className="text-center text-amber-400 text-sm mb-4">{error}</p>
        )}

        {/* Your Referral Code */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8 bg-gradient-to-r from-[#EDF5E6] to-[#D9EFCF] border border-nature-leaf/30 rounded-2xl p-6"
        >
          <h2 className="text-xl font-bold text-nature-blossom mb-4 flex items-center gap-2">
            <Link2 className="h-5 w-5" />
            Your Referral Link
          </h2>
          {referralData && (
            <>
              <div className="flex items-center gap-3 mb-4">
                <code className="flex-1 break-all rounded-lg bg-surface-card px-4 py-3 text-sm text-amber-600 font-mono">
                  {referralData.referral_url}
                </code>
                <button
                  onClick={copyCode}
                  className="rounded-lg bg-surface-card px-4 py-3 text-sm text-text-secondary hover:bg-[#EDEAE0]"
                >
                  {copied ? <CheckCircle className="h-5 w-5 text-green-400" /> : <Copy className="h-5 w-5" />}
                </button>
              </div>
              <div className="flex items-center gap-3">
                <button
                  onClick={shareInvite}
                  className="flex-1 rounded-lg bg-nature-leaf px-4 py-2 font-semibold text-text-primary hover:bg-nature-moss flex items-center justify-center gap-2"
                >
                  <Share2 className="h-4 w-4" />
                  Share Invite
                </button>
                <div className="text-right">
                  <p className="text-sm text-text-muted">Total Referrals</p>
                  <p className="text-2xl font-bold text-text-primary">{referralData.total_referrals}</p>
                </div>
              </div>
            </>
          )}
        </motion.div>

        {/* Rewards Info */}
        <div className="grid grid-cols-2 gap-4 mb-8">
          <motion.div
            className="bg-white border border-nature-leaf/20 rounded-xl p-4 text-center"
            whileHover={{ scale: 1.02 }}
          >
            <div className="text-3xl mb-2">🎯</div>
            <h3 className="font-bold text-text-primary">You Earn</h3>
            <p className="text-sm text-text-muted">+100 XP + 50 Coins per referral</p>
          </motion.div>
          <motion.div
            className="bg-white border border-nature-leaf/20 rounded-xl p-4 text-center"
            whileHover={{ scale: 1.02 }}
          >
            <div className="text-3xl mb-2">🎁</div>
            <h3 className="font-bold text-text-primary">Friend Earns</h3>
            <p className="text-sm text-text-muted">+50 XP + 25 Coins on signup</p>
          </motion.div>
        </div>

        {/* Leaderboard */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white border border-nature-leaf/20 rounded-2xl p-6"
        >
          <div className="flex items-center gap-2 mb-4">
            <Trophy className="h-5 w-5 text-amber-400" />
            <h2 className="text-lg font-bold text-text-primary">Top Referrers</h2>
          </div>
          {leaderboard.length === 0 ? (
            <p className="text-text-muted text-sm text-center py-4">
              No referrals yet. Be the first!
            </p>
          ) : (
            <ul className="space-y-2">
              {leaderboard.map((entry, idx) => (
                <li
                  key={entry.user_id}
                  className="flex items-center justify-between rounded-lg bg-surface-card px-3 py-2"
                >
                  <span className="flex items-center gap-3">
                    <span className="text-sm font-bold text-text-muted">#{idx + 1}</span>
                    <Users className="h-4 w-4 text-text-muted" />
                    <span className="text-sm text-text-secondary">
                      {entry.name || entry.user_id?.slice(0, 8)}
                    </span>
                  </span>
                  <span className="text-sm font-bold text-amber-400">
                    {entry.total_referrals} referrals
                  </span>
                </li>
              ))}
            </ul>
          )}
        </motion.div>
      </div>
    </div>
  );
}
