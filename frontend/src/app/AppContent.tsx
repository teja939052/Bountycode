import { useEffect, useState, Suspense, lazy } from "react";
import { useJuice } from "../juice/JuiceProvider";
import { useGamificationData } from "../hooks/useGamificationData";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import CustomCursor from "../components/CustomCursor";
import CookieBanner from "../components/CookieBanner";
import { DashboardSkeleton } from "../components/ui/Skeleton";
import { AnimatedRoutes } from "./AppRoutes";
import ComboCounter from "../components/ComboCounter";
import ComboWarningOverlay from "../juice/ComboWarningOverlay";
import RouteErrorBoundary from "../components/RouteErrorBoundary";

const Onboarding = lazy(() => import("../components/Onboarding"));
const DiamondsPopup = lazy(() => import("../components/XPPopup"));
const RewardShowcase = lazy(() => import("../components/RewardShowcase"));
const BottomNav = lazy(() => import("../components/BottomNav"));

export function PageSuspense({ children }: { children: React.ReactNode }) {
  return <Suspense fallback={<DashboardSkeleton />}>{children}</Suspense>;
}

export default function AppContent() {
  const { showXP } = useJuice();
  const [xpPopup, setXpPopup] = useState({
    show: false,
    diamonds: 0,
    level: 0,
    streak: 0,
    badges: [] as string[],
    critical: false,
    criticalBonus: 0,
  });
  const [rewardShowcase, setRewardShowcase] = useState<{
    visible: boolean;
    breakdown: {
      baseXP: number;
      multipliers: {
        streak: number;
        combo: number;
        first_of_day: boolean;
        critical: number;
        double_xp: boolean;
      };
      totalXP: number;
      coins: number;
      stars: number;
      streak: number;
      leveledUp: boolean;
      newLevel?: number;
      newBadges?: unknown[];
      milestone?: Record<string, unknown>;
      bossLevel?: number | null;
      streakFrozen?: boolean;
    } | null;
  }>({ visible: false, breakdown: null });
  const [searchOpen, setSearchOpen] = useState(false);

  const { combo } = useGamificationData();
  const currentCombo = (combo?.current_combo as number | undefined) ?? 0;
  const comboMultiplier = (combo?.multiplier as number | undefined) ?? 1;

  useEffect(() => {
    const handler = (e: Event) => {
      const detail = (e as CustomEvent).detail || {};
      const { diamonds, level, streak, badges, critical } = detail;
      if (diamonds) {
        const isBig = (diamonds || 0) >= 100;
        setXpPopup({
          show: true,
          diamonds,
          level: level || 0,
          streak: streak || 0,
          badges: (badges as string[]) || [],
          critical: critical || false,
          criticalBonus: (critical as { bonus?: number } | undefined)?.bonus || 0,
        });
        showXP(diamonds, window.innerWidth / 2, window.innerHeight / 2, isBig);
      }
    };
    window.addEventListener("diamonds-gained", handler);
    return () => window.removeEventListener("diamonds-gained", handler);
  }, [showXP]);

  useEffect(() => {
    const showLevelUp = (e: Event) => {
      const detail = (e as CustomEvent<{ newLevel?: number }>).detail || {};
      setRewardShowcase((prev) => ({
        visible: true,
        breakdown: prev.breakdown
          ? { ...prev.breakdown, leveledUp: true, newLevel: detail.newLevel || prev.breakdown.newLevel }
          : prev.breakdown,
      }));
    };

    const showReward = (e: Event) => {
      const detail = (e as CustomEvent<{
        amount?: number;
        baseXP?: number;
        multipliers?: {
          streak: number;
          combo: number;
          first_of_day: boolean;
          critical: number;
          double_xp: boolean;
        };
        leveledUp?: boolean;
        bossLevel?: number | null;
        milestone?: Record<string, unknown>;
        critical?: boolean;
        criticalBonus?: number;
        coins?: number;
        stars?: number;
        streak?: number;
        newLevel?: number;
        newBadges?: unknown[];
        streakFrozen?: boolean;
      }>).detail || {};
      const amount = detail.amount || 0;
      const baseXP = detail.baseXP ?? Math.round(amount / Math.max(0.01, (detail.multipliers?.streak || 1) * (detail.multipliers?.combo || 1) * (detail.multipliers?.critical || 1) * (detail.multipliers?.double_xp ? 2 : 1)));
      const shouldShow =
        detail.leveledUp ||
        detail.bossLevel ||
        (detail.milestone && Object.keys(detail.milestone).length > 0) ||
        (detail.critical && (detail.criticalBonus || 0) >= 50) ||
        amount >= 100;

      if (!shouldShow) return;

      setRewardShowcase({
        visible: true,
        breakdown: {
          baseXP,
          multipliers: detail.multipliers ?? {
            streak: 1,
            combo: 1,
            first_of_day: false,
            critical: 1,
            double_xp: false,
          },
          totalXP: amount,
          coins: detail.coins || 0,
          stars: detail.stars || 0,
          streak: detail.streak || 0,
          leveledUp: detail.leveledUp || false,
          newLevel: detail.newLevel,
          newBadges: detail.newBadges,
          milestone: detail.milestone,
          bossLevel: detail.bossLevel,
          streakFrozen: detail.streakFrozen,
        },
      });
    };
    window.addEventListener("juice:levelup", showLevelUp);
    window.addEventListener("juice:diamonds", showReward);
    return () => {
      window.removeEventListener("juice:levelup", showLevelUp);
      window.removeEventListener("juice:diamonds", showReward);
    };
  }, []);

  useEffect(() => {
    const handleKeydown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setSearchOpen((prev) => !prev);
      }
      if (e.key === "Escape" && searchOpen) {
        setSearchOpen(false);
      }
    };
    window.addEventListener("keydown", handleKeydown);
    return () => window.removeEventListener("keydown", handleKeydown);
  }, [searchOpen]);

  return (
    <>
      <div className="min-h-screen flex flex-col relative">
        <CustomCursor />
        <div className="relative z-10 flex flex-col min-h-screen">
          <Navbar />
          <main className="flex-1" id="main-content" role="main">
            <PageSuspense>
              <RouteErrorBoundary>
                <AnimatedRoutes />
              </RouteErrorBoundary>
            </PageSuspense>
          </main>
          <Footer />
          <CookieBanner />
          <Suspense fallback={null}>
            <Onboarding />
            <XPPopup
              show={xpPopup.show}
              xpGained={xpPopup.diamonds}
              level={xpPopup.level}
              streak={xpPopup.streak}
              newBadges={xpPopup.badges}
              critical={xpPopup.critical}
              criticalBonus={xpPopup.criticalBonus}
              onClose={() => setXpPopup((prev) => ({ ...prev, show: false }))}
            />
            <Suspense fallback={null}>
              <RewardShowcase
                visible={rewardShowcase.visible}
                breakdown={rewardShowcase.breakdown}
                onContinue={() => setRewardShowcase((prev) => ({ ...prev, visible: false }))}
              />
            </Suspense>
            <ComboCounter
              combo={currentCombo}
              multiplier={comboMultiplier}
              visible={currentCombo >= 2}
            />
            <ComboWarningOverlay
              seconds={(combo?.combo_decay_seconds as number | undefined) ?? 0}
              visible={currentCombo >= 3}
            />
          </Suspense>
          <Suspense fallback={null}>
            <BottomNav />
          </Suspense>
        </div>
        <div className="h-16 md:hidden" />
      </div>
    </>
  );
}
