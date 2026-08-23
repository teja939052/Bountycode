/**
 * Mentor — Captain Byte, the deterministic guide.
 *
 * Rules (DESIGN FREEZE V2):
 * - One character, consistent personality: warm, wry, never sarcastic at user's expense.
 * - Dialogue comes from state, NOT random strings.
 * - Appears in: onboarding, mission start, boss intro, reward reveal, stuck states.
 * - SVG only — no emoji, no raster images.
 */

export type MentorMood =
  | "welcome"    // first meeting / landing
  | "briefing"   // mission start
  | "proud"      // after success
  | "encouraging" // after failure / struggle
  | "serious"    // boss battle
  | "celebrating"; // big win

interface MentorProps {
  mood?: MentorMood;
  message: string;
  /** Compact = avatar + speech bubble inline; full = larger card */
  size?: "compact" | "full";
  className?: string;
}

/** SVG portrait of Captain Byte — original design, geometric-adventure style. */
export function MentorAvatar({ size = 64, mood = "welcome" }: { size?: number; mood?: MentorMood }) {
  const accent =
    mood === "serious" ? "#E96A5B" :
    mood === "celebrating" || mood === "proud" ? "#EAB74D" :
    mood === "encouraging" ? "#5BA7A0" : "#22C55E";

  return (
    <svg width={size} height={size} viewBox="0 0 64 64" fill="none" aria-hidden="true">
      {/* Head */}
      <rect x="14" y="12" width="36" height="32" rx="8" fill="#F5EFE8" stroke="#A8754F" strokeWidth="2.5" />
      {/* Bandana */}
      <path d="M14 20c6-4 30-4 36 0v-3c0-4-3-7-7-7H21c-4 0-7 3-7 7v3z" fill={accent} />
      <path d="M46 16l8-3-5 7" fill={accent} stroke={accent} strokeWidth="1.5" strokeLinejoin="round" />
      <circle cx="18" cy="17" r="1.2" fill="#FFFFFF" opacity="0.7" />
      <circle cx="24" cy="15.5" r="1.2" fill="#FFFFFF" opacity="0.7" />
      {/* Eyes — expression varies with mood */}
      {mood === "serious" ? (
        <>
          <line x1="23" y1="29" x2="29" y2="31" stroke="#17211B" strokeWidth="2.5" strokeLinecap="round" />
          <line x1="41" y1="29" x2="35" y2="31" stroke="#17211B" strokeWidth="2.5" strokeLinecap="round" />
        </>
      ) : (
        <>
          <circle cx="26" cy="30" r="2.6" fill="#17211B" />
          <circle cx="38" cy="30" r="2.6" fill="#17211B" />
          <circle cx="27" cy="29" r="0.9" fill="#FFFFFF" />
          <circle cx="39" cy="29" r="0.9" fill="#FFFFFF" />
        </>
      )}
      {/* Mouth */}
      {mood === "celebrating" ? (
        <path d="M25 38q7 6 14 0" stroke="#17211B" strokeWidth="2.2" strokeLinecap="round" fill="none" />
      ) : mood === "encouraging" ? (
        <path d="M26 39h12" stroke="#17211B" strokeWidth="2.2" strokeLinecap="round" />
      ) : (
        <path d="M26 38q6 4 12 0" stroke="#17211B" strokeWidth="2.2" strokeLinecap="round" fill="none" />
      )}
      {/* Scar detail — character depth */}
      <path d="M44 26l3 6" stroke="#C9A47E" strokeWidth="1.5" strokeLinecap="round" />
      {/* Collar */}
      <path d="M20 44h24l4 8H16l4-8z" fill="#5BA7A0" />
      {/* Gold earring */}
      <circle cx="49" cy="34" r="2" stroke="#EAB74D" strokeWidth="2" fill="none" />
    </svg>
  );
}

export function Mentor({ mood = "welcome", message, size = "compact", className = "" }: MentorProps) {
  const avatarSize = size === "full" ? 88 : 56;

  if (size === "full") {
    return (
      <div className={`bounty-card flex items-start gap-4 p-5 ${className}`}>
        <div className="shrink-0">
          <MentorAvatar size={avatarSize} mood={mood} />
        </div>
        <div className="min-w-0">
          <p className="adventure-label mb-1">Captain Byte</p>
          <p className="text-sm leading-relaxed text-text">{message}</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`flex items-center gap-3 ${className}`}>
      <MentorAvatar size={avatarSize} mood={mood} />
      <div className="surface-bg surface-border relative rounded-xl border px-4 py-2.5 shadow-card">
        <p className="text-sm leading-snug text-text">
          <span className="font-bold text-primary-dark">Captain Byte:</span> {message}
        </p>
      </div>
    </div>
  );
}
