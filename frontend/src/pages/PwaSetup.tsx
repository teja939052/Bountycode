import { useState, useEffect, useCallback } from "react";
import { motion } from "framer-motion";
import {
  Download, Wifi, WifiOff, Bell, BellOff, BookOpen, HardDrive, Check, Smartphone,
} from "lucide-react";
import useReducedMotion from "../hooks/useReducedMotion";
import useOnline from "../hooks/useOnline";
import { getCachedLessonCount } from "../utils/offlineCache";
import {
  isPushSupported, requestPushPermission, subscribeToPush, getStoredSubscription,
} from "../services/pushNotifications";

const OFFLINE_LESSONS_KEY = "placementpro_offline_lessons";

function StatusPill({ online }) {
  return (
    <span
      className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-semibold border ${
        online
          ? "bg-nature-bark text-nature-blossom border-nature-leaf/30"
          : "bg-amber-500/10 text-amber-400 border-amber-500/30"
      }`}
    >
      {online ? <Wifi size={14} /> : <WifiOff size={14} />}
      {online ? "Online" : "Offline"}
    </span>
  );
}

function Toggle({ checked, onChange, disabled }) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={checked}
      disabled={disabled}
      onClick={() => onChange(!checked)}
      className={`relative w-12 h-7 rounded-full transition-colors shrink-0 ${
        checked ? "bg-emerald-500" : "bg-[#E5E0D3]"
      } ${disabled ? "opacity-50 cursor-not-allowed" : "cursor-pointer"}`}
    >
      <span
        className={`absolute top-0.5 left-0.5 w-6 h-6 rounded-full bg-white shadow transition-transform ${
          checked ? "translate-x-5" : ""
        }`}
      />
    </button>
  );
}

export default function PwaSetup() {
  const reduced = useReducedMotion();
  const isOnline = useOnline();
  const [deferredPrompt, setDeferredPrompt] = useState(null);
  const [installed, setInstalled] = useState(false);
  const [offlineEnabled, setOfflineEnabled] = useState(
    () => localStorage.getItem(OFFLINE_LESSONS_KEY) === "true"
  );
  const [pushSupported] = useState(() => isPushSupported());
  const [permission, setPermission] = useState(() =>
    typeof Notification !== "undefined" ? Notification.permission : "unsupported"
  );
  const [subscribed, setSubscribed] = useState(() => Boolean(getStoredSubscription()));
  const [cachedCount, setCachedCount] = useState(0);
  const [busy, setBusy] = useState(false);

  const refreshCachedCount = useCallback(() => {
    getCachedLessonCount()
      .then(setCachedCount)
      .catch(() => setCachedCount(0));
  }, []);

  useEffect(() => {
    setInstalled(window.matchMedia("(display-mode: standalone)").matches);
    const handler = (e) => {
      e.preventDefault();
      setDeferredPrompt(e);
    };
    window.addEventListener("beforeinstallprompt", handler);
    return () => window.removeEventListener("beforeinstallprompt", handler);
  }, []);

  useEffect(() => {
    refreshCachedCount();
  }, [refreshCachedCount]);

  const handleInstall = async () => {
    if (!deferredPrompt) return;
    deferredPrompt.prompt();
    const result = await deferredPrompt.userChoice;
    if (result.outcome === "accepted") setInstalled(true);
    setDeferredPrompt(null);
  };

  const handleToggleOffline = async (enabled) => {
    setOfflineEnabled(enabled);
    localStorage.setItem(OFFLINE_LESSONS_KEY, String(enabled));
    if (!enabled) return;
    setBusy(true);
    try {
      const result = await requestPushPermission();
      setPermission(result);
      if (result === "granted") {
        const subscription = await subscribeToPush();
        setSubscribed(Boolean(subscription));
      }
    } finally {
      setBusy(false);
    }
  };

  const fade = (delay = 0) =>
    reduced ? {} : { opacity: 0, y: 16, transition: { delay } };

  return (
    <div className="min-h-screen bg-surface-base text-text-primary">
      <div className="max-w-2xl mx-auto px-4 py-10 md:py-14">
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: -16 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center gap-3 mb-8"
        >
          <div className="p-3 bg-gradient-to-br from-[#EDF5E6] to-[#D9EFCF] rounded-2xl border border-nature-leaf/30">
            <Smartphone className="w-7 h-7 text-nature-blossom" />
          </div>
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-[#1F2937] via-[#4F8F57] to-[#7BB661] bg-clip-text text-transparent">
              Offline & Notifications
            </h1>
            <p className="text-text-muted text-sm mt-1">
              Install the app, save lessons offline, and stay notified
            </p>
          </div>
        </motion.div>

        <motion.div
          initial={fade(0.05)}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center justify-between gap-4 rounded-2xl border border-nature-leaf/20 bg-white p-4 mb-6"
        >
          <div className="flex items-center gap-3">
            <div
              className={`w-10 h-10 rounded-xl flex items-center justify-center ${
                isOnline
                  ? "bg-nature-bark text-nature-blossom"
                  : "bg-amber-500/15 text-amber-400"
              }`}
            >
              {isOnline ? <Wifi size={20} /> : <WifiOff size={20} />}
            </div>
            <div>
              <p className="font-semibold text-sm text-text-primary">Connection Status</p>
              <p className="text-xs text-text-muted">
                {isOnline
                  ? "You are connected to the internet"
                  : "You are offline — cached content is available"}
              </p>
            </div>
          </div>
          <StatusPill online={isOnline} />
        </motion.div>

        <div className="space-y-4">
          <motion.div
            initial={fade(0.1)}
            animate={{ opacity: 1, y: 0 }}
            className="rounded-2xl border border-nature-leaf/20 bg-white p-6"
          >
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-surface-card text-nature-blossom flex items-center justify-center">
                <Download size={20} />
              </div>
              <div>
                <h2 className="font-semibold text-text-primary">Install App</h2>
                <p className="text-xs text-text-muted mt-0.5">
                  Add PlacementPro to your home screen for full-screen access
                </p>
              </div>
            </div>
            <div className="mt-5">
              {installed ? (
                <span className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium bg-nature-bark text-nature-blossom border border-nature-leaf/30">
                  <Check size={16} /> Installed
                </span>
              ) : deferredPrompt ? (
                <button
                  onClick={handleInstall}
                  className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-nature-leaf hover:bg-nature-moss text-white text-sm font-semibold transition-colors"
                >
                  <Download size={16} /> Install App
                </button>
              ) : (
                <p className="text-xs text-text-muted">
                  Use your browser's "Add to Home Screen" / "Install app" option
                </p>
              )}
            </div>
          </motion.div>

          <motion.div
            initial={fade(0.15)}
            animate={{ opacity: 1, y: 0 }}
            className="rounded-2xl border border-nature-leaf/20 bg-white p-6"
          >
            <div className="flex items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-nature-bark text-nature-blossom flex items-center justify-center">
                  <BookOpen size={20} />
                </div>
                <div>
                  <h2 className="font-semibold text-text-primary">Enable Offline Lessons</h2>
                  <p className="text-xs text-text-muted mt-0.5">
                    Save lessons to your device and read them without an internet
                    connection
                  </p>
                </div>
              </div>
              <Toggle
                checked={offlineEnabled}
                onChange={handleToggleOffline}
                disabled={busy || !pushSupported}
              />
            </div>
            <div className="mt-4 flex flex-wrap items-center gap-2">
              <span
                className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-medium border ${
                  permission === "granted"
                    ? "bg-nature-bark text-nature-blossom border-nature-leaf/30"
                    : "bg-surface-card text-text-muted border-nature-leaf/20"
                }`}
              >
                {permission === "granted" ? <Bell size={12} /> : <BellOff size={12} />}
                Notifications: {permission}
              </span>
              <span
                className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-medium border ${
                  subscribed
                    ? "bg-nature-bark text-nature-blossom border-nature-leaf/30"
                    : "bg-surface-card text-text-muted border-nature-leaf/20"
                }`}
              >
                {subscribed ? <Check size={12} /> : <BellOff size={12} />}
                {subscribed ? "Subscribed" : "Not subscribed"}
              </span>
            </div>
          </motion.div>

          <motion.div
            initial={fade(0.2)}
            animate={{ opacity: 1, y: 0 }}
            className="rounded-2xl border border-nature-leaf/20 bg-white p-6 flex items-center justify-between gap-4"
          >
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-surface-card text-nature-blossom flex items-center justify-center">
                <HardDrive size={20} />
              </div>
              <div>
                <h2 className="font-semibold text-text-primary">Cached Lessons</h2>
                <p className="text-xs text-text-muted mt-0.5">
                  Lessons saved on this device for offline reading
                </p>
              </div>
            </div>
            <span className="text-2xl font-bold font-mono bg-gradient-to-r from-[#4F8F57] to-[#7BB661] bg-clip-text text-transparent">
              {cachedCount}
            </span>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
