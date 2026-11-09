"use client";

import { useState, useEffect } from "react";
import { Flame, Zap, Star, Crown, Heart, Trophy } from "lucide-react";
import { motion } from "framer-motion";

interface StreakDisplayProps {
  streak: number;
  streakFreezeCount?: number;
  onFreezeClick?: () => void;
  className?: string;
}

export function StreakDisplay({ streak, streakFreezeCount = 0, onFreezeClick, className }: StreakDisplayProps) {
  const [isMilestone, setIsMilestone] = useState(false);

  useEffect(() => {
    if (streak > 0 && streak % 7 === 0) {
      setIsMilestone(true);
      setTimeout(() => setIsMilestone(false), 3000);
    }
  }, [streak]);

  const milestoneMilestones = [3, 7, 14, 30, 60, 100, 365];
  const isMilestoneDay = milestoneMilestones.includes(streak);

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex items-center gap-3 ${className}`}
    >
      <div className="relative streak-flame">
        <span className="flame-emoji">🔥</span>
        {isMilestoneDay && <span className="absolute -top-2 -right-2 w-3 h-3 bg-yellow-400 rounded-full animate-ping" />}
      </div>
      <div className="flex flex-col">
        <span className="streak-number">{streak}</span>
        <span className="streak-label">{streak === 1 ? "day streak" : "day streak"}</span>
      </div>
      {isMilestoneDay && (
        <span className="text-xs font-bold text-yellow-600 bg-yellow-100 px-2 py-0.5 rounded-md">
          Milestone!
        </span>
      )}
      {streakFreezeCount > 0 && onFreezeClick && (
        <button
          onClick={onFreezeClick}
          className="streak-freeze"
          aria-label="Use streak freeze"
        >
          <Zap size={14} className="text-yellow-500" />
          <span>{streakFreezeCount}</span>
        </button>
      )}
    </motion.div>
  );
}

interface XPLevelProps {
  xp: number;
  level: number;
  xpToNext: number;
  className?: string;
}

export function XPLevelBar({ xp, level, xpToNext, className }: XPLevelProps) {
  const progress = Math.min(100, Math.round((xp % xpToNext) / xpToNext * 100));

  return (
    <div className={`flex flex-col gap-4 ${className}`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Zap size={16} className="text-yellow-500" />
          <span className="text-sm font-bold text-text-primary">XP</span>
        </div>
        <span className="text-sm font-mono text-text-muted">{xp.toLocaleString()}</span>
      </div>
      <div className="flex items-center justify-between gap-2 mb-1">
        <span className="text-xs font-semibold text-text-muted">Level {level}</span>
        <span className="text-xs font-mono text-text-muted">{xp % xpToNext} / {xpToNext}</span>
      </div>
      <div className="progress-track w-full h-2 bg-gray-100 rounded-full overflow-hidden">
        <div
          className="progress-fill h-full bg-gradient-to-r from-green-400 to-emerald-500 rounded-full transition-all duration-500"
          style={{ width: `${progress}%` }}
        />
      </div>
    </div>
  );
}

interface HeartsProps {
  hearts: number;
  maxHearts?: number;
  onHeartLost?: () => void;
  className?: string;
}

export function HeartsDisplay({ hearts, maxHearts = 3, onHeartLost, className }: HeartsProps) {
  return (
    <div className={`hearts-container ${className}`}>
      {Array.from({ length: maxHearts }).map((_, i) => (
        <div
          key={i}
          className={`heart ${i < hearts ? "full" : "lost"}`}
          aria-label={`Heart ${i + 1}`}
        >
          <Heart size={16} />
        </div>
      ))}
    </div>
  );
}

interface LessonCardProps {
  id: string;
  title: string;
  emoji: string;
  description?: string;
  type: "theory" | "practice" | "challenge" | "project" | "boss" | "quiz";
  diamonds: number;
  status: "locked" | "current" | "completed";
  progress: number;
  onClick?: () => void;
  className?: string;
}

export function LessonCard({
  id,
  title,
  emoji,
  description,
  type,
  diamonds,
  status,
  progress,
  onClick,
  className,
}: LessonCardProps) {
  const typeColors: Record<string, string> = {
    theory: "text-blue-500",
    practice: "text-green-500",
    challenge: "text-orange-500",
    project: "text-purple-500",
    boss: "text-red-500",
    quiz: "text-indigo-500",
  };

  const statusStyles: Record<string, string> = {
    locked: "bg-gray-50 border-gray-200 opacity-70 cursor-not-allowed",
    current: "bg-blue-50 border-blue-200 ring-1 ring-blue-300 shadow-lg",
    completed: "bg-green-50 border-green-200",
  };

  return (
    <motion.div
      whileHover={{ y: -2 }}
      whileTap={{ y: 0 }}
      className={`lesson-card ${statusStyles[status]} ${className}`}
      onClick={status === "locked" ? undefined : onClick}
      role="button"
      tabIndex={status === "locked" ? -1 : 0}
      onKeyDown={(e) => { if (e.key === "Enter" && onClick) onClick(); }}
    >
      <div className="lesson-card-header">
        <div className="flex flex-col">
          <span className="lesson-card-emoji">{emoji}</span>
          <h3 className="lesson-card-title">{title}</h3>
          <span className={`lesson-card-type ${typeColors[type]}`}>{type}</span>
        </div>
        <div className="lesson-card-diamonds">
          <Star size={16} fill="currentColor" />
          {diamonds}
        </div>
      </div>
      <div className="lesson-card-body">
        {description && <p className="lesson-card-desc">{description}</p>}
        <div className="lesson-card-progress">
          <div className="lesson-card-progress-fill" style={{ width: `${progress}%` }} />
        </div>
      </div>
      <div className="lesson-card-footer">
        <span className={`lesson-card-status ${status}`}>
          {status === "completed" ? "Done" : status === "current" ? "Next" : "Locked"}
        </span>
        {status === "completed" && (
          <span className="text-green-500">
            <Trophy size={14} />
          </span>
        )}
      </div>
    </motion.div>
  );
}

interface CelebrationModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  subtitle?: string;
  emoji?: string;
  xpGained?: number;
  streakGained?: number;
  onClaim?: () => void;
}

export function CelebrationModal({
  isOpen,
  onClose,
  title,
  subtitle,
  emoji = "🎉",
  xpGained,
  streakGained,
  onClaim,
}: CelebrationModalProps) {
  if (!isOpen) return null;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="celebration-overlay"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className="celebration-card"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="celebration-emoji">{emoji}</div>
        <h2 className="celebration-title">{title}</h2>
        {subtitle && <p className="celebration-subtitle">{subtitle}</p>}
        <div className="celebration-rewards">
          {xpGained !== undefined && (
            <div className="celebration-reward">
              <span className="celebration-reward-value">+{xpGained}</span>
              <span className="celebration-reward-label">XP</span>
            </div>
          )}
          {streakGained !== undefined && (
            <div className="celebration-reward">
              <span className="celebration-reward-value">🔥 {streakGained}</span>
              <span className="celebration-reward-label">Streak</span>
            </div>
          )}
        </div>
        <button
          onClick={onClose}
          className="w-full btn-gradient-gold rounded-xl px-6 py-3 text-sm font-bold shadow-lg transition-all hover:scale-[1.02] active:scale-[0.98]"
        >
          {onClaim ? "Claim Reward" : "Continue"}
        </button>
      </motion.div>
    </motion.div>
  );
}

interface LessonToastProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  xpGained?: number;
  streak?: number;
}

export function LessonToast({
  isOpen,
  onClose,
  title,
  xpGained,
  streak,
}: LessonToastProps) {
  if (!isOpen) return null;

  return (
    <motion.div
      initial={{ y: 20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      exit={{ y: 20, opacity: 0 }}
      className="lesson-toast lesson-toast-success"
    >
      <span className="lesson-toast-icon">✅</span>
      <div className="flex flex-col">
        <span className="font-bold text-text-primary">{title}</span>
        {xpGained !== undefined && (
          <span className="text-xs text-text-muted">+{xpGained} XP {streak ? `• 🔥 ${streak}` : ""}</span>
        )}
      </div>
    </motion.div>
  );
}
