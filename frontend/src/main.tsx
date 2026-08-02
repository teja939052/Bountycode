import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";
import { registerServiceWorker } from "./pwa";
import PwaInstallPrompt from "./components/PwaInstallPrompt";
import { installGlobalErrorTracker } from "./services/errorTracker";
import DebugPanel from "./components/DebugPanel";

installGlobalErrorTracker();
registerServiceWorker();

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
    <DebugPanel />
    <PwaInstallPrompt />
  </React.StrictMode>
);
