import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import api from "../services/api";
import { Trophy, Flame } from "lucide-react";
import useReducedMotion from "../hooks/useReducedMotion";

export default function GamificationCard() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const reduced = useReducedMotion();

  useEffect(() => {
    const loadProfile = async () => {
      try {
        const data = await api.getGamificationProfile();
        setProfile(data);
      } catch (err) {
        console.error("Failed to load gamification profile");
      }
      setLoading(false);
    };
    loadProfile();
  }, []);

  if (loading || !profile) return null;

  const getLevelColor = (level) => {
    if (level >= 20) return "text-yellow-500";
    if (level >= 15) return "text-purple-500";
    if (level >= 10) return "text-blue-500";
    if (level >= 5) return "text-green-500";
    return "text-gray-600";
  };

  const xpProgress = Math.min(100, (profile.xp % 100));

  return (
    <div className="card bg-gradient-to-r from-indigo-500 to-purple-600 text-white">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <motion.div
            className={`w-12 h-12 rounded-full bg-white/20 flex items-center justify-center text-xl font-bold ${getLevelColor(profile.level)}`}
            initial={reduced ? {} : { scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", stiffness: 260, damping: 20 }}
          >
            {profile.level}
          </motion.div>
          <div>
            <p className="font-bold">Level {profile.level}</p>
            <p className="text-sm text-white/80">{profile.xp} XP</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <motion.div
            initial={reduced ? {} : { rotate: -10 }}
            animate={reduced ? {} : { rotate: [0, -10, 10, -10, 0] }}
            transition={{ duration: 0.5, delay: 0.5 }}
          >
            <Flame size={20} className="text-orange-300" />
          </motion.div>
          <span className="font-bold">{profile.streak}</span>
          <span className="text-sm text-white/80">day streak</span>
        </div>
      </div>

      {/* XP Progress Bar */}
      <div className="mb-4">
        <div className="flex justify-between text-xs mb-1">
          <span>Level {profile.level}</span>
          <span>Level {profile.level + 1}</span>
        </div>
        <div className="w-full bg-white/20 rounded-full h-2 overflow-hidden">
          <motion.div
            className="bg-white h-2 rounded-full"
            initial={reduced ? { width: `${xpProgress}%` } : { width: 0 }}
            animate={{ width: `${xpProgress}%` }}
            transition={{ duration: 1, ease: "easeOut", delay: 0.3 }}
          />
        </div>
        <p className="text-xs text-white/70 mt-1">{profile.xp_to_next_level} XP to next level</p>
      </div>

      {/* Quick Stats with stagger animation */}
      <div className="grid grid-cols-4 gap-2 text-center">
        {[
          { value: profile.total_interviews || 0, label: "Interviews" },
          { value: profile.total_aptitude || 0, label: "Aptitude" },
          { value: profile.total_coding || 0, label: "Coding" },
          { value: profile.total_system_design || 0, label: "System" },
        ].map((stat, i) => (
          <motion.div
            key={stat.label}
            className="bg-white/10 rounded-lg p-2"
            initial={reduced ? {} : { opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 + i * 0.1 }}
          >
            <p className="text-lg font-bold">{stat.value}</p>
            <p className="text-xs text-white/70">{stat.label}</p>
          </motion.div>
        ))}
      </div>

      {/* Badges */}
      {profile.badges_details?.length > 0 && (
        <div className="mt-4">
          <p className="text-sm font-medium mb-2">Recent Badges</p>
          <div className="flex flex-wrap gap-2">
            {profile.badges_details.slice(0, 5).map((badge, i) => (
              <motion.div
                key={i}
                className="bg-white/20 rounded-full px-3 py-1 text-xs flex items-center gap-1"
                title={badge.description}
                initial={reduced ? {} : { scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: "spring", delay: 0.5 + i * 0.1 }}
              >
                <span>{badge.icon}</span>
                <span>{badge.name}</span>
              </motion.div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
