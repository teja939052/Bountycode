import { useEffect } from "react";
import { BrowserRouter as Router } from "react-router-dom";
import ErrorBoundary from "./components/ErrorBoundary";
import { ToastProvider } from "./components/Toast";
import { ThemeProvider } from "./components/ThemeProvider";
import { BackgroundProvider } from "./contexts/BackgroundContext";
import { JuiceProvider } from "./juice/JuiceProvider";
import AppContent from "./app/AppContent";
import useAuthStore from "./store/authStore";

export default function App() {
  const { loadUser } = useAuthStore();

  useEffect(() => {
    loadUser();
  }, [loadUser]);

  return (
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
  );
}
