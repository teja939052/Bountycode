import { useState, useEffect, useCallback } from "react";
import { Bug, X, Copy, Trash2, RefreshCw } from "lucide-react";
import { getTrackedErrors, clearTrackedErrors } from "../services/errorTracker";

function copyText(text) {
  try {
    navigator.clipboard.writeText(text);
  } catch {
    const ta = document.createElement("textarea");
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand("copy");
    document.body.removeChild(ta);
  }
}

export default function DebugPanel() {
  const [open, setOpen] = useState(false);
  const [errors, setErrors] = useState([]);
  const [unread, setUnread] = useState(0);

  const refresh = useCallback(() => {
    setErrors(getTrackedErrors());
  }, []);

  useEffect(() => {
    const handler = () => {
      refresh();
      setUnread((n) => n + 1);
    };
    window.addEventListener("pp-error-tracked", handler);
    refresh();
    return () => window.removeEventListener("pp-error-tracked", handler);
  }, [refresh]);

  useEffect(() => {
    if (open) setUnread(0);
  }, [open]);

  return (
    <>
      <button
        onClick={() => setOpen((v) => !v)}
        title="Debug errors"
        className="fixed bottom-20 right-4 z-[9999] flex h-10 w-10 items-center justify-center rounded-full border border-cyber-red/40 bg-black/70 text-cyber-red shadow-lg backdrop-blur transition hover:bg-cyber-red/20"
      >
        <Bug size={18} />
        {unread > 0 && !open && (
          <span className="absolute -top-1 -right-1 flex h-4 min-w-4 items-center justify-center rounded-full bg-cyber-red px-1 text-[10px] font-bold text-white">
            {unread}
          </span>
        )}
      </button>

      {open && (
        <div className="fixed bottom-36 right-4 z-[9999] flex max-h-[70vh] w-[420px] max-w-[calc(100vw-2rem)] flex-col rounded-xl border border-cyber-red/30 bg-black/90 shadow-2xl backdrop-blur">
          <div className="flex items-center justify-between border-b border-white/10 px-4 py-3">
            <div className="flex items-center gap-2 font-mono text-sm font-bold text-cyber-red">
              <Bug size={16} /> Error Tracker <span className="text-white/40">({errors.length})</span>
            </div>
            <div className="flex items-center gap-2">
              <button onClick={() => { clearTrackedErrors(); refresh(); }} className="text-white/40 hover:text-white" title="Clear">
                <Trash2 size={16} />
              </button>
              <button onClick={refresh} className="text-white/40 hover:text-white" title="Refresh">
                <RefreshCw size={16} />
              </button>
              <button onClick={() => setOpen(false)} className="text-white/40 hover:text-white" title="Close">
                <X size={16} />
              </button>
            </div>
          </div>

          <div className="flex-1 overflow-y-auto p-3 space-y-2">
            {errors.length === 0 && (
              <p className="font-mono text-xs text-white/40">No errors tracked yet. Any crash, rejected promise, or console.error will show here and post to /api/v1/debug/log.</p>
            )}
            {errors.map((err, i) => (
              <div key={i} className="rounded-lg border border-white/10 bg-white/5 p-2">
                <div className="flex items-start justify-between gap-2">
                  <div className="min-w-0">
                    <p className="break-words font-mono text-xs font-semibold text-cyber-red">{err.message}</p>
                    <p className="mt-0.5 font-mono text-[10px] text-white/40">
                      {err.component} · {err.url} · {err.at}
                    </p>
                  </div>
                  <button onClick={() => copyText(`${err.message}\n\n${err.stack || ""}`)} className="shrink-0 text-white/40 hover:text-white" title="Copy">
                    <Copy size={14} />
                  </button>
                </div>
                {err.stack && (
                  <pre className="mt-1 max-h-32 overflow-y-auto whitespace-pre-wrap break-words font-mono text-[10px] leading-tight text-white/60">
                    {err.stack}
                  </pre>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </>
  );
}
