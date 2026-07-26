import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import api from "../services/api";
import { Link } from "react-router-dom";
import {
  Flame, Trophy, Zap, Target, Github, Code2, Settings,
  ChevronRight, ExternalLink, Award, TrendingUp, Calendar
} from "lucide-react";
import useReducedMotion from "../hooks/useReducedMotion";
import ActivityHeatmap from "./ActivityHeatmap";

const SKILL_ICONS = {
  dsa: "💻",
  system_design: "🏗️",
  behavioral: "🎤",
  aptitude: "🧮",
  resume: "📄",
};

export default function ProfileSidebar() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const reduced = useReducedMotion();

  useEffect(() => {
    const load = async () => {
      try {
        const data = await api.getProfileStats();
        setStats(data);
      } catch {
        // fallback: keep null and render minimal UI
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  if (loading) {
    return (
      <aside className="w-72 min-h-screen glass p-6 space-y-6 overflow-y-auto hidden lg:block">
        <div className="animate-pulse space-y-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-full bg-gray-700" />
            <div className="flex-1 space-y-2">
              <div className="h-4 bg-gray-700 rounded w-3/4" />
              <div className="h-3 bg-gray-700 rounded w-1/2" />
            </div>
          </div>
          <div className="h-24 bg-gray-700 rounded" />
          <div className="h-32 bg-gray-700 rounded" />
        </div>
      </aside>
    );
  }

  const user = stats || {};
  const displayName = user.name || "User";
  const initials = displayName.split(" ").map(n => n[0]).join("").slice(0, 2).toUpperCase();

  return (
    <aside className="w-72 min-h-screen glass p-6 space-y-6 overflow-y-auto hidden lg:block">
      {/* Avatar + Name */}
      <div className="flex items-center gap-3">
        <div className="w-12 h-12 rounded-full bg-gradient-to-br from-cyber-blue to-cyber-purple flex items-center justify-center text-white font-bold text-sm">
          {initials}
        </div>
        <div className="min-w-0">
          <h3 className="font-semibold text-sm text-white truncate">{displayName}</h3>
          <p className="text-xs text-gray-400">Level {user.level || 1} · {user.plan || "free"}</p>
        </div>
      </div>

      {/* Streak */}
      <div className="glass-static p-3 rounded-xl flex items-center gap-3">
        <span className="text-2xl">🔥</span>
        <div>
          <p className="text-sm font-semibold text-white">{user.streak || 0} day streak</p>
          <p className="text-xs text-gray-400">Longest: {user.longest_streak || 0}</p>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 gap-2">
        <Stat label="Solved" value={user.total_solved || 0} />
        <Stat label="XP" value={user.xp || 0} />
        <Stat label="Interviews" value={user.total_interviews || 0} />
        <Stat label="Coding" value={user.total_coding || 0} />
      </div>

      {/* Badges */}
      {user.badges?.length > 0 && (
        <div>
          <p className="text-xs text-gray-400 mb-2 flex items-center gap-1">
            <Award size={12} /> Recent Badges
          </p>
          <div className="flex gap-2 flex-wrap">
            {user.badges.slice(0, 3).map((badge, i) => (
              <span
                key={i}
                className="text-xl"
                title={badge.name || badge.description || "Badge"}
              >
                {badge.icon || "🏆"}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Skills */}
      {user.skills && (
        <div>
          <p className="text-xs text-gray-400 mb-2 flex items-center gap-1">
            <TrendingUp size={12} /> Skills
          </p>
          <div className="space-y-2">
            {Object.entries(user.skills).map(([key, val]) => (
              <div key={key} className="flex items-center justify-between">
                <span className="text-xs text-gray-300 capitalize flex items-center gap-1">
                  <span>{SKILL_ICONS[key] || "📊"}</span>
                  {key.replace("_", " ")}
                </span>
                <span className="text-xs font-mono text-gray-400">{val}%</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Activity Heatmap */}
      {user.heatmap?.length > 0 && (
        <div>
          <p className="text-xs text-gray-400 mb-2 flex items-center gap-1">
            <Calendar size={12} /> Activity
          </p>
          <ActivityHeatmap data={user.heatmap} />
        </div>
      )}

      {/* Integrations */}
      <div>
        <p className="text-xs text-gray-400 mb-2">Integrations</p>
        <div className="space-y-1">
          {user.github_username ? (
            <a href={`https://github.com/${user.github_username}`} target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 text-xs text-gray-400 hover:text-white transition-colors">
              <Github size={12} /> {user.github_username}
            </a>
          ) : (
            <p className="text-xs text-gray-600">GitHub: not linked</p>
          )}
          {user.leetcode_username ? (
            <p className="text-xs text-gray-400 flex items-center gap-1">
              <Code2 size={12} /> {user.leetcode_username}
            </p>
          ) : (
            <p className="text-xs text-gray-600">LeetCode: not linked</p>
          )}
        </div>
      </div>

      {/* Quick Links */}
      <div className="space-y-1 pt-2 border-t border-space-border">
        <Link to="/analytics" className="flex items-center gap-2 text-xs text-gray-400 hover:text-white transition-colors">
          <Target size={12} /> Full Analytics
        </Link>
        <Link to="/career-profile" className="flex items-center gap-2 text-xs text-gray-400 hover:text-white transition-colors">
          <Settings size={12} /> Edit Profile
        </Link>
      </div>
    </aside>
  );
}

function Stat({ label, value }) {
  return (
    <div className="glass-static p-2 rounded-lg text-center">
      <p className="text-sm font-bold text-white">{value}</p>
      <p className="text-[10px] text-gray-400">{label}</p>
    </div>
  );
}
