import { useEffect, useState, useCallback } from "react";
import { BrowserRouter as Router } from "react-router-dom";
import ErrorBoundary from "./components/ErrorBoundary";
import { ToastProvider } from "./components/Toast";
import { ThemeProvider } from "./components/ThemeProvider";
import { BackgroundProvider } from "./contexts/BackgroundContext";
import { JuiceProvider } from "./juice/JuiceProvider";
import AppContent from "./app/AppContent";
import { BountyCodeSplash } from "./components/brand/BountyCodeBrandMotion";
import useAuthStore from "./store/authStore";

const BOOT_SPLASH_KEY = "bountycode.boot.splash.shown";

export default function App() {
  const { loadUser } = useAuthStore();
  const [bootReady, setBootReady] = useState(false);
  const [showSplash, setShowSplash] = useState(false);

  useEffect(() => {
    const init = async () => {
      await loadUser();
      const alreadyShown = sessionStorage.getItem(BOOT_SPLASH_KEY) === "1";
      if (!alreadyShown) {
        setShowSplash(true);
        sessionStorage.setItem(BOOT_SPLASH_KEY, "1");
      }
      setBootReady(true);
    };
    init();
  }, [loadUser]);

  const handleSplashComplete = useCallback(() => {
    setShowSplash(false);
  }, []);

  if (!bootReady) {
    return (
      <div className="fixed inset-0 z-[200] flex items-center justify-center bg-[#0F1724]" aria-hidden="true" />
    );
  }

  return (
    <>
      {showSplash && <BountyCodeSplash duration={1450} onComplete={handleSplashComplete} />}
      <ErrorBoundary>
        <ToastProvider>
          <ThemeProvider>
            <BackgroundProvider>
              <JuiceProvider>
                <Router>
                  <AppContent />
                </Router>
              </JuiceProvider>
            </BackgroundProvider>
          </ThemeProvider>
        </ToastProvider>
      </ErrorBoundary>
    </>
  );
}
