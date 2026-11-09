import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { BountyTriquetra } from "../brand/BountyTriquetra";

export default function SplashScreen() {
  const [show, setShow] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => setShow(false), 1800);
    return () => clearTimeout(timer);
  }, []);

  if (!show) return null;

  return (
    <motion.div
      initial={{ opacity: 1 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.8, ease: "easeInOut" }}
      className="fixed inset-0 z-[1000] flex items-center justify-center bg-[#fbe4ec]"
    >
      <motion.div
        initial={{ scale: 0.7, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.5, opacity: 0 }}
        transition={{ duration: 0.7, ease: "backOut" }}
        className="flex items-center justify-center gap-5"
      >
        <div className="relative w-32 h-32">
          <BountyTriquetra className="w-full h-full" variant="cyan" />
          <div className="absolute inset-0 rounded-full border-2 border-[#28D3C5]/40 animate-ping" />
        </div>
        <div className="text-[#17211B] font-display font-extrabold tracking-tight text-5xl tracking-tighter">
          BountyCode
        </div>
      </motion.div>
    </motion.div>
  );
}
