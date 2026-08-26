import { useState, useEffect } from "react";
import { useLearningGuide } from "../hooks/useLearningGuide";
import { Play, Check, Trophy, Zap } from "lucide-react";
import api from "../services/api";

type MiniProjectLesson = {
  id: string;
  title: string;
  description: string;
  requirements: string[];
  codeTemplate: string;
  language: "python" | "javascript" | "java" | "cpp";
  testCases?: Array<{ input: string; expectedOutput: string }>;
  hint?: string;
  onCompleteCallback?: () => void;
};

interface MiniProjectState {
  isRunning: boolean;
  executionResult: string | null;
  executionError: string | null;
  testResults: Array<{ passed: boolean; output: string }>;
  isSubmitted: boolean;
  attempts: number;
}

export function MiniProjectLesson({
  lesson,
  onComplete,
}: {
  lesson: MiniProjectLesson;
  onComplete: (progress: {
    id: string;
    isCompleted: boolean;
    xpEarned: number;
  }) => void;
}) {
  const [state, setState] = useState<MiniProjectState>({
    isRunning: false,
    executionResult: null,
    executionError: null,
    testResults: [],
    isSubmitted: false,
    attempts: 0,
  });
  const { advanceToPractice, markComplete, awardXP } = useLearningGuide("user_123");
  const [editCode, setEditCode] = useState(lesson.codeTemplate);

  // Execute code
  const runCode = useCallback(async () => {
    setState({
      ...state,
      isRunning: true,
      executionResult: null,
      executionError: null,
      testResults: [],
    });

    try {
      const res = await api.compiler.execute({
        code: editCode,
        language: lesson.language,
      });

      setState({
        ...state,
        isRunning: false,
        executionResult: res.output || null,
        executionError: res.error || null,
      });

      // Run test cases if available
      let results = [];
      if (lesson.testCases && res.output) {
        for (const tc of lesson.testCases) {
          const passed = res.output.includes(tc.expectedOutput);
          results.push({
            passed,
            output: res.output,
          });
        }
      }
      setState({
        ...state,
        testResults: results,
      });
    } catch (err) {
      setState({
        ...state,
        isRunning: false,
        executionError: "Execution failed",
        testResults: [],
      });
    }
  }, [editCode, lesson.language]);

  // Check if all tests pass
  const allTestsPass = state.testResults.every((t) => t.passed);

  // Submit project
  const submitProject = useCallback(async () => {
    setState({
      ...state,
      isSubmitted: true,
      attempts: state.attempts + 1,
    });

    // Award XP
    awardXP(50);

    onComplete({
      id: lesson.id,
      isCompleted: allTestsPass,
      xpEarned: allTestsPass ? 50 : 25,
    });
  }, [allTestsPass, awardXP]);

  return (
    <div className="p-6 bg-[var(--pp-surface)] border border-[var(--pp-border)] rounded-2xl shadow-soft-lg">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 rounded-[10px] bg-primary-soft flex items-center justify-center">
          <Trophy size={20} className="text-gold" />
        </div>
        <div>
          <h2 className="font-medium text-text-primary">{lesson.title}</h2>
          <p className="text-text-muted text-sm">{lesson.description}</p>
        </div>
      </div>

      <div className="mb-6">
        <div className="flex items-center gap-2 text-xs text-text-muted mb-2">
          <span>Language:</span>
          <span className="font-mono text-primary">{lesson.language.toUpperCase()}</span>
        </div>
        <textarea
          value={editCode}
          onChange={(e) => setEditCode(e.target.value)}
          className="w-full rounded-xl border border-border p-4 font-mono text-sm text-text-primary bg-surface-2 resize-none focus:outline-none focus:ring-2 focus:ring-primary/20 min-h-[200px]"
        />
      </div>

      <div className="mb-4">
        <button
          onClick={runCode}
          disabled={state.isRunning}
          className="flex-1 px-4 py-2 rounded-xl bg-primary text-white text-sm font-medium hover:bg-primary-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {state.isRunning ? "Running..." : "▶ Run Code"}
        </button>
      </div>

      {/* Execution Results */}
      {state.executionResult !== null || state.executionError !== null && (
        <div className="mb-4 p-4 rounded-xl border-t-4 {
          state.executionError
            ? "bg-error/10 border border-error/20 text-error"
            : state.isRunning
            ? "bg-primary/20 border border-primary text-primary"
            : ""
        }">
          {state.executionError && <p className="text-error text-sm mb-2">⚠ {state.executionError}</p>}
          {state.executionResult && <p className="font-mono text-sm line-clamp-3">{state.executionResult}</p>}
        </div>
      )}

      {/* Test Results */}
      {lesson.testCases && state.testResults.length > 0 && (
        <div className="mb-4">
          <p className="text-text-muted text-sm mb-2">Test Results:</p>
          <div className="grid grid-cols-2 gap-2">
            {state.testResults.map((result, i) => (
              <div key={i} className={result.passed ? "bg-success/10 border border-success/20 text-success" : "bg-error/10 border border-error/20 text-error">
                <span className="font-medium">{result.passed ? "✅ Pass" : "❌ Fail"}</span>
                <span className="text-xs ml-2">{result.output.substring(0, 50)}${result.output.length > 50 ? "..." : ""}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Requirements */}
      {lesson.requirements && (
        <div className="mb-4">
          <p className="text-text-muted text-sm mb-2">Requirements:</p>
          <ul className="list-disc list-inside text-text-muted space-y-1">
            {lesson.requirements.map((req, i) => (
              <li key={i} className="text-sm">
                {req}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Action Buttons */}
      <div className="mt-6 flex gap-3">
        {state.isSubmitted ? (
          <>
            <button
              onClick={submitProject}
              disabled={!allTestsPass}
              className="flex-1 px-4 py-2 rounded-xl bg-success text-white text-sm font-medium hover:bg-success/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              ✅ Submit Project
            </button>
            {!allTestsPass && (
              <button
                onClick={() => setState((prev) => ({ ...prev, isSubmitted: false }))}
                className="flex-1 px-4 py-2 rounded-xl bg-surface-2 border border-border text-text-primary text-sm font-medium hover:bg-surface-100 transition-colors mt-2"
              >
                ↺ Revise & Resubmit
              </button>
            )}
          </>
        ) : (
          <>
            <button
              onClick={runCode}
              className="flex-1 px-4 py-2 rounded-xl bg-primary text-white text-sm font-medium hover:bg-primary-dark transition-colors"
            >
              ▶ Run Code
            </button>
            {lesson.hint && (
              <button
                onClick={() => alert(lesson.hint)}
                className="flex-1 px-4 py-2 rounded-xl bg-primary-soft text-primary/80 text-sm font-medium hover:bg-primary/90 transition-colors mt-2"
              >
                💡 Hint
              </button>
            )}
          </>
        )}
      </div>
    </div>
  );
}