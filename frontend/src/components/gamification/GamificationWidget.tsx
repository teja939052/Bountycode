import { Zap, Flame, Trophy, ShieldCheck, ArrowRight } from 'lucide-react';
import { CODDY, getLevelLabel, coddyGlow } from './palette';

export interface GamificationWidgetProps {
  xp: number;
  level: number;
  streak: number;
  league?: number;
  badges?: number;
  onOpenJourney?: () => void;
}

export default function GamificationWidget({ xp, level = 1, streak = 0, league, badges = 0, onOpenJourney }: GamificationWidgetProps) {
  const label = getLevelLabel(level);
  const color = CODDY[label.color];

  return (
    <div
      onClick={onOpenJourney}
      className="relative bg-white dark:bg-slate-900 border border-white/30 dark:border-white/10 rounded-2xl p-4 shadow-sm backdrop-blur-md cursor-pointer group"
      style={{ boxShadow: `0 0 20px ${color.base}15` }}
    >
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-xl flex items-center justify-center font-display font-bold text-[10px]" style={{
            background: `linear-gradient(135deg, ${color.light}30, ${CODDY.blue.light}20)`,
            color: color.base,
            border: `1px solid ${color.base}60`,
          }}>
            {level}
          </div>
          <span className="text-[10px] font-bold text-ink dark:text-slate-200 uppercase tracking-tighter">{label.label}</span>
        </div>
        <div className="flex items-center gap-1.5 text-[10px] font-mono font-bold">
          <Trophy size={11} className="text-score-500" />
          <span className="text-score-600 dark:text-score-400">#{league ?? '—'}</span>
        </div>
      </div>

      <div className="h-2 bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden border border-white/20 dark:border-white/10 mb-2">
        <div className="h-full rounded-full" style={{ background: `linear-gradient(90deg, ${color.base}, ${CODDY.blue.base})`, width: '60%', transition: 'width 0.8s ease' }} />
      </div>

      <div className="flex items-center justify-between text-[10px] font-mono">
        <div className="flex items-center gap-1">
          <Flame size={11} className="text-streak-500" />
          <span className="text-streak-600 dark:text-streak-400">{streak}</span>
          <span className="text-slate-500 dark:text-slate-500">day streak</span>
        </div>
        <div className="flex items-center gap-1">
          <Zap size={11} className="text-score-500" />
          <span className="text-score-600 dark:text-score-400">{xp} XP</span>
        </div>
        <div className="flex items-center gap-1">
          <ShieldCheck size={11} className="text-success-500" />
          <span className="text-success-600 dark:text-success-400">{badges}</span>
        </div>
        <ArrowRight size={11} className="text-slate-400" />
      </div>
    </div>
  );
}


