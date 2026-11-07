import { useCallback, useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
  ArrowLeft,
  ArrowRight,
  CheckCircle2,
  Lightbulb,
  Loader2,
  Trophy,
  XCircle,
} from "lucide-react";
import api from "../services/api";
import { Card, SectionHeader } from "../design-system/Card";
import { Button } from "../design-system/Button";
import { PageShell } from "../design-system/PageShell";
import Markdown from "../components/learning/Markdown";
import PracticeConsole from "../components/learning/PracticeConsole";

interface QuizContent {
  question: string;
  options: string[];
}

interface SectionContent {
  heading?: string;
  body?: string;
  code?: string;
  pro_tip?: string;
}

interface MistakeContent {
  mistake?: string;
  fix?: string;
  code?: string;
  fixed_code?: string;
}

interface ExerciseContent {
  description?: string;
  starter_code?: string;
  hints?: string[];
  expected_output?: string;
}

interface LessonContent {
  theory?: string;
  analogy?: string;
  sections?: SectionContent[];
  code_example?: { code?: string; annotations?: { line: number; text: string }[] };
  common_mistakes?: MistakeContent[];
  exercise?: ExerciseContent;
  quiz?: QuizContent;
  quizzes?: QuizContent[];
  key_takeaways?: string[];
  next_steps?: string;
}

interface LessonMeta {
  id: string;
  title: string;
  type?: string;
  xp?: number;
}

interface LessonPayload {
  lesson: LessonMeta;
  completed: boolean;
  next_lesson: LessonMeta | null;
  level: { id: string; name: string; emoji?: string; color?: string };
  content: LessonContent;
  quiz_progress: { required: string[]; passed: number[] };
}

interface QuizVerdict {
  is_correct: boolean;
  explanation: string | null;
}

interface CompletionResult {
  xp_gained?: number;
  bonus_xp?: number;
  total_xp?: number;
  already_completed?: boolean;
}

/** Every quiz the lesson presents, in the same order the API grades them. */
function quizzesOf(content: LessonContent): QuizContent[] {
  const list: QuizContent[] = [];
  if (content.quiz) list.push(content.quiz);
  for (const quiz of content.quizzes || []) {
    if (!list.includes(quiz)) list.push(quiz);
  }
  return list;
}

function CodeBlock({ code }: { code?: string }) {
  if (!code) return null;
  return (
    <pre className="my-3 overflow-x-auto rounded-xl border border-border bg-[#F6F8F3] p-4 font-mono text-[13px] leading-relaxed text-[#2F3E2F]">
      <code>{code}</code>
    </pre>
  );
}

