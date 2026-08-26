import React, { useRef, useEffect, useState } from "react";

interface TsParticlesConfig {
  particles: {
    number: { value: number; density: { enable: boolean; area_x: number; area_y: number } };
    color: { value: string };
    shape: { type: string; stroke: { width: number; color: string } };
    opacity: { value: number; random: boolean };
    size: { value: number; random: boolean };
    line_linked: { enable: boolean; distance: number; color: string; opacity: number; width: number };
    move: { enable: boolean; speed: number; direction: string; random: boolean; straight: boolean; out_mode: string; bounce: boolean };
    array?: any[];
  };
  interactivity: {
    detect_on: string;
    events: {
      onhover: { enable: boolean; mode: string };
      onclick: { enable: boolean; mode: string };
      resize: boolean;
    };
    modes: {
      grab: { distance: number; line_linked: { opacity: number, width: number } };
      bubble: { distance: number; size: number, duration: number };
      repulse: { distance: number; duration: number };
      push: { particles_nb: number };
      remove: { particles_nb: number };
    };
  };
  retina_detect: boolean;
  fps_limit: number;
}

export default function ArrakisBackground({ reducedMotion = false }: { reducedMotion?: boolean }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [canvasHeight, setCanvasHeight] = useState(0);

  useEffect(() => {
    if (!canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d')!;
    const particles: any[] = [];
    let animationId: number | null = null;

    // Respect reduced motion
    if (reducedMotion) {
      canvas.style.display = 'none';
      return;
    }

    // Set initial canvas size based on parent container
    function resize() {
      if (canvasRef.current) {
        const parent = canvasRef.current.parentElement;
        const rect = parent.getBoundingClientRect();
        canvas.width = rect.width;
        canvas.height = rect.height;
        setCanvasHeight(rect.height);
      }
    }
    resize();
    window.addEventListener('resize', resize);

    // Sand grain particle class
    class Particle {
      x: number;
      y: number;
      vx: number;
      vy: number;
      radius: number;
      hue: number;
      opacity: number;
      
      constructor() {
        // Start at random position within canvas
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        // Sand-like colors: warm browns, light oranges - 30-50 degree hue range
        this.hue = 35 + Math.random() * 15; // 35-50 degree range (warm sand tones)
        this.radius = Math.random() * 2 + 0.5;
        this.opacity = 0.5 + Math.random() * 0.3; // 0.5-0.8 opacity
        this.vx = (Math.random() - 0.5) * 0.3; // Very slow, smooth movement
        this.vy = (Math.random() - 0.5) * 0.3;
      }

      update() {
        this.x += this.vx;
        this.y += this.vy;

        // Wrap around edges with seamless loop
        if (this.x > canvas.width + this.radius) this.x = -this.radius;
        if (this.x < -this.radius) this.x = canvas.width + this.radius;
        if (this.y > canvas.height + this.radius) this.y = -this.radius;
        if (this.y < -this.radius) this.y = canvas.height + this.radius;
      }

      draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        // Sand color with varying opacity - warm beige tones
        // Using #E9D6A3 (sand) and #FDF6EB (sand-soft) color palette
        const sandColor = `rgba(233, 214, 163, ${this.opacity * 0.6})`; // #E9D6A3 with opacity
        ctx.fillStyle = sandColor;
        ctx.fill();
      }
    }

    // Initialize particles - limited count for performance and calm effect
    const particleCount = Math.min(20, Math.floor((canvas.width * canvas.height) / 50000));
    for (let i = 0; i < particleCount; i++) {
      particles.push(new Particle());
    }

    // Animation loop
    function animate() {
      // Clear with sand gradient background
      if (canvas.height > 0) {
        const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
        gradient.addColorStop(0, '#FDF6EB'); // sand-soft top
        gradient.addColorStop(1, '#E9D6A3'); // sand bottom
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
      }

      particles.forEach(p => {
        p.update();
        p.draw();
      });

      animationId = requestAnimationFrame(animate);
    }

    animate();

    // Cleanup
    return () => {
      if (animationId) cancelAnimationFrame(animationId);
      window.removeEventListener('resize', resize);
    };
  }, [reducedMotion, canvasHeight]);

  return (
    <canvas
      ref={canvasRef}
      className="absolute inset-0 z-0"
      style={{ height: '100%' }}
    />
  );
}