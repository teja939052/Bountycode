import { ShieldCheck, Award, Zap, Flame, Trophy, Zap as ZapIcon } from 'lucide-react';
import { CODDY, coddyGlow, coddyRadial } from './palette';

export interface BadgeProps {
  id: string;
  name: string;
  description?: string;
  tier: 'bronze' | 'silver' | 'gold' | 'platinum';
  icon: React.ReactNode;
  earned?: boolean;
  earnedAt?: string;
  size?: 'sm' | 'md' | 'lg';
}

const TIER_CONFIG = {
  bronze: { base: CODDY.bronze.base, light: CODDY.bronze.light },
  silver: { base: CODDY.silver.base, light: CODDY.silver.light },
  gold: { base: CODDY.gold.base, light: CODDY.gold.light },
  platinum: { base: CODDY.platinum.base, light: CODDY.platinum.light },
} as const;

export default function Badge({ id, name, description, tier = 'bronze', icon, earned = false, size = 'md' }: BadgeProps) {
  const config = TIER_CONFIG[tier];
  const sizes = { sm: { w: 8, h: 8, icon: 14, text: 'text-[10px]' }, md: { w: 10, h: 10, icon: 18, text: 'text-xs' }, lg: { w: 14, h: 14, icon: 24, text: 'text-sm' } };
  const s = sizes[size];

  return (
    <div className="relative group cursor-default" title={name}>
      <div
        className={`relative w-${s.w} h-${s.h} rounded-2xl flex items-center justify-center ${earned ? `border-2 border-${config.base.replace('#', '')} bg-${config.base.replace('#', '')}10 dark:bg-${config.base.replace('#', '')}20 shadow-[${coddyGlow(config.base.replace('#', '').slice(0, -2), '40').replace('0 0 24px', '0 0 12px')}]` : 'border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/50 grayscale opacity-60'}`}
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
          {earned && tier !== 'bronze' && (
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
