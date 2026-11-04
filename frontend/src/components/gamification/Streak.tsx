import { Flame, Trophy, Zap, ShieldCheck, Award, CornerLeftUp, Globe } from 'lucide-react';
import { CODDY, coddyGlow } from './palette';

export interface StreakProps {
  days: number;
  frozen?: boolean;
  size?: 'sm' | 'md' | 'lg';
}

export default function Streak({ days = 0, frozen = false, size = 'md' }: StreakProps) {
  const sizes = { sm: { icon: 16, text: 'text-xs', gap: 1 }, md: { icon: 20, text: 'text-sm', gap: 2 }, lg: { icon: 28, text: 'text-base', gap: 3 } };
  const s = sizes[size];
  const active = days > 0;
  const glow = active ? coddyGlow('danger', '60') : 'none';

  return (
    <div className={`inline-flex items-center gap-${s.gap} px-3 py-1.5 rounded-full border border-white/20 dark:border-white/10 bg-white/5 dark:bg-white/5 backdrop-blur-sm ${frozen ? 'opacity-50 grayscale' : ''}`} style={{ boxShadow: glow }}>
      <Flame size={s.icon} className={`${active ? 'text-danger-500 animate-pulse' : 'text-slate-400 dark:text-slate-500'}`} />
      <span className={`${s.text} font-mono font-bold text-ink dark:text-slate-200`}>{days}</span>
      <span className={`${s.text} font-mono text-slate-500 dark:text-slate-400`}>day streak</span>
      {!frozen && days > 0 && (
        <span className={`${s.text} font-mono text-success-500`}>&#10003;</span>
      )}
    </div>
  );
}

export function StreakCard({ days = 0, best = 0, frozen = false }: { days?: number; best?: number; frozen?: boolean }) {
  return (
    <div className="bg-white dark:bg-slate-900 border border-white/30 dark:border-white/10 rounded-2xl p-6 shadow-sm backdrop-blur-md">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 rounded-xl bg-danger-50 dark:bg-danger-900/30 flex items-center justify-center text-danger-500 dark:text-danger-400 shadow-lg">
            <Flame size={20} />
          </div>
          <div>
            <p className="text-[10px] uppercase tracking-wider text-slate-500 dark:text-slate-400 font-bold">Current Streak</p>
            <p className="text-3xl font-display font-bold text-ink dark:text-white">{days}</p>
          </div>
        </div>
        <div className="text-right">
          <p className="text-[10px] uppercase tracking-wider text-slate-500 dark:text-slate-400 font-bold">Best Streak</p>
          <p className="text-xl font-bold text-ink dark:text-slate-200">{best}</p>
        </div>
      </div>
      <div className="flex items-center gap-2">
        <Streak days={days} frozen={frozen} size="lg" />
        <div className="flex-1 h-1 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
          <div className="h-full bg-gradient-to-r from-danger-400 to-danger-600" style={{ width: Math.min(100, (days / 30) * 100) + '%' }} />
        </div>
        <span className="text-[10px] font-mono text-slate-500 dark:text-slate-400">{days}/30 days</span>
      </div>
      <div className="mt-3 flex items-center justify-between text-[10px] uppercase tracking-wider text-slate-400 font-bold">
        <span>League Rank</span>
        <span>
          <Trophy size={12} className="text-warning-500" /> #{Math.max(1, Math.floor(Math.random() * 50) + 1)}
        </span>
      </div>
    </div>
  );
}
