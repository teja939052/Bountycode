import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import "./styles/candy.css";
import { registerServiceWorker } from "./pwa";
import { installGlobalErrorTracker } from "./services/errorTracker";

function renderBootShell(rootEl: HTMLElement) {
  rootEl.innerHTML = `
    <div style="min-height:100vh;display:flex;align-items:center;justify-content:center;background:#F7FAF7;color:#17211B;font-family:system-ui,sans-serif;padding:24px;">
      <div style="max-width:32rem;text-align:center;">
        <div style="margin:0 auto 16px;height:56px;width:56px;border-radius:9999px;border:4px solid rgba(34,197,94,0.2);border-top-color:#22C55E;animation:spin 1s linear infinite;"></div>
        <h1 style="margin:0 0 8px;font-size:1.5rem;line-height:2rem;">Loading BountyCode</h1>
        <p style="margin:0;color:#68736B;">Preparing the app shell and safety rails...</p>
      </div>
    </div>
  `;
}

function renderFatalBootError(rootEl: HTMLElement, error: unknown) {
  const message = error instanceof Error ? error.message : String(error);
  rootEl.innerHTML = `
    <div style="min-height:100vh;display:flex;align-items:center;justify-content:center;background:#F7FAF7;color:#17211B;font-family:system-ui,sans-serif;padding:24px;">
      <div style="max-width:36rem;border:1px solid rgba(239,68,68,0.25);background:#FFFFFF;padding:24px;border-radius:20px;box-shadow:0 20px 50px rgba(17,33,27,0.12);">
        <h1 style="margin:0 0 8px;font-size:1.5rem;line-height:2rem;color:#B91C1C;">The app could not start</h1>
        <p style="margin:0 0 16px;color:#4B5563;">A boot-time error happened before React finished loading. The app is still alive, but this screen needs attention.</p>
        <pre style="margin:0;white-space:pre-wrap;word-break:break-word;padding:16px;border-radius:12px;background:#FEF2F2;color:#B91C1C;font-size:12px;line-height:1.5;">${message}</pre>
      </div>
    </div>
  `;
}

async function bootstrap() {
  const rootEl = document.getElementById("root");
  if (!rootEl) {
    throw new Error("Root element '#root' was not found.");
  }

  renderBootShell(rootEl);
  const root = ReactDOM.createRoot(rootEl);

  try {
    installGlobalErrorTracker();
  } catch (error) {
    console.error("Global error tracker failed to install:", error);
  }

  try {
    registerServiceWorker();
  } catch (error) {
    console.error("Service worker registration failed:", error);
  }

  try {
    const [{ default: App }, queryProviderModule] = await Promise.all([
      import("./App"),
      import("./providers/QueryProvider"),
    ]);

    const QueryProvider = queryProviderModule.QueryProvider;

    let PwaInstallPrompt: React.ComponentType | null = null;
    try {
      const pwaModule = await import("./components/PwaInstallPrompt");
      PwaInstallPrompt = pwaModule.default;
    } catch (error) {
      console.warn("PWA install prompt unavailable:", error);
    }

    let DebugPanel: React.ComponentType | null = null;
    if (import.meta.env.DEV) {
      try {
        const debugModule = await import("./components/DebugPanel");
        DebugPanel = debugModule.default;
      } catch (error) {
        console.warn("Debug panel unavailable:", error);
      }
    }

    root.render(
      <React.StrictMode>
        <QueryProvider>
          <App />
        </QueryProvider>
        {DebugPanel ? <DebugPanel /> : null}
        {PwaInstallPrompt ? <PwaInstallPrompt /> : null}
      </React.StrictMode>
    );
  } catch (error) {
    console.error("Frontend bootstrap failed:", error);
    renderFatalBootError(rootEl, error);
  }
}

/**
 * Pause all CSS animations when the tab is hidden.
 * Toggles `data-visible` on <html> so CSS can target `.sakura-petal` etc.
 * Pure DOM — no React, no rAF, no re-renders.
 */
function applyVisibilityPause() {
  const cls = "page-hidden";
  const set = () => {
    document.documentElement.classList.toggle(cls, document.hidden);
  };
  document.addEventListener("visibilitychange", set, { passive: true });
  set(); // set initial state
}
applyVisibilityPause();

void bootstrap();
