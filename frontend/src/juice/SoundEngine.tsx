declare global {
  interface Window {
    webkitAudioContext: typeof AudioContext;
  }
}

class SoundEngine {
  private ctx: AudioContext | null = null;
  enabled: boolean;
  volume: number;

  constructor() {
    this.enabled = localStorage.getItem('sound_enabled') !== 'false';
    this.volume = parseFloat(localStorage.getItem('sound_volume') || '0.5');
  }

  _ensureContext() {
    const ctx = (window.AudioContext || window.webkitAudioContext);
    if (!this.ctx) {
      this.ctx = new ctx();
    }
    if (this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  _playTone(frequency: number, duration: number, type: OscillatorType = 'square', volume = 0.3) {
    if (!this.enabled) return;
    this._ensureContext();
    const osc = this.ctx!.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = type;
    osc.frequency.setValueAtTime(frequency, this.ctx.currentTime);
    gain.gain.setValueAtTime(volume * this.volume, this.ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + duration);
    osc.connect(gain);
    gain.connect(this.ctx.destination);
    osc.start();
    osc.stop(this.ctx.currentTime + duration);
  }

  _playNoise(duration: number, volume = 0.2) {
    if (!this.enabled) return;
    this._ensureContext();
    const bufferSize = this.ctx!.sampleRate * duration;
    const buffer = this.ctx!.createBuffer(1, bufferSize, this.ctx!.sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) {
      data[i] = Math.random() * 2 - 1;
    }
    const source = this.ctx!.createBufferSource();
    source.buffer = buffer;
    const gain = this.ctx!.createGain();
    gain.gain.setValueAtTime(volume * this.volume, this.ctx!.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.ctx!.currentTime + duration);
    source.connect(gain);
    gain.connect(this.ctx!.destination);
    source.start();
  }

  xpCollect() {
    this._playTone(523, 0.08, 'square', 0.2);
    setTimeout(() => this._playTone(659, 0.08, 'square', 0.2), 60);
    setTimeout(() => this._playTone(784, 0.12, 'square', 0.2), 120);
  }

  levelUp() {
    this._playTone(523, 0.15, 'square', 0.25);
    setTimeout(() => this._playTone(659, 0.15, 'square', 0.25), 100);
    setTimeout(() => this._playTone(784, 0.15, 'square', 0.25), 200);
    setTimeout(() => this._playTone(1047, 0.3, 'square', 0.3), 300);
  }

  badgeUnlock() {
    this._playTone(1047, 0.1, 'sine', 0.15);
    setTimeout(() => this._playTone(1319, 0.1, 'sine', 0.15), 80);
    setTimeout(() => this._playTone(1568, 0.2, 'sine', 0.2), 160);
  }

  streakFire() {
    this._playNoise(0.4, 0.2);
    setTimeout(() => this._playTone(200, 0.5, 'sawtooth', 0.15), 100);
  }

  correctAnswer() {
    this._playTone(523, 0.1, 'sine', 0.25);
    setTimeout(() => this._playTone(659, 0.15, 'sine', 0.25), 80);
  }

  wrongAnswer() {
    this._playTone(300, 0.2, 'sawtooth', 0.15);
    setTimeout(() => this._playTone(200, 0.3, 'sawtooth', 0.12), 150);
  }

  buttonClick() {
    this._playTone(800, 0.04, 'square', 0.1);
  }

  cardFlip() {
    this._playNoise(0.06, 0.1);
    setTimeout(() => this._playTone(1200, 0.08, 'sine', 0.1), 40);
  }

  questComplete() {
    this._playTone(440, 0.1, 'sine', 0.2);
    setTimeout(() => this._playTone(554, 0.1, 'sine', 0.2), 100);
    setTimeout(() => this._playTone(659, 0.1, 'sine', 0.2), 200);
    setTimeout(() => this._playTone(880, 0.2, 'sine', 0.25), 300);
  }

  battleStart() {
    this._playTone(220, 0.5, 'sawtooth', 0.2);
    setTimeout(() => this._playTone(330, 0.5, 'sawtooth', 0.2), 300);
    setTimeout(() => this._playTone(440, 0.8, 'sawtooth', 0.25), 600);
  }

  countdown() {
    this._playTone(1000, 0.15, 'square', 0.2);
  }

  countdownGo() {
    this._playTone(1200, 0.3, 'square', 0.3);
  }

  toggle(): boolean {
    this.enabled = !this.enabled;
    localStorage.setItem('sound_enabled', String(this.enabled));
    return this.enabled;
  }

  setVolume(v: number) {
    this.volume = Math.max(0, Math.min(1, v));
    localStorage.setItem('sound_volume', String(v));
  }
}

const soundEngine = new SoundEngine();
export default soundEngine;
