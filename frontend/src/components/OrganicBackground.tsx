import { useState, useEffect } from "react";

interface OrganicBackgroundProps {
  showParticles?: boolean;
  reducedMotion?: boolean;
}

export function OrganicBackground({ showParticles = true, reducedMotion = false }: OrganicBackgroundProps) {
  const [particles, setParticles] = useState<any[]>([]);
  const [angle, setAngle] = useState(0);

  // Generate organic particle positions
  useEffect(() => {
    if (reducedMotion) return;

    const count = showParticles ? 8 : 3;
    const particles = Array.from({ length: count }, (_, i) => ({
      id: i,
      x: Math.random(),
      y: Math.random(),
      size: Math.random() * 20 + 10,
      opacity: Math.random() * 0.5 + 0.1,
      delay: i * 0.5,
    }));

    setParticles(particles);

    let angle = 0;
    const animate = () => {
      angle += 0.5;
      setAngle(angle);
      requestAnimationFrame(animate);
    };
    animate();
  }, [reducedMotion, showParticles]);

  return (
    <div
      className="pointer-events-none fixed inset-0 z-0 overflow-hidden bg-[var(--pp-surface)]"
      style={{
        backgroundImage: `
          radial-gradient(ellipse at 20% 20%, rgba(34, 197, 94, 0.08) 0%, transparent 50%),
          radial-gradient(ellipse at 80% 80%, rgba(34, 197, 94, 0.05) 0%, transparent 50%),
          radial-gradient(ellipse at 50% 50%, rgba(34, 197, 94, 0.03) 0%, transparent 70%)
        `,
        backgroundAttachment: 'fixed',
      }}
    >
      {showParticles && !reducedMotion && particles.length > 0 && (
        <div className="absolute inset-0 overflow-hidden">
          {particles.map((p) => (
            <div
              key={p.id}
              className={`absolute rounded-full bg-primary/${Math.round(p.opacity * 100)} shadow-md transition-all duration-200 ease-out`}
              style={{
                width: p.size,
                height: p.size,
                left: `${p.x * 100}%`,
                top: `${p.y * 100}%`,
                animation: `float 20s ease-in-out infinite`,
                animationDelay: p.delay + 's',
              }}
            />
          ))}
        </div>
      )}

      {/* Subtle rotating gradient overlay */}
      <div
        className="absolute inset-0 opacity-10 translate-x-1/2 -translate-y-1/2 rotate-[var(--angle,0)] bg-gradient-to-br from-primary/5 via-transparent to-primary/5"
        style={{ '--angle': `${angle}deg` }}
      />
    </div>
  );
}