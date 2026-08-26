import { useRef, useCallback } from 'react';
import { motion } from 'framer-motion';
import { getLevelForXP, getLevelColor } from './XPBar';

export default function ShareCard({ user, stats, onClose }) {
  const cardRef = useRef(null);
  const level = getLevelForXP(user?.xp || 0);
  const levelColor = getLevelColor(level);

  const handleDownload = useCallback(async () => {
    if (!cardRef.current) return;
    try {
      const html2canvas = (await import('html2canvas')).default;
      const canvas = await html2canvas(cardRef.current, {
        backgroundColor: '#0B0C10',
        scale: 2,
        useCORS: true,
      });
      const link = document.createElement('a');
      link.download = `bountycode-${user?.name || 'user'}-stats.png`;
      link.href = canvas.toDataURL('image/png');
      link.click();
    } catch (err) {
      console.error('Failed to generate image:', err);
    }
  }, [user]);

  const handleShare = useCallback(async () => {
    const text = `🚀 Level ${level} on BountyCode! ${stats?.total_solved || 0} problems solved · ${stats?.streak || 0} day streak 🔥\n\n#BountyCode #Coding #PlacementPrep`;
    if (navigator.share) {
      try { await navigator.share({ text, title: 'My BountyCode Stats' }); } catch {}
    } else {
      navigator.clipboard?.writeText(text);
    }
  }, [level, stats, user]);

  return (
    <div className="space-y-4">
      {/* Shareable Card */}
      <div ref={cardRef} className="rounded-2xl overflow-hidden border border-gray-700/30" style={{ background: 'linear-gradient(135deg, #0B0C10 0%, #111318 50%, #0B0C10 100%)' }}>
        {/* Header */}
        <div className="p-6 text-center border-b border-gray-700/20">
          <div className="flex items-center justify-center gap-2 mb-3">
            <div className="w-8 h-8 bg-gradient-to-br from-cyber-blue to-cyber-purple rounded-lg flex items-center justify-center">
              <span className="text-text-primary text-sm font-bold">⚡</span>
            </div>
            <span className="text-sm font-display font-bold text-text-primary tracking-wider">PLACEMENT<span className="text-cyber-blue">PRO</span></span>
          </div>

          {/* Avatar + Name */}
          <div
            className="w-16 h-16 rounded-xl mx-auto mb-3 flex items-center justify-center text-2xl font-display font-black text-text-primary"
            style={{ background: `linear-gradient(135deg, ${levelColor.from}30, ${levelColor.to}20)`, border: `2px solid ${levelColor.from}40` }}
          >
            {(user?.name || 'U')[0].toUpperCase()}
          </div>
          <h2 className="text-lg font-display font-bold text-text-primary">{user?.name || 'User'}</h2>
          <p className="text-xs font-mono mt-1" style={{ color: levelColor.from }}>
            Level {level} · {levelColor.label}
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-3 gap-px bg-gray-700/10">
          {[
            { value: stats?.total_solved || 0, label: 'Problems', color: '#22C55E' },
            { value: `${stats?.streak || 0}🔥`, label: 'Day Streak', color: '#EAB308' },
            { value: (user?.xp || 0).toLocaleString(), label: 'XP', color: '#3B82F6' },
          ].map((stat) => (
            <div key={stat.label} className="bg-[#0B0C10] p-4 text-center">
              <p className="text-xl font-display font-black" style={{ color: stat.color }}>{stat.value}</p>
              <p className="text-[9px] font-mono text-gray-500 uppercase tracking-wider mt-1">{stat.label}</p>
            </div>
          ))}
        </div>

        {/* Bottom */}
        <div className="p-4 text-center border-t border-gray-700/20">
          <p className="text-[9px] font-mono text-gray-600">bountycode.in · Power your placement prep</p>
        </div>
      </div>

      {/* Actions */}
      <div className="flex gap-3">
        <button onClick={handleDownload} className="btn-primary flex-1 text-sm">
          📥 Download PNG
        </button>
        <button onClick={handleShare} className="btn-secondary flex-1 text-sm">
          📤 Share
        </button>
        {onClose && (
          <button onClick={onClose} className="btn-ghost text-sm">Close</button>
        )}
      </div>
    </div>
  );
}
