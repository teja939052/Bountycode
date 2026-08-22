import { useEffect, useState } from "react";
import { motion, useSpring, useMotionValue } from "framer-motion";
import useReducedMotion from "../hooks/useReducedMotion";
import useMediaQuery from "../hooks/useMediaQuery";

const DOT_SIZE = 10;
const CIRCLE_SIZE = 40;
const RING_HOVER_SIZE = 56;
const RED = "#e8390e";
const INK = "#0c0906";

export default function CustomCursor() {
  const [hovered, setHovered] = useState(false);
  const reduced = useReducedMotion();
  const isTouch = typeof navigator !== "undefined" && "ontouchstart" in window;
  const isMobile = useMediaQuery("(hover: none)");

  // Dot tracks mouse directly (instant); ring lags behind (spring).
  const dotX = useMotionValue(0);
  const dotY = useMotionValue(0);
  const ringX = useSpring(0, { damping: 25, stiffness: 150 });
  const ringY = useSpring(0, { damping: 25, stiffness: 150 });

  useEffect(() => {
    if (reduced || isTouch || isMobile) return;

    document.body.style.cursor = "none";

    const handleMouseMove = (e: MouseEvent) => {
      dotX.set(e.clientX);
      dotY.set(e.clientY);
      ringX.set(e.clientX);
      ringY.set(e.clientY);
    };

    window.addEventListener("mousemove", handleMouseMove, { passive: true });

    const selector =
      "a, button, [role='button'], input, textarea, select, label, summary";

    const addHover = () => setHovered(true);
    const removeHover = () => setHovered(false);

    const attachListeners = () => {
      document.querySelectorAll(selector).forEach((el) => {
        el.addEventListener("mouseenter", addHover);
        el.addEventListener("mouseleave", removeHover);
      });
    };

    const observer = new MutationObserver(attachListeners);
    observer.observe(document.body, { childList: true, subtree: true });
    attachListeners();

    const handleMouseLeave = () => {
      document.body.style.cursor = "";
    };
    const handleMouseEnter = () => {
      document.body.style.cursor = "none";
    };

    document.addEventListener("mouseleave", handleMouseLeave);
    document.addEventListener("mouseenter", handleMouseEnter);

    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      document.removeEventListener("mouseleave", handleMouseLeave);
      document.removeEventListener("mouseenter", handleMouseEnter);
      observer.disconnect();
      dotX.stop();
      dotY.stop();
      ringX.stop();
      ringY.stop();
      document.body.style.cursor = "";
    };
  }, [reduced, isTouch, isMobile, dotX, dotY, ringX, ringY]);

  if (reduced || isTouch || isMobile) return null;

  return (
    <>
      <motion.div
        className="fixed top-0 left-0 rounded-full pointer-events-none z-[9999]"
        style={{
          width: DOT_SIZE,
          height: DOT_SIZE,
          backgroundColor: RED,
          x: dotX,
          y: dotY,
        }}
        animate={{ scale: hovered ? 1.6 : 1 }}
        transition={{ type: "spring", stiffness: 300, damping: 20 }}
      />

      <motion.div
        className="fixed top-0 left-0 rounded-full pointer-events-none z-[9998] border"
        style={{
          x: ringX,
          y: ringY,
        }}
        animate={{
          width: hovered ? RING_HOVER_SIZE : CIRCLE_SIZE,
          height: hovered ? RING_HOVER_SIZE : CIRCLE_SIZE,
          borderColor: hovered ? RED : INK,
        }}
        transition={{ type: "tween", duration: 0.15 }}
      />
    </>
  );
}
