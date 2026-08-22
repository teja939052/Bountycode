import { useMemo, useState, useEffect } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import {
  ArrowLeft,
  ArrowRight,
  CheckCircle2,
  Code2,
  Eye,
  EyeOff,
  Lightbulb,
  Lock,
  RotateCcw,
  Sparkles,
  XCircle,
} from "lucide-react";
import { useLesson } from "../hooks/useLesson";
import { gamificationApi } from "../services/api/gamification";
import { compilerApi } from "../services/api/coding";
import Spinner from "../components/ui/Spinner";
import Markdown from "../components/learning/Markdown";

const PROGRESS_KEY = "pp_curriculum_progress_v1";
const WEB_TRACKS = ["html", "css", "javascript"];
const RUNNABLE_TRACKS = ["python", "java", "cpp"];

function readProgress() {
  try {
    return JSON.parse(localStorage.getItem(PROGRESS_KEY) || "{}");
  } catch {
    return {};
  }
}

function writeProgress(map) {
  try {
    localStorage.setItem(PROGRESS_KEY, JSON.stringify(map));
  } catch {}
}

function buildPreviewDoc(language, exercise) {
  const code = exercise?.code || "";
  if (language === "html") return code;
  if (language === "css") {
    return `<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>${code}</style>
</head>
<body>
  <h1>Live CSS Preview</h1>
  <div class="demo-box">Styling applied from your code</div>
  <style>.demo-box { padding: 16px; border-radius: 12px; background: #eee; }</style>
</body>
</html>`;
  }
  if (language === "javascript") {
    return `<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>body { font-family: system-ui, sans-serif; padding: 24px; }</style>
</head>
<body>
  <div id="js-output">Running your script…</div>
  <script>
${code}
document.addEventListener("DOMContentLoaded", () => {
  const out = document.getElementById("js-output");
  if (!out) return;
  const log = [];
  const origLog = console.log;
  console.log = (...args) => { log.push(args.map(String).join(" ")); out.innerHTML = log.join("<br>"); origLog.apply(console, args); };
});
  </script>
</body>
</html>`;
  }
  return code;
}

