import React from 'react';

const TYPE_STYLES = {
  diamonds: { color: '#a78bfa', icon: '⚡' },
  streak: { color: '#f59e0b', icon: '🔥' },
  level: { color: '#6366f1', icon: '⬆' },
  badge: { color: '#34d399', icon: '🏅' },
  coins: { color: '#fbbf24', icon: '🪙' },
  achievement: { color: '#f472b6', icon: '🌟' },
};

export default function FloatingTextOverlay({ texts }) {
  return (
    <div className="fixed inset-0 pointer-events-none z-[9999] overflow-hidden">
      {texts.map((item) => {
        const style = TYPE_STYLES[item.type] || TYPE_STYLES.diamonds;
        return (
          <motion.div
            key={item.id}
            className={`absolute font-bold ${item.size || 'text-2xl'}`}
            style={{
              left: item.x || '50%',
              top: item.y || '50%',
              color: item.color || style.color,
              textShadow: `0 0 20px ${item.color || style.color}80, 0 0 40px ${item.color || style.color}40`,
            }}
            initial={{ opacity: 0, y: 0, scale: 0.5 }}
            animate={{ opacity: [0, 1, 1, 0], y: [-20, -100, -160], scale: [0.5, 1.3, 1, 0.8] }}
            transition={{ duration: 1.8, ease: 'easeOut' }}
          >
            {style.icon} {item.text}
          </motion.div>
        );
      })}
    </div>
  );
}
