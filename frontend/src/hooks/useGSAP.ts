// @ts-nocheck
import { useEffect, useMemo } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

if (typeof window !== "undefined") {
  gsap.registerPlugin(ScrollTrigger);
}

export function useGSAPScrollTrigger(
  ref: { current: HTMLElement | null },
  options?: {
    y?: number;
    opacity?: number;
    scale?: number;
    duration?: number;
    start?: string;
    end?: string;
    scrub?: boolean | number;
    markers?: boolean;
  }
) {
  const reducedMotion = useMemo(
    () => typeof window !== "undefined" && window.matchMedia?.("(prefers-reduced-motion: reduce)").matches,
    []
  );

  useEffect(() => {
    if (reducedMotion || !ref.current) return;
    const ctx = gsap.context(() => {
      gsap.fromTo(
        ref.current,
        { y: options?.y ?? 30, opacity: options?.opacity ?? 0, scale: options?.scale ?? 1 },
        {
          y: 0,
          opacity: 1,
          scale: 1,
          duration: options?.duration ?? 0.8,
          ease: "power3.out",
          scrollTrigger: {
            trigger: ref.current,
            start: options?.start ?? "top 85%",
            end: options?.end ?? "top 40%",
            scrub: options?.scrub ?? false,
            markers: options?.markers ?? false,
          },
        }
      );
    }, ref);
    return () => ctx.revert();
  }, [ref, reducedMotion, options]);
}

export function useGSAPStagger(
  ref: { current: HTMLElement | null },
  options?: {
    y?: number;
    opacity?: number;
    scale?: number;
    duration?: number;
    stagger?: number;
    start?: string;
    end?: string;
    scrub?: boolean | number;
    markers?: boolean;
  }
) {
  const reducedMotion = useMemo(
    () => typeof window !== "undefined" && window.matchMedia?.("(prefers-reduced-motion: reduce)").matches,
    []
  );

  useEffect(() => {
    const el = ref.current;
    if (reducedMotion || !el) return;
    const ctx = gsap.context(() => {
      const children = el.children;
      if (!children || children.length === 0) return;
      gsap.fromTo(
        children,
        { y: options?.y ?? 24, opacity: options?.opacity ?? 0, scale: options?.scale ?? 1 },
        {
          y: 0,
          opacity: 1,
          scale: 1,
          duration: options?.duration ?? 0.6,
          stagger: options?.stagger ?? 0.08,
          ease: "power3.out",
          scrollTrigger: {
            trigger: el,
            start: options?.start ?? "top 85%",
            end: options?.end ?? "top 30%",
            scrub: options?.scrub ?? false,
            markers: options?.markers ?? false,
          },
        }
      );
    }, el);
    return () => ctx.revert();
  }, [ref, reducedMotion, options]);
}

export function useParallax(
  ref: { current: HTMLElement | null },
  speed = 0.15,
  start = "top bottom",
  end = "bottom top"
) {
  const reducedMotion = useMemo(
    () => typeof window !== "undefined" && window.matchMedia?.("(prefers-reduced-motion: reduce)").matches,
    []
  );

  useEffect(() => {
    if (reducedMotion || !ref.current) return;
    const ctx = gsap.context(() => {
      gsap.to(ref.current, {
        y: () => window.innerHeight * speed,
        ease: "none",
        scrollTrigger: {
          trigger: ref.current,
          start,
          end,
          scrub: true,
        },
      });
    }, ref);
    return () => ctx.revert();
  }, [ref, reducedMotion, speed, start, end]);
}
