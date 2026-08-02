import { useState, useEffect, memo, useCallback } from "react";
import { motion } from "framer-motion";
import api from "../services/api";
import { Link } from "react-router-dom";
import {
  Target, Github, Code2, Settings,
  Award, TrendingUp, Calendar, Palette, Shield
} from "lucide-react";
import useReducedMotion from "../hooks/useReducedMotion";
import ActivityHeatmap from "./ActivityHeatmap";
import AvatarCustomizer from "./AvatarCustomizer";

const SKILL_ICONS = {
  dsa: "💻",
  system_design: "🏗️",
  behavioral: "🎤",
  aptitude: "🧮",
  resume: "📄",
};

const ProfileSidebar = memo(function ProfileSidebar() {
  const [stats, setStats] = useState(null);
  const [readinessScore, setReadinessScore] = useState(null);
  const [loading, setLoading] = useState(true);
  const [avatarOpen, setAvatarOpen] = useState(false);
  const [avatar, setAvatar] = useState(() => {
    try {
      const saved = localStorage.getItem("placementpro_avatar");
      return saved ? JSON.parse(saved) : null;
    } catch { return null; }
  });
  const reduced = useReducedMotion();

  const handleAvatarSave = useCallback((newAvatar) => {
    setAvatar(newAvatar);
    localStorage.setItem("placementpro_avatar", JSON.stringify(newAvatar));
  }, []);

  useEffect(() => {
    const load = async () => {
      try {
        const [data, readiness] = await Promise.all([
          api.getProfileStats(),
          api.getReadinessScore().catch(() => null),
        ]);
        setStats(data);
        setReadinessScore(readiness);
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
    <>
    <aside className="w-72 min-h-screen glass p-6 space-y-6 overflow-y-auto hidden lg:block">
      {/* Avatar + Name */}
      <div className="flex items-center gap-3">
        <button
          onClick={() => setAvatarOpen(true)}
          className="group relative shrink-0"
          title="Customize avatar"
        >
          <AvatarDisplay avatar={avatar} initials={initials} size="w-12 h-12" textSize="text-sm" />
          <div className="absolute -bottom-1 -right-1 w-5 h-5 rounded-full bg-indigo-500 border-2 border-gray-900 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
            <Palette size={10} className="text-white" />
          </div>
        </button>
        <div className="min-w-0">
          <h3 className="font-semibold text-sm text-text-primary truncate">{displayName}</h3>
          <p className="text-xs text-gray-400">Level {user.level || 1} · {user.plan || "free"}</p>
        </div>
      </div>

      {/* Streak */}
      <div className="glass-static p-3 rounded-xl flex items-center gap-3">
        <span className="text-2xl">🔥</span>
        <div>
          <p className="text-sm font-semibold text-text-primary">{user.streak || 0} day streak</p>
          <p className="text-xs text-gray-400">Longest: {user.longest_streak || 0}</p>
        </div>
      </div>

      {/* Readiness Score */}
      {readinessScore && (
        <div className="glass-static p-3 rounded-xl">
          <div className="flex items-center justify-between mb-1">
            <p className="text-xs text-gray-400 flex items-center gap-1">
              <Shield size={12} /> Readiness Score
            </p>
            <span className="text-sm font-bold font-mono text-indigo-400">{readinessScore.score}%</span>
          </div>
          <div className="w-full h-2 bg-gray-800 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full transition-all duration-500"
              style={{ width: `${readinessScore.score}%` }}
            />
          </div>
          <p className="text-[10px] text-gray-500 mt-1">{readinessScore.next_milestone}</p>
        </div>
      )}

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
                <span className="text-xs font-mono text-gray-400">{String(val)}%</span>
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
            <a href={`https://github.com/${user.github_username}`} target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 text-xs text-gray-400 hover:text-text-primary transition-colors">
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

      {/* Customize button */}
      <button
        onClick={() => setAvatarOpen(true)}
        className="w-full flex items-center gap-2 px-3 py-2 rounded-xl text-xs text-gray-400 hover:text-white hover:bg-gray-800/50 transition-colors border border-gray-700/30"
      >
        <Palette size={12} />
        Customize Avatar
      </button>

      {/* Quick Links */}
      <div className="space-y-1 pt-2 border-t border-space-border">
        <Link to="/analytics" className="flex items-center gap-2 text-xs text-gray-400 hover:text-text-primary transition-colors">
          <Target size={12} /> Full Analytics
        </Link>
        <Link to="/career-profile" className="flex items-center gap-2 text-xs text-gray-400 hover:text-text-primary transition-colors">
          <Settings size={12} /> Edit Profile
        </Link>
      </div>
    </aside>

    {avatarOpen && (
      <div className="hidden lg:block">
        <AvatarCustomizer
          open={avatarOpen}
          onClose={() => setAvatarOpen(false)}
          onSave={handleAvatarSave}
          currentAvatar={avatar}
        />
      </div>
    )}
  </>
  );
});

function AvatarDisplay({ avatar, initials, size, textSize }) {
  const BG_COLORS = [
    "from-indigo-500 to-indigo-600",
    "from-emerald-500 to-emerald-600",
    "from-amber-500 to-amber-600",
    "from-rose-500 to-rose-600",
    "from-cyan-500 to-cyan-600",
    "from-violet-500 to-violet-600",
    "from-teal-500 to-teal-600",
    "from-orange-500 to-orange-600",
    "from-pink-500 to-pink-600",
    "from-blue-500 to-blue-600",
    "from-purple-500 to-purple-600",
    "from-slate-500 to-slate-600",
  ];

  const SHAPE_CLASSES = ["rounded-full", "rounded-xl", "rounded-2xl"];
  const BORDER_CLASSES = [
    "border-0",
    "border-2 border-indigo-400 shadow-[0_0_12px_rgba(99,102,241,0.5)]",
    "border-2 border-white rounded-none",
    "border-2 border-transparent bg-gradient-to-br from-indigo-400 to-amber-400 bg-clip-padding p-[2px]",
  ];

  const AVATAR_EMOJIS = [
    "💻","🚀","⚡","🎯","🔥","💡","🎮","🏆","🛡️","⚔️",
    "📚","🧠","🎨","🔧","⭐","🌟","💎","🧩","🎪","🎭",
    "🎲","🎸","🎹","🎧","🎤","🏅","📈","📊","🗺️","🔬",
    "🤖","👾","🦄","🌈","🍀","🌊",
  ];

  if (!avatar) {
    return (
      <div className={`${size} rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold ${textSize}`}>
        {initials}
      </div>
    );
  }

  const shapeClass = SHAPE_CLASSES[avatar.shape] || SHAPE_CLASSES[0];
  const bgClass = BG_COLORS[avatar.bgColor] || BG_COLORS[0];
  const borderClass = BORDER_CLASSES[avatar.border] || BORDER_CLASSES[0];

  if (avatar.mode === "pixel" && avatar.pixelGrid) {
    const hasPixels = avatar.pixelGrid.some(row => row.some(c => c));
    if (hasPixels) {
      return (
        <div className={`${size} ${shapeClass} bg-gray-800 ${borderClass} overflow-hidden relative`}>
          {drawPixelPreview(avatar.pixelGrid)}
        </div>
      );
    }
  }

  return (
    <div className={`${size} ${shapeClass} bg-gradient-to-br ${bgClass} ${borderClass} flex items-center justify-center text-white font-bold ${textSize}`}>
      {avatar.mode === "initials" && <span>{initials}</span>}
      {avatar.mode === "emoji" && <span>{AVATAR_EMOJIS[avatar.emoji] || "💻"}</span>}
      {avatar.mode === "pixel" && <span className="text-lg">🎮</span>}
    </div>
  );
}

function drawPixelPreview(grid) {
  if (!grid) return null;
  const pixels = [];
  for (let r = 0; r < 8; r++) {
    for (let c = 0; c < 8; c++) {
      if (grid[r]?.[c]) {
        pixels.push(
          <div
            key={`${r}-${c}`}
            className="absolute bg-indigo-400"
            style={{
              width: "12.5%",
              height: "12.5%",
              left: `${c * 12.5}%`,
              top: `${r * 12.5}%`,
            }}
          />
        );
      }
    }
  }
  return pixels;
}

function Stat({ label, value }) {
  return (
    <div className="glass-static p-2 rounded-lg text-center">
      <p className="text-sm font-bold text-text-primary">{value}</p>
      <p className="text-[10px] text-gray-400">{label}</p>
    </div>
  );
}

ProfileSidebar.displayName = "ProfileSidebar";

export default ProfileSidebar;
