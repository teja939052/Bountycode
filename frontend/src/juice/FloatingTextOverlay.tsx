import React from 'react';

const TYPE_STYLES = {
  xp: { color: '#a78bfa', icon: '⚡' },
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
        const style = TYPE_STYLES[item.type] || TYPE_STYLES.xp;
        return (
          <div
            key={item.id}
            className="absolute text-2xl font-bold floating-text-item"
            style={{
              left: item.x || '50%',
              top: item.y || '50%',
              color: item.color || style.color,
              textShadow: `0 0 20px ${item.color || style.color}80, 0 0 40px ${item.color || style.color}40`,
              animation: `floatUp 1.5s ease-out forwards`,
            }}
          >
            {style.icon} {item.text}
          </div>
        );
      })}
    </div>
  );
}
