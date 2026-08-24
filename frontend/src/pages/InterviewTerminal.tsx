import { useCallback, useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import {
  Mic,
  MicOff,
  Send,
  Swords,
  Target,
  Volume2,
  VolumeX,
  Anchor,
} from "lucide-react";
import {
  MasteryBar,
  MentorAvatar,
  PageShell,
  ReadinessRing,
} from "../design-system";
import { Button } from "../design-system/Button";
import { interviewChatApi } from "../services/api/interviewChat";
import type {
  ChatEndResponse,
  ChatMessage,
  ChatReport,
} from "../services/api/interviewChat";

const COMPANY_CHIPS = [
  "TCS",
  "Infosys",
  "Wipro",
  "Accenture",
  "Cognizant",
  "Amazon",
  "Swiggy",
  "Flipkart",
];

const ROUNDS = [
  {
    id: "service",
    name: "Service Deck",
    tag: "Mass Recruiter Round",
    desc: "Rapid-fire basics, OOPs, pseudo-code dry runs, output prediction. Panel pace: under a minute per answer.",
    icon: Target,
  },
  {
    id: "product",
    name: "Product Deck",
    tag: "Deep-Dive Round",
    desc: "One problem, pushed to its limits. Complexity, edge cases, scale, trade-offs. Byte follows your thread.",
    icon: Swords,
  },
] as const;

type Phase = "setup" | "session" | "report";

export default function InterviewTerminal() {
  const [phase, setPhase] = useState<Phase>("setup");
  const [roundType, setRoundType] = useState<string>("service");
  const [companyTarget, setCompanyTarget] = useState("TCS");
  const [jobRole, setJobRole] = useState("Software Engineer");
  const [difficulty, setDifficulty] = useState("medium");

  const [sessionId, setSessionId] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [turnCount, setTurnCount] = useState(0);
  const [turnsLeft, setTurnsLeft] = useState(30);
  const [briefing, setBriefing] = useState("");

  const [input, setInput] = useState("");
  const [starting, setStarting] = useState(false);
  const [sending, setSending] = useState(false);
  const [ending, setEnding] = useState(false);
  const [error, setError] = useState("");

  const [voiceOn, setVoiceOn] = useState(false);
  const [result, setResult] = useState<ChatEndResponse | null>(null);

  const transcriptRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    transcriptRef.current?.scrollTo({
      top: transcriptRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages, phase]);

  const speak = useCallback(
    (text: string) => {
      if (!voiceOn || typeof window.speechSynthesis === "undefined") return;
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 1.02;
      utterance.pitch = 0.9;
      window.speechSynthesis.speak(utterance);
    },
    [voiceOn],
  );

  useEffect(() => {
    return () => {
      if (typeof window.speechSynthesis !== "undefined") {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  async function handleStart() {
    setStarting(true);
    setError("");
    try {
      const res = await interviewChatApi.start(
        roundType,
        companyTarget || "general",
        jobRole || "Software Engineer",
        difficulty,
      );
      setSessionId(res.session_id);
      setMessages([{ role: "assistant", content: res.opener }]);
      setTurnsLeft(res.max_turns);
      setTurnCount(0);
      setBriefing(res.briefing);
      setResult(null);
      setPhase("session");
      speak(res.opener);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not start the interview");
    } finally {
      setStarting(false);
    }
  }

  async function handleSend() {
    const text = input.trim();
    if (!text || sending) return;
    setInput("");
    setMessages(prev => [...prev, { role: "user", content: text }]);
    setSending(true);
    setError("");
    try {
      const res = await interviewChatApi.submitTurn(sessionId, text);
      setMessages(prev => [...prev, { role: "assistant", content: res.reply }]);
      setTurnCount(res.turn_count);
      setTurnsLeft(res.turns_left);
      speak(res.reply);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Transmission failed — try again");
      setMessages(prev => prev.slice(0, -1));
      setInput(text);
    } finally {
      setSending(false);
      inputRef.current?.focus();
    }
  }

  async function handleEnd() {
    if (!confirm("Drop anchor and get your debrief?")) return;
    setEnding(true);
    setError("");
    try {
      const res = await interviewChatApi.end(sessionId);
      setResult(res);
      setPhase("report");
      if (typeof window.speechSynthesis !== "undefined") {
        window.speechSynthesis.cancel();
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not end the session");
    } finally {
      setEnding(false);
    }
  }

  function resetToSetup() {
    if (typeof window.speechSynthesis !== "undefined") {
      window.speechSynthesis.cancel();
    }
    setPhase("setup");
    setMessages([]);
    setSessionId("");
    setResult(null);
    setError("");
  }

  if (phase === "setup") {
    return (
      <PageShell theme="focus">
        <div className="mx-auto max-w-3xl px-4 py-8 md:py-12">
          <header className="mb-10 flex items-center gap-4">
            <MentorAvatar size={64} mood="serious" />
            <div>
              <p className="text-xs font-bold uppercase tracking-widest text-text-muted">
                Captain Byte at the helm
              </p>
              <h1 className="text-2xl font-extrabold text-text md:text-3xl">
                Interview Terminal
              </h1>
              <p className="text-sm text-text-muted">
                A live conversation — not a quiz. Byte asks, you answer, he digs deeper.
              </p>
            </div>
          </header>

          <section className="mb-6 grid gap-4 sm:grid-cols-2">
            {ROUNDS.map(round => {
              const active = roundType === round.id;
              const Icon = round.icon;
              return (
                <button
                  key={round.id}
                  onClick={() => setRoundType(round.id)}
                  aria-pressed={active}
                  className={`rounded-xl border-2 p-4 text-left transition-colors ${
                    active
                      ? "border-primary bg-mint/60"
                      : "border-line bg-surface hover:border-primary/40"
                  }`}
                >
                  <div className="mb-2 flex items-center gap-2">
                    <Icon
                      size={18}
                      className={active ? "text-primary" : "text-text-muted"}
                    />
                    <span className="font-bold text-text">{round.name}</span>
                  </div>
                  <p className="text-[11px] font-bold uppercase tracking-wider text-primary">
                    {round.tag}
                  </p>
                  <p className="mt-2 text-sm text-text-muted">{round.desc}</p>
                </button>
              );
            })}
          </section>

          <section className="bounty-card mb-6 space-y-4 p-5">
            <div>
              <label
                htmlFor="terminal-company"
                className="mb-1 block text-xs font-bold uppercase tracking-wider text-text-muted"
              >
                Company flavor
              </label>
              <input
                id="terminal-company"
                value={companyTarget}
                onChange={e => setCompanyTarget(e.target.value)}
                placeholder="e.g. TCS, Amazon, Swiggy"
                maxLength={60}
                className="w-full rounded-lg border border-line bg-surface px-3 py-2 text-sm text-text outline-none focus:border-primary"
              />
              <div className="mt-2 flex flex-wrap gap-1.5">
                {COMPANY_CHIPS.map(c => (
                  <button
                    key={c}
                    onClick={() => setCompanyTarget(c)}
                    className={`rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors ${
                      companyTarget === c
                        ? "border-primary bg-primary text-white"
                        : "border-line bg-surface text-text-muted hover:border-primary/50 hover:text-text"
                    }`}
                  >
                    {c}
                  </button>
                ))}
              </div>
            </div>

            <div className="grid gap-4 sm:grid-cols-2">
              <div>
                <label
                  htmlFor="terminal-role"
                  className="mb-1 block text-xs font-bold uppercase tracking-wider text-text-muted"
                >
                  Role
                </label>
                <input
                  id="terminal-role"
                  value={jobRole}
                  onChange={e => setJobRole(e.target.value)}
                  placeholder="Software Engineer"
                  maxLength={80}
                  className="w-full rounded-lg border border-line bg-surface px-3 py-2 text-sm text-text outline-none focus:border-primary"
                />
              </div>
              <div>
                <label
                  htmlFor="terminal-difficulty"
                  className="mb-1 block text-xs font-bold uppercase tracking-wider text-text-muted"
                >
                  Difficulty
                </label>
                <select
                  id="terminal-difficulty"
                  value={difficulty}
                  onChange={e => setDifficulty(e.target.value)}
                  className="w-full rounded-lg border border-line bg-surface px-3 py-2 text-sm text-text outline-none focus:border-primary"
                >
                  <option value="easy">Easy — calm seas</option>
                  <option value="medium">Medium — steady swell</option>
                  <option value="hard">Hard — storm watch</option>
                </select>
              </div>
            </div>
          </section>

          {error && (
            <p className="mb-4 rounded-lg border border-coral/30 bg-red-50 px-3 py-2 text-sm text-coral">
              {error}
            </p>
          )}

          <div className="flex items-center gap-3">
            <Button size="lg" loading={starting} onClick={handleStart}>
              <Anchor size={16} /> Begin Interview
            </Button>
            <Button variant="ghost" onClick={() => history.back()}>
              Cancel
            </Button>
          </div>

          <p className="mt-6 text-center text-sm text-text-muted">
            Prefer the classic format?{" "}
            <Link to="/interview" className="font-semibold text-ocean underline">
              Standard interview →
            </Link>
          </p>
        </div>
      </PageShell>
    );
  }

  if (phase === "session") {
    return (
      <PageShell theme="focus">
        <div className="mx-auto flex h-[calc(100vh-7rem)] max-w-3xl flex-col px-4 pt-6 md:h-screen">
          <header className="mb-3 flex items-center justify-between border-b border-line pb-3">
            <div className="flex items-center gap-3">
              <MentorAvatar size={44} mood="serious" />
              <div>
                <h1 className="text-sm font-extrabold text-text">
                  Captain Byte — {roundType === "service" ? "Service Deck" : "Product Deck"}
                </h1>
                <p className="text-xs text-text-muted">
                  {companyTarget} · {jobRole} · turn {turnCount}/{turnCount + turnsLeft}
                </p>
              </div>
            </div>
            <button
              onClick={() => setVoiceOn(v => !v)}
              aria-label={voiceOn ? "Mute Byte's voice" : "Speak Byte's replies"}
              title={voiceOn ? "Voice on" : "Voice off"}
              className={`flex h-9 w-9 items-center justify-center rounded-lg border transition-colors ${
                voiceOn
                  ? "border-primary bg-mint text-primary"
                  : "border-line bg-surface text-text-muted hover:text-text"
              }`}
            >
              {voiceOn ? <Volume2 size={17} /> : <VolumeX size={17} />}
            </button>
          </header>

          {briefing && (
            <p className="mb-3 rounded-lg border border-sky/25 bg-sky-50 px-3 py-2 text-xs font-medium text-ocean">
              {briefing}
            </p>
          )}

          <div
            ref={transcriptRef}
            className="min-h-0 flex-1 space-y-4 overflow-y-auto rounded-xl border border-line bg-surface p-4"
          >
            {messages.map((m, i) =>
              m.role === "assistant" ? (
                <div key={i} className="flex items-start gap-2.5">
                  <MentorAvatar size={32} mood="serious" />
                  <div className="max-w-[85%] rounded-2xl rounded-tl-sm border border-line bg-canvas px-3.5 py-2.5">
                    <p className="whitespace-pre-wrap text-sm leading-relaxed text-text">
                      {m.content}
                    </p>
                  </div>
                </div>
              ) : (
                <div key={i} className="flex justify-end">
                  <div className="max-w-[85%] whitespace-pre-wrap rounded-2xl rounded-tr-sm bg-primary px-3.5 py-2.5 text-sm leading-relaxed text-white">
                    {m.content}
                  </div>
                </div>
              ),
            )}
            {sending && (
              <div className="flex items-start gap-2.5 opacity-60">
                <MentorAvatar size={32} mood="serious" />
                <div className="rounded-2xl rounded-tl-sm border border-line bg-canvas px-3.5 py-2.5 text-sm text-text-muted">
                  Byte is thinking…
                </div>
              </div>
            )}
          </div>

          {error && (
            <p className="mt-2 rounded-lg border border-coral/30 bg-red-50 px-3 py-2 text-sm text-coral">
              {error}
            </p>
          )}

          <footer className="pt-3">
            <div className="flex items-end gap-2">
              <textarea
                ref={inputRef}
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={e => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    handleSend();
                  }
                }}
                rows={2}
                placeholder="Answer in your own words… (Enter to send)"
                disabled={sending}
                className="min-h-[52px] flex-1 resize-none rounded-xl border border-line bg-surface px-3.5 py-2.5 text-sm text-text outline-none focus:border-primary disabled:opacity-60"
              />
              <Button
                variant="primary"
                size="lg"
                loading={sending}
                disabled={!input.trim()}
                onClick={handleSend}
                aria-label="Send answer"
              >
                <Send size={16} />
              </Button>
            </div>
            <div className="mt-2 flex items-center justify-between">
              <p className="flex items-center gap-1 text-xs text-text-muted">
                {voiceOn ? <Mic size={12} /> : <MicOff size={12} />}
                {voiceOn ? "Byte speaks aloud" : "Voice muted"} · answers are typed
              </p>
              <Button variant="outline" size="sm" loading={ending} onClick={handleEnd}>
                End &amp; Debrief
              </Button>
            </div>
          </footer>
        </div>
      </PageShell>
    );
  }

  // report
  const report: ChatReport = result?.report ?? {};
  const breakdown = report.breakdown ?? {};
  const barTones = ["primary", "ocean", "tech", "gold"] as const;

  return (
    <PageShell theme="celebration">
      <div className="mx-auto max-w-3xl px-4 py-8 md:py-12">
        <header className="mb-8 flex flex-col items-center text-center">
          <ReadinessRing value={result?.final_score ?? 0} size={132} label="Debrief Score" />
          <h1 className="mt-4 text-2xl font-extrabold text-text">
            Session Complete
          </h1>
          <p className="max-w-md text-sm text-text-muted">
            {roundType === "service" ? "Service-deck drill" : "Product-deck dive"} ·{" "}
            {companyTarget} · logged for your readiness score.
          </p>
          {typeof report.verdict === "string" && report.verdict && (
            <blockquote className="bounty-card mt-4 flex items-start gap-3 p-4 text-left">
              <MentorAvatar size={40} mood="encouraging" />
              <p className="text-sm italic leading-relaxed text-text">
                “{report.verdict}”
              </p>
            </blockquote>
          )}
        </header>

        {Object.keys(breakdown).length > 0 && (
          <section className="bounty-card mb-6 space-y-3 p-5">
            <h2 className="text-xs font-bold uppercase tracking-widest text-text-muted">
              Skill breakdown
            </h2>
            {Object.entries(breakdown).map(([key, val], i) => (
              <MasteryBar
                key={key}
                label={key.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase())}
                value={Number(val) || 0}
                tone={barTones[i % barTones.length]}
              />
            ))}
          </section>
        )}

        {(report.strengths?.length || report.improvements?.length) && (
          <section className="mb-6 grid gap-4 sm:grid-cols-2">
            {report.strengths && report.strengths.length > 0 && (
              <div className="rounded-xl border border-primary/25 bg-mint/40 p-4">
                <h2 className="mb-2 text-xs font-bold uppercase tracking-widest text-primary">
                  Strengths
                </h2>
                <ul className="space-y-1.5 text-sm text-text">
                  {report.strengths.map(s => (
                    <li key={s}>· {s}</li>
                  ))}
                </ul>
              </div>
            )}
            {report.improvements && report.improvements.length > 0 && (
              <div className="rounded-xl border border-coral/25 bg-red-50 p-4">
                <h2 className="mb-2 text-xs font-bold uppercase tracking-widest text-coral">
                  Work on these
                </h2>
                <ul className="space-y-1.5 text-sm text-text">
                  {report.improvements.map(s => (
                    <li key={s}>· {s}</li>
                  ))}
                </ul>
              </div>
            )}
          </section>
        )}

        {!!result?.xp_gained && (
          <p className="mb-6 text-center text-sm font-bold text-reward">
            +{result.xp_gained} XP earned
          </p>
        )}

        <div className="flex flex-wrap items-center justify-center gap-3">
          <Button size="lg" onClick={resetToSetup}>
            New Interview
          </Button>
          <Link to="/home">
            <Button variant="ghost" size="lg">
              Back to Home
            </Button>
          </Link>
        </div>
      </div>
    </PageShell>
  );
}
