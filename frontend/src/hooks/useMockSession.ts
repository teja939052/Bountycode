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
  const [state, setState] = useState<MockSessionState>({
    currentSectionIndex: 0,
    timeRemainingSeconds: sections[0]?.duration_minutes * 60 || 0,
    completedSectionIds: [],
    tabViolationsCount: 0,
    answers: {},
    isFullscreen: false,
    isExamComplete: false,
  });

  useEffect(() => {
    setState({
      currentSectionIndex: 0,
      timeRemainingSeconds: sections[0]?.duration_minutes ? sections[0].duration_minutes * 60 : 0,
      completedSectionIds: [],
      tabViolationsCount: 0,
      answers: {},
      isFullscreen: false,
      isExamComplete: false,
    });
  }, [mockId, sections.length]);

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
    advanceSection,
    currentSection,
    canGoBack,
    isLocked,
  };
}
