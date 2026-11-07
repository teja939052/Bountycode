/**
 * SoundSea — zero-asset WebAudio ambience + SFX for the voyage map.
 *
 * No audio files, no bandwidth, no dependencies. Three generative ambient
 * themes (meadow / plains / embers) built from detuned oscillators through
 * a lowpass filter with a slow LFO, plus one-shot SFX (sail whoosh, chime,
 * fanfare, campfire pop). Everything starts on a user gesture (autoplay
 * policy) and honors a persisted mute toggle.
 */

export type BgmTheme = "meadow" | "plains" | "embers" | "pirate";

const MUTE_KEY = "pp_audio_muted";

let ctx: AudioContext | null = null;
let ambientNodes: { stop: () => void } | null = null;
let currentTheme: BgmTheme | null = null;

export function isMuted(): boolean {
  try {
    return localStorage.getItem(MUTE_KEY) === "1";
  } catch {
    return false;
  }
}

export function setMuted(muted: boolean) {
  try {
    localStorage.setItem(MUTE_KEY, muted ? "1" : "0");
  } catch {
    /* private mode — sound just stays on */
  }
  if (muted) stopAmbient();
}

function ensureCtx(): AudioContext | null {
  if (typeof window === "undefined") return null;
  if (isMuted()) return null;
  try {
    if (!ctx) {
      const AC = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
      ctx = new AC();
    }
    if (ctx.state === "suspended") void ctx.resume();
    return ctx;
  } catch {
    return null;
  }
}

// Pentatonic-ish pads per theme: [root freq, intervals in semitones, filter Hz]
const THEMES: Record<BgmTheme, { root: number; steps: number[]; cutoff: number; gain: number }> = {
  meadow: { root: 261.63, steps: [0, 4, 7, 12, 16], cutoff: 900, gain: 0.045 },
  plains: { root: 220.0, steps: [0, 3, 7, 12, 14], cutoff: 700, gain: 0.05 },
  embers: { root: 174.61, steps: [0, 3, 5, 10, 12], cutoff: 520, gain: 0.055 },
  pirate: { root: 110.0, steps: [0, 3, 7, 12, 17], cutoff: 650, gain: 0.06 },
};

export function themeForWorld(worldId?: string | null): BgmTheme {
  if (!worldId) return "meadow";
  if (/boss|arena|pressure|dynamic/i.test(worldId)) return "embers";
  if (/pattern|plain|search|sort|recursion|linked|stack|queue/i.test(worldId)) return "plains";
  if (/pirate|cove|shore|treasure|hashing|searchlands|graphs/i.test(worldId ?? "")) return "pirate";
  return "meadow";
}

export function startAmbient(theme: BgmTheme) {
  const ac = ensureCtx();
  if (!ac) return;
  if (ambientNodes && currentTheme === theme) return;
  stopAmbient();
  currentTheme = theme;

  const cfg = THEMES[theme];
  const master = ac.createGain();
  master.gain.value = 0;
  master.connect(ac.destination);
  master.gain.linearRampToValueAtTime(cfg.gain, ac.currentTime + 2.5);

  const filter = ac.createBiquadFilter();
  filter.type = "lowpass";
  filter.frequency.value = cfg.cutoff;
  filter.connect(master);

  // Slow breathing LFO on the filter.
  const lfo = ac.createOscillator();
  lfo.frequency.value = 0.07;
  const lfoGain = ac.createGain();
  lfoGain.gain.value = cfg.cutoff * 0.35;
  lfo.connect(lfoGain);
  lfoGain.connect(filter.frequency);
  lfo.start();

  const oscs: OscillatorNode[] = cfg.steps.map((st, i) => {
    const o = ac.createOscillator();
    o.type = i % 2 ? "sine" : "triangle";
    o.frequency.value = cfg.root * Math.pow(2, st / 12);
    o.detune.value = (i - 2) * 4;
    const g = ac.createGain();
    g.gain.value = 1 / cfg.steps.length;
    o.connect(g);
    g.connect(filter);
    // Gentle arpeggiated entrances so it feels alive, not static.
    o.start(ac.currentTime + i * 0.9);
    return o;
  });

  // Soft wave crashes: filtered noise swell every ~9s.
  const noiseTimer = window.setInterval(() => {
    if (!ctx || isMuted()) return;
    const dur = 2.2;
    const buf = ac.createBuffer(1, ac.sampleRate * dur, ac.sampleRate);
    const data = buf.getChannelData(0);
    for (let i = 0; i < data.length; i++) {
      const k = i / data.length;
      data[i] = (Math.random() * 2 - 1) * Math.sin(Math.PI * k) * 0.5;
    }
    const src = ac.createBufferSource();
    src.buffer = buf;
    const nf = ac.createBiquadFilter();
    nf.type = "lowpass";
    nf.frequency.value = 600;
    const ng = ac.createGain();
    ng.gain.value = 0.05;
    src.connect(nf);
    nf.connect(ng);
    ng.connect(ac.destination);
    src.start();
  }, 9000);

  ambientNodes = {
    stop: () => {
      window.clearInterval(noiseTimer);
      try {
        master.gain.linearRampToValueAtTime(0, ac.currentTime + 0.6);
        window.setTimeout(() => {
          oscs.forEach((o) => { try { o.stop(); } catch { /* already stopped */ } });
          try { lfo.stop(); } catch { /* already stopped */ }
          master.disconnect();
        }, 700);
      } catch {
        /* context gone */
      }
    },
  };
}

