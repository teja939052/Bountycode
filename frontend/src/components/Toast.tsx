import { useState, useCallback, useMemo, createContext, useContext } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle, XCircle, AlertTriangle, Info, X } from 'lucide-react';

// Toast notification system — replaces silent catches with visible feedback

const ToastContext = createContext(null);

const TOAST_STYLES = {
  success: { icon: CheckCircle, bg: 'bg-green-500/10', border: 'border-green-500/30', text: 'text-green-400' },
  error: { icon: XCircle, bg: 'bg-red-500/10', border: 'border-red-500/30', text: 'text-red-400' },
  warning: { icon: AlertTriangle, bg: 'bg-yellow-500/10', border: 'border-yellow-500/30', text: 'text-yellow-400' },
  info: { icon: Info, bg: 'bg-blue-500/10', border: 'border-blue-500/30', text: 'text-blue-400' },
};

let toastId = 0;

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const addToast = useCallback((message, type = 'info', duration = 4000) => {
    const id = ++toastId;
    setToasts(prev => [...prev, { id, message, type }]);
    if (duration > 0) {
      setTimeout(() => {
        setToasts(prev => prev.filter(t => t.id !== id));
      }, duration);
    }
    return id;
  }, []);

  const removeToast = useCallback((id) => {
    setToasts(prev => prev.filter(t => t.id !== id));
  }, []);

  const toast = useMemo(() => ({
    success: (msg, dur) => addToast(msg, 'success', dur),
    error: (msg, dur) => addToast(msg, 'error', dur),
    warning: (msg, dur) => addToast(msg, 'warning', dur),
    info: (msg, dur) => addToast(msg, 'info', dur),
  }), [addToast]);

  return (
    <ToastContext.Provider value={toast}>
      {children}
      {/* Toast container */}
      <div className="fixed top-4 right-4 z-[200] flex flex-col gap-2 pointer-events-none max-w-sm">
        <AnimatePresence>
          {toasts.map(t => {
            const style = TOAST_STYLES[t.type] || TOAST_STYLES.info;
            const Icon = style.icon;
            return (
              <motion.div
                key={t.id}
                initial={{ opacity: 0, x: 50, scale: 0.95 }}
                animate={{ opacity: 1, x: 0, scale: 1 }}
                exit={{ opacity: 0, x: 50, scale: 0.95 }}
                className={`pointer-events-auto flex items-start gap-3 px-4 py-3 rounded-xl border backdrop-blur-sm ${style.bg} ${style.border}`}
              >
                <Icon size={16} className={`${style.text} shrink-0 mt-0.5`} />
                <p className="text-xs font-mono text-gray-300 flex-1">{t.message}</p>
                <button
                  onClick={() => removeToast(t.id)}
                  className="text-gray-500 hover:text-gray-300 shrink-0"
                >
                  <X size={12} />
                </button>
              </motion.div>
            );
          })}
        </AnimatePresence>
      </div>
    </ToastContext.Provider>
  );
}

export function useToast() {
  const ctx = useContext(ToastContext);
  if (!ctx) {
    // Fallback if used outside provider
    return {
      success: (msg) => console.log('[SUCCESS]', msg),
      error: (msg) => console.error('[ERROR]', msg),
      warning: (msg) => console.warn('[WARN]', msg),
      info: (msg) => console.info('[INFO]', msg),
    };
  }
  return ctx;
}
