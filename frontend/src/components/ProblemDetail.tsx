import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { motion } from "framer-motion";
import api from "../services/api";
import {
  CheckCircle2,
  XCircle,
  Clock,
  Lock,
  Building2,
  BarChart3,
  ArrowLeft,
  Sparkles,
  Lightbulb,
  TrendingUp,
  Users,
  Zap,
  MessageSquare,
  ThumbsUp,
  ExternalLink,
  Brain,
  Quote,
  Target,
  BookOpen,
} from "lucide-react";

const DIFFICULTY_STYLES: Record<string, string> = {
  easy: "text-emerald-700 bg-emerald-50 border border-emerald-200",
  medium: "text-amber-700 bg-amber-50 border border-amber-200",
  hard: "text-rose-700 bg-rose-50 border border-rose-200",
  expert: "text-violet-700 bg-violet-50 border border-violet-200",
};

const TABS = [
  { id: "description", label: "Description", icon: <BarChart3 size={13} /> },
  { id: "solutions", label: "Solutions", icon: <Zap size={13} /> },
  { id: "submissions", label: "Submissions", icon: <TrendingUp size={13} /> },
  { id: "discussions", label: "Discuss", icon: <MessageSquare size={13} /> },
];

export default function ProblemDetail({ problemId: propId, problem: propProblem }) {
  const { id: routeId } = useParams();
  const id = propId || routeId;
  const [problem, setProblem] = useState(propProblem || null);
  const [loading, setLoading] = useState(!propProblem);
  const [solved, setSolved] = useState(false);
  const [activeSection, setActiveSection] = useState("description");
  const [hintsRevealed, setHintsRevealed] = useState(0);
  const [similarProblems, setSimilarProblems] = useState([]);
  const [acceptance, setAcceptance] = useState(null);
  const [discussions, setDiscussions] = useState([]);
  const [discussionContent, setDiscussionContent] = useState("");
  const [submittingDiscussion, setSubmittingDiscussion] = useState(false);

  useEffect(() => {
    if (propProblem) {
      setProblem(propProblem);
      setLoading(false);
      return;
    }

    const load = async () => {
      setLoading(true);
      try {
        const [problemData, solvedData] = await Promise.all([
          api.questions.getFull(id),
          api.questions.isSolved(id).catch(() => ({ solved: false })),
        ]);

        setProblem(problemData);
        setSolved(solvedData.solved);
        api.getAcceptanceRate(id).then(setAcceptance).catch(() => {});
        api.getSimilarProblems(id, 5).then(setSimilarProblems).catch(() => {});
        api.community.getDiscussions(id, "best", 1).then((d) => setDiscussions(d.discussions || [])).catch(() => {});
      } catch {
        setProblem(null);
      } finally {
        setLoading(false);
      }
    };

    load();
  }, [id, propProblem]);

  const handlePostDiscussion = async () => {
    if (!discussionContent.trim()) return;
    setSubmittingDiscussion(true);
    try {
      await api.community.createDiscussion(id, discussionContent, null, null, "discussion");
      setDiscussionContent("");
      api.community.getDiscussions(id, "best", 1).then((d) => setDiscussions(d.discussions || [])).catch(() => {});
    } catch {
      // keep the UI calm on failures
    } finally {
      setSubmittingDiscussion(false);
    }
  };

  if (loading) {
    return (
      <div className="h-full overflow-y-auto bg-[color:var(--bg-base,#f6f3ea)] p-4 sm:p-6">
        <div className="animate-pulse space-y-3 rounded-3xl border border-black/5 bg-white p-4 shadow-sm sm:p-6">
          <div className="h-6 w-2/3 rounded bg-black/5" />
          <div className="h-4 w-1/3 rounded bg-black/5" />
          <div className="h-32 rounded-2xl bg-black/5" />
        </div>
      </div>
    );
  }

  if (!problem) {
    return (
      <div className="flex h-full items-center justify-center p-6">
        <div className="text-center">
          <XCircle size={48} className="mx-auto mb-3 text-text-muted" />
          <p className="text-text-secondary">Problem not found</p>
          <Link to="/question-bank" className="mt-2 inline-block text-sm text-nature-blossom hover:underline">
            Back to Question Bank
          </Link>
        </div>
      </div>
    );
  }

  const difficultyClass = DIFFICULTY_STYLES[problem.difficulty] || DIFFICULTY_STYLES.medium;
  const acceptanceRate = problem.acceptance_rate || acceptance?.acceptance_rate || null;
  const totalSubmissions = problem.total_submissions || acceptance?.total_submissions || null;
  const avgTime = problem.avg_time || null;
  const companies = problem.companies || problem.company || [];
  const companyList = Array.isArray(companies) ? companies : [companies].filter(Boolean);
  const hints = problem.hints || [];
  const topics = Array.isArray(problem.topics) ? problem.topics : problem.topic ? [problem.topic] : [];
  const dsaGuide = problem.dsa_guide || { approach: "", data_structures: [], patterns: [], tips: [] };
  const expectedTime = problem.expected_time_complexity || null;
  const expectedSpace = problem.expected_space_complexity || null;
  const visibleTestCases = Array.isArray(problem.visible_test_cases) ? problem.visible_test_cases : [];
  const examples = Array.isArray(problem.examples) ? problem.examples : [];
  const constraints = Array.isArray(problem.constraints) ? problem.constraints : [];

  return (
    <div className="h-full overflow-y-auto bg-[color:var(--bg-base,#f6f3ea)]">
      <div className="sticky top-0 z-10 flex items-center gap-0 border-b border-black/5 bg-white/90 px-3 backdrop-blur sm:px-4">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveSection(tab.id)}
            className={`flex items-center gap-1.5 border-b-2 px-3 py-2.5 text-xs font-medium transition-colors ${
              activeSection === tab.id
                ? "border-[#4F8F57] text-nature-blossom"
                : "border-transparent text-text-muted hover:text-text-primary"
            }`}
          >
            {tab.icon} {tab.label}
          </button>
        ))}
      </div>

      <div className="space-y-5 p-4 sm:p-5">
        {activeSection === "description" && (
          <>
            <div className="rounded-3xl border border-black/5 bg-white p-4 shadow-sm">
              <div className="flex items-start justify-between gap-3">
                <div className="flex min-w-0 items-start gap-3">
                  <Link to="/question-bank" className="mt-1 text-text-muted transition-colors hover:text-text-primary">
                    <ArrowLeft size={18} />
                  </Link>
                  <h1 className="text-lg font-bold leading-tight text-text-primary sm:text-xl">
                    {problem.question_title || problem.question}
                  </h1>
                </div>
                <div className="flex shrink-0 items-center gap-2">
                  {solved && (
                    <span className="flex items-center gap-1 rounded-full border border-emerald-200 bg-emerald-50 px-2 py-1 text-[10px] text-emerald-700">
                      <CheckCircle2 size={12} /> Solved
                    </span>
                  )}
                  <span className={`rounded-full px-3 py-1 text-[10px] font-medium ${difficultyClass}`}>
                    {problem.difficulty}
                  </span>
                </div>
              </div>
            </div>

            <div className="flex flex-wrap items-center gap-4 rounded-2xl border border-black/5 bg-white px-4 py-3 text-[11px] text-text-muted">
              {acceptanceRate != null && (
                <div className="flex items-center gap-1.5">
                  <Users size={12} />
                  <span>
                    Acceptance: <span className="font-medium text-text-primary">{acceptanceRate}%</span>
                  </span>
                  {totalSubmissions > 0 && (
                    <span className="text-text-dim">({totalSubmissions.toLocaleString()} submissions)</span>
                  )}
                </div>
              )}
              {avgTime && (
                <div className="flex items-center gap-1.5">
                  <Clock size={12} />
                  <span>
                    Avg Time: <span className="font-medium text-text-primary">{avgTime}</span>
                  </span>
                </div>
              )}
              {problem.frequency != null && (
                <div className="flex items-center gap-1.5">
                  <TrendingUp size={12} />
                  <span>{problem.frequency} practices</span>
                </div>
              )}
            </div>

            {(expectedTime || expectedSpace) && (
              <div className="flex flex-wrap items-center gap-3 rounded-2xl border border-sky-200 bg-sky-50 px-4 py-3">
                <span className="text-[10px] font-medium uppercase tracking-wide text-sky-700">
                  Expected Complexity
                </span>
                {expectedTime && (
                  <span className="text-xs text-text-secondary">
                    Time:{" "}
                    <code className="rounded bg-white px-1.5 py-0.5 font-mono text-[11px] text-emerald-700">
                      {expectedTime}
                    </code>
                  </span>
                )}
                {expectedSpace && (
                  <span className="text-xs text-text-secondary">
                    Space:{" "}
                    <code className="rounded bg-white px-1.5 py-0.5 font-mono text-[11px] text-emerald-700">
                      {expectedSpace}
                    </code>
                  </span>
                )}
              </div>
            )}

            {companyList.length > 0 && (
              <div className="flex flex-wrap items-center gap-2">
                <Building2 size={12} className="text-text-muted" />
                {companyList.map((c, i) => (
                  <span key={i} className="rounded-full border border-sky-200 bg-sky-50 px-2.5 py-1 text-[10px] text-sky-700">
                    {c}
                  </span>
                ))}
              </div>
            )}

            {topics.length > 0 && (
              <div className="flex flex-wrap gap-1.5">
                {topics.map((topic, i) => (
                  <span key={i} className="rounded-full border border-black/5 bg-black/5 px-2 py-1 text-[10px] text-text-secondary">
                    {topic}
                  </span>
                ))}
              </div>
            )}

            {(problem.statement || problem.description) && (
              <div className="whitespace-pre-wrap text-sm leading-relaxed text-text-secondary">
                {problem.statement || problem.description}
              </div>
            )}

            {examples.length > 0 && (
              <div className="space-y-3">
                <h3 className="text-sm font-semibold text-text-primary">Examples</h3>
                {examples.map((ex, i) => (
                  <div key={i} className="space-y-2 rounded-2xl border border-black/5 bg-white p-4 shadow-sm">
                    <span className="text-[10px] font-medium text-text-muted">Example {i + 1}</span>
                    <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
                      <div>
                        <span className="text-[10px] text-text-muted">Input:</span>
                        <pre className="mt-1 whitespace-pre-wrap rounded-xl bg-surface-base p-2 font-mono text-xs text-emerald-700">
                          {ex.input || ex.input_text || ""}
                        </pre>
                      </div>
                      <div>
                        <span className="text-[10px] text-text-muted">Output:</span>
                        <pre className="mt-1 whitespace-pre-wrap rounded-xl bg-surface-base p-2 font-mono text-xs text-emerald-700">
                          {ex.output || ex.output_text || ""}
                        </pre>
                      </div>
                    </div>
                    {ex.explanation && <p className="mt-2 text-xs italic text-text-muted">{ex.explanation}</p>}
                  </div>
                ))}
              </div>
            )}

            {constraints.length > 0 && (
              <div className="rounded-2xl border border-black/5 bg-white p-4 shadow-sm">
                <h3 className="mb-2 text-sm font-semibold text-text-primary">Constraints</h3>
                <ul className="space-y-1">
                  {constraints.map((c, i) => (
                    <li key={i} className="font-mono text-xs text-text-secondary">
                      <span className="mr-2 text-nature-blossom">•</span>
                      {c}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {problem.follow_up && (
              <div className="rounded-2xl border border-amber-200 bg-amber-50 p-4 shadow-sm">
                <h3 className="mb-2 flex items-center gap-2 text-xs font-semibold text-amber-700">
                  <Sparkles size={12} /> Follow-up
                </h3>
                <p className="text-xs leading-relaxed text-amber-800">{problem.follow_up}</p>
              </div>
            )}

            {(dsaGuide.approach || dsaGuide.data_structures?.length > 0 || dsaGuide.patterns?.length > 0 || dsaGuide.tips?.length > 0) && (
              <div className="space-y-4 rounded-2xl border border-black/5 bg-white p-4 shadow-sm">
                <div className="flex items-start gap-3 rounded-2xl border border-sky-200 bg-sky-50 p-4">
                  <Quote size={20} className="mt-0.5 shrink-0 text-sky-600" />
                  <div>
                    <p className="text-sm italic text-text-secondary">
                      "Every expert was once a beginner. Break the problem down, trust the process, and code with confidence."
                    </p>
                    <span className="mt-1 block text-[10px] text-text-muted">Daily Motivation</span>
                  </div>
                </div>

                {dsaGuide.approach && (
                  <div>
                    <h4 className="mb-2 flex items-center gap-2 text-xs font-semibold text-text-primary">
                      <Target size={12} className="text-nature-blossom" /> Approach
                    </h4>
                    <p className="text-xs leading-relaxed text-text-secondary">{dsaGuide.approach}</p>
                  </div>
                )}

                {dsaGuide.data_structures?.length > 0 && (
                  <div>
                    <h4 className="mb-2 flex items-center gap-2 text-xs font-semibold text-text-primary">
                      <BookOpen size={12} className="text-nature-blossom" /> Data Structures
                    </h4>
                    <div className="flex flex-wrap gap-1.5">
                      {dsaGuide.data_structures.map((ds, i) => (
                        <span key={i} className="rounded-full border border-emerald-200 bg-emerald-50 px-2 py-1 text-[10px] text-emerald-700">
                          {ds}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {dsaGuide.patterns?.length > 0 && (
                  <div>
                    <h4 className="mb-2 flex items-center gap-2 text-xs font-semibold text-text-primary">
                      <Brain size={12} className="text-nature-blossom" /> Patterns
                    </h4>
                    <div className="flex flex-wrap gap-1.5">
                      {dsaGuide.patterns.map((pattern, i) => (
                        <span key={i} className="rounded-full border border-amber-200 bg-amber-50 px-2 py-1 text-[10px] text-amber-700">
                          {pattern}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {dsaGuide.tips?.length > 0 && (
                  <div>
                    <h4 className="mb-2 flex items-center gap-2 text-xs font-semibold text-text-primary">
                      <Zap size={12} className="text-amber-500" /> Pro Tips
                    </h4>
                    <ul className="space-y-1.5">
                      {dsaGuide.tips.map((tip, i) => (
                        <li key={i} className="flex items-start gap-2 text-xs text-text-secondary">
                          <span className="mt-0.5 text-amber-500">▸</span>
                          {tip}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}

            {hints.length > 0 && (
              <div className="rounded-2xl border border-amber-200 bg-amber-50 p-4">
                <h3 className="mb-3 flex items-center gap-2 text-sm font-semibold text-amber-700">
                  <Lightbulb size={14} /> Hints
                  <span className="ml-auto text-[10px] font-normal text-text-muted">
                    {hintsRevealed}/{hints.length} revealed
                  </span>
                </h3>
                <div className="space-y-2">
                  {hints.map((hint, i) => (
                    <div key={i}>
                      {i < hintsRevealed ? (
                        <motion.div
                          initial={{ opacity: 0, height: 0 }}
                          animate={{ opacity: 1, height: "auto" }}
                          className="rounded-xl border border-amber-200 bg-white p-3 text-xs text-text-secondary"
                        >
                          <span className="mr-2 font-medium text-amber-600">{i + 1}.</span>
                          {hint}
                        </motion.div>
                      ) : i === hintsRevealed ? (
                        <button
                          onClick={() => setHintsRevealed(hintsRevealed + 1)}
                          className="flex items-center gap-1 text-xs text-amber-700 hover:text-amber-800"
                        >
                          <Sparkles size={12} /> Reveal Hint {i + 1}
                        </button>
                      ) : null}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {visibleTestCases.length > 0 && (
              <div className="rounded-2xl border border-black/5 bg-white p-4 shadow-sm">
                <h3 className="mb-3 text-sm font-semibold text-text-primary">Test Cases</h3>
                <div className="space-y-2">
                  {visibleTestCases.map((tc, i) => (
                    <div key={i} className="rounded-xl border border-black/5 bg-surface-base p-3">
                      <div className="grid grid-cols-1 gap-3 text-xs md:grid-cols-2">
                        <div>
                          <span className="mb-1 block text-text-muted">Input</span>
                          <pre className="whitespace-pre-wrap font-mono text-[11px] text-emerald-700">
                            {tc.input || tc.stdin || ""}
                          </pre>
                        </div>
                        <div>
                          <span className="mb-1 block text-text-muted">Expected Output</span>
                          <pre className="whitespace-pre-wrap font-mono text-[11px] text-emerald-700">
                            {tc.expected || tc.expected_output || ""}
                          </pre>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {problem.solution && !problem.solution.locked && (
              <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4">
                <h3 className="mb-2 flex items-center gap-2 text-sm font-semibold text-emerald-700">
                  <Zap size={14} /> Solution
                </h3>
                <pre className="whitespace-pre-wrap font-mono text-xs text-text-secondary">
                  {typeof problem.solution === "string" ? problem.solution : JSON.stringify(problem.solution, null, 2)}
                </pre>
              </div>
            )}

            {problem.solution?.locked && (
              <div className="flex items-center gap-2 rounded-2xl border border-black/5 bg-white p-4 text-text-muted shadow-sm">
                <Lock size={16} />
                <span className="text-xs">{problem.solution.message || "Upgrade to Pro to unlock the solution"}</span>
              </div>
            )}

            {similarProblems.length > 0 && (
              <div className="rounded-2xl border border-black/5 bg-white p-4 shadow-sm">
                <h3 className="mb-3 text-sm font-semibold text-text-primary">Similar Problems</h3>
                <div className="space-y-1.5">
                  {similarProblems.map((sp, i) => (
                    <Link key={i} to={`/solve/${sp.id}`} className="group flex items-center justify-between rounded-lg px-2 py-1.5 transition-colors hover:bg-black/5">
                      <div className="flex items-center gap-2">
                        <span className={`rounded px-1.5 py-0.5 text-[10px] ${DIFFICULTY_STYLES[sp.difficulty] || "text-text-muted bg-black/5 border border-black/5"}`}>
                          {sp.difficulty?.charAt(0).toUpperCase()}
                        </span>
                        <span className="text-xs text-text-secondary group-hover:text-text-primary">
                          {sp.question_title || sp.question}
                        </span>
                      </div>
                      <ExternalLink size={11} className="text-text-dim group-hover:text-text-secondary" />
                    </Link>
                  ))}
                </div>
              </div>
            )}
          </>
        )}

        {activeSection === "solutions" && (
          <div className="space-y-4">
            {problem.solution && !problem.solution.locked ? (
              <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-5">
                <h3 className="mb-3 flex items-center gap-2 text-sm font-semibold text-emerald-700">
                  <Zap size={14} /> Official Solution
                </h3>
                <pre className="whitespace-pre-wrap font-mono text-xs leading-relaxed text-text-secondary">
                  {typeof problem.solution === "string" ? problem.solution : JSON.stringify(problem.solution, null, 2)}
                </pre>
              </div>
            ) : (
              <div className="py-12 text-center text-text-muted">
                <Lock size={32} className="mx-auto mb-3 opacity-50" />
                <p className="text-sm">Solve this problem or upgrade to Pro to unlock solutions</p>
              </div>
            )}
          </div>
        )}

        {activeSection === "submissions" && (
          <div className="py-12 text-center text-text-muted">
            <TrendingUp size={32} className="mx-auto mb-3 opacity-50" />
            <p className="text-sm">Submit your code in the editor to see submissions here</p>
          </div>
        )}

        {activeSection === "discussions" && (
          <div className="space-y-4">
            <div className="flex gap-2">
              <textarea
                value={discussionContent}
                onChange={(e) => setDiscussionContent(e.target.value)}
                placeholder="Share your approach, solution, or ask a question..."
                className="min-h-24 flex-1 resize-none rounded-xl border border-black/5 bg-white px-3 py-2 text-xs text-text-secondary focus:border-nature-leaf focus:outline-none"
                rows={3}
              />
            </div>
            <button
              onClick={handlePostDiscussion}
              disabled={submittingDiscussion || !discussionContent.trim()}
              className="rounded-lg bg-nature-leaf px-3 py-1.5 text-xs font-medium text-white transition-colors hover:bg-nature-moss disabled:opacity-50"
            >
              {submittingDiscussion ? "Posting..." : "Post"}
            </button>

            {discussions.length === 0 ? (
              <div className="py-8 text-center text-text-muted">
                <MessageSquare size={24} className="mx-auto mb-2 opacity-50" />
                <p className="text-xs">No discussions yet. Be the first!</p>
              </div>
            ) : (
              <div className="space-y-3">
                {discussions.map((d, i) => (
                  <div key={d.id || i} className="rounded-xl border border-black/5 bg-white p-3 shadow-sm">
                    <div className="mb-2 flex items-center gap-2">
                      <span className="text-xs font-medium text-text-primary">{d.user_name || "Anonymous"}</span>
                      <span className="text-[10px] text-text-muted">
                        {d.created_at ? new Date(d.created_at).toLocaleDateString() : ""}
                      </span>
                      {d.discussion_type === "solution" && (
                        <span className="rounded bg-emerald-50 px-1.5 py-0.5 text-[10px] text-emerald-700">Solution</span>
                      )}
                    </div>
                    <p className="whitespace-pre-wrap text-xs text-text-secondary">{d.content}</p>
                    {d.upvotes > 0 && (
                      <div className="mt-2 flex items-center gap-1 text-[10px] text-text-muted">
                        <ThumbsUp size={10} /> {d.upvotes}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
