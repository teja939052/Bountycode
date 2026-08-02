import React from 'react';
import { useJuice } from './JuiceProvider';

export default function SoundToggle() {
  const { soundEnabled, toggleSound } = useJuice();

  return (
    <button
      onClick={toggleSound}
      className="fixed bottom-20 right-4 z-50 w-10 h-10 rounded-full flex items-center justify-center text-lg transition-all hover:scale-110"
      style={{
        background: soundEnabled ? 'rgba(99,102,241,0.2)' : 'rgba(100,116,139,0.2)',
        border: `1px solid ${soundEnabled ? 'rgba(99,102,241,0.4)' : 'rgba(100,116,139,0.3)'}`,
      }}
      title={soundEnabled ? 'Mute sounds' : 'Enable sounds'}
    >
      {soundEnabled ? '🔊' : '🔇'}
    </button>
  );
}
