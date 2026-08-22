import { X } from "lucide-react";

export default function Modal({ isOpen, onClose, title, children }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-end justify-center p-3 sm:items-center sm:p-4" role="dialog" aria-modal="true" aria-labelledby="modal-title">
      <div className="fixed inset-0 bg-slate-950/55 backdrop-blur-sm" onClick={onClose} aria-hidden="true" />
      <div className="relative w-full max-w-2xl overflow-hidden rounded-3xl border border-black/5 bg-[color:var(--bg-card,#fff)] shadow-[0_30px_80px_rgba(15,23,42,0.25)] max-h-[88vh]">
        <div className="flex items-center justify-between gap-3 border-b border-black/5 px-4 py-3 sm:px-6">
          <h2 id="modal-title" className="text-base font-semibold text-text-primary sm:text-lg">{title}</h2>
          <button onClick={onClose} className="rounded-full p-2 text-text-muted transition-colors hover:bg-black/5 hover:text-text-primary" aria-label="Close dialog">
            <X size={18} />
          </button>
        </div>
        <div className="max-h-[calc(88vh-57px)] overflow-y-auto px-4 py-4 sm:px-6 sm:py-5">
          {children}
        </div>
      </div>
    </div>
  );
}
