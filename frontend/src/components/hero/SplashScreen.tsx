import { useState, useEffect } from "react";
import { motion } from "framer-motion";

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
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.6, opacity: 0 }}
        transition={{ duration: 0.6, ease: "backOut" }}
        className="flex items-center justify-center gap-4"
      >
        <div className="relative w-24 h-24">
          <img
            src="/assets/logo/bountycode-icon.svg"
            alt="BountyCode triquetra logo"
            className="w-full h-full drop-shadow-[0_20px_40px_rgba(23,33,27,0.15)]"
          />
          <div className="absolute inset-0 rounded-full border-2 border-[#5BA7A0]/30 animate-ping" />
        </div>
        <div className="text-[#17211B] font-display font-extrabold tracking-tight text-3xl">
          BountyCode
        </div>
      </motion.div>
    </motion.div>
  );
}
