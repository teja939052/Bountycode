import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import "./styles/candy.css";
import "./styles/candy.css";
import { registerServiceWorker } from "./pwa";
import { installGlobalErrorTracker } from "./services/errorTracker";

function renderBootShell(rootEl: HTMLElement) {
  rootEl.innerHTML = `
    <div style="min-height:100vh;display:flex;align-items:center;justify-content:center;background:#050816;color:#e5e7eb;font-family:system-ui,sans-serif;padding:24px;">
      <div style="max-width:32rem;text-align:center;">
        <div style="margin:0 auto 16px;height:56px;width:56px;border-radius:9999px;border:4px solid rgba(99,102,241,0.25);border-top-color:#6366f1;animation:spin 1s linear infinite;"></div>
        <h1 style="margin:0 0 8px;font-size:1.5rem;line-height:2rem;">Loading PlacementPro</h1>
        <p style="margin:0;color:#9ca3af;">Preparing the app shell and safety rails...</p>
      </div>
    </div>
  `;
}

function renderFatalBootError(rootEl: HTMLElement, error: unknown) {
  const message = error instanceof Error ? error.message : String(error);
  rootEl.innerHTML = `
    <div style="min-height:100vh;display:flex;align-items:center;justify-content:center;background:#050816;color:#e5e7eb;font-family:system-ui,sans-serif;padding:24px;">
      <div style="max-width:36rem;border:1px solid rgba(239,68,68,0.25);background:rgba(17,24,39,0.92);padding:24px;border-radius:20px;box-shadow:0 20px 50px rgba(0,0,0,0.35);">
        <h1 style="margin:0 0 8px;font-size:1.5rem;line-height:2rem;color:#fca5a5;">The app could not start</h1>
        <p style="margin:0 0 16px;color:#d1d5db;">A boot-time error happened before React finished loading. The app is still alive, but this screen needs attention.</p>
        <pre style="margin:0;white-space:pre-wrap;word-break:break-word;padding:16px;border-radius:12px;background:rgba(0,0,0,0.35);color:#fca5a5;font-size:12px;line-height:1.5;">${message}</pre>
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

void bootstrap();