export default function LessonView() {
  const { languageId = "", levelId = "", lessonId = "" } = useParams<{
    languageId: string;
    levelId: string;
    lessonId: string;
  }>();

  const [data, setData] = useState<LessonPayload | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [choices, setChoices] = useState<Record<number, number>>({});
  const [verdicts, setVerdicts] = useState<Record<number, QuizVerdict>>({});
  const [passed, setPassed] = useState<number[]>([]);
  const [grading, setGrading] = useState<number | null>(null);

  const [completing, setCompleting] = useState(false);
  const [completion, setCompletion] = useState<CompletionResult | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const payload = (await api.get(
        `/api/v1/learning/${languageId}/${levelId}/${lessonId}`
      )) as LessonPayload;
      setData(payload);
      setPassed(payload.quiz_progress?.passed || []);
      setChoices({});
      setVerdicts({});
      setCompletion(null);
    } catch (err) {
      const detail = (err as { detail?: string })?.detail;
      setError(detail || "Could not load this lesson.");
    } finally {
      setLoading(false);
    }
  }, [languageId, levelId, lessonId]);

  useEffect(() => {
    void load();
  }, [load]);

  const quizzes = useMemo(() => (data ? quizzesOf(data.content) : []), [data]);
  const allQuizzesPassed = quizzes.every((_, index) => passed.includes(index));

  const submitQuiz = async (index: number) => {
    const choice = choices[index];
    if (choice === undefined) return;
    setGrading(index);
    setError("");
    try {
      // The server owns the answer key; the client only sends the choice.
      const verdict = (await api.post(
        `/api/v1/learning/${languageId}/${levelId}/${lessonId}/quiz`,
        { quiz_index: index, choice }
      )) as QuizVerdict;
      setVerdicts((prev) => ({ ...prev, [index]: verdict }));
      if (verdict.is_correct) {
        setPassed((prev) => (prev.includes(index) ? prev : [...prev, index]));
      }
    } catch (err) {
      const detail = (err as { detail?: string })?.detail;
      setError(detail || "Could not grade that answer.");
    } finally {
      setGrading(null);
    }
  };

  const completeLesson = async () => {
    setCompleting(true);
    setError("");
    try {
      const result = (await api.post(
        `/api/v1/learning/${languageId}/${levelId}/${lessonId}/complete`,
        {}
      )) as CompletionResult;
      setCompletion(result);
      setData((prev) => (prev ? { ...prev, completed: true } : prev));
    } catch (err) {
      const detail = (err as { detail?: string })?.detail;
      setError(detail || "Could not complete this lesson.");
    } finally {
      setCompleting(false);
    }
  };

  if (loading) {
    return (
      <PageShell theme="nature" className="max-w-4xl mx-auto px-4 py-10">
        <div className="flex items-center gap-3 text-text-muted">
          <Loader2 size={18} className="animate-spin" /> Loading lesson…
        </div>
      </PageShell>
    );
  }

  if (!data) {
    return (
      <PageShell theme="nature" className="max-w-4xl mx-auto px-4 py-10">
        <Card>
          <p className="mb-4 text-sm text-red-500">{error || "Lesson not found."}</p>
          <Link to={`/learn/${languageId}`}>
            <Button variant="outline" size="sm">
              <ArrowLeft size={16} className="mr-2" /> Back to path
            </Button>
          </Link>
        </Card>
      </PageShell>
    );
  }

  const { lesson, content, level, next_lesson: nextLesson } = data;
  const completed = data.completed || Boolean(completion && !completion.already_completed);

  return (
    <PageShell theme="nature" className="max-w-4xl mx-auto px-4 py-8">
      <div className="mb-6 flex flex-wrap items-center justify-between gap-3">
        <Link to={`/learn/${languageId}`}>
          <Button variant="ghost" size="sm">
            <ArrowLeft size={16} className="mr-2" /> {level.emoji} {level.name}
          </Button>
        </Link>
        <span className="text-xs font-semibold uppercase tracking-wide text-text-muted">
          {lesson.type || "lesson"} · {lesson.xp ?? 0} XP
        </span>
      </div>

      <SectionHeader eyebrow={level.name} title={lesson.title} />

      {error && (
        <div className="mb-4 rounded-lg border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      )}

      {completed && (
        <Card tone="mint" className="mb-6 flex items-center gap-3">
          <CheckCircle2 size={20} className="text-primary" />
          <p className="text-sm text-text">
            {completion?.xp_gained
              ? `Lesson complete — earned ${completion.xp_gained} XP.`
              : "You already completed this lesson."}
          </p>
        </Card>
      )}

      {content.theory && (
        <Card className="mb-6">
          <Markdown>{content.theory}</Markdown>
        </Card>
      )}

      {content.analogy && (
        <Card tone="sand" className="mb-6 flex gap-3">
          <Lightbulb size={20} className="mt-0.5 shrink-0 text-reward" />
          <p className="text-sm italic text-text">{content.analogy}</p>
        </Card>
      )}

      {(content.sections || []).map((section, index) => (
        <Card key={index} className="mb-6">
          {section.heading && (
            <h3 className="mb-2 font-display text-lg font-bold text-text">
              {section.heading}
            </h3>
          )}
          {section.body && <Markdown>{section.body}</Markdown>}
          <CodeBlock code={section.code} />
          {section.pro_tip && (
            <p className="mt-3 rounded-lg bg-[#F4FAEF] px-3 py-2 text-xs text-text-secondary">
              <span className="font-semibold text-primary">Pro tip: </span>
              {section.pro_tip}
            </p>
          )}
        </Card>
      ))}

      {content.code_example?.code && (
        <Card className="mb-6">
          <h3 className="mb-2 font-display text-lg font-bold text-text">Example</h3>
          <CodeBlock code={content.code_example.code} />
          {content.code_example.annotations && content.code_example.annotations.length > 0 && (
            <ul className="mt-3 space-y-1 text-sm text-text-secondary">
              {content.code_example.annotations.map((note, index) => (
                <li key={index}>
                  <span className="font-mono text-xs text-text-muted">line {note.line}:</span>{" "}
                  {note.text}
                </li>
              ))}
            </ul>
          )}
        </Card>
      )}

      {(content.common_mistakes || []).length > 0 && (
        <Card className="mb-6">
          <h3 className="mb-3 font-display text-lg font-bold text-text">Common mistakes</h3>
          <div className="space-y-4">
            {(content.common_mistakes || []).map((mistake, index) => (
              <div key={index} className="rounded-lg border border-border p-3">
                {mistake.mistake && (
                  <p className="flex items-start gap-2 text-sm text-red-600">
                    <XCircle size={16} className="mt-0.5 shrink-0" /> {mistake.mistake}
                  </p>
                )}
                <CodeBlock code={mistake.code} />
                {mistake.fix && (
                  <p className="flex items-start gap-2 text-sm text-primary">
                    <CheckCircle2 size={16} className="mt-0.5 shrink-0" /> {mistake.fix}
                  </p>
                )}
                <CodeBlock code={mistake.fixed_code} />
              </div>
            ))}
          </div>
        </Card>
      )}

      {content.exercise?.description && (
        <Card className="mb-6">
          <h3 className="mb-2 font-display text-lg font-bold text-text">Practice</h3>
          <p className="mb-2 text-sm text-text-secondary">{content.exercise.description}</p>
          {content.exercise.expected_output && (
            <p className="mb-2 text-xs text-text-muted">
              Expected output: <span className="font-mono">{content.exercise.expected_output}</span>
            </p>
          )}
          {(content.exercise.hints || []).length > 0 && (
            <ul className="mb-4 list-disc space-y-1 pl-5 text-xs text-text-muted">
              {(content.exercise.hints || []).map((hint, index) => (
                <li key={index}>{hint}</li>
              ))}
            </ul>
          )}
          <PracticeConsole
            language={languageId}
            initialCode={content.exercise.starter_code || ""}
            height={260}
            title="Try it yourself"
          />
        </Card>
      )}

      {quizzes.length > 0 && (
        <Card className="mb-6">
          <h3 className="mb-3 font-display text-lg font-bold text-text">Check your understanding</h3>
          <div className="space-y-6">
            {quizzes.map((quiz, index) => {
              const verdict = verdicts[index];
              const isPassed = passed.includes(index);
              return (
                <div key={index}>
                  <p className="mb-3 text-sm font-semibold text-text">{quiz.question}</p>
                  <div className="space-y-2">
                    {quiz.options.map((option, optionIndex) => {
                      const selected = choices[index] === optionIndex;
                      const tone = !verdict || !verdict.is_correct
                        ? selected
                          ? "border-primary bg-[#F4FAEF]"
                          : "border-border hover:border-primary/50"
                        : selected
                        ? "border-primary bg-[#EAF7E1]"
                        : "border-border";
                      return (
                        <button
                          key={optionIndex}
                          type="button"
                          onClick={() =>
                            setChoices((prev) => ({ ...prev, [index]: optionIndex }))
                          }
                          className={`w-full rounded-lg border px-4 py-2.5 text-left text-sm text-text transition-colors ${tone}`}
                        >
                          <span className="mr-2 font-mono text-xs text-text-muted">
                            {String.fromCharCode(65 + optionIndex)}
                          </span>
                          {option}
                        </button>
                      );
                    })}
                  </div>

                  <div className="mt-3 flex items-center gap-3">
                    <Button
                      size="sm"
                      disabled={choices[index] === undefined || grading === index}
                      onClick={() => void submitQuiz(index)}
                    >
                      {grading === index ? (
                        <Loader2 size={14} className="mr-2 animate-spin" />
                      ) : null}
                      {verdict?.is_correct ? "Check again" : "Submit answer"}
                    </Button>
                    {isPassed && (
                      <span className="flex items-center gap-1 text-xs font-semibold text-primary">
                        <CheckCircle2 size={14} /> Passed
                      </span>
                    )}
                  </div>

                  {verdict && (
                    <div
                      className={`mt-3 rounded-lg border px-3 py-2 text-sm ${
                        verdict.is_correct
                          ? "border-primary/30 bg-[#F4FAEF] text-primary"
                          : "border-red-200 bg-red-50 text-red-600"
                      }`}
                    >
                      {verdict.is_correct
                        ? verdict.explanation || "Correct!"
                        : "Not quite — try again."}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </Card>
      )}

      {(content.key_takeaways || []).length > 0 && (
        <Card className="mb-6">
          <h3 className="mb-2 font-display text-lg font-bold text-text">Key takeaways</h3>
          <ul className="list-disc space-y-1 pl-5 text-sm text-text-secondary">
            {(content.key_takeaways || []).map((takeaway, index) => (
              <li key={index}>{takeaway}</li>
            ))}
          </ul>
          {content.next_steps && (
            <p className="mt-3 text-xs text-text-muted">{content.next_steps}</p>
          )}
        </Card>
      )}

      {!completed && (
        <Card className="mb-6 flex flex-wrap items-center justify-between gap-3">
          <p className="text-sm text-text-muted">
            {quizzes.length === 0
              ? "Finished reading? Mark this lesson complete."
              : allQuizzesPassed
              ? "All quizzes passed. Mark this lesson complete."
              : "Pass every quiz above to complete this lesson."}
          </p>
          <Button
            disabled={completing || !allQuizzesPassed}
            onClick={() => void completeLesson()}
          >
            {completing ? <Loader2 size={14} className="mr-2 animate-spin" /> : <Trophy size={14} className="mr-2" />}
            Complete lesson
          </Button>
        </Card>
      )}

      {nextLesson && (
        <div className="flex justify-end">
          <Link to={`/learn/${languageId}/${levelId}/${nextLesson.id}`}>
            <Button variant="outline" size="sm">
              Next: {nextLesson.title} <ArrowRight size={16} className="ml-2" />
            </Button>
          </Link>
        </div>
      )}
    </PageShell>
  );
}
