import { Gift, Sparkles, Crown, Zap, ShieldCheck } from 'lucide-react';
import { CODDY, coddyGlow, coddyRadial } from './palette';

export interface ChestProps {
  type: 'wood' | 'silver' | 'gold' | 'diamond';
  opened?: boolean;
  onOpen?: () => void;
  size?: 'sm' | 'md' | 'lg';
}

const CHEST_CONFIG = {
  wood: { icon: <Gift size={24} className="text-amber-500" />, gradient: 'linear-gradient(135deg, #8B4513, #A0522D)', glow: CODDY.warning.base },
  silver: { icon: <ShieldCheck size={24} className="text-silver-400" />, gradient: 'linear-gradient(135deg, #B0B0B0, #E0E0E0)', glow: CODDY.silver.base },
  gold: { icon: <Crown size={24} className="text-amber-400" />, gradient: 'linear-gradient(135deg, #F59E0B, #FCD34D)', glow: CODDY.gold.base },
  diamond: { icon: <Sparkles size={24} className="text-cyan-400" />, gradient: 'linear-gradient(135deg, #06B6D4, #818CF8)', glow: CODDY.blue.base },
} as const;

export default function Chest({ type = 'wood', opened = false, onOpen, size = 'md' }: ChestProps) {
  const config = CHEST_CONFIG[type];
  const sizes = { sm: { w: 48, h: 48, icon: 20 }, md: { w: 64, h: 64, icon: 28 }, lg: { w: 88, h: 88, icon: 36 } };
  const s = sizes[size];

  return (
    <div
      onClick={opened ? undefined : onOpen}
      className={`relative w-${s.w} h-${s.h} rounded-xl flex flex-col items-center justify-center p-2 cursor-pointer ${opened ? 'opacity-60 scale-95' : 'opacity-100 scale-100 transition-all duration-200 hover:scale-105'}`}
      title={opened ? "Opened" : "Tap to open"}
    >
      <div className={`w-full h-full rounded-xl flex items-center justify-center bg-white dark:bg-slate-800 border border-white/30 dark:border-white/10 shadow-lg ${opened ? 'shadow-[0_0_20px_' + config.glow + '40]' : ''}`} style={{ boxShadow: opened ? coddyGlow(type, '60') : '0 4px 12px rgba(0,0,0,0.1)' }}>
        <div className={`relative z-10 ${opened ? 'animate-pulse' : ''}`}>{config.icon}</div>
        {opened && (
          <div className="absolute -top-4 left-1/2 -translate-x-1/2 flex items-center gap-1 px-2 py-1 rounded-full bg-white dark:bg-slate-800 border border-white/30 text-[10px] font-bold text-ink dark:text-white shadow-lg">
            <Zap size={10} className="text-warning-500" /> Rewarded
          </div>
        )}
      </div>
      <div className="mt-1 text-[10px] font-mono font-bold text-slate-500 dark:text-slate-400 uppercase">{type}</div>
    </div>
  );
}

export function ChestRow({ chests = [] }: { chests?: any[] }) {
  return (
    <div className="flex gap-3 overflow-x-auto pb-2">
      {chests.map((c) => (
        <Chest key={c.id || c.type} type={c.type} opened={c.opened} onOpen={c.onOpen} size="md" />
      ))}
    </div>
  );
}
