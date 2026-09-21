import React, { createContext, useContext, useCallback, useRef, useState } from 'react';
import soundEngine from './SoundEngine';
import ScreenJuiceOverlay from './ScreenJuiceOverlay';
import FloatingTextOverlay from './FloatingTextOverlay';
import CelebrationOverlay from '../components/CelebrationOverlay';

export interface JuiceContextValue {
  play: (soundName: string) => void;
  showFloatingText: (opts: { text: string; type?: string; x: number; y: number; color?: string; size?: string }) => void;
  showXP: (amount: number, x: number, y: number, big?: boolean) => void;
  showCoins: (amount: number, x: number, y: number) => void;
  showLevelUp: (level: number) => void;
  showStreakCeremony: (days: number) => void;
  showBadgeUnlock: (badge: unknown) => void;
  showCardReveal: (card: unknown) => void;
  showBossDefeat: (boss: unknown) => void;
  showDailyLogin: (reward: unknown, streak: number) => void;
  showAchievement: (chain: unknown) => void;
  showCriticalHit: (text: string, subtext: string) => void;
  screenShake: (intensity?: number, duration?: number) => void;
  screenFlash: (color?: string, duration?: number) => void;
  dismissCeremony: (id: number) => void;
  soundEnabled: boolean;
  toggleSound: () => void;
  soundVolume: number;
  setSoundVolume: (v: number) => void;
}

const JuiceContext = createContext<JuiceContextValue | null>(null);

export function useJuice() {
  const ctx = useContext(JuiceContext);
  if (!ctx) throw new Error('useJuice must be used within JuiceProvider');
  return ctx;
}

