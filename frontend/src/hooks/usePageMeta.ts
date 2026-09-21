import { useEffect } from "react";

const SITE = "BountyCode";

/**
 * Lightweight per-page title/meta for the Vite SPA.
 * In-app UX only (document.title + meta description while navigating).
 * Honest limitation: crawlers/link unfurls read the static index.html,
 * not these JS-set tags — no SSR/prerendering is being attempted here.
 */
export function usePageMeta(title: string, description?: string) {
  useEffect(() => {
    const full = title.includes(SITE) ? title : `${title} — ${SITE}`;
    document.title = full;
    if (description) {
      let tag = document.querySelector<HTMLMetaElement>('meta[name="description"]');
      if (!tag) {
        tag = document.createElement("meta");
        tag.name = "description";
        document.head.appendChild(tag);
      }
      tag.content = description;
    }
    return () => {
      document.title = `${SITE} — Placement Preparation: Coding Practice, Mock Interviews, Resume ATS`;
    };
  }, [title, description]);
}
