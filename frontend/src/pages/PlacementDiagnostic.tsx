// @ts-nocheck
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import Spinner from "../components/ui/Spinner";
import { Mentor, MentorMood } from "../design-system/Mentor";

type DiagnosticQuestion = {
  id: string;
  type: string;
  title: string;
  prompt: string;
  code?: string;
  options?: Array<{ id: string; text: string }>;
  correct_set?: string[];
  expected_output?: string;
  canonical_skills?: string[];
  explanation?: string;
};

type DiagnosticState = {
  role: string;
  question_count: number;
  questions: DiagnosticQuestion[];
};

export default function PlacementDiagnostic() {
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [state, setState] = useState<DiagnosticState | null>(null);
  const [answers, setAnswers] = useState<Record<string, any>>({});
  const [result, setResult] = useState<any>(null);
  const [captainByte, setCaptainByte] = useState<{ intro: string; mood: MentorMood }>({
    intro: "This mixed diagnostic establishes your baseline across aptitude, coding, and CS.",
    mood: "briefing",
  });

  useEffect(() => {
    let cancelled = false;
    async function load() {
      try {
        const res = await fetch("/api/v1/onboarding/diagnostic/start?role=sde");
        if (!res.ok) throw new Error("Failed");
        const json = await res.json();
        if (!cancelled) {
          setState(json);
          setCaptainByte({
            intro: `🧭 Captain Byte: ${json.question_count} questions. Answer as honestly as you can — this shapes your entire campaign.`,
            mood: "encouraging",
          });
        }
      } catch {
        if (!cancelled) {
          setCaptainByte({
            intro: "Could not load diagnostic. Try again.",
            mood: "stuck",
          });
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    load();
    return () => { cancelled = true; };
  }, []);

  const handleAnswer = (questionId: string, value: any) => {
    setAnswers((prev) => ({ ...prev, [questionId]: value }));
  };

  const handleSubmit = async () => {
    if (!state) return;
    setSubmitting(true);
    try {
      const res = await fetch("/api/v1/onboarding/diagnostic/complete", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ role: "sde", answers }),
      });
      if (!res.ok) throw new Error("Failed");
      const json = await res.json();
      setResult(json);

      const dims = json.readiness?.dimensions || [];
      const strengths = dims.filter((d: any) => d.status === "strength");
      const weaknesses = dims.filter((d: any) => d.status === "weakness");
      const developing = dims.filter((d: any) => d.status === "developing");

      let message = `🧭 Captain Byte: Diagnostic complete. Readiness: ${json.readiness?.overall ?? "—"}%. `;
      if (strengths.length) {
        message += `You're already strong in ${strengths.map((s: any) => s.label).join(" and ")}. `;
      }
      if (weaknesses.length) {
        message += `We'll focus on ${weaknesses.map((s: any) => s.label).join(" and ")} first. `;
      }
      if (developing.length) {
        message += `${developing.map((s: any) => s.label).join(" and ")} are developing — we'll push them next.`;
      }

      setCaptainByte({
        intro: message,
        mood: "celebrating",
      });
    } catch {
      setCaptainByte({
        intro: "Could not submit diagnostic. Try again.",
        mood: "stuck",
      });
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0f0f0f] flex items-center justify-center">
        <div className="text-center">
          <Spinner />
          <p className="mt-3 text-sm text-[#9a9a9a]">Loading diagnostic...</p>
        </div>
      </div>
    );
  }

  if (result) {
    const dimensions = result.readiness?.dimensions || [];
    const strengths = dimensions.filter((d: any) => d.status === "strength");
    const weaknesses = dimensions.filter((d: any) => d.status === "weakness");
    const developing = dimensions.filter((d: any) => d.status === "developing");
    const firstMission = result.first_missions?.[0];

    return (
      <div className="min-h-screen bg-[#0f0f0f] text-[#e9e9e9]">
        <div className="mx-auto max-w-3xl px-4 py-8 sm:px-6 lg:px-8 space-y-6">
          <Mentor mood={captainByte.mood} message={captainByte.intro} />

          <div className="rounded-xl border border-[#2a2a2a] bg-[#141414] p-6">
            <h2 className="text-xl font-bold">Your starting point</h2>
            <p className="mt-2 text-sm text-[#9a9a9a]">
              You don't need to study everything. Here's where you stand today.
            </p>

            <div className="mt-5 grid grid-cols-2 gap-3 sm:grid-cols-5">
              {dimensions.map((dim: any) => (
                <div key={dim.id} className="rounded-xl bg-[#1f1f1f] px-3 py-3 text-center">
                  <div className="text-xl">{dim.icon}</div>
                  <div className="mt-1 text-xs text-[#9a9a9a]">{dim.label}</div>
                  <div className="mt-1 text-lg font-bold">
                    {typeof dim.score === "number" ? `${Math.round(dim.score)}%` : "—"}
                  </div>
                  <div
                    className={`mt-1 text-[10px] uppercase tracking-wider ${
                      dim.status === "strength"
                        ? "text-green-400"
                        : dim.status === "weakness"
                          ? "text-red-400"
                          : dim.status === "developing"
                            ? "text-yellow-400"
                            : "text-[#9a9a9a]"
                    }`}
                  >
                    {dim.status === "strength"
                      ? "Strength"
                      : dim.status === "weakness"
                        ? "Weakness"
                        : dim.status === "developing"
                          ? "Developing"
                          : "Unknown"}
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-5 grid grid-cols-1 gap-3 sm:grid-cols-3">
              <div className="rounded-xl bg-green-500/5 border border-green-500/20 p-4">
                <div className="text-xs font-semibold uppercase tracking-wider text-green-400">
                  {strengths.length} Strength{strengths.length === 1 ? "" : "s"}
                </div>
                <div className="mt-2 text-sm text-[#e9e9e9]">
                  {strengths.length
                    ? strengths.map((s: any) => `${s.icon} ${s.label}`).join(", ")
                    : "None yet"}
                </div>
              </div>
              <div className="rounded-xl bg-yellow-500/5 border border-yellow-500/20 p-4">
                <div className="text-xs font-semibold uppercase tracking-wider text-yellow-400">
                  {developing.length} Developing
                </div>
                <div className="mt-2 text-sm text-[#e9e9e9]">
                  {developing.length
                    ? developing.map((s: any) => `${s.icon} ${s.label}`).join(", ")
                    : "None yet"}
                </div>
              </div>
              <div className="rounded-xl bg-red-500/5 border border-red-500/20 p-4">
                <div className="text-xs font-semibold uppercase tracking-wider text-red-400">
                  {weaknesses.length} Weakness{weaknesses.length === 1 ? "" : "es"}
                </div>
                <div className="mt-2 text-sm text-[#e9e9e9]">
                  {weaknesses.length
                    ? weaknesses.map((s: any) => `${s.icon} ${s.label}`).join(", ")
                    : "None yet"}
                </div>
              </div>
            </div>

            {firstMission && (
              <div className="mt-5 rounded-xl border border-[#ffa11655] bg-[#1c1c1c] p-5">
                <div className="text-xs font-mono uppercase tracking-wider text-[#ffa116] mb-1">
                  Why you're starting here
                </div>
                <p className="text-sm text-[#9a9a9a]">
                  {(() => {
                    const weak = weaknesses.slice(0, 2);
                    if (!weak.length) return "You have a strong baseline. We're starting with your first targeted mission.";
                    const labels = weak.map((w) => `${w.icon} ${w.label}`).join(" and ");
                    return `Your diagnostic shows weakness in ${labels}. This mission is chosen because it directly repairs those gaps before moving to harder placement questions.`;
                  })()}
                </p>
                <div className="mt-4 rounded-lg bg-[#0f0f0f] border border-[#2a2a2a] p-4">
                  <div className="text-xs font-mono uppercase tracking-wider text-[#9a9a9a] mb-2">
                    Today's first mission
                  </div>
                  <div className="text-lg font-bold text-[#e9e9e9]">{firstMission.title}</div>
                  <p className="mt-1 text-sm text-[#9a9a9a]">{firstMission.description}</p>
                  <div className="mt-3 flex flex-wrap gap-3 text-xs text-[#9a9a9a]">
                    {firstMission.estimated_minutes ? (
                      <span>⏱ {firstMission.estimated_minutes} min</span>
                    ) : null}
                    {firstMission.xp_reward ? <span>⭐ {firstMission.xp_reward} XP</span> : null}
                    {firstMission.topic ? (
                      <span>🎯 {firstMission.topic.replace(/_/g, " ")}</span>
                    ) : null}
                  </div>
                </div>
                <div className="mt-3 text-xs text-[#9a9a9a]">
                  Complete this and tomorrow's mission will change based on how well you transfer this skill.
                </div>
              </div>
            )}
          </div>

          <div className="flex items-center justify-between">
            <Link to="/placement" className="text-xs text-[#9a9a9a] hover:text-[#e9e9e9]">
              Back to campaign
            </Link>
            <Link
              to="/placement"
              className="inline-flex items-center rounded-lg bg-[#ffa116] px-5 py-2 text-sm font-semibold text-black transition-colors hover:brightness-110"
            >
              Start today's mission
            </Link>
          </div>
        </div>
      </div>
    );
  }

  if (!state) {
    return (
      <div className="min-h-screen bg-[#0f0f0f] flex items-center justify-center">
        <div className="text-center">
          <p className="text-sm text-[#9a9a9a]">No diagnostic available.</p>
          <Link to="/placement" className="mt-4 inline-block text-[#ffa116]">Back to campaign</Link>
        </div>
      </div>
    );
  }

  const allAnswered = state.questions.every((q) => answers[q.id] !== undefined && answers[q.id] !== "");

  return (
    <div className="min-h-screen bg-[#0f0f0f] text-[#e9e9e9]">
      <div className="mx-auto max-w-3xl px-4 py-8 sm:px-6 lg:px-8 space-y-6">
        <Mentor mood={captainByte.mood} message={captainByte.intro} />
        <div className="rounded-xl border border-[#2a2a2a] bg-[#141414] p-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold">Placement Diagnostic</h2>
              <p className="mt-1 text-sm text-[#9a9a9a]">
                {state.questions.length} questions · aptitude, coding, and CS
              </p>
            </div>
            <div className="text-xs text-[#9a9a9a]">
              {state.questions.filter((q) => answers[q.id] !== undefined && answers[q.id] !== "").length}/{state.questions.length} answered
            </div>
          </div>
        </div>

        <div className="space-y-4">
          {state.questions.map((q, idx) => (
            <motion.div
              key={q.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.05 }}
              className="rounded-xl border border-[#2a2a2a] bg-[#141414] p-5"
            >
              <div className="text-xs font-mono uppercase tracking-wider text-[#ffa116] mb-2">
                Q{idx + 1} · {q.type}
              </div>
              <p className="text-sm font-semibold text-[#e9e9e9]">{q.prompt || q.title}</p>
              {q.code && (
                <pre className="mt-3 rounded-lg bg-[#0f0f0f] p-3 text-xs text-[#9a9a9a] overflow-x-auto">
                  {q.code}
                </pre>
              )}
              {q.type === "predict" && q.options && (
                <div className="mt-4 space-y-2">
                  {q.options.map((opt) => (
                    <button
                      key={opt.id}
                      onClick={() => handleAnswer(q.id, opt.id)}
                      className={`w-full rounded-lg border px-3 py-2 text-left text-sm transition-colors ${
                        answers[q.id] === opt.id
                          ? "border-[#ffa116] bg-[#ffa116]/10"
                          : "border-[#2a2a2a] hover:border-[#ffa11655]"
                      }`}
                    >
                      {opt.text}
                    </button>
                  ))}
                </div>
              )}
              {q.type === "break" && (
                <div className="mt-4">
                  <textarea
                    value={answers[q.id] || ""}
                    onChange={(e) => handleAnswer(q.id, e.target.value)}
                    placeholder="List the issues you see, separated by commas..."
                    className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] placeholder:text-[#9a9a9a] focus:border-[#ffa116] focus:outline-none"
                    rows={3}
                  />
                </div>
              )}
              {q.type === "explore" && (
                <div className="mt-4">
                  <input
                    value={answers[q.id] || ""}
                    onChange={(e) => handleAnswer(q.id, e.target.value)}
                    placeholder="What is the output?"
                    className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] placeholder:text-[#9a9a9a] focus:border-[#ffa116] focus:outline-none"
                  />
                </div>
              )}
            </motion.div>
          ))}
        </div>

        <div className="flex items-center justify-between">
          <Link to="/placement" className="text-xs text-[#9a9a9a] hover:text-[#e9e9e9]">
            Skip for now
          </Link>
          <button
            onClick={handleSubmit}
            disabled={!allAnswered || submitting}
            className="inline-flex items-center rounded-lg bg-[#ffa116] px-5 py-2 text-sm font-semibold text-black transition-colors hover:brightness-110 disabled:opacity-60"
          >
            {submitting ? "Submitting..." : "Submit diagnostic"}
          </button>
        </div>
      </div>
    </div>
  );
}
