import { useEffect, useRef, useState } from "react";

export default function AnimatedNumber({ value, duration = 800, className = "" }) {
  const [display, setDisplay] = useState(0);
  const ref = useRef(null);
  const startRef = useRef(0);
  const startTimeRef = useRef(null);

  useEffect(() => {
    const target = typeof value === "number" ? value : parseInt(value, 10) || 0;
    startRef.current = display;
    startTimeRef.current = null;

    if (ref.current) cancelAnimationFrame(ref.current);

    const step = (timestamp) => {
      if (!startTimeRef.current) startTimeRef.current = timestamp;
      const progress = Math.min((timestamp - startTimeRef.current) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = Math.round(startRef.current + (target - startRef.current) * eased);
      setDisplay(current);
      if (progress < 1) {
        ref.current = requestAnimationFrame(step);
      }
    };

    ref.current = requestAnimationFrame(step);
    return () => {
      if (ref.current) cancelAnimationFrame(ref.current);
    };
  }, [value, duration]);

  return <span className={className}>{display}</span>;
}
