import React, { createContext, useContext, useCallback, useRef, useState } from 'react';
import soundEngine from './SoundEngine';
import ScreenJuiceOverlay from './ScreenJuiceOverlay';
import FloatingTextOverlay from './FloatingTextOverlay';
import CeremonyOverlay from './CeremonyOverlay';

const JuiceContext = createContext(null);

export function useJuice() {
  const ctx = useContext(JuiceContext);
  if (!ctx) throw new Error('useJuice must be used within JuiceProvider');
  return ctx;
}

export function JuiceProvider({ children }) {
  const [activeCeremonies, setActiveCeremonies] = useState([]);
  const [floatingTexts, setFloatingTexts] = useState([]);
  const [screenJuice, setScreenJuice] = useState(null);

  const floatingIdRef = useRef(0);
  const ceremonyIdRef = useRef(0);

  const play = useCallback((soundName) => {
    if (soundEngine[soundName]) {
      soundEngine[soundName]();
    }
  }, []);

  const showFloatingText = useCallback(({ text, type = 'xp', x, y, color }) => {
    const id = ++floatingIdRef.current;
    const item = { id, text, type, x, y, color };
    setFloatingTexts(prev => [...prev, item]);
    setTimeout(() => {
      setFloatingTexts(prev => prev.filter(f => f.id !== id));
    }, 1500);
  }, []);

  const showXP = useCallback((amount, x, y) => {
    play('xpCollect');
    showFloatingText({ text: `+${amount} XP`, type: 'xp', x, y, color: '#a78bfa' });
  }, [play, showFloatingText]);

  const showLevelUp = useCallback((level) => {
    play('levelUp');
    setActiveCeremonies(prev => [...prev, {
      id: ++ceremonyIdRef.current,
      type: 'levelup',
      data: { level },
      duration: 3000,
    }]);
    setScreenJuice({ type: 'flash', color: 'rgba(99,102,241,0.3)', duration: 500 });
    setTimeout(() => setScreenJuice(null), 500);
    for (let i = 0; i < 5; i++) {
      setTimeout(() => {
        showFloatingText({
          text: `+${Math.floor(Math.random() * 50 + 20)} XP`,
          type: 'xp',
          x: Math.random() * window.innerWidth,
          y: Math.random() * window.innerHeight * 0.5,
          color: '#a78bfa'
        });
      }, i * 200);
    }
  }, [play, showFloatingText]);

  const showStreakCeremony = useCallback((days) => {
    play('streakFire');
    const id = ++ceremonyIdRef.current;
    setActiveCeremonies(prev => [...prev, {
      id,
      type: 'streak',
      data: { days },
      duration: 3000,
    }]);
    setScreenJuice({ type: 'pulse', color: '#f59e0b', duration: 2000 });
    setTimeout(() => setScreenJuice(null), 2000);
    setTimeout(() => {
      setActiveCeremonies(prev => prev.filter(c => c.id !== id));
    }, 3000);
  }, [play]);

  const showBadgeUnlock = useCallback((badge) => {
    play('badgeUnlock');
    const id = ++ceremonyIdRef.current;
    setActiveCeremonies(prev => [...prev, {
      id,
      type: 'badge',
      data: badge,
      duration: 3500,
    }]);
    setScreenJuice({ type: 'sparkle', duration: 1500 });
    setTimeout(() => setScreenJuice(null), 1500);
    setTimeout(() => {
      setActiveCeremonies(prev => prev.filter(c => c.id !== id));
    }, 3500);
  }, [play]);

  const showCardReveal = useCallback((card) => {
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
    }, 3000);
  }, [play]);

  const screenShake = useCallback((intensity = 5, duration = 300) => {
    setScreenJuice({ type: 'shake', intensity, duration });
    setTimeout(() => setScreenJuice(null), duration);
  }, []);

  const screenFlash = useCallback((color = 'rgba(99,102,241,0.3)', duration = 300) => {
    setScreenJuice({ type: 'flash', color, duration });
    setTimeout(() => setScreenJuice(null), duration);
  }, []);

  const dismissCeremony = useCallback((id) => {
    setActiveCeremonies(prev => prev.filter(c => c.id !== id));
  }, []);

  const value = {
    play,
    showFloatingText, showXP, showLevelUp,
    showStreakCeremony, showBadgeUnlock, showCardReveal,
    screenShake, screenFlash,
    dismissCeremony,
    soundEnabled: soundEngine.enabled,
    toggleSound: () => soundEngine.toggle(),
    soundVolume: soundEngine.volume,
    setSoundVolume: (v) => soundEngine.setVolume(v),
  };

  return (
    <JuiceContext.Provider value={value}>
      {children}
      <ScreenJuiceOverlay juice={screenJuice} />
      <FloatingTextOverlay texts={floatingTexts} />
      <CeremonyOverlay
        ceremonies={activeCeremonies}
        onDismiss={dismissCeremony}
        play={play}
      />
    </JuiceContext.Provider>
  );
}
