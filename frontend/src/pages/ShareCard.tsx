import { useState, useEffect, useCallback } from "react";
import { motion } from "framer-motion";
import { shareableAchievementsApi } from "../services/api/shareableAchievements.ts";
import useAuthStore from "../store/authStore";
import { Share2, Copy, Check, Award, Flame, Brain, Crown, Rocket, Star } from "lucide-react";

const TEMPLATE_ICONS = {
  victory: "🏆",
  streak: "🔥",
  smart: "🧠",
  legend: "👑",
  rocket: "🚀",
};

const TEMPLATE_COLORS = {
  victory: "from-amber-500 to-orange-600",
  streak: "from-red-500 to-pink-600",
  smart: "from-[#4F8F57] to-[#7BB661]",
  legend: "from-[#4F8F57] to-[#7BB661]",
  rocket: "from-sky-500 to-blue-600",
};

export default function ShareCard() {
  const user = useAuthStore((s) => s.user);
  const [cards, setCards] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);
  const [selectedCard, setSelectedCard] = useState(null);
  const [shareResult, setShareResult] = useState("");

  const loadCards = useCallback(async () => {
    try {
      const res = await shareableAchievementsApi.myCards();
      setCards(res.cards || []);
    } catch (e) {
      setError(e.message || "Could not load cards");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadCards();
  }, [loadCards]);

  const handleGenerate = async (type) => {
    setError("");
    try {
      const res = await shareableAchievementsApi.generate(type, { score: Math.floor(Math.random() * 100) + 50 });
      setCards((prev) => [res, ...prev]);
      setShareResult(`Card generated! ${res.share_text}`);
      setTimeout(() => setShareResult(""), 3000);
    } catch (e) {
      setError(e.message || "Could not generate card");
    }
  };

  const handleShare = async (token) => {
    setCopied(false);
    try {
      const res = await shareableAchievementsApi.share(token);
      setShareResult(res.message);
      setTimeout(() => setShareResult(""), 3000);
    } catch (e) {
      setError(e.message || "Share failed");
    }
  };

  const handleCopyLink = (cardUrl) => {
    navigator.clipboard.writeText(window.location.origin + cardUrl);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-surface-base text-text-primary">
        <div className="animate-pulse text-nature-blossom">Loading Achievements...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-surface-base text-text-primary px-4 py-8">
      <div className="max-w-5xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold">
            <span className="bg-gradient-to-r from-[#4F8F57] via-[#7BB661] to-[#B8D9A8] bg-clip-text text-transparent">
              Shareable Achievements
            </span>
          </h1>
          <p className="text-text-muted mt-2">
            Generate shareable cards. Show off your wins. Inspire your campus.
          </p>
        </div>

        {error && (
          <p className="text-center text-amber-400 text-sm mb-4 bg-amber-500/10 border border-amber-500/30 rounded-lg py-2 px-4 max-w-md mx-auto">
            {error}
          </p>
        )}

        {shareResult && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-4 bg-green-500/10 border border-green-500/30 rounded-lg py-2 text-nature-blossom text-sm"
          >
            {shareResult}
          </motion.div>
        )}

        {/* Generate Cards */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8 bg-white border border-nature-leaf/20 rounded-2xl p-6"
        >
          <h2 className="text-xl font-bold text-text-primary mb-4 flex items-center gap-2">
            <Award className="h-5 w-5 text-amber-400" />
            Generate Achievement Card
          </h2>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {[
              { type: "interview_complete", label: "🎙️ Interview", icon: "🎙️" },
              { type: "aptitude_score", label: "📝 Aptitude", icon: "📝" },
              { type: "coding_solved", label: "💻 Coding", icon: "💻" },
              { type: "castle_defend", label: "🏰 Castle", icon: "🏰" },
              { type: "daily_streak", label: "🔥 Streak", icon: "🔥" },
              { type: "level_up", label: "⬆️ Level Up", icon: "⬆️" },
              { type: "badge_earned", label: "🎖️ Badge", icon: "🎖️" },
              { type: "tower_climb", label: "🏗️ Tower", icon: "🏗️" },
            ].map((item) => (
              <button
                key={item.type}
                onClick={() => handleGenerate(item.type)}
                className="rounded-xl border border-nature-leaf/20 bg-surface-base p-4 text-center hover:border-nature-leaf/30 hover:bg-surface-card transition-all"
              >
                <div className="text-2xl mb-1">{item.icon}</div>
                <div className="text-xs font-bold text-text-secondary">{item.label}</div>
              </button>
            ))}
          </div>
        </motion.div>

        {/* Cards Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {cards.map((card, idx) => (
            <motion.div
              key={card._id || idx}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="rounded-2xl border border-nature-leaf/20 bg-white overflow-hidden"
            >
              <div
                className={`h-32 bg-gradient-to-br ${TEMPLATE_COLORS[card.template || "victory"]} flex items-center justify-center relative`}
              >
                <div className="text-5xl">{TEMPLATE_ICONS[card.template || "victory"]}</div>
                <div className="absolute top-3 right-3 bg-surface-2 rounded-full px-2 py-1 text-xs text-text-primary">
                  {card.achievement_type?.replace("_", " ")}
                </div>
              </div>
              <div className="p-4">
                <p className="font-bold text-text-primary text-sm">{card.user_name || user?.name || "Player"}</p>
                <p className="text-xs text-text-muted mt-1">
                  {card.achievement_type?.replace("_", " ")} — {card.score_data?.score || "N/A"}
                </p>
                <div className="flex gap-2 mt-3">
                  <button
                    onClick={() => handleCopyLink(card.card_url)}
                    className="flex-1 rounded-lg bg-nature-leaf px-3 py-2 text-xs font-bold text-text-primary hover:bg-nature-moss flex items-center justify-center gap-1"
                  >
                    {copied ? <Check className="h-3 w-3" /> : <Copy className="h-3 w-3" />}
                    {copied ? "Copied!" : "Copy Link"}
                  </button>
                  <button
                    onClick={() => handleShare(card._id)}
                    className="flex-1 rounded-lg bg-green-600 px-3 py-2 text-xs font-bold text-text-primary hover:bg-green-500 flex items-center justify-center gap-1"
                  >
                    <Share2 className="h-3 w-3" />
                    Share
                  </button>
                </div>
                <p className="text-xs text-text-muted mt-2">
                  Shares: {card.shares || 0}
                </p>
              </div>
            </motion.div>
          ))}
        </div>

        {cards.length === 0 && !loading && (
          <p className="text-center text-text-muted mt-8">
            No achievement cards yet. Generate one above!
          </p>
        )}
      </div>
    </div>
  );
}