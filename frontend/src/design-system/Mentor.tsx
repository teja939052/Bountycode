// @ts-nocheck
/**
 * Mentor — Captain Byte, the deterministic guide.
 *
 * Rules:
 * - One character, consistent personality: warm, wry, never sarcastic at user's expense.
 * - Dialogue comes from state, NOT random strings.
 * - Appears in: onboarding, mission start, boss intro, reward reveal, stuck states.
 * - SVG only — no emoji, no raster images.
 */

export type MentorMood =
  | "welcome"
  | "briefing"
  | "explaining"
  | "correcting"
  | "encouraging"
  | "proud"
  | "celebrating"
  | "serious"
  | "thinking"
  | "stuck"
  | "handoff";

interface MentorProps {
  mood?: MentorMood;
  message: string;
  /** Compact = avatar + speech bubble inline; full = larger card */
  size?: "compact" | "full";
  className?: string;
}

const ACCENT_BY_MOOD: Record<MentorMood, string> = {
  welcome: "#22C55E",
  briefing: "#22C55E",
  explaining: "#5BA7A0",
  correcting: "#5BA7A0",
  encouraging: "#5BA7A0",
  proud: "#EAB74D",
  celebrating: "#EAB74D",
  serious: "#E96A5B",
  thinking: "#22C55E",
  stuck: "#f59e0b",
  handoff: "#22C55E",
};

export function MentorAvatar({ size = 64, mood = "welcome" }: { size?: number; mood?: MentorMood }) {
  const accent = ACCENT_BY_MOOD[mood] || "#22C55E";
  const isSerious = mood === "serious";
  const isStuck = mood === "stuck";
  const isThinking = mood === "thinking";
  const isExplaining = mood === "explaining";
  const isCorrecting = mood === "correcting";

  return (
    <svg width={size} height={size} viewBox="0 0 64 64" fill="none" aria-hidden="true">
      {/* Head */}
      <rect x="14" y="12" width="36" height="32" rx="8" fill="#F5EFE8" stroke="#A8754F" strokeWidth="2.5" />
      {/* Bandana */}
      <path d="M14 20c6-4 30-4 36 0v-3c0-4-3-7-7-7H21c-4 0-7 3-7 7v3z" fill={accent} />
      <path d="M46 16l8-3-5 7" fill={accent} stroke={accent} strokeWidth="1.5" strokeLinejoin="round" />
      <circle cx="18" cy="17" r="1.2" fill="#FFFFFF" opacity="0.7" />
      <circle cx="24" cy="15.5" r="1.2" fill="#FFFFFF" opacity="0.7" />

      {/* Eyebrows */}
      {isStuck && (
        <>
          <path d="M22 26l4 2" stroke="#17211B" strokeWidth="1.8" strokeLinecap="round" />
          <path d="M38 26l-4 2" stroke="#17211B" strokeWidth="1.8" strokeLinecap="round" />
        </>
      )}
      {isSerious && (
        <>
          <path d="M22 26l5 2" stroke="#17211B" strokeWidth="1.8" strokeLinecap="round" />
          <path d="M37 26l-5 2" stroke="#17211B" strokeWidth="1.8" strokeLinecap="round" />
        </>
      )}
      {isThinking && (
        <>
          <path d="M21 26l3 1.5" stroke="#17211B" strokeWidth="1.8" strokeLinecap="round" />
          <path d="M40 26l-3 1.5" stroke="#17211B" strokeWidth="1.8" strokeLinecap="round" />
        </>
      )}

      {/* Eyes */}
      {isSerious || isCorrecting ? (
        <>
          <line x1="23" y1="29" x2="29" y2="31" stroke="#17211B" strokeWidth="2.5" strokeLinecap="round" />
          <line x1="41" y1="29" x2="35" y2="31" stroke="#17211B" strokeWidth="2.5" strokeLinecap="round" />
        </>
      ) : isStuck ? (
        <>
          <circle cx="26" cy="30.5" r="2.4" fill="#17211B" />
          <circle cx="38" cy="30.5" r="2.4" fill="#17211B" />
          <circle cx="24.5" cy="29.5" r="0.8" fill="#FFFFFF" opacity="0.8" />
          <circle cx="36.5" cy="29.5" r="0.8" fill="#FFFFFF" opacity="0.8" />
        </>
      ) : isThinking ? (
        <>
          <circle cx="26" cy="29" r="2.4" fill="#17211B" />
          <circle cx="38" cy="31" r="2.4" fill="#17211B" />
          <circle cx="27" cy="28" r="0.8" fill="#FFFFFF" opacity="0.8" />
          <circle cx="39" cy="30" r="0.8" fill="#FFFFFF" opacity="0.8" />
        </>
      ) : isExplaining ? (
        <>
          <circle cx="25" cy="30" r="2.4" fill="#17211B" />
          <circle cx="39" cy="30" r="2.4" fill="#17211B" />
          <circle cx="26" cy="29" r="0.8" fill="#FFFFFF" opacity="0.8" />
          <circle cx="40" cy="29" r="0.8" fill="#FFFFFF" opacity="0.8" />
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
      ) : mood === "encouraging" || mood === "handoff" ? (
        <path d="M26 39h12" stroke="#17211B" strokeWidth="2.2" strokeLinecap="round" />
      ) : mood === "correcting" || mood === "serious" ? (
        <path d="M26 40h12" stroke="#17211B" strokeWidth="2.2" strokeLinecap="round" />
      ) : mood === "stuck" ? (
        <path d="M26 41q6-2 12 0" stroke="#17211B" strokeWidth="2.2" strokeLinecap="round" fill="none" />
      ) : mood === "thinking" ? (
        <circle cx="32" cy="40" r="1.4" fill="#17211B" />
      ) : mood === "explaining" ? (
        <path d="M28 39c1 2 8 2 8 0" stroke="#17211B" strokeWidth="2.2" strokeLinecap="round" fill="none" />
      ) : (
        <path d="M26 38q6 4 12 0" stroke="#17211B" strokeWidth="2.2" strokeLinecap="round" fill="none" />
      )}

      {/* Scar detail */}
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
