import React from 'react';

export default function ScreenJuiceOverlay({ juice }) {
  if (!juice) return null;

  const { type, color = '#6366f1', intensity = 5, duration = 300 } = juice;

  const getStyle = () => {
    switch (type) {
      case 'shake':
        return {
          animation: `screenShake ${duration}ms ease-out`,
          transform: `translate(${intensity}px, ${intensity}px)`,
        };
      case 'flash':
        return {
          backgroundColor: color,
          animation: `screenFlash ${duration}ms ease-out`,
        };
      case 'pulse':
        return {
          background: `radial-gradient(circle at 50% 50%, ${color}40 0%, transparent 70%)`,
          animation: `screenPulse ${duration}ms ease-out`,
        };
      case 'sparkle':
        return {
          background: `radial-gradient(circle at ${Math.random() * 100}% ${Math.random() * 100}%, rgba(255,255,255,0.15) 0%, transparent 50%)`,
          animation: `screenSparkle ${duration}ms ease-out`,
        };
      default:
        return {};
    }
  };

  return (
    <div
      className="fixed inset-0 pointer-events-none z-[9998]"
      style={{
        ...getStyle(),
        animationFillMode: 'forwards',
      }}
    />
  );
}