export function JuiceProvider({ children }: { children: React.ReactNode }) {
  const [activeCeremonies, setActiveCeremonies] = useState<{ id: number; type: string; data: unknown; duration: number }[]>([]);
  const [floatingTexts, setFloatingTexts] = useState<{ id: number; text: string; type: string; x: number; y: number; color?: string; size?: string }[]>([]);
  const [screenJuice, setScreenJuice] = useState<{ type: string; color?: string; intensity?: number; duration?: number; text?: string; subtext?: string } | null>(null);

  const floatingIdRef = useRef(0);
  const ceremonyIdRef = useRef(0);

  const play = useCallback((soundName: string) => {
    if (soundEngine[soundName]) {
      soundEngine[soundName]();
    }
  }, []);

  const showFloatingText = useCallback(({ text, type = 'diamonds', x, y, color, size = 'text-2xl' }: { text: string; type?: string; x: number; y: number; color?: string; size?: string }) => {
    const id = ++floatingIdRef.current;
    const item = { id, text, type, x, y, color, size };
    setFloatingTexts(prev => [...prev, item]);
    setTimeout(() => {
      setFloatingTexts(prev => prev.filter(f => f.id !== id));
    }, 1800);
  }, []);

  const showXP = useCallback((amount: number, x: number, y: number, big = false) => {
    if (big) {
      play('xpBig');
    } else {
      play('xpCollect');
    }
    showFloatingText({
      text: `+${amount} Diamonds`,
      type: 'diamonds',
      x,
      y,
      color: '#a78bfa',
      size: big ? 'text-4xl' : 'text-2xl',
    });
  }, [play, showFloatingText]);

  const showCoins = useCallback((amount: number, x: number, y: number) => {
    play('xpCollect');
    showFloatingText({
      text: `+${amount} 🪙`,
      type: 'coins',
      x,
      y,
      color: '#fbbf24',
    });
  }, [play, showFloatingText]);

  const showLevelUp = useCallback((level: number) => {
    play('levelUp');
    const id = ++ceremonyIdRef.current;
    setActiveCeremonies(prev => [...prev, {
      id,
      type: 'levelup',
      data: { level },
      duration: 3000,
    }]);
    setScreenJuice({ type: 'flash', color: 'rgba(99,102,241,0.3)', duration: 600 });
    setTimeout(() => setScreenJuice(null), 600);
    for (let i = 0; i < 8; i++) {
      setTimeout(() => {
        showFloatingText({
          text: `+${Math.floor(Math.random() * 50 + 20)} Diamonds`,
          type: 'diamonds',
          x: Math.random() * window.innerWidth,
          y: Math.random() * window.innerHeight * 0.5,
          color: '#a78bfa',
          size: 'text-3xl',
        });
      }, i * 180);
    }
  }, [play, showFloatingText]);

  const showStreakCeremony = useCallback((days: number) => {
    play('streakFire');
    const id = ++ceremonyIdRef.current;
    setActiveCeremonies(prev => [...prev, {
      id,
      type: 'streak',
      data: { days },
      duration: 3000,
    }]);
    setScreenJuice({ type: 'pulse', color: '#f59e0b', duration: 2500 });
    setTimeout(() => setScreenJuice(null), 2500);
    setTimeout(() => {
      setActiveCeremonies(prev => prev.filter(c => c.id !== id));
    }, 3500);
  }, [play]);

  const showBadgeUnlock = useCallback((badge: unknown) => {
    play('badgeUnlock');
    const id = ++ceremonyIdRef.current;
    setActiveCeremonies(prev => [...prev, {
      id,
      type: 'badge',
      data: badge,
      duration: 3500,
    }]);
    setScreenJuice({ type: 'sparkle', duration: 2000 });
    setTimeout(() => setScreenJuice(null), 2000);
    setTimeout(() => {
      setActiveCeremonies(prev => prev.filter(c => c.id !== id));
    }, 4000);
  }, [play]);

  const showCardReveal = useCallback((card: unknown) => {
    play('cardFlip');
    const id = ++ceremonyIdRef.current;
    setActiveCeremonies(prev => [...prev, {
      id,
      type: 'card',
      data: card,
      duration: 3000,
    }]);
    setTimeout(() => {
      setActiveCeremonies(prev => prev.filter(c => c.id !== id));
    }, 3500);
  }, [play]);

  const showBossDefeat = useCallback((boss: unknown) => {
    play('bossDefeat');
    const id = ++ceremonyIdRef.current;
    setActiveCeremonies(prev => [...prev, {
      id,
      type: 'boss',
      data: boss,
      duration: 4000,
    }]);
    setScreenJuice({ type: 'impact', color: 'rgba(245,158,11,0.4)', duration: 800 });
    setTimeout(() => setScreenJuice(null), 800);
    setTimeout(() => {
      setActiveCeremonies(prev => prev.filter(c => c.id !== id));
    }, 4500);
  }, [play]);

  const showDailyLogin = useCallback((reward: unknown, streak: number) => {
    play('dailyLogin');
    const id = ++ceremonyIdRef.current;
    setActiveCeremonies(prev => [...prev, {
      id,
      type: 'daily-login',
      data: { reward, streak },
      duration: 4500,
    }]);
    setScreenJuice({ type: 'sparkle', duration: 2500 });
    setTimeout(() => setScreenJuice(null), 2500);
    setTimeout(() => {
      setActiveCeremonies(prev => prev.filter(c => c.id !== id));
    }, 5000);
  }, [play]);

  const showAchievement = useCallback((chain: unknown) => {
    play('achievement');
    const id = ++ceremonyIdRef.current;
    setActiveCeremonies(prev => [...prev, {
      id,
      type: 'achievement',
      data: chain,
      duration: 5000,
    }]);
    setScreenJuice({ type: 'vignette', color: '#f59e0b', duration: 3000 });
    setTimeout(() => setScreenJuice(null), 3000);
    setTimeout(() => {
      setActiveCeremonies(prev => prev.filter(c => c.id !== id));
    }, 5500);
  }, [play]);

  const showCriticalHit = useCallback((text: string, subtext: string) => {
    play('criticalHit');
    const id = ++ceremonyIdRef.current;
    setActiveCeremonies(prev => [...prev, {
      id,
      type: 'critical',
      data: { title: text, subtitle: subtext },
      duration: 1500,
    }]);
    setScreenJuice({ type: 'chromatic', color: 'rgba(245,158,11,0.3)', duration: 600, text, subtext });
    setTimeout(() => setScreenJuice(null), 600);
    setTimeout(() => {
      setActiveCeremonies(prev => prev.filter(c => c.id !== id));
    }, 1500);
  }, [play]);

  const screenShake = useCallback((intensity = 6, duration = 350) => {
    setScreenJuice({ type: 'shake', intensity, duration });
    setTimeout(() => setScreenJuice(null), duration);
  }, []);

  const screenFlash = useCallback((color = 'rgba(99,102,241,0.3)', duration = 400) => {
    setScreenJuice({ type: 'flash', color, duration });
    setTimeout(() => setScreenJuice(null), duration);
  }, []);

  const dismissCeremony = useCallback((id: number) => {
    setActiveCeremonies(prev => prev.filter(c => c.id !== id));
  }, []);

  const value = {
    play,
    showFloatingText, showXP, showCoins, showLevelUp,
    showStreakCeremony, showBadgeUnlock, showCardReveal,
    showBossDefeat, showDailyLogin, showAchievement, showCriticalHit,
    screenShake, screenFlash,
    dismissCeremony,
    soundEnabled: soundEngine.enabled,
    toggleSound: () => soundEngine.toggle(),
    soundVolume: soundEngine.volume,
    setSoundVolume: (v: number) => soundEngine.setVolume(v),
  };

  return (
    <JuiceContext.Provider value={value}>
      {children}
      <ScreenJuiceOverlay juice={screenJuice} />
      <FloatingTextOverlay texts={floatingTexts} />
      <CelebrationOverlay
        show={activeCeremonies.length > 0}
        type={activeCeremonies[activeCeremonies.length - 1]?.type || "confetti"}
        title={(activeCeremonies[activeCeremonies.length - 1]?.data as { title?: string })?.title}
        subtitle={(activeCeremonies[activeCeremonies.length - 1]?.data as { subtitle?: string })?.subtitle}
        diamonds={(activeCeremonies[activeCeremonies.length - 1]?.data as { diamonds?: number })?.diamonds}
        onClose={dismissCeremony.bind(null, activeCeremonies[activeCeremonies.length - 1]?.id)}
      />
    </JuiceContext.Provider>
  );
}

