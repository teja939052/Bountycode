import { ShieldCheck, Award, Zap, Flame, Trophy, Zap as ZapIcon } from 'lucide-react';
import { CODDY, coddyGlow } from './palette';

export interface BadgeProps {
  id: string;
  name: string;
  description?: string;
  tier: 'streak' | 'score' | 'energy' | 'blue' | 'pro' | 'success' | 'hearts';
  icon: React.ReactNode;
  earned?: boolean;
  earnedAt?: string;
  size?: 'sm' | 'md' | 'lg';
}

const TIER_CONFIG = {
  streak:   { base: CODDY.streak.base, light: CODDY.streak.light },
  score:    { base: CODDY.score.base,  light: CODDY.score.light },
  energy:   { base: CODDY.energy.base, light: CODDY.energy.light },
  blue:     { base: CODDY.blue.base,   light: CODDY.blue.light },
  pro:      { base: CODDY.pro.base,    light: CODDY.pro.light },
  success:  { base: CODDY.success.base,light: CODDY.success.light },
  hearts:   { base: CODDY.hearts.base, light: CODDY.hearts.light },
} as const;

const TIER_CLASS = {
  streak:   "text-streak-500 dark:text-streak-400 bg-streak-50 dark:bg-streak-900/30 border-streak-500/30 dark:border-streak-400/50",
  score:    "text-score-500 dark:text-score-400 bg-score-50 dark:bg-score-900/30 border-score-500/30 dark:border-score-400/50",
  energy:   "text-energy-500 dark:text-energy-400 bg-energy-50 dark:bg-energy-900/30 border-energy-500/30 dark:border-energy-400/50",
  blue:     "text-coddy-500 dark:text-coddy-400 bg-coddy-50 dark:bg-coddy-900/30 border-coddy-500/30 dark:border-coddy-400/50",
  pro:      "text-pro-500 dark:text-pro-400 bg-pro-50 dark:bg-pro-900/30 border-pro-500/30 dark:border-pro-400/50",
  success:  "text-success-500 dark:text-success-400 bg-success-50 dark:bg-success-900/30 border-success-500/30 dark:border-success-400/50",
  hearts:   "text-hearts-500 dark:text-hearts-400 bg-hearts-50 dark:bg-hearts-900/30 border-hearts-500/30 dark:border-hearts-400/50",
} as const;

export default function Badge({ id, name, description, tier = 'streak', icon, earned = false, size = 'md' }: BadgeProps) {
  const config = TIER_CONFIG[tier];
  const tierClass = TIER_CLASS[tier];
  const sizes = { sm: { w: 8, h: 8, icon: 14, text: 'text-[10px]' }, md: { w: 10, h: 10, icon: 18, text: 'text-xs' }, lg: { w: 14, h: 14, icon: 24, text: 'text-sm' } };
  const s = sizes[size];

  return (
    <div className="relative group cursor-default" title={name}>
      <div
        className={`relative w-${s.w} h-${s.h} rounded-2xl flex items-center justify-center ${earned ? `border-2 border-${tier.replace(/[A-Z]/g, '-$&').toLowerCase()} bg-${tier.replace(/[A-Z]/g, '-$&').toLowerCase()}10 dark:bg-${tier.replace(/[A-Z]/g, '-$&').toLowerCase()}20 shadow-[${coddyGlow(tier, '40').replace('0 0 24px', '0 0 12px')}]` : 'border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/50 grayscale opacity-60'}`}
        style={{
          boxShadow: earned ? coddyGlow(tier, '50') : 'none',
        }}
      >
        <div className={`relative z-10 ${icon}`} />
        {!earned && (
          <div className="absolute inset-0 rounded-2xl flex items-center justify-center bg-white/60 dark:bg-slate-900/80">
            <span className="text-slate-400">🔒</span>
          </div>
        )}
        <div className="absolute -right-1 -top-1 w-3 h-3 rounded-full border-2 border-white dark:border-white bg-white dark:bg-white">
          {earned && tier !== 'streak' && (
            <span className="text-[7px] font-bold" style={{ color: config.base }}>{tier[0].toUpperCase()}</span>
          )}
        </div>
      </div>
      {description && (
        <div className="absolute -bottom-8 left-1/2 -translate-x-1/2 whitespace-nowrap text-[9px] text-slate-600 dark:text-slate-400 bg-white dark:bg-slate-800 px-2 py-1 rounded border border-white/30 dark:border-white/10 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
          {description}
        </div>
      )}
    </div>
  );
}

export function BadgeGrid({ badges = [] }: { badges?: any[] }) {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
      {badges.map((b) => (
        <Badge key={b.id} id={b.id} name={b.name} description={b.description} tier={b.tier} icon={b.icon || <Award size={16} />} earned={b.earned} size="md" />
      ))}
    </div>
  );
}
