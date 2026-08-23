import { useState, useEffect } from "react";
import { Palette, Check, Lock, Sparkles } from "lucide-react";
import api from "../services/api";
import type { ThemeInfo } from "../services/api/themes";
import { useThemeStore, THEME_INFO } from "../store/themeStore";
import type { ThemeMode } from "../store/themeStore";
import useAuthStore from "../store/authStore";
import { useToast } from "../components/Toast";

export default function CustomThemes() {
  const { user } = useAuthStore();
  const themeStore = useThemeStore();
  const [unlocked, setUnlocked] = useState<string[]>([]);
  const [isPro, setIsPro] = useState(false);
  const [loading, setLoading] = useState(true);
  const [applying, setApplying] = useState<string | null>(null);
  const toast = useToast();

  const isProUser = isPro || user?.plan === "pro" || user?.plan === "lifetime";

  const fetchThemes = async () => {
    try {
      const data = await api.themes.list();
      setUnlocked(data.unlocked || THEME_INFO.filter((t) => !t.pro).map((t) => t.id));
      setIsPro(data.is_pro);
    } catch (e: any) {
      toast.error(e.message || "Failed to load themes");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchThemes(); }, []);

  const selectTheme = async (theme: ThemeInfo) => {
    if (theme.pro && !isProUser) {
      return toast.warning("Premium theme — upgrade to Pro!");
    }
    setApplying(theme.id);
    try {
      await api.themes.select(theme.id);
      themeStore.setMode(theme.id as ThemeMode);
      toast.success(`Applied ${theme.name} theme`);
    } catch (e: any) {
      toast.error(e.message || "Failed to select theme");
    } finally {
      setApplying(null);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen py-8 px-4 flex items-center justify-center">
        <div className="animate-pulse text-brand-sky">Loading themes…</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-6 sm:py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <header className="mb-8">
          <h1 className="text-3xl font-display font-extrabold text-text-primary flex items-center gap-3">
            <Palette className="text-brand-sky" size={28} />
            Custom Themes
          </h1>
          <p className="text-text-secondary mt-1">
            Personalize PlacementPro with 10 color themes. {THEME_INFO.filter((t) => t.pro).length} are Pro-exclusive.
          </p>
          {!isProUser && (
            <a
              href="/pricing"
              className="inline-flex items-center gap-1 text-sm text-brand-sky hover:underline mt-1"
            >
              <Sparkles size={14} /> Upgrade to Pro for premium themes
            </a>
          )}
        </header>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">{THEME_INFO.map((theme) => {
            const locked = theme.pro && !isProUser;
            const current = themeStore.mode === theme.id;
            const available = unlocked.includes(theme.id) || !theme.pro;
            const buttonClass = current
              ? "border-brand-primary ring-2 ring-brand-primary/40"
              : "border-gray-200 bg-white hover:bg-gray-50";
            return (
              <button
                key={theme.id}
                onClick={() => selectTheme(theme)}
                disabled={locked || applying === theme.id}
                className={`relative rounded-xl border-2 p-4 text-left transition-all disabled:opacity-60 ${buttonClass}`}
              >
                <div
                  className="h-12 rounded-lg mb-3"
                  style={{
                    background: `linear-gradient(90deg, ${theme.preview.from}, ${theme.preview.to})`,
                  }}
                />
                <div className="flex items-center justify-between">
                  <div>
                    <span className="font-bold text-text-primary block">{theme.name}</span>
                    <span className="text-xs text-text-light capitalize">{theme.id}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    {locked && <Lock size={16} className="text-yellow-500" />}
                    {current && <Check size={16} className="text-brand-sky" />}
                  </div>
                </div>
                {locked && (
                  <div className="absolute inset-0 rounded-xl bg-surface-2 border-border flex items-center justify-center">
                    <Lock size={24} className="text-text-primary/70" />
                  </div>
                )}
              </button>
            );
          })}
        </div>

        <div className="mt-8 rounded-xl border border-gray-200 bg-white border-border/50 p-4">
          <h3 className="font-bold text-text-primary mb-2">Current theme</h3>
          <p className="text-sm text-text-secondary">
            <span className="font-medium text-brand-primary">{themeStore.mode}</span> · Applied across the app and persisted to your account.
          </p>
          <p className="text-xs text-text-muted mt-1">
            Pro themes ({THEME_INFO.filter((t) => t.pro).length}) unlock with a Pro or Lifetime plan — one payment, all future themes included.
          </p>
        </div>
      </div>
    </div>
  );
}
