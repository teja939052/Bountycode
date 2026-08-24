import React, { useRef, useEffect } from "react";

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

    // Set canvas size
    function resize() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    // Particle class
    class Particle {
      x: number;
      y: number;
      vx: number;
      vy: number;
      radius: number;
      hue: number;
      
      constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.vx = (Math.random() - 0.5) * 2;
        this.vy = (Math.random() - 0.5) * 2;
        this.radius = Math.random() * 2 + 1;
        this.hue = Math.random() * 360;
      }

      update() {
        this.x += this.vx;
        this.y += this.vy;

        // Wrap around edges
        if (this.x > canvas.width + this.radius) this.x = -this.radius;
        if (this.x < -this.radius) this.x = canvas.width + this.radius;
        if (this.y > canvas.height + this.radius) this.y = -this.radius;
        if (this.y < -this.radius) this.y = canvas.height + this.radius;
      }

      draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = `hsl(${this.hue}, 70%, 70%)`;
        ctx.fill();
      }
    }

    // Initialize particles
    const particleCount = Math.min(50, Math.floor((canvas.width * canvas.height) / 15000));
    for (let i = 0; i < particleCount; i++) {
      particles.push(new Particle());
    }

    // Connection function
    function connectParticles() {
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
      const dx = particles[i].x - particles[j].x;
      const dy = particles[i].y - particles[j].y;
      const distance = Math.sqrt(dx * dx + dy * dy);

      if (distance < 150) {
        ctx.beginPath();
        ctx.moveTo(particles[i].x, particles[i].y);
        ctx.lineTo(particles[j].x, particles[j].y);
        ctx.strokeStyle = `rgba(34, 197, 94, ${1 - distance / 150 * 0.5})`;
        ctx.lineWidth = 1;
        ctx.stroke();
      }
    }
      }
    }

    // Animation loop
    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Background gradient
      const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
      gradient.addColorStop(0, '#0a0a1e');
      gradient.addColorStop(1, '#1a1a3a');
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      particles.forEach(p => {
        p.update();
        p.draw();
      });

      connectParticles();

      animationId = requestAnimationFrame(animate);
    }

    animate();

    // Cleanup
    return () => {
      if (animationId) cancelAnimationFrame(animationId);
      window.removeEventListener('resize', resize);
    };
  }, [reducedMotion]);

  return (
    <canvas
      ref={canvasRef}
      className="absolute inset-0"
      style={{ background: 'transparent' }}
    />
  );
}