import { useCallback, useEffect, useState } from "react";

const CACHE_PREFIX = "pp_curriculum_v1";
const CACHE_TTL = 60 * 60 * 24; // 24h in seconds

export interface Lesson {
  id: string;
  title: string;
  type?: string;
  xp?: number;
  section?: string;
  duration?: string;
  content?: {
    theory?: string;
    codeSnippets?: Array<{ code: string; output?: string }>;
    exercise?: {
      instruction: string;
      code?: string;
      language?: string;
      expected?: string;
      stdin?: string;
      hints?: string[];
      required?: string[];
      starterCode?: string;
    };
    quiz?: Array<{
      question: string;
      options: string[];
      correct: number;
    }>;
  };
  completion?: {
    nextLesson?: string;
  };
}

function readCache(key: string) {
  try {
    const raw = localStorage.getItem(`${CACHE_PREFIX}:${key}`);
    if (!raw) return null;
    const { t, data } = JSON.parse(raw);
    if (Date.now() - t > CACHE_TTL * 1000) return null;
    return data;
  } catch {
    return null;
  }
}

function writeCache(key: string, data: unknown) {
  try {
    localStorage.setItem(
      `${CACHE_PREFIX}:${key}`,
      JSON.stringify({ t: Date.now(), data })
    );
  } catch {
    // storage full or unavailable — non-fatal
  }
}

export function useCurriculumIndex() {
  const [index, setIndex] = useState<Record<string, unknown> | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    const cached = readCache("index");
    if (cached) {
      setIndex(cached);
      setLoading(false);
    }
    fetch("/curriculum/index.json")
      .then((r) => {
        if (!r.ok) throw new Error("curriculum index unavailable");
        return r.json();
      })
      .then((data) => {
        if (!active) return;
        writeCache("index", data);
        setIndex(data);
        setLoading(false);
      })
      .catch((err) => {
        if (!active) return;
        if (!cached) {
          setError(err instanceof Error ? err.message : "Failed to load curriculum");
          setLoading(false);
        }
      });
    return () => {
      active = false;
    };
  }, []);

  return { index, loading, error };
}

export function useLesson(trackId: string, lessonId: string) {
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const cacheKey = `${trackId}/${lessonId}`;

  useEffect(() => {
    let active = true;
    if (!trackId || !lessonId) return;
    setLoading(true);
    const cached = readCache(cacheKey);
    if (cached) {
      setLesson(cached as Lesson);
      setLoading(false);
    }
    fetch(`/curriculum/languages/${trackId}/${lessonId}.json`)
      .then((r) => {
        if (!r.ok) throw new Error("lesson not found");
        return r.json();
      })
      .then((data) => {
        if (!active) return;
        writeCache(cacheKey, data);
        setLesson(data as Lesson);
        setLoading(false);
      })
      .catch((err) => {
        if (!active) return;
        if (!cached) {
          setError(err instanceof Error ? err.message : "Failed to load lesson");
          setLoading(false);
        }
      });
    return () => {
      active = false;
    };
  }, [trackId, lessonId, cacheKey]);

  const preload = useCallback(
    (nextId: string) => {
      if (!trackId || !nextId) return;
      const key = `${trackId}/${nextId}`;
      if (readCache(key)) return;
      fetch(`/curriculum/languages/${trackId}/${nextId}.json`)
        .then((r) => (r.ok ? r.json() : null))
        .then((data) => {
          if (data) writeCache(key, data);
        })
        .catch(() => {});
    },
    [trackId]
  );

  return { lesson, loading, error, preload };
}