export function stopAmbient() {
  ambientNodes?.stop();
  ambientNodes = null;
  currentTheme = null;
}

type SfxName = "sail" | "chime" | "fanfare" | "pop" | "boss";

export function sfx(name: SfxName) {
  const ac = ensureCtx();
  if (!ac) return;
  const t = ac.currentTime;
  try {
    if (name === "sail") {
      // Filtered noise sweep up — a whoosh.
      const dur = 0.65;
      const buf = ac.createBuffer(1, ac.sampleRate * dur, ac.sampleRate);
      const data = buf.getChannelData(0);
      for (let i = 0; i < data.length; i++) data[i] = Math.random() * 2 - 1;
      const src = ac.createBufferSource();
      src.buffer = buf;
      const f = ac.createBiquadFilter();
      f.type = "bandpass";
      f.Q.value = 1.2;
      f.frequency.setValueAtTime(300, t);
      f.frequency.exponentialRampToValueAtTime(2400, t + dur);
      const g = ac.createGain();
      g.gain.setValueAtTime(0.0001, t);
      g.gain.exponentialRampToValueAtTime(0.22, t + 0.12);
      g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
      src.connect(f); f.connect(g); g.connect(ac.destination);
      src.start(t);
    } else if (name === "chime" || name === "pop") {
      const notes = name === "chime" ? [523.25, 659.25, 783.99] : [392.0, 523.25];
      notes.forEach((freq, i) => {
        const o = ac.createOscillator();
        o.type = "sine";
        o.frequency.value = freq;
        const g = ac.createGain();
        const t0 = t + i * 0.09;
        g.gain.setValueAtTime(0.0001, t0);
        g.gain.exponentialRampToValueAtTime(0.18, t0 + 0.02);
        g.gain.exponentialRampToValueAtTime(0.0001, t0 + 0.5);
        o.connect(g); g.connect(ac.destination);
        o.start(t0); o.stop(t0 + 0.55);
      });
    } else if (name === "fanfare" || name === "boss") {
      const notes = name === "fanfare"
        ? [261.63, 329.63, 392.0, 523.25]
        : [196.0, 185.0, 196.0, 147.0];
      notes.forEach((freq, i) => {
        const o = ac.createOscillator();
        o.type = name === "fanfare" ? "triangle" : "sawtooth";
        o.frequency.value = freq;
        const f = ac.createBiquadFilter();
        f.type = "lowpass";
        f.frequency.value = name === "fanfare" ? 2400 : 900;
        const g = ac.createGain();
        const t0 = t + i * 0.13;
        g.gain.setValueAtTime(0.0001, t0);
        g.gain.exponentialRampToValueAtTime(0.16, t0 + 0.03);
        g.gain.exponentialRampToValueAtTime(0.0001, t0 + 0.6);
        o.connect(f); f.connect(g); g.connect(ac.destination);
        o.start(t0); o.stop(t0 + 0.65);
      });
    }
  } catch {
    /* audio is garnish — never break the app */
  }
}
