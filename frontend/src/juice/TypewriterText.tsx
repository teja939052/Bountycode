import React, { useState, useEffect, useRef } from 'react';

export default function TypewriterText({ text, speed = 30, onComplete, className = '' }) {
  const [displayed, setDisplayed] = useState('');
  const [isComplete, setIsComplete] = useState(false);
  const indexRef = useRef(0);

  useEffect(() => {
    setDisplayed('');
    indexRef.current = 0;
    setIsComplete(false);
  }, [text]);

  useEffect(() => {
    if (!text) return;

    const interval = setInterval(() => {
      if (indexRef.current < text.length) {
        setDisplayed(text.slice(0, indexRef.current + 1));
        indexRef.current++;
      } else {
        clearInterval(interval);
        setIsComplete(true);
        onComplete?.();
      }
    }, speed);

    return () => clearInterval(interval);
  }, [text, speed]);

  return (
    <span className={className}>
      {displayed}
      {!isComplete && (
        <span className="inline-block w-[2px] h-[1em] bg-indigo-400 ml-0.5 animate-pulse" />
      )}
    </span>
  );
}
