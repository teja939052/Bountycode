import { ShieldCheck, Users } from "lucide-react";

// Matches the exam-memory crowd gate (VERIFY_THRESHOLD = 5 independent
// reporters). 1 report is a single recollection — never surfaced as verified.
const CONFIRMED_THRESHOLD = 5;

export default function TestTakerAttestation({ count }: { count?: number }) {
  if (typeof count !== "number" || count < 1) return null;
  const confirmed = count >= CONFIRMED_THRESHOLD;
  const Icon = confirmed ? ShieldCheck : Users;
  const label = confirmed
    ? `Confirmed by ${count} test-takers`
    : count === 1
    ? "Reported by 1 test-taker"
    : `Reported by ${count} test-takers`;
  return (
    <span
      className={
        confirmed
          ? "inline-flex items-center gap-1 rounded-full bg-emerald-50 border border-emerald-200 px-2 py-0.5 font-mono text-[9px] normal-case text-emerald-700"
          : "inline-flex items-center gap-1 rounded-full bg-amber-50 border border-amber-200 px-2 py-0.5 font-mono text-[9px] normal-case text-amber-700"
      }
      title={
        confirmed
          ? "5+ independent test-takers reported this question; it is part of the reviewed bank."
          : "Independent test-taker recollection awaiting corroboration."
      }
    >
      <Icon size={10} />
      {label}
    </span>
  );
}