import { useState, useEffect } from "react";
import { X, Download } from "lucide-react";

const VISIT_KEY = "placementpro_pwa_visits";
const DISMISSED_KEY = "placementpro_pwa_dismissed";

export default function PwaInstallPrompt() {
  const [show, setShow] = useState(false);
  const [deferredPrompt, setDeferredPrompt] = useState(null);

  useEffect(() => {
    const visits = parseInt(localStorage.getItem(VISIT_KEY) || "0", 10);
    localStorage.setItem(VISIT_KEY, String(visits + 1));
    const dismissed = localStorage.getItem(DISMISSED_KEY) === "true";
    const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
    const isStandalone = window.matchMedia("(display-mode: standalone)").matches;

    if (!dismissed && !isStandalone && isMobile && visits >= 1) {
      setShow(true);
    }

    const handler = (e) => {
      e.preventDefault();
      setDeferredPrompt(e);
    };
    window.addEventListener("beforeinstallprompt", handler);
    return () => window.removeEventListener("beforeinstallprompt", handler);
  }, []);

  const handleInstall = async () => {
    if (deferredPrompt) {
      deferredPrompt.prompt();
      const result = await deferredPrompt.userChoice;
      if (result.outcome === "accepted") {
        setShow(false);
      }
      setDeferredPrompt(null);
    }
  };

  const handleDismiss = () => {
    localStorage.setItem(DISMISSED_KEY, "true");
    setShow(false);
  };

  if (!show) return null;

  return (
    <div className="fixed bottom-20 left-4 right-4 z-50 md:left-auto md:right-4 md:w-80">
      <div className="glass p-4 rounded-xl border border-indigo-500/20 shadow-lg">
        <div className="flex items-start justify-between mb-2">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center">
              <Download size={16} className="text-text-primary" />
            </div>
            <p className="text-sm font-semibold text-text-primary">Install PlacementPro</p>
          </div>
          <button onClick={handleDismiss} className="text-gray-400 hover:text-white transition-colors">
            <X size={16} />
          </button>
        </div>
        <p className="text-xs text-gray-400 mb-3">
          Install the app for the best experience — practice anywhere, even offline.
        </p>
        <button
          onClick={handleInstall}
          className="w-full py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-text-primary text-sm font-semibold transition-colors"
        >
          Install App
        </button>
      </div>
    </div>
  );
}
