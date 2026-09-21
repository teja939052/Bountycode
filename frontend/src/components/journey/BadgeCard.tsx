import { useState, useEffect, useReducedMotion } from "react";
import { motion } from "framer-motion";

export default function BadgeCard({
  userId,
  cleared,
}: {
  userId: string;
  cleared: Array<{ id: string; adventure_name: string }>;
}) {
  const [copied, setCopied] = useState(false);
  const reduceMotion = useReducedMotion();
  const badgeUrl = `/api/v1/gamification/badge/${encodeURIComponent(userId)}.svg`;
  const snippet = `<img src="${badgeUrl}" alt="BountyCode voyage rank" />`;
  const copy = async () => {
    try {
      await navigator.clipboard.writeText(snippet);
    } catch {
      window.prompt("Copy your badge embed:", snippet);
      return;
    }
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1600);
  };
  return (
    <motion.div
      initial={reduceMotion ? false : { y: 12, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="mb-3 rounded-2xl border border-accent-warm/30 bg-card p-4"
    >
      <div className="flex items-center gap-3">
        <img src={badgeUrl} alt="Your BountyCode voyage rank badge" className="h-12 w-auto rounded-lg" loading="lazy" />
        <div className="flex-1 min-w-0">
          <p className="text-sm font-bold text-primary">
            🏅 {cleared.length === 1 ? "World cleared" : `${cleared.length} worlds cleared`} — take the proof with you
          </p>
          <p className="text-[11px] text-muted truncate">
            Latest: {cleared[cleared.length - 1]?.adventure_name}. Embed it on GitHub or your resume.
          </p>
        </div>
        <button
          onClick={copy}
          className="shrink-0 rounded-xl bg-accent-warm px-3 py-2 text-xs font-bold text-white"
        >
          {copied ? "Copied!" : "Copy embed"}
        </button>
      </div>
    </motion.div>
  );
}
