import { Hexagon, Flame, Zap, Trophy, Target, Star, Zap as ZapIcon } from 'lucide-react';
import { CODDY } from './palette';

export interface JourneyTileProps {
  id: string;
  label: string;
  status: 'done' | 'active' | 'locked';
  topic?: string;
  onClick?: () => void;
  size?: 'sm' | 'md' | 'lg';
}

const STATUS_CONFIG = {
  done: { bg: CODDY.success.light, border: CODDY.success.base, text: CODDY.success.base, icon: <Star size={14} className="text-success-500" /> },
  active: { bg: CODDY.blue.light, border: CODDY.blue.base, text: CODDY.blue.base, icon: <Zap size={14} className="text-coddy-500" /> },
  locked: { bg: CODDY.mist.base, border: "#D1D5DB", text: "#9CA3AF", icon: <Target size={14} className="text-slate-400" /> },
} as const;

export default function JourneyTile({ id, label, status, topic, onClick, size = 'md' }: JourneyTileProps) {
  const cfg = STATUS_CONFIG[status];
  const sizes = { sm: { w: 40, h: 40, text: 'text-[9px]' }, md: { w: 48, h: 48, text: 'text-xs' }, lg: { w: 64, h: 64, text: 'text-sm' } };
  const s = sizes[size];

  return (
    <div
      onClick={onClick}
      className={`relative w-${s.w} h-${s.h} rounded-2xl flex flex-col items-center justify-center cursor-pointer transition-all duration-200 ${status === 'locked' ? 'opacity-60 grayscale' : 'opacity-100 hover:scale-105 shadow-md'}`}
      style={{
        background: cfg.bg,
        border: `1px solid ${cfg.border}`,
        boxShadow: status === 'done' ? `0 0 12px ${cfg.border}30` : 'none',
      }}
    >
      <div className="relative z-10 mb-1">{cfg.icon}</div>
      <span className={`${s.text} font-mono font-bold text-ink dark:text-slate-200 ${status === 'done' ? 'text-success-500' : status === 'active' ? 'text-coddy-500' : 'text-slate-500'}`}>
        {label}
      </span>
      {status === 'done' && (
        <div className="absolute top-1 right-1 w-3 h-3 rounded-full bg-success-500 border-2 border-white dark:border-white" />
      )}
      {status === 'locked' && (
        <div className="absolute inset-0 rounded-2xl flex items-center justify-center bg-white/10 dark:bg-white/5">
          <span className="text-[10px]">🔒</span>
        </div>
      )}
    </div>
  );
}

export function JourneyPath({ tiles = [] }: { tiles?: JourneyTileProps[] }) {
  return (
    <div className="flex gap-2 overflow-x-auto pb-2">
      {tiles.map((t) => (
        <JourneyTile key={t.id} id={t.id} label={t.label} status={t.status} topic={t.topic} onClick={t.onClick} size="md" />
      ))}
    </div>
  );
}
