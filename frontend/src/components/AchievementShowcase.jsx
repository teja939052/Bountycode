import { useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import gsap from 'gsap';

const BADGE_RARITY = {
  first_solve: { rarity: 'uncommon', color: '#22C55E', emoji: '🎯', title: 'First Blood' },
  speed_demon: { rarity: 'rare', color: '#3B82F6', emoji: '⚡', title: 'Speed Demon' },
  streak_master: { rarity: 'epic', color: '#A855F7', emoji: '🔥', title: 'Streak Master' },
  code_warrior: { rarity: 'rare', color: '#3B82F6', emoji: '⚔️', title: 'Code Warrior' },
  interview_pro: { rarity: 'epic', color: '#A855F7', emoji: '🎙️', title: 'Interview Pro' },
  resume_master: { rarity: 'uncommon', color: '#22C55E', emoji: '📄', title: 'Resume Master' },
  aptitude_king: { rarity: 'rare', color: '#3B82F6', emoji: '🧮', title: 'Aptitude King' },
  social_butterfly: { rarity: 'uncommon', color: '#22C55E', emoji: '🦋', title: 'Social Butterfly' },
  legendary_streak: { rarity: 'legendary', color: '#EAB308', emoji: '👑', title: '30-Day Legend' },
  mythic_solver: { rarity: 'mythic', color: '#EC4899', emoji: '💎', title: 'Mythic Solver' },
  early_bird: { rarity: 'common', color: '#9CA3AF', emoji: '🌅', title: 'Early Bird' },
  night_owl: { rarity: 'common', color: '#9CA3AF', emoji: '🦉', title: 'Night Owl' },
  perfect_score: { rarity: 'legendary', color: '#EAB308', emoji: '💯', title: 'Perfect Score' },
  company_hunter: { rarity: 'epic', color: '#A855F7', emoji: '🏢', title: 'Company Hunter' },
  system_architect: { rarity: 'legendary', color: '#EAB308', emoji: '🏗️', title: 'System Architect' },
  data_wizard: { rarity: 'epic', color: '#A855F7', emoji: '🧙', title: 'Data Wizard' },
};

const GLOW_COLORS = {
  common: 'rgba(156,163,175,0.08)',
  uncommon: 'rgba(34,197,94,0.12)',
  rare: 'rgba(59,130,246,0.18)',
  epic: 'rgba(168,85,247,0.22)',
  legendary: 'rgba(234,179,8,0.28)',
  mythic: 'rgba(236,72,153,0.32)',
};

export default function AchievementShowcase({ badges = [], maxDisplay = 8, showTitle = true }) {
  const containerRef = useRef(null);

  useEffect(() => {
    if (containerRef.current) {
      gsap.fromTo(
        containerRef.current.children,
        { opacity: 0, scale: 0.7, rotate: -8 },
        { opacity: 1, scale: 1, rotate: 0, stagger: 0.06, duration: 0.4, ease: 'back.out(1.7)' }
      );
    }
  }, [badges]);

  const displayBadges = badges.slice(0, maxDisplay);
  const remaining = badges.length - maxDisplay;

  return (
    <div>
      {showTitle && (
        <div className="flex items-center justify-between mb-3">
          <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400">
            Achievement Showcase
          </h3>
          <span className="text-[10px] font-mono text-gray-600">
            {badges.length} earned
          </span>
        </div>
      )}

      <div ref={containerRef} className="flex flex-wrap gap-3">
        {displayBadges.map((badge, i) => {
          const info = BADGE_RARITY[badge] || { rarity: 'common', color: '#9CA3AF', emoji: '🏅', title: badge };
          return (
            <motion.div
              key={badge}
              whileHover={{ scale: 1.15, rotate: 5, zIndex: 10 }}
              className="relative flex flex-col items-center gap-1 cursor-pointer group"
            >
              <div
                className="w-12 h-12 rounded-xl flex items-center justify-center text-xl transition-all duration-300"
                style={{
                  background: `linear-gradient(135deg, ${info.color}18, ${info.color}08)`,
                  border: `2px solid ${info.color}30`,
                  boxShadow: `0 0 12px ${GLOW_COLORS[info.rarity]}`,
                }}
              >
                {info.emoji}
              </div>
              <span className="text-[8px] font-mono text-gray-500 group-hover:text-gray-300 transition-colors text-center leading-tight w-14 truncate">
                {info.title}
              </span>

              {/* Rarity indicator dot */}
              <div
                className="absolute -top-0.5 -right-0.5 w-2 h-2 rounded-full"
                style={{ backgroundColor: info.color }}
              />
            </motion.div>
          );
        })}

        {remaining > 0 && (
          <motion.div
            whileHover={{ scale: 1.1 }}
            className="flex flex-col items-center gap-1 cursor-pointer"
          >
            <div className="w-12 h-12 rounded-xl flex items-center justify-center text-xs font-mono font-bold text-gray-500 bg-gray-800/50 border border-gray-700/30">
              +{remaining}
            </div>
            <span className="text-[8px] font-mono text-gray-600">more</span>
          </motion.div>
        )}

        {badges.length === 0 && (
          <div className="text-center py-6 w-full">
            <div className="text-2xl mb-2">🏅</div>
            <p className="text-xs text-gray-500 font-mono">Complete activities to earn badges!</p>
          </div>
        )}
      </div>
    </div>
  );
}