export default function LearnLesson() {
  const { trackId, lessonId } = useParams();
  const navigate = useNavigate();
  const { lesson, loading, error, preload } = useLesson(trackId, lessonId);

  const [code, setCode] = useState("");
  const [showHints, setShowHints] = useState(false);
  const [hintCount, setHintCount] = useState(1);
  const [checkResult, setCheckResult] = useState(null);
  const [quizAnswers, setQuizAnswers] = useState({});
  const [quizResult, setQuizResult] = useState(null);
  const [completed, setCompleted] = useState(false);
  const [justCompleted, setJustCompleted] = useState(false);
  const [showPreview, setShowPreview] = useState(true);
  const [runOutput, setRunOutput] = useState(null);
  const [running, setRunning] = useState(false);

  const isProject = lesson?.type === "project";
  const exercise = lesson?.content?.exercise;
  const quiz = lesson?.content?.quiz || [];
  const isWebTrack = WEB_TRACKS.includes(trackId);
  const exerciseLanguage = exercise?.language || (trackId === "javascript" ? "javascript" : trackId);

  useEffect(() => {
    if (!lesson?.id) return;
    setCode(exercise?.starterCode || "");
    setShowHints(false);
    setHintCount(1);
    setCheckResult(null);
    setQuizAnswers({});
    setQuizResult(null);
    setCompleted(!!readProgress()[lesson.id]);
    setJustCompleted(false);
    setRunOutput(null);
    setRunning(false);
  }, [lesson?.id]);

  useEffect(() => {
    if (lesson?.completion?.nextLesson) {
      preload(lesson.completion.nextLesson);
    }
  }, [lesson?.completion?.nextLesson, preload]);

  const previewDoc = useMemo(
    () => buildPreviewDoc(trackId, { code }),
    [trackId, code]
  );

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-surface-base">
        <Spinner />
      </div>
    );
  }

  if (error || !lesson) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center gap-4 bg-surface-base px-6 text-center">
        <Lock size={32} className="text-text-muted" />
        <p className="text-lg font-semibold text-text-primary">Lesson unavailable</p>
        <p className="text-sm text-text-muted">{error || "We couldn't load this lesson."}</p>
        <Link to={`/curriculum/${trackId}`} className="text-sm font-semibold text-nature-blossom">
          Back to track
        </Link>
      </div>
    );
  }

  const allRequiredPassed = () => {
    if (!exercise?.required?.length) return false;
    const normalized = code.replace(/\s+/g, " ");
    return exercise.required.every((needle) => normalized.includes(needle.replace(/\s+/g, " ")));
  };

  const handleCheck = async () => {
    // Runnable tracks with an expected output get REAL output grading.
    if (RUNNABLE_TRACKS.includes(trackId) && exercise?.expected) {
      setRunning(true);
      setCheckResult(null);
      try {
        const res = await compilerApi.executeCode({
          code,
          language: exerciseLanguage,
          stdin: exercise?.stdin || "",
          timeout: 5,
        });
        const actual = (res?.stdout || res?.output || "").trim();
        const expected = String(exercise.expected).trim();
        const normalized = (s) => s.replace(/\s+/g, " ").trim();
        const ok = normalized(actual) === normalized(expected);
        setCheckResult(ok);
        setRunOutput({
          ok,
          text: actual || "(no output produced)",
          expected,
        });
      } catch (err) {
        setCheckResult(false);
        setRunOutput({ ok: false, text: err?.message || "Run failed", expected: String(exercise.expected) });
      } finally {
        setRunning(false);
      }
      return;
    }
    const ok = allRequiredPassed();
    setCheckResult(ok);
  };

  const handleHint = () => {
    setHintCount((c) => Math.min(c + 1, exercise?.hints?.length || 1));
  };

  const handleRun = async () => {
    if (running) return;
    setRunning(true);
    setRunOutput(null);
    try {
      const res = await compilerApi.executeCode({
        code,
        language: exerciseLanguage,
        stdin: exercise?.stdin || "",
        timeout: 5,
      });
      setRunOutput({
        ok: !(res?.stderr || (res?.error && res?.error !== "Compilation failed")),
        text:
          res?.output ||
          res?.stdout ||
          res?.error ||
          (res?.compile?.output ? res.compile.output : "No output"),
      });
    } catch (err) {
      setRunOutput({ ok: false, text: err?.message || "Run failed" });
    } finally {
      setRunning(false);
    }
  };

  const handleQuizAnswer = (qIndex, optIndex) => {
    const next = { ...quizAnswers, [qIndex]: optIndex };
    setQuizAnswers(next);
    if (quiz.length && Object.keys(next).length === quiz.length) {
      const correct = quiz.filter((q, i) => next[i] === q.correct).length;
      setQuizResult({
        correct,
        total: quiz.length,
        passed: correct === quiz.length,
      });
    }
  };

  const markComplete = async () => {
    const progress = readProgress();
    progress[lesson.id] = {
      completedAt: Date.now(),
      xp: lesson.xp,
      track: trackId,
    };
    writeProgress(progress);
    setCompleted(true);
    setJustCompleted(true);
    try {
      await gamificationApi.recordActivity("learning", lesson.xp, "curriculum", trackId);
    } catch {}
    if (lesson.completion?.nextLesson) {
      setTimeout(() => navigate(`/curriculum/${trackId}/${lesson.completion.nextLesson}`), 1200);
    }
  };

  const resetCode = () => setCode(exercise?.starterCode || "");

  const sectionLabel = lesson.section || "Lesson";

  return (
    <div className="min-h-screen bg-surface-base text-text-primary">
      <div className="sticky top-0 z-20 border-b border-[#E5E7EB] bg-white/90 backdrop-blur">
        <div className="mx-auto flex max-w-[1400px] items-center justify-between gap-4 px-4 py-3">
          <div className="flex items-center gap-3">
            <Link
              to={`/curriculum/${trackId}`}
              className="flex h-9 w-9 items-center justify-center rounded-full border border-[#E5E7EB] text-text-muted hover:bg-[#F3F4F6]"
              aria-label="Back to track"
            >
              <ArrowLeft size={16} />
            </Link>
            <div>
              <p className="text-[11px] font-semibold uppercase tracking-wider text-nature-blossom">
                {sectionLabel}
              </p>
              <h1 className="font-display text-base font-bold leading-tight">{lesson.title}</h1>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <span className="hidden rounded-full border border-nature-bark bg-[#EEF5E7] px-3 py-1 text-xs font-semibold text-nature-blossom sm:block">
              +{lesson.xp} XP
            </span>
            {completed && (
              <span className="flex items-center gap-1 rounded-full bg-green-100 px-3 py-1 text-xs font-semibold text-green-700">
                <CheckCircle2 size={14} /> Completed
              </span>
            )}
          </div>
        </div>
      </div>

      <div className="mx-auto grid max-w-[1400px] grid-cols-1 gap-6 p-4 lg:grid-cols-2">
        {/* Left: content */}
        <div className="min-w-0 space-y-6">
          <section className="rounded-3xl border border-[#E5E7EB] bg-white p-6 shadow-[0_1px_2px_rgba(31,41,55,0.04)]">
            <Markdown>{lesson.content?.theory}</Markdown>
          </section>

          {lesson.content?.codeSnippets?.length > 0 && (
            <section className="rounded-3xl border border-[#E5E7EB] bg-white p-6">
              <h3 className="mb-3 flex items-center gap-2 font-display text-sm font-bold uppercase tracking-wider text-nature-blossom">
                <Sparkles size={15} /> Walkthrough
              </h3>
              <div className="space-y-4">
                {lesson.content.codeSnippets.map((s, i) => (
                  <div key={i}>
                    <pre className="overflow-x-auto rounded-xl border border-[#E5E7EB] bg-[#F9FAFB] p-4 font-mono text-[13px] leading-relaxed">
                      <code>{s.code}</code>
                    </pre>
                    {s.output && (
                      <p className="mt-1 text-xs italic text-text-muted">→ {s.output}</p>
                    )}
                  </div>
                ))}
              </div>
            </section>
          )}

          {exercise && (
            <section className="rounded-3xl border border-[#E5E7EB] bg-white p-6">
              <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
                <h3 className="flex items-center gap-2 font-display text-sm font-bold uppercase tracking-wider text-nature-blossom">
                  <Code2 size={15} /> {isProject ? "Build it" : "Your turn"}
                </h3>
                <div className="flex items-center gap-2">
                  <button
                    onClick={resetCode}
                    className="flex items-center gap-1 rounded-full border border-[#E5E7EB] px-3 py-1 text-xs font-semibold text-text-muted hover:bg-[#F3F4F6]"
                  >
                    <RotateCcw size={13} /> Reset
                  </button>
                  <button
                    onClick={() => setShowPreview((p) => !p)}
                    className="flex items-center gap-1 rounded-full border border-[#E5E7EB] px-3 py-1 text-xs font-semibold text-text-muted hover:bg-[#F3F4F6]"
                  >
                    {showPreview ? <EyeOff size={13} /> : <Eye size={13} />}
                    {showPreview ? "Hide preview" : "Show preview"}
                  </button>
                </div>
              </div>

              <p className="mb-3 text-sm leading-relaxed text-text-secondary">{exercise.instruction}</p>

              <textarea
                value={code}
                onChange={(e) => {
                  setCode(e.target.value);
                  setCheckResult(null);
                }}
                spellCheck={false}
                className="h-64 w-full resize-y rounded-xl border border-[#E5E7EB] bg-[#F9FAFB] p-4 font-mono text-[13px] leading-relaxed text-text-primary outline-none focus:border-nature-leaf focus:ring-2 focus:ring-nature-leaf/20"
                aria-label="Code editor"
              />

              <div className="mt-3 flex flex-wrap items-center gap-2">
                <button
                  onClick={handleCheck}
                  className="rounded-full bg-nature-leaf px-5 py-2 text-sm font-bold text-white transition-colors hover:bg-nature-moss"
                >
                  Check answer
                </button>
                {RUNNABLE_TRACKS.includes(trackId) && (
                  <button
                    onClick={handleRun}
                    disabled={running}
                    className="rounded-full bg-[#1F2937] px-5 py-2 text-sm font-bold text-white transition-colors hover:bg-[#374151] disabled:opacity-60"
                  >
                    {running ? "Running…" : "Run code"}
                  </button>
                )}
                {exercise.hints?.length > 0 && (
                  <button
                    onClick={handleHint}
                    className="flex items-center gap-1.5 rounded-full border border-[#EAB308]/40 bg-[#FEFCE8] px-4 py-2 text-sm font-semibold text-[#854D0E] hover:bg-[#FEF9C3]"
                  >
                    <Lightbulb size={15} /> Hint
                  </button>
                )}
              </div>

              {showHints && exercise.hints?.length > 0 && (
                <div className="mt-3 space-y-2 rounded-xl border border-[#EAB308]/30 bg-[#FEFCE8] p-4">
                  {exercise.hints.slice(0, hintCount).map((h, i) => (
                    <p key={i} className="text-sm text-[#854D0E]">
                      {h}
                    </p>
                  ))}
                </div>
              )}

              {checkResult === true && (
                <div className="mt-3 flex items-center gap-2 rounded-xl border border-green-200 bg-green-50 px-4 py-3 text-sm font-semibold text-green-700">
                  <CheckCircle2 size={16} />
                  {runOutput?.expected ? "All tests passed — output matches!" : "Correct! Looks great."}
                </div>
              )}
              {checkResult === false && (
                <div className="mt-3 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-semibold text-red-700">
                  {runOutput?.expected ? (
                    <div className="space-y-1 font-mono text-[13px]">
                      <p className="flex items-center gap-2">
                        <XCircle size={16} className="shrink-0" /> Your output: {runOutput.text || "(empty)"}
                      </p>
                      <p className="text-green-700">Expected: {runOutput.expected}</p>
                    </div>
                  ) : (
                    <p className="flex items-center gap-2">
                      <XCircle size={16} className="shrink-0" /> Not quite — check the requirements and try again.
                    </p>
                  )}
                </div>
              )}
            </section>
          )}

          {quiz.length > 0 && (
            <section className="rounded-3xl border border-[#E5E7EB] bg-white p-6">
              <h3 className="mb-4 flex items-center gap-2 font-display text-sm font-bold uppercase tracking-wider text-nature-blossom">
                <Lightbulb size={15} /> Quick check
              </h3>
              <div className="space-y-5">
                {quiz.map((q, qi) => (
                  <div key={qi}>
                    <p className="mb-2 text-sm font-semibold text-text-primary">
                      {qi + 1}. {q.question}
                    </p>
                    <div className="grid grid-cols-1 gap-2 sm:grid-cols-3">
                      {q.options.map((opt, oi) => {
                        const isSelected = quizAnswers[qi] === oi;
                        const showCorrect =
                          quizResult && oi === q.correct;
                        const showWrong = quizResult && isSelected && oi !== q.correct;
                        return (
                          <button
                            key={oi}
                            onClick={() => handleQuizAnswer(qi, oi)}
                            className={`rounded-xl border px-3 py-2 text-left text-sm transition-colors ${
                              showCorrect
                                ? "border-green-300 bg-green-50 font-semibold text-green-700"
                                : showWrong
                                ? "border-red-300 bg-red-50 text-red-700"
                                : isSelected
                                ? "border-[#4F8F57] bg-[#EEF5E7] text-text-primary"
                                : "border-[#E5E7EB] bg-white text-text-secondary hover:bg-[#F9FAFB]"
                            }`}
                          >
                            {opt}
                          </button>
                        );
                      })}
                    </div>
                  </div>
                ))}
              </div>
              {quizResult && (
                <p
                  className={`mt-4 rounded-xl px-4 py-3 text-sm font-semibold ${
                    quizResult.passed
                      ? "bg-green-50 text-green-700"
                      : "bg-red-50 text-red-700"
                  }`}
                >
                  {quizResult.passed
                    ? `All ${quizResult.total} correct — nice!`
                    : `${quizResult.correct}/${quizResult.total} correct — review the theory above and retry.`}
                </p>
              )}
            </section>
          )}

          <div className="flex items-center justify-between gap-4 pb-10">
            {lesson.completion?.nextLesson ? (
              <button
                onClick={markComplete}
                className="flex items-center gap-2 rounded-full bg-[#1F2937] px-6 py-3 text-sm font-bold text-white transition-colors hover:bg-[#374151]"
              >
                {justCompleted ? "Completed!" : "Complete lesson"}
                <ArrowRight size={16} />
              </button>
            ) : (
              <button
                onClick={markComplete}
                className="rounded-full bg-nature-leaf px-6 py-3 text-sm font-bold text-white transition-colors hover:bg-nature-moss"
              >
                {justCompleted ? "Finished!" : "Finish track"}
              </button>
            )}
            <span className="hidden text-xs text-text-muted sm:block">
              {isProject ? "Project" : "Lesson"} · {lesson.duration || "5 min"}
            </span>
          </div>
        </div>

        {/* Right: live preview / run output */}
        {showPreview && (isWebTrack || RUNNABLE_TRACKS.includes(trackId)) && (
          <div className="lg:sticky lg:top-[65px] lg:h-[calc(100vh-85px)]">
            <div className="flex h-full flex-col overflow-hidden rounded-3xl border border-[#E5E7EB] bg-white">
              <div className="flex items-center justify-between border-b border-[#E5E7EB] bg-[#F9FAFB] px-4 py-2.5">
                <p className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-text-muted">
                  <Eye size={13} /> {isWebTrack ? "Live preview" : "Output"}
                </p>
                <span className="flex gap-1.5">
                  <span className="h-2.5 w-2.5 rounded-full bg-[#FCA5A5]" />
                  <span className="h-2.5 w-2.5 rounded-full bg-[#FCD34D]" />
                  <span className="h-2.5 w-2.5 rounded-full bg-[#86EFAC]" />
                </span>
              </div>
              {isWebTrack ? (
                <iframe
                  title="Live preview"
                  srcDoc={previewDoc}
                  sandbox="allow-scripts allow-modals"
                  className="min-h-[300px] w-full flex-1 bg-white lg:min-h-0"
                />
              ) : (
                <div className="flex w-full flex-1 flex-col bg-[#111827] font-mono text-[13px] text-[#D1D5DB]">
                  <div className="flex items-center justify-between border-b border-[#1F2937] px-4 py-2">
                    <span className="text-xs uppercase tracking-wider text-text-muted">
                      {exerciseLanguage}
                    </span>
                    <button
                      onClick={handleRun}
                      disabled={running}
                      className="rounded-full bg-nature-leaf px-3 py-1 text-xs font-bold text-white hover:bg-nature-moss disabled:opacity-60"
                    >
                      {running ? "Running…" : "Run"}
                    </button>
                  </div>
                  <pre className="flex-1 overflow-auto p-4 whitespace-pre-wrap">
                    {running
                      ? "Running your code…"
                      : runOutput
                      ? runOutput.text
                      : "Click Run to execute your code in a real sandbox."}
                  </pre>
                  {runOutput && !runOutput.ok && (
                    <div className="border-t border-red-500/40 bg-red-500/10 px-4 py-2 text-xs text-red-300">
                      Your code produced an error or no output — review it and try again.
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
