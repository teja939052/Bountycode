import { motion } from "framer-motion";
import useReducedMotion from "../../hooks/useReducedMotion";

const SHARDS = [
  {
    className: "left-[8%] top-[10%] h-44 w-44 rounded-[2.5rem]",
    style: "bg-brand-sky/20 border-brand-sky/20",
    animate: { y: [0, -10, 0], x: [0, 8, 0], rotate: [8, 14, 8] },
  },
  {
    className: "right-[8%] top-[16%] h-32 w-32 rounded-[1.75rem]",
    style: "bg-brand-lavender/16 border-brand-lavender/18",
    animate: { y: [0, 12, 0], x: [0, -8, 0], rotate: [-10, -4, -10] },
  },
  {
    className: "left-[14%] bottom-[12%] h-24 w-24 rounded-[1.5rem]",
    style: "bg-brand-gold/14 border-brand-gold/16",
    animate: { y: [0, -8, 0], x: [0, 6, 0], rotate: [28, 22, 28] },
  },
  {
    className: "right-[20%] bottom-[18%] h-36 w-36 rounded-[2rem]",
    style: "bg-brand-teal/12 border-brand-teal/15",
    animate: { y: [0, -14, 0], x: [0, 10, 0], rotate: [-6, 2, -6] },
  },
];

export default function SpaceBackground() {
  const reduced = useReducedMotion();

  return (
    <div className="fixed inset-0 z-0 overflow-hidden pointer-events-none">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(72,149,239,0.16),transparent_34%),radial-gradient(circle_at_80%_10%,rgba(124,109,175,0.14),transparent_28%),radial-gradient(circle_at_18%_88%,rgba(42,157,143,0.12),transparent_26%),linear-gradient(180deg,#F9F5EF_0%,#F4EFE8_45%,#EFE8DF_100%)]" />
      <div className="absolute inset-0 bg-[linear-gradient(rgba(11,16,32,0.035)_1px,transparent_1px),linear-gradient(90deg,rgba(11,16,32,0.035)_1px,transparent_1px)] bg-[size:56px_56px] opacity-40" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,transparent_0,transparent_52%,rgba(11,16,32,0.06)_100%)]" />

      <div className="absolute inset-x-0 top-0 h-28 bg-gradient-to-b from-white/55 to-transparent" />
      <div className="absolute inset-x-0 bottom-0 h-28 bg-gradient-to-t from-white/30 to-transparent" />

      {!reduced && (
        <div className="absolute inset-0">
          <motion.div
            className="absolute left-[4%] top-[18%] h-72 w-72 rounded-full bg-brand-sky/12 blur-3xl"
            animate={{ scale: [1, 1.08, 1], opacity: [0.45, 0.65, 0.45] }}
            transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
          />
          <motion.div
            className="absolute right-[5%] top-[12%] h-80 w-80 rounded-full bg-brand-lavender/10 blur-3xl"
            animate={{ scale: [1, 0.92, 1], opacity: [0.35, 0.55, 0.35] }}
            transition={{ duration: 12, repeat: Infinity, ease: "easeInOut" }}
          />
          <motion.div
            className="absolute left-1/2 bottom-[8%] h-80 w-80 -translate-x-1/2 rounded-full bg-brand-teal/10 blur-3xl"
            animate={{ y: [0, -10, 0], opacity: [0.28, 0.44, 0.28] }}
            transition={{ duration: 9, repeat: Infinity, ease: "easeInOut" }}
          />

          {SHARDS.map((shard, index) => (
            <motion.div
              key={shard.className}
              className={`absolute hidden md:block border backdrop-blur-sm ${shard.className} ${shard.style}`}
              animate={shard.animate}
              transition={{
                duration: 8 + index,
                repeat: Infinity,
                ease: "easeInOut",
              }}
            >
              <div className="absolute inset-0 rounded-[inherit] bg-white/5" />
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
