import { useEffect, useState } from "react";
import { getLesson, saveLesson } from "../utils/offlineCache";

export default function useLessonCache(languageId, lessonId, content) {
  const [cachedContent, setCachedContent] = useState(null);
  const [isCached, setIsCached] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    let active = true;
    setIsCached(false);
    setCachedContent(null);
    if (!languageId || !lessonId) return () => {
      active = false;
    };
    getLesson(languageId, lessonId)
      .then((stored) => {
        if (!active) return;
        setCachedContent(stored);
        setIsCached(stored !== null && stored !== undefined);
      })
      .catch(() => {});
    return () => {
      active = false;
    };
  }, [languageId, lessonId]);

  useEffect(() => {
    if (!languageId || !lessonId || content === null || content === undefined)
      return;
    let active = true;
    setIsSaving(true);
    saveLesson(languageId, lessonId, content)
      .then(() => {
        if (active) setIsCached(true);
      })
      .catch(() => {})
      .finally(() => {
        if (active) setIsSaving(false);
      });
    return () => {
      active = false;
    };
  }, [languageId, lessonId, content]);

  return { cachedContent, isCached, isSaving };
}
