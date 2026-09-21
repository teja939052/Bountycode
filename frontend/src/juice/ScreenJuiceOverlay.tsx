import React from 'react';

export default function ScreenJuiceOverlay({ juice }) {
  if (!juice) return null;

  const { type, color = '#6366f1', intensity = 6, duration = 300, text, subtext } = juice;

  const getStyle = (): React.CSSProperties => {
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
          background: `radial-gradient(circle at 50% 50%, ${color}50 0%, transparent 70%)`,
          animation: `screenPulse ${duration}ms ease-out`,
        };
      case 'sparkle':
        return {
          background: `radial-gradient(circle at ${Math.random() * 100}% ${Math.random() * 100}%, rgba(255,255,255,0.2) 0%, transparent 50%)`,
          animation: `screenSparkle ${duration}ms ease-out`,
        };
      case 'vignette':
        return {
          background: 'radial-gradient(circle at 50% 50%, transparent 30%, rgba(0,0,0,0.7) 100%)',
          animation: `vignetteIn ${duration}ms ease-out`,
        };
      case 'chromatic':
        return {
          background: 'transparent',
          animation: `chromatic ${duration}ms ease-out`,
          boxShadow: `inset 0 0 80px ${color}40`,
        };
      case 'impact':
        return {
          background: `radial-gradient(circle at 50% 50%, ${color}80 0%, transparent 60%)`,
          animation: `impactFlash ${duration}ms ease-out`,
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
    >
      {text && (
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-4xl font-black text-white" style={{
            textShadow: `0 0 40px ${color}`,
            animation: 'floatUp 0.6s ease-out 0.1s both',
          }}>
            {text}
          </div>
        </div>
      )}
      {subtext && (
        <div className="absolute inset-0 flex items-center justify-center mt-16">
          <div className="text-lg font-bold text-white/80" style={{
            textShadow: '0 0 20px rgba(0,0,0,0.8)',
            animation: 'floatUp 0.6s ease-out 0.3s both',
          }}>
            {subtext}
          </div>
        </div>
      )}
    </div>
  );
}
