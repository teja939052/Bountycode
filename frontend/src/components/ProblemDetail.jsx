import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import api from "../services/api";
import {
  CheckCircle2, XCircle, Clock, Lock, Building2,
  Tag, BarChart3, ArrowLeft, Sparkles, Lightbulb,
  TrendingUp, Users, Zap, ChevronDown, ChevronRight,
  BarChart, MessageSquare, ThumbsUp, ExternalLink
} from "lucide-react";

const DIFFICULTY_STYLES = {
  easy: "text-green-400 bg-green-900/30 border border-green-800",
  medium: "text-yellow-400 bg-yellow-900/30 border border-yellow-800",
  hard: "text-red-400 bg-red-900/30 border border-red-800",
  expert: "text-purple-400 bg-purple-900/30 border border-purple-800",
};

const DIFFICULTY_BAR_COLORS = {
  easy: "bg-green-500",
  medium: "bg-yellow-500",
  hard: "bg-red-500",
  expert: "bg-purple-500",
};

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
          api.getQuestionFull(id),
          api.isQuestionSolved(id).catch(() => ({ solved: false })),
        ]);
        setProblem(problemData);
        setSolved(solvedData.solved);
        // Load supplementary data
        api.getAcceptanceRate(id).then(setAcceptance).catch(() => {});
        api.getSimilarProblems(id, 5).then(setSimilarProblems).catch(() => {});
        api.getDiscussions(id, "best", 1).then((d) => setDiscussions(d.discussions || [])).catch(() => {});
      } catch {
        setProblem(null);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [id]);

  const handlePostDiscussion = async () => {
    if (!discussionContent.trim()) return;
    setSubmittingDiscussion(true);
    try {
      await api.createDiscussion(id, discussionContent, null, null, "discussion");
      setDiscussionContent("");
      api.getDiscussions(id, "best", 1).then((d) => setDiscussions(d.discussions || [])).catch(() => {});
    } catch {} finally {
      setSubmittingDiscussion(false);
    }
  };

  if (loading) {
    return (
      <div className="h-full overflow-y-auto p-6 space-y-4">
        <div className="animate-pulse space-y-3">
          <div className="h-6 bg-gray-700 rounded w-2/3" />
          <div className="h-4 bg-gray-700 rounded w-1/3" />
          <div className="h-32 bg-gray-700 rounded" />
        </div>
      </div>
    );
  }

  if (!problem) {
    return (
      <div className="h-full flex items-center justify-center p-6">
        <div className="text-center">
          <XCircle size={48} className="mx-auto text-gray-600 mb-3" />
          <p className="text-gray-400">Problem not found</p>
          <Link to="/question-bank" className="text-cyber-blue hover:underline text-sm mt-2 inline-block">Back to Question Bank</Link>
        </div>
      </div>
    );
  }

  const difficultyClass = DIFFICULTY_STYLES[problem.difficulty] || DIFFICULTY_STYLES.medium;
  const acceptanceRate = problem.acceptance_rate || acceptance?.acceptance_rate || null;
  const totalSubmissions = problem.total_submissions || acceptance?.total_submissions || null;
  const totalAccepted = problem.total_accepted || acceptance?.total_accepted || null;
  const avgTime = problem.avg_time || null;
  const companies = problem.companies || problem.company || [];
  const companyList = Array.isArray(companies) ? companies : [companies].filter(Boolean);
  const hints = problem.hints || [];
  const expectedTime = problem.expected_time_complexity || null;
  const expectedSpace = problem.expected_space_complexity || null;

  return (
    <div className="h-full overflow-y-auto">
      {/* Tab Navigation */}
      <div className="sticky top-0 z-10 flex items-center gap-0 border-b border-space-border bg-space-panel/80 backdrop-blur-sm px-4">
        {[
          { id: "description", label: "Description", icon: <BarChart3 size={13} /> },
          { id: "solutions", label: "Solutions", icon: <Zap size={13} /> },
          { id: "submissions", label: "Submissions", icon: <TrendingUp size={13} /> },
          { id: "discussions", label: "Discuss", icon: <MessageSquare size={13} /> },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveSection(tab.id)}
            className={`flex items-center gap-1.5 px-3 py-2.5 text-xs font-medium border-b-2 transition-colors ${
              activeSection === tab.id ? "border-cyber-blue text-cyber-blue" : "border-transparent text-gray-500 hover:text-gray-300"
            }`}
          >
            {tab.icon} {tab.label}
          </button>
        ))}
      </div>

      <div className="p-5 space-y-5">
        {/* Description Tab */}
        {activeSection === "description" && (
          <>
            {/* Header */}
            <div className="flex items-start justify-between gap-3">
              <div className="flex items-center gap-3">
                <Link to="/question-bank" className="text-gray-400 hover:text-white transition-colors mt-1">
                  <ArrowLeft size={18} />
                </Link>
                <h1 className="text-xl font-bold text-white leading-tight">{problem.question_title || problem.question}</h1>
              </div>
              <div className="flex items-center gap-2 shrink-0">
                {solved && (
                  <span className="flex items-center gap-1 text-[10px] text-green-400 bg-green-900/30 border border-green-800 px-2 py-1 rounded-full">
                    <CheckCircle2 size={12} /> Solved
                  </span>
                )}
                <span className={`text-[10px] px-3 py-1 rounded-full font-medium ${difficultyClass}`}>
                  {problem.difficulty}
                </span>
              </div>
            </div>

            {/* Stats Bar (GFG-style) */}
            <div className="flex flex-wrap items-center gap-4 text-[11px] text-gray-400">
              {acceptanceRate != null && (
                <div className="flex items-center gap-1.5">
                  <Users size={12} />
                  <span>Acceptance: <span className="text-gray-300 font-medium">{acceptanceRate}%</span></span>
                  {totalSubmissions > 0 && <span className="text-gray-600">({totalSubmissions.toLocaleString()} submissions)</span>}
                </div>
              )}
              {avgTime && (
                <div className="flex items-center gap-1.5">
                  <Clock size={12} />
                  <span>Avg Time: <span className="text-gray-300 font-medium">{avgTime}</span></span>
                </div>
              )}
              {problem.frequency != null && (
                <div className="flex items-center gap-1.5">
                  <TrendingUp size={12} />
                  <span>{problem.frequency} practices</span>
                </div>
              )}
            </div>

            {/* Expected Complexity (GFG-style) */}
            {(expectedTime || expectedSpace) && (
              <div className="flex items-center gap-4 bg-blue-900/10 border border-blue-800/30 rounded-lg px-4 py-2.5">
                <span className="text-[10px] text-blue-400 font-medium uppercase tracking-wide">Expected Complexity</span>
                {expectedTime && (
                  <span className="text-xs text-gray-300">
                    Time: <code className="px-1.5 py-0.5 bg-gray-800 rounded text-green-400 font-mono text-[11px]">{expectedTime}</code>
                  </span>
                )}
                {expectedSpace && (
                  <span className="text-xs text-gray-300">
                    Space: <code className="px-1.5 py-0.5 bg-gray-800 rounded text-green-400 font-mono text-[11px]">{expectedSpace}</code>
                  </span>
                )}
              </div>
            )}

            {/* Company Tags */}
            {companyList.length > 0 && (
              <div className="flex items-center gap-2 flex-wrap">
                <Building2 size={12} className="text-gray-500" />
                {companyList.map((c, i) => (
                  <span key={i} className="text-[10px] px-2.5 py-1 bg-blue-900/20 border border-blue-800/30 text-blue-400 rounded-full">
                    {c}
                  </span>
                ))}
              </div>
            )}

            {/* Topic Tags */}
            {problem.topics?.length > 0 && (
              <div className="flex flex-wrap gap-1.5">
                {problem.topics.map((topic, i) => (
                  <span key={i} className="text-[10px] px-2 py-1 rounded-full bg-gray-800 text-gray-300 border border-gray-700">
                    {topic}
                  </span>
                ))}
              </div>
            )}

            {/* Statement */}
            {problem.statement && (
              <div className="text-sm text-gray-300 leading-relaxed whitespace-pre-wrap">
                {problem.statement}
              </div>
            )}

            {/* Examples */}
            {problem.examples?.length > 0 && (
              <div className="space-y-3">
                <h3 className="text-sm font-semibold text-gray-300">Examples</h3>
                {problem.examples.map((ex, i) => (
                  <div key={i} className="bg-space-void/80 border border-space-border rounded-xl p-4 space-y-2">
                    <div>
                      <span className="text-[10px] text-gray-500 font-medium">Example {i + 1}</span>
                      <div className="mt-1.5 grid grid-cols-2 gap-3">
                        <div>
                          <span className="text-[10px] text-gray-500">Input:</span>
                          <pre className="text-xs text-green-400 font-mono mt-1 whitespace-pre-wrap bg-gray-900/50 rounded p-2">{ex.input || ex.input_text || ""}</pre>
                        </div>
                        <div>
                          <span className="text-[10px] text-gray-500">Output:</span>
                          <pre className="text-xs text-green-400 font-mono mt-1 whitespace-pre-wrap bg-gray-900/50 rounded p-2">{ex.output || ex.output_text || ""}</pre>
                        </div>
                      </div>
                      {ex.explanation && (
                        <p className="text-xs text-gray-400 mt-2 italic">{ex.explanation}</p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Constraints */}
            {problem.constraints?.length > 0 && (
              <div className="bg-space-void/50 border border-space-border rounded-xl p-4">
                <h3 className="text-sm font-semibold text-gray-300 mb-2">Constraints</h3>
                <ul className="space-y-1">
                  {problem.constraints.map((c, i) => (
                    <li key={i} className="text-xs text-gray-400 font-mono">
                      <span className="text-cyber-blue mr-2">•</span>{c}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Hints (progressive reveal like LeetCode) */}
            {hints.length > 0 && (
              <div className="bg-yellow-900/10 border border-yellow-800/30 rounded-xl p-4">
                <h3 className="text-sm font-semibold text-yellow-400 mb-3 flex items-center gap-2">
                  <Lightbulb size={14} /> Hints
                  <span className="text-[10px] text-gray-500 font-normal ml-auto">{hintsRevealed}/{hints.length} revealed</span>
                </h3>
                <div className="space-y-2">
                  {hints.map((hint, i) => (
                    <div key={i}>
                      {i < hintsRevealed ? (
                        <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }} className="text-xs text-gray-300 bg-yellow-900/10 rounded-lg p-3 border border-yellow-800/20">
                          <span className="text-yellow-500 font-medium mr-2">{i + 1}.</span>{hint}
                        </motion.div>
                      ) : i === hintsRevealed ? (
                        <button onClick={() => setHintsRevealed(hintsRevealed + 1)} className="text-xs text-yellow-400 hover:text-yellow-300 flex items-center gap-1">
                          <Sparkles size={12} /> Reveal Hint {i + 1}
                        </button>
                      ) : null}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Visible Test Cases */}
            {problem.visible_test_cases?.length > 0 && (
              <div className="bg-space-void/50 border border-space-border rounded-xl p-4">
                <h3 className="text-sm font-semibold text-gray-300 mb-3">Test Cases</h3>
                <div className="space-y-2">
                  {problem.visible_test_cases.map((tc, i) => (
                    <div key={i} className="bg-space-panel/50 rounded-lg p-3 border border-space-border">
                      <div className="grid grid-cols-2 gap-3 text-xs">
                        <div>
                          <span className="text-gray-500 block mb-1">Input</span>
                          <pre className="text-green-400 font-mono whitespace-pre-wrap text-[11px]">{tc.input || tc.stdin || ""}</pre>
                        </div>
                        <div>
                          <span className="text-gray-500 block mb-1">Expected Output</span>
                          <pre className="text-green-400 font-mono whitespace-pre-wrap text-[11px]">{tc.expected || tc.expected_output || ""}</pre>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Solution */}
            {problem.solution && !problem.solution.locked && (
              <div className="bg-green-900/10 border border-green-800/30 rounded-xl p-4">
                <h3 className="text-sm font-semibold text-green-400 mb-2 flex items-center gap-2"><Zap size={14} /> Solution</h3>
                <pre className="text-xs text-gray-300 font-mono whitespace-pre-wrap">
                  {typeof problem.solution === "string" ? problem.solution : JSON.stringify(problem.solution, null, 2)}
                </pre>
              </div>
            )}

            {problem.solution?.locked && (
              <div className="bg-gray-800/50 border border-gray-700 rounded-xl p-4 flex items-center gap-2 text-gray-500">
                <Lock size={16} />
                <span className="text-xs">{problem.solution.message || "Upgrade to Pro to unlock the solution"}</span>
              </div>
            )}

            {/* Similar Problems */}
            {similarProblems.length > 0 && (
              <div className="border border-space-border rounded-xl p-4">
                <h3 className="text-sm font-semibold text-gray-300 mb-3">Similar Problems</h3>
                <div className="space-y-1.5">
                  {similarProblems.map((sp, i) => (
                    <Link key={i} to={`/solve/${sp.id}`} className="flex items-center justify-between py-1.5 px-2 rounded hover:bg-gray-800/50 transition-colors group">
                      <div className="flex items-center gap-2">
                        <span className={`text-[10px] px-1.5 py-0.5 rounded ${DIFFICULTY_STYLES[sp.difficulty] || "text-gray-400"}`}>{sp.difficulty?.charAt(0).toUpperCase()}</span>
                        <span className="text-xs text-gray-300 group-hover:text-white">{sp.question_title || sp.question}</span>
                      </div>
                      <ExternalLink size={11} className="text-gray-600 group-hover:text-gray-400" />
                    </Link>
                  ))}
                </div>
              </div>
            )}
          </>
        )}

        {/* Solutions Tab */}
        {activeSection === "solutions" && (
          <div className="space-y-4">
            {problem.solution && !problem.solution.locked ? (
              <div className="bg-green-900/10 border border-green-800/30 rounded-xl p-5">
                <h3 className="text-sm font-semibold text-green-400 mb-3 flex items-center gap-2"><Zap size={14} /> Official Solution</h3>
                <pre className="text-xs text-gray-300 font-mono whitespace-pre-wrap leading-relaxed">
                  {typeof problem.solution === "string" ? problem.solution : JSON.stringify(problem.solution, null, 2)}
                </pre>
              </div>
            ) : (
              <div className="text-center py-12 text-gray-500">
                <Lock size={32} className="mx-auto mb-3 opacity-50" />
                <p className="text-sm">Solve this problem or upgrade to Pro to unlock solutions</p>
              </div>
            )}
          </div>
        )}

        {/* Submissions Tab */}
        {activeSection === "submissions" && (
          <div className="text-center py-12 text-gray-500">
            <TrendingUp size={32} className="mx-auto mb-3 opacity-50" />
            <p className="text-sm">Submit your code in the editor to see submissions here</p>
          </div>
        )}

        {/* Discussions Tab */}
        {activeSection === "discussions" && (
          <div className="space-y-4">
            <div className="flex gap-2">
              <textarea
                value={discussionContent}
                onChange={(e) => setDiscussionContent(e.target.value)}
                placeholder="Share your approach, solution, or ask a question..."
                className="flex-1 px-3 py-2 bg-space-void border border-space-border rounded-lg text-xs text-gray-200 focus:border-cyber-blue focus:outline-none resize-none"
                rows={3}
              />
            </div>
            <button
              onClick={handlePostDiscussion}
              disabled={submittingDiscussion || !discussionContent.trim()}
              className="px-3 py-1.5 bg-cyber-blue hover:bg-cyber-blue/80 disabled:opacity-50 text-space-void text-xs font-medium rounded-lg transition-colors"
            >
              {submittingDiscussion ? "Posting..." : "Post"}
            </button>

            {discussions.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <MessageSquare size={24} className="mx-auto mb-2 opacity-50" />
                <p className="text-xs">No discussions yet. Be the first!</p>
              </div>
            ) : (
              <div className="space-y-3">
                {discussions.map((d, i) => (
                  <div key={d.id || i} className="bg-space-void/50 border border-space-border rounded-lg p-3">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-xs font-medium text-gray-300">{d.user_name || "Anonymous"}</span>
                      <span className="text-[10px] text-gray-500">{d.created_at ? new Date(d.created_at).toLocaleDateString() : ""}</span>
                      {d.discussion_type === "solution" && (
                        <span className="text-[10px] px-1.5 py-0.5 bg-green-900/30 text-green-400 rounded">Solution</span>
                      )}
                    </div>
                    <p className="text-xs text-gray-300 whitespace-pre-wrap">{d.content}</p>
                    {d.upvotes > 0 && (
                      <div className="flex items-center gap-1 mt-2 text-[10px] text-gray-500">
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
