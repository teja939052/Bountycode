import { useEffect, useRef, useMemo, useCallback, useState } from "react";
import { motion } from "framer-motion";

interface Particle {
  id: number;
  x: number;
  y: number;
  size: number;
  duration: number;
  delay: number;
  type: "firefly" | "petal" | "leaf" | "sparkle";
  color: string;
  drift: number;
}

const PARTICLE_COLORS = {
  firefly: ["#ffd700", "#ffec8b", "#fffacd", "#ffeb3b"],
  petal: ["#ffb7c5", "#ffc0cb", "#ffd1dc", "#ffe4e1"],
  leaf: ["#7BB661", "#4F8F57", "#8bc34a", "#689f38"],
  sparkle: ["#ffffff", "#fffacd", "#e0e0ff", "#ffe4b5"],
};

function ParticleShape({ type, size, color }: { type: string; size: number; color: string }) {
  const style: Record<string, React.CSSProperties> = {
    firefly: {
      width: size,
      height: size,
      borderRadius: "50%",
      background: `radial-gradient(circle, ${color} 0%, transparent 70%)`,
      animation: `candy-pulse ${2 + Math.random()}s ease-in-out infinite`,
      animationDelay: `${Math.random() * 2}s`,
    },
    petal: {
      width: size,
      height: size * 1.4,
      borderRadius: "50%",
      background: `radial-gradient(ellipse, ${color} 0%, transparent 70%)`,
      animation: `candy-float ${5 + Math.random() * 3}s ease-in-out infinite`,
      animationDelay: `${Math.random() * 5}s`,
    },
    leaf: {
      width: size,
      height: size,
      background: color,
      opacity: 0.6,
      borderRadius: "50% 0",
      animation: `candy-spin ${8 + Math.random() * 4}s linear infinite`,
      animationDelay: `${Math.random() * 8}s`,
    },
    sparkle: {
      width: size,
      height: size,
      background: `radial-gradient(circle, ${color} 0%, transparent 60%)`,
      animation: `candy-pulse ${1.5 + Math.random()}s ease-in-out infinite`,
      animationDelay: `${Math.random() * 1.5}s`,
    },
  };

  return <span className="absolute inline-block" style={style[type] || style.sparkle} />;
}

export default function AmbientParticles({ count = 12, types = ["firefly", "petal", "sparkle"] }: { count?: number; types?: string[] }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [isInView, setIsInView] = useState(false);
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const mq = window.matchMedia("(max-width: 640px)");
    setIsMobile(mq.matches);
    const handler = (e: MediaQueryListEvent) => setIsMobile(e.matches);
    mq.addEventListener("change", handler);

    const motionQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    setPrefersReducedMotion(motionQuery.matches);
    const motionHandler = (e: MediaQueryListEvent) => setPrefersReducedMotion(e.matches);
    motionQuery.addEventListener("change", motionHandler);

    return () => {
      mq.removeEventListener("change", handler);
      motionQuery.removeEventListener("change", motionHandler);
    };
  }, []);

  useEffect(() => {
    const node = containerRef.current;
    if (!node) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        setIsInView(entry.isIntersecting);
      },
      { threshold: 0.1 }
    );

    observer.observe(node);
    return () => observer.disconnect();
  }, []);

  const particles = useMemo(() => {
    if (prefersReducedMotion) return [];
    const effectiveCount = isMobile ? Math.floor(count / 3) : count;
    return Array.from({ length: effectiveCount }, (_, i) => ({
      id: i,
      x: Math.random() * 100,
      y: Math.random() * 100,
      size: Math.random() * 6 + 3,
      duration: Math.random() * 15 + 10,
      delay: Math.random() * 8,
      type: types[Math.floor(Math.random() * types.length)] as Particle["type"],
      color: PARTICLE_COLORS[types[Math.floor(Math.random() * types.length)] as keyof typeof PARTICLE_COLORS]?.[Math.floor(Math.random() * 4)] || "#ffffff",
      drift: (Math.random() - 0.5) * 20,
    }));
  }, [count, types, prefersReducedMotion, isMobile]);

  if (prefersReducedMotion || !isInView) return null;

  return (
    <div ref={containerRef} className="absolute inset-0 overflow-hidden pointer-events-none" aria-hidden="true">
      {particles.map((particle) => (
        <motion.span
          key={particle.id}
          className="absolute inline-block"
          initial={{ x: `${particle.x}%`, y: `${particle.y}%`, opacity: 0 }}
          animate={{
            x: [`${particle.x}%`, `${particle.x + particle.drift}%`, `${particle.x}%`],
            y: [`${particle.y}%`, `${particle.y - 10}%`, `${particle.y + 8}%`, `${particle.y}%`],
            opacity: [0, 0.7, 0.5, 0.8, 0],
          }}
          transition={{
            duration: particle.duration,
            delay: particle.delay,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        >
          <ParticleShape type={particle.type} size={particle.size} color={particle.color} />
        </motion.span>
      ))}
    </div>
  );
}
