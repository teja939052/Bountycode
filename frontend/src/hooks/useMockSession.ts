import { useState, useEffect, useCallback, useRef } from "react";

export interface Section {
  id: string;
  title: string;
  duration_minutes: number;
  question_ids: string[];
}

export interface MockSessionState {
  currentSectionIndex: number;
  timeRemainingSeconds: number;
  completedSectionIds: string[];
  tabViolationsCount: number;
  answers: Record<string, string>;
  flaggedQuestionIds: string[];
  lastSavedAt: number | null;
  isFullscreen: boolean;
  isExamComplete: boolean;
}

export interface UseMockSessionOptions {
  mockId: string;
  sections: Section[];
  onExamComplete: (state: MockSessionState) => void;
  maxTabViolations?: number;
}

export interface UseMockSessionReturn {
  state: MockSessionState;
  triggerFullscreen: () => Promise<void>;
  handleAnswerSelection: (questionId: string, answer: string) => void;
  toggleFlag: (questionId: string) => void;
  advanceSection: () => void;
  currentSection: Section | undefined;
  canGoBack: boolean;
  isLocked: boolean;
}

export function useMockSession({
  mockId,
  sections,
  onExamComplete,
  maxTabViolations = 3,
}: UseMockSessionOptions): UseMockSessionReturn {
  const storageKey = mockId ? `bountycode:mock-session:${mockId}` : "";
  const [state, setState] = useState<MockSessionState>({
    currentSectionIndex: 0,
    timeRemainingSeconds: sections[0]?.duration_minutes * 60 || 0,
    completedSectionIds: [],
    tabViolationsCount: 0,
    answers: {},
    flaggedQuestionIds: [],
    lastSavedAt: null,
    isFullscreen: false,
    isExamComplete: false,
  });

  useEffect(() => {
    let restored: MockSessionState | null = null;
    if (storageKey && sections.length) {
      try {
        const raw = sessionStorage.getItem(storageKey);
        const parsed = raw ? JSON.parse(raw) : null;
        if (parsed && Number(parsed.currentSectionIndex) < sections.length && !parsed.isExamComplete) {
          restored = {
            ...parsed,
            currentSectionIndex: Math.max(0, Number(parsed.currentSectionIndex) || 0),
            timeRemainingSeconds: Math.max(0, Number(parsed.timeRemainingSeconds) || 0),
            completedSectionIds: Array.isArray(parsed.completedSectionIds) ? parsed.completedSectionIds : [],
            flaggedQuestionIds: Array.isArray(parsed.flaggedQuestionIds) ? parsed.flaggedQuestionIds.map(String) : [],
            answers: parsed.answers && typeof parsed.answers === "object" ? parsed.answers : {},
            lastSavedAt: Number(parsed.lastSavedAt) || null,
          };
        }
      } catch {
        restored = null;
      }
    }
    setState({
      ...(restored || {
        currentSectionIndex: 0,
        timeRemainingSeconds: sections[0]?.duration_minutes ? sections[0].duration_minutes * 60 : 0,
        completedSectionIds: [],
        tabViolationsCount: 0,
        answers: {},
        flaggedQuestionIds: [],
        lastSavedAt: null,
        isFullscreen: false,
        isExamComplete: false,
      }),
    });
  }, [storageKey, sections.length]);

  useEffect(() => {
    if (!storageKey || !sections.length || state.isExamComplete) return;
    try {
      const saved = { ...state, lastSavedAt: Date.now() };
      sessionStorage.setItem(storageKey, JSON.stringify(saved));
      if (!state.lastSavedAt) setState((prev) => ({ ...prev, lastSavedAt: saved.lastSavedAt }));
    } catch {
      // Private browsing or storage limits should never block an assessment.
    }
  }, [storageKey, sections.length, state]);

  useEffect(() => {
    if (!storageKey || !state.isExamComplete) return;
    try { sessionStorage.removeItem(storageKey); } catch { /* ignore storage failures */ }
  }, [storageKey, state.isExamComplete]);

  const onExamCompleteRef = useRef(onExamComplete);
  onExamCompleteRef.current = onExamComplete;

  const currentSection = sections[state.currentSectionIndex];
  const canGoBack = state.currentSectionIndex > 0 && !state.isExamComplete;
  const isLocked = state.isExamComplete;

  const triggerFullscreen = useCallback(async () => {
    try {
      if (!document.fullscreenElement && !document.webkitFullscreenElement) {
        await document.documentElement.requestFullscreen().catch(() => {});
      }
      setState((prev) => ({ ...prev, isFullscreen: true }));
    } catch {
      setState((prev) => ({ ...prev, isFullscreen: false }));
    }
  }, []);

  const handleAnswerSelection = useCallback((questionId: string, answer: string) => {
    setState((prev) => ({
      ...prev,
      answers: { ...prev.answers, [questionId]: answer },
    }));
  }, []);

  const toggleFlag = useCallback((questionId: string) => {
    setState((prev) => ({
      ...prev,
      flaggedQuestionIds: prev.flaggedQuestionIds.includes(questionId)
        ? prev.flaggedQuestionIds.filter((id) => id !== questionId)
        : [...prev.flaggedQuestionIds, questionId],
    }));
  }, []);

  const advanceSection = useCallback(() => {
    setState((prev) => {
      const nextIndex = prev.currentSectionIndex + 1;
      const currentSection = sections[prev.currentSectionIndex];
      if (!currentSection || !currentSection.id) {
        return prev;
      }
      const updatedCompleted = [...prev.completedSectionIds, currentSection.id];

      if (nextIndex >= sections.length) {
        const finalState = {
          ...prev,
          completedSectionIds: updatedCompleted,
          timeRemainingSeconds: 0,
          isExamComplete: true,
        };
        onExamCompleteRef.current(finalState);
        return finalState;
      }

      return {
        ...prev,
        currentSectionIndex: nextIndex,
        completedSectionIds: updatedCompleted,
        timeRemainingSeconds: sections[nextIndex].duration_minutes * 60,
      };
    });
  }, [sections]);

  useEffect(() => {
    if (!sections.length || state.timeRemainingSeconds > 0 || state.isExamComplete) {
      return;
    }
    advanceSection();
  }, [state.timeRemainingSeconds, state.isExamComplete, advanceSection, sections.length]);

  useEffect(() => {
    const handleVisibilityChange = () => {
      if (state.isExamComplete) return;

      if (document.hidden) {
        setState((prev) => {
          const newViolations = prev.tabViolationsCount + 1;
          if (newViolations >= maxTabViolations) {
            const finalState = {
              ...prev,
              tabViolationsCount: newViolations,
              isExamComplete: true,
            };
            onExamCompleteRef.current(finalState);
            return finalState;
          }
          return { ...prev, tabViolationsCount: newViolations };
        });
      }
    };

    const handleFullscreenChange = () => {
      const isFs = !!(document.fullscreenElement || document.webkitFullscreenElement);
      setState((prev) => ({ ...prev, isFullscreen: isFs }));
    };

    document.addEventListener("visibilitychange", handleVisibilityChange);
    document.addEventListener("fullscreenchange", handleFullscreenChange);
    document.addEventListener("webkitfullscreenchange", handleFullscreenChange);

    return () => {
      document.removeEventListener("visibilitychange", handleVisibilityChange);
      document.removeEventListener("fullscreenchange", handleFullscreenChange);
      document.removeEventListener("webkitfullscreenchange", handleFullscreenChange);
    };
  }, [maxTabViolations, state.isExamComplete]);

  return {
    state,
    triggerFullscreen,
    handleAnswerSelection,
    toggleFlag,
    advanceSection,
    currentSection,
    canGoBack,
    isLocked,
  };
}
