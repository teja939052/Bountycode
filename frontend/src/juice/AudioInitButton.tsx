import { useEffect, useRef } from 'react';
import soundEngine from './SoundEngine';

export default function AudioInitButton() {
  const inited = useRef(false);

  useEffect(() => {
    const init = () => {
      if (inited.current) return;
      inited.current = true;
      soundEngine._ensureContext();
      document.removeEventListener('click', init);
      document.removeEventListener('touchstart', init);
      document.removeEventListener('keydown', init);
    };
    document.addEventListener('click', init);
    document.addEventListener('touchstart', init);
    document.addEventListener('keydown', init);
    return () => {
      document.removeEventListener('click', init);
      document.removeEventListener('touchstart', init);
      document.removeEventListener('keydown', init);
    };
  }, []);

  return null;
}
