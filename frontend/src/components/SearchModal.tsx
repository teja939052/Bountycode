// @ts-nocheck
import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { Search, ArrowRight, X } from "lucide-react";
import Fuse from "fuse.js";

const ROUTES = [
  { path: "/placement", label: "Today", desc: "Today's mission", category: "Journey" },
  { path: "/curriculum", label: "Learn", desc: "Placement curriculum", category: "Journey" },
  { path: "/question-bank", label: "Practice", desc: "Question bank", category: "Journey" },
  { path: "/mock-oa", label: "Assess", desc: "Mock online assessment", category: "Journey" },
  { path: "/profile", label: "Profile", desc: "Career profile", category: "Journey" },
  { path: "/aptitude", label: "Aptitude Test", desc: "Quant · Logical · Verbal", category: "Practice" },
  { path: "/coding", label: "Coding Challenges", desc: "Timed problems", category: "Practice" },
  { path: "/daily-challenge", label: "Daily Challenge", desc: "Adaptive missions", category: "Practice" },
  { path: "/battlefield", label: "Battlefield", desc: "Pattern mastery", category: "Practice" },
  { path: "/compiler", label: "Compiler", desc: "Run code", category: "Tools" },
  { path: "/interview", label: "Mock Interview", desc: "Interview sessions", category: "Tools" },
  { path: "/resume", label: "Resume Builder", desc: "Upload or generate", category: "Tools" },
  { path: "/ats", label: "ATS Optimizer", desc: "Match to job description", category: "Tools" },
  { path: "/pricing", label: "Pricing", desc: "Pro and Lifetime", category: "Account" },
];

const fuse = new Fuse(ROUTES, {
  keys: [
    { name: "label", weight: 0.5 },
    { name: "desc", weight: 0.3 },
    { name: "category", weight: 0.2 },
  ],
  threshold: 0.35,
});

export default function SearchModal({ open, onClose }: { open: boolean; onClose: () => void }) {
  const [query, setQuery] = useState("");
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const listRef = useRef<HTMLDivElement>(null);

  const results = query.trim() ? fuse.search(query.trim()).map((r) => r.item) : ROUTES;

  useEffect(() => {
    if (!open) return;
    setQuery("");
    setSelectedIndex(0);
    const timer = setTimeout(() => inputRef.current?.focus(), 50);
    return () => clearTimeout(timer);
  }, [open]);

  useEffect(() => {
    if (!open) return;
    const handler = (e: KeyboardEvent) => {
      if (e.key === "ArrowDown") {
        e.preventDefault();
        setSelectedIndex((prev) => Math.min(prev + 1, results.length - 1));
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        setSelectedIndex((prev) => Math.max(prev - 1, 0));
      } else if (e.key === "Enter") {
        e.preventDefault();
        const target = results[selectedIndex];
        if (target) {
          window.location.href = target.path;
          onClose();
        }
      } else if (e.key === "Escape") {
        onClose();
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [open, results, selectedIndex, onClose]);

  useEffect(() => {
    if (!open || !listRef.current) return;
    const selected = listRef.current.children[selectedIndex] as HTMLElement | undefined;
    selected?.scrollIntoView({ block: "nearest" });
  }, [selectedIndex, open]);

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-[60] flex items-start justify-center pt-[15vh] px-4">
      <div className="absolute inset-0 bg-black/40 backdrop-blur-sm" onClick={onClose} />
      <div className="relative w-full max-w-xl rounded-2xl border border-border bg-white shadow-2xl overflow-hidden">
        <div className="flex items-center gap-3 px-4 py-3 border-b border-border">
          <Search size={18} className="text-text-muted shrink-0" />
          <input
            ref={inputRef}
            value={query}
            onChange={(e) => { setQuery(e.target.value); setSelectedIndex(0); }}
            placeholder="Search pages, features, tools..."
            className="flex-1 bg-transparent text-sm text-text-primary placeholder:text-text-muted outline-none"
          />
          <kbd className="hidden sm:inline-flex items-center rounded-md border border-border px-2 py-1 text-[10px] font-mono text-text-muted">
            ESC
          </kbd>
        </div>
        <div ref={listRef} className="max-h-[50vh] overflow-y-auto py-2">
          {results.length === 0 ? (
            <div className="px-4 py-8 text-center text-sm text-text-muted">No results found</div>
          ) : (
            results.map((item, idx) => (
              <Link
                key={item.path}
                to={item.path}
                onClick={onClose}
                className={`flex items-center justify-between px-4 py-2.5 transition-colors ${
                  idx === selectedIndex ? "bg-surface-2" : "hover:bg-surface-2"
                }`}
              >
                <div className="min-w-0">
                  <div className="text-sm font-medium text-text-primary">{item.label}</div>
                  <div className="text-xs text-text-muted truncate">{item.desc}</div>
                </div>
                <div className="flex items-center gap-2 shrink-0 ml-3">
                  <span className="text-[10px] font-mono uppercase tracking-wide text-text-muted">{item.category}</span>
                  <ArrowRight size={14} className="text-text-muted" />
                </div>
              </Link>
            ))
          )}
        </div>
        <div className="flex items-center justify-between px-4 py-2 border-t border-border bg-surface-2/50">
          <div className="flex items-center gap-3 text-[10px] text-text-muted">
            <span className="flex items-center gap-1"><kbd className="rounded border border-border px-1 py-0.5 font-mono">↑↓</kbd> navigate</span>
            <span className="flex items-center gap-1"><kbd className="rounded border border-border px-1 py-0.5 font-mono">↵</kbd> open</span>
          </div>
          <button onClick={onClose} className="text-text-muted hover:text-text-primary">
            <X size={14} />
          </button>
        </div>
      </div>
    </div>
  );
}
