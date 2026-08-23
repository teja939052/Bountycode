import { useEffect, useRef, useState } from "react";

/**
 * Falling Leaves Background — subtle green leaves drifting downward.
 * 
 * Visual cue for the "green theme" / "growth / progress" motif.
 * Very low opacity so it doesn't distract from foreground content.
 * Respects `prefers-reduced-motion`.
 */
export function LeavesBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Resize canvas to fill the viewport
    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resize();
    window.addEventListener("resize", resize);

    // Leaf data structure
    type Leaf = {
      x: number;
      y: number;
      size: number;
      speed: number;
      rotation: number;
      rotationSpeed: number;
    };

    const leaves: Leaf[] = [];
    const leafCount = 30 + Math.random() * 20; // 30–50 leaves

    for (let i = 0; i < leafCount; i++) {
      leaves.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height - canvas.height,
        size: 8 + Math.random() * 16,
        speed: 0.5 + Math.random() * 1.5,
        rotation: Math.random() * 360,
        rotationSpeed: (Math.random() - 0.5) * 2,
      });
    }

    // Green gradient for leaves
    const leafGradient = ctx.createLinearGradient(0, 0, 0, leafCount * 20);
    leafGradient.addColorStop(0, "#22C55E");
    leafGradient.addColorStop(0.5, "#16A34A");
    leafGradient.addColorStop(1, "#15803D");

    let animationId: number;

    function drawLeaf(ctx: CanvasRenderingContext2D, leaf: Leaf) {
      ctx.save();
      ctx.translate(leaf.x, leaf.y);
      ctx.rotate((leaf.rotation * Math.PI) / 180);

      ctx.fillStyle = leafGradient;
      ctx.beginPath();
      // Simple leaf shape: base + two lobes
      ctx.moveTo(0, -leaf.size);
      ctx.bezierCurveTo(leaf.size * 0.3, -leaf.size * 0.25, leaf.size * 0.3, leaf.size * 0.25, 0, leaf.size * 0.5);
      ctx.bezierCurveTo(-leaf.size * 0.3, leaf.size * 0.25, -leaf.size * 0.3, -leaf.size * 0.25, 0, -leaf.size);
      ctx.closePath();
      ctx.fill();
      ctx.globalAlpha = 0.12;
      ctx.restore();
    }

    function animate() {
      if (!mounted) return;

      ctx.clearRect(0, 0, canvas.width, canvas.height);

      leaves.forEach((leaf) => {
        leaf.y += leaf.speed;
        leaf.rotation += leaf.rotationSpeed;

        // Wrap around — if leaf goes below viewport, reset to top
        if (leaf.y > canvas.height + leaf.size) {
          leaf.y = -leaf.size;
          leaf.x = Math.random() * canvas.width;
          leaf.rotation = Math.random() * 360;
        }

        drawLeaf(ctx, leaf);
      });

      animationId = requestAnimationFrame(animate);
    }

    animate();

    const handleResize = () => {
      resize();
    };
    window.addEventListener("resize", handleResize);

    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)");

    if (reduced.matches) {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      animationId = undefined;
    }

    return () => {
      window.removeEventListener("resize", handleResize);
      if (animationId) cancelAnimationFrame(animationId);
      setMounted(false);
    };
  }, []);

  if (!mounted) return null;

  return <canvas ref={canvasRef} className="fixed inset-0 pointer-events-none z-0" />;
}