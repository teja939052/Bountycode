import { motion } from 'framer-motion';

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
};

const GLOW_COLORS = {
  common: 'rgba(156,163,175,0.10)',
  uncommon: 'rgba(34,197,94,0.14)',
  rare: 'rgba(59,130,246,0.18)',
  epic: 'rgba(168,85,247,0.22)',
  legendary: 'rgba(234,179,8,0.28)',
  mythic: 'rgba(236,72,153,0.32)',
};

const RARITY_LABEL = {
  common: 'Common',
  uncommon: 'Uncommon',
  rare: 'Rare',
  epic: 'Epic',
  legendary: 'Legendary',
  mythic: 'Mythic',
};

export default function AchievementShowcase({ badges = [], maxDisplay = 8, showTitle = true }) {
  const displayBadges = badges.slice(0, maxDisplay);
  const remaining = badges.length - maxDisplay;

  const containerVariants = {
    hidden: {},
    visible: { transition: { staggerChildren: 0.06 } },
  };

  const itemVariants = {
    hidden: { opacity: 0, scale: 0.7, rotate: -8 },
    visible: { opacity: 1, scale: 1, rotate: 0, transition: { duration: 0.4, ease: [0.34, 1.56, 0.64, 1] } },
  };

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

      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        key={badges.join(',')}
        className="grid grid-cols-4 sm:grid-cols-6 gap-3"
      >
        {displayBadges.map((badge) => {
          const info = BADGE_RARITY[badge as keyof typeof BADGE_RARITY] || { rarity: 'common', color: '#9CA3AF', emoji: '🏅', title: badge };
          const glow = GLOW_COLORS[info.rarity as keyof typeof GLOW_COLORS] || GLOW_COLORS.common;
          return (
            <motion.div
              key={badge}
              variants={itemVariants}
              whileHover={{ scale: 1.12, rotate: 4, zIndex: 10 }}
              className="relative flex flex-col items-center gap-1.5 cursor-pointer group"
            >
              <div
                className="gamification-border-gradient w-full aspect-square rounded-2xl flex items-center justify-center text-2xl transition-transform duration-300"
                style={{
                  background: 'linear-gradient(135deg, rgba(255,255,255,0.55), rgba(255,255,255,0.35))',
                  boxShadow: `0 0 18px ${glow}`,
                }}
              >
                <span className="relative z-10">{info.emoji}</span>
              </div>
              <span className="text-[8px] font-mono text-gray-500 group-hover:text-gray-300 transition-colors text-center leading-tight w-full truncate">
                {info.title}
              </span>
              <span
                className="text-[8px] font-mono px-1.5 py-0.5 rounded-full"
                style={{
                  backgroundColor: `${info.color}18`,
                  color: info.color,
                  border: `1px solid ${info.color}30`,
                }}
              >
                {RARITY_LABEL[info.rarity as keyof typeof RARITY_LABEL] || info.rarity}
              </span>

              <div
                className="absolute -top-1 -right-1 w-2.5 h-2.5 rounded-full"
                style={{ backgroundColor: info.color, boxShadow: `0 0 8px ${info.color}60` }}
              />
            </motion.div>
          );
        })}

        {remaining > 0 && (
          <motion.div
            whileHover={{ scale: 1.08 }}
            className="flex flex-col items-center gap-1.5 cursor-pointer"
          >
            <div className="w-full aspect-square rounded-2xl flex items-center justify-center text-xs font-mono font-bold text-gray-500 bg-gray-800/40 border border-gray-700/25">
              +{remaining}
            </div>
            <span className="text-[8px] font-mono text-gray-600">more</span>
          </motion.div>
        )}

        {badges.length === 0 && (
          <div className="text-center py-6 w-full col-span-full">
            <div className="text-3xl mb-2">🏅</div>
            <p className="text-xs text-gray-500 font-mono">Complete activities to earn badges!</p>
          </div>
        )}
      </motion.div>
    </div>
  );
}
