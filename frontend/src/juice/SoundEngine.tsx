declare global {
  interface Window {
    webkitAudioContext: typeof AudioContext;
  }
}

type OscillatorType = OscillatorType;

class SoundEngine {
  private ctx: AudioContext | null = null;
  private masterGain: GainNode | null = null;
  enabled: boolean;
  volume: number;
  private activeOscillators: OscillatorNode[] = [];

  constructor() {
    this.enabled = localStorage.getItem('sound_enabled') !== 'false';
    this.volume = parseFloat(localStorage.getItem('sound_volume') || '0.6');
  }

  _ensureContext() {
    const AudioCtx = window.AudioContext || (window as any).webkitAudioContext;
    if (!this.ctx) {
      this.ctx = new AudioCtx();
      this.masterGain = this.ctx.createGain();
      this.masterGain.gain.setValueAtTime(this.volume, this.ctx.currentTime);
      this.masterGain.connect(this.ctx.destination);
    }
    if (this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  _playTone(frequency: number, duration: number, type: OscillatorType = 'square', volume = 0.3, slideTo?: number) {
    if (!this.enabled) return;
    this._ensureContext();
    const osc = this.ctx!.createOscillator();
    const gain = this.ctx!.createGain();
    osc.type = type;
    osc.frequency.setValueAtTime(frequency, this.ctx!.currentTime);
    if (slideTo) {
      osc.frequency.exponentialRampToValueAtTime(Math.max(1, slideTo), this.ctx!.currentTime + duration);
    }
    gain.gain.setValueAtTime(volume * this.volume, this.ctx!.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.ctx!.currentTime + duration);
    osc.connect(gain);
    gain.connect(this.masterGain!);
    osc.start();
    osc.stop(this.ctx!.currentTime + duration);
    this.activeOscillators.push(osc);
    osc.onended = () => {
      this.activeOscillators = this.activeOscillators.filter(o => o !== osc);
    };
  }

  _playNoise(duration: number, volume = 0.2, filterFreq = 3000) {
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
    const filter = this.ctx!.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(filterFreq, this.ctx!.currentTime);
    const gain = this.ctx!.createGain();
    gain.gain.setValueAtTime(volume * this.volume, this.ctx!.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.ctx!.currentTime + duration);
    source.connect(filter);
    filter.connect(gain);
    gain.connect(this.masterGain!);
    source.start();
  }

  _playRise(duration: number, volume = 0.2) {
    if (!this.enabled) return;
    this._ensureContext();
    const osc = this.ctx!.createOscillator();
    const gain = this.ctx!.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(220, this.ctx!.currentTime);
    osc.frequency.exponentialRampToValueAtTime(880, this.ctx!.currentTime + duration);
    gain.gain.setValueAtTime(volume * this.volume, this.ctx!.currentTime);
    gain.gain.linearRampToValueAtTime(0.001, this.ctx!.currentTime + duration);
    osc.connect(gain);
    gain.connect(this.masterGain!);
    osc.start();
    osc.stop(this.ctx!.currentTime + duration);
  }

  xpCollect() {
    this._playTone(523, 0.06, 'square', 0.15);
    setTimeout(() => this._playTone(659, 0.06, 'square', 0.15), 50);
    setTimeout(() => this._playTone(784, 0.1, 'square', 0.2), 100);
  }

  xpBig() {
    this._playTone(523, 0.08, 'square', 0.2);
    setTimeout(() => this._playTone(659, 0.08, 'square', 0.2), 70);
    setTimeout(() => this._playTone(784, 0.08, 'square', 0.2), 140);
    setTimeout(() => this._playTone(1047, 0.2, 'square', 0.25), 210);
  }

  levelUp() {
    this._playTone(523, 0.12, 'square', 0.2);
    setTimeout(() => this._playTone(659, 0.12, 'square', 0.2), 80);
    setTimeout(() => this._playTone(784, 0.12, 'square', 0.2), 160);
    setTimeout(() => this._playTone(1047, 0.35, 'square', 0.3), 240);
  }

  badgeUnlock() {
    this._playTone(1047, 0.08, 'sine', 0.15);
    setTimeout(() => this._playTone(1319, 0.08, 'sine', 0.15), 60);
    setTimeout(() => this._playTone(1568, 0.18, 'sine', 0.2), 120);
  }

  streakFire() {
    this._playNoise(0.5, 0.25, 4000);
    setTimeout(() => this._playTone(200, 0.6, 'sawtooth', 0.2), 80);
  }

  correctAnswer() {
    this._playTone(523, 0.08, 'sine', 0.2);
    setTimeout(() => this._playTone(659, 0.12, 'sine', 0.2), 70);
  }

  wrongAnswer() {
    this._playTone(300, 0.2, 'sawtooth', 0.12);
    setTimeout(() => this._playTone(200, 0.35, 'sawtooth', 0.1), 140);
  }

  buttonClick() {
    this._playTone(800, 0.03, 'square', 0.08);
  }

  cardFlip() {
    this._playNoise(0.05, 0.08, 2000);
    setTimeout(() => this._playTone(1200, 0.06, 'sine', 0.1), 30);
  }

  questComplete() {
    this._playTone(440, 0.1, 'sine', 0.2);
    setTimeout(() => this._playTone(554, 0.1, 'sine', 0.2), 90);
    setTimeout(() => this._playTone(659, 0.1, 'sine', 0.2), 180);
    setTimeout(() => this._playTone(880, 0.25, 'sine', 0.25), 270);
  }

  battleStart() {
    this._playTone(220, 0.5, 'sawtooth', 0.2);
    setTimeout(() => this._playTone(330, 0.5, 'sawtooth', 0.2), 250);
    setTimeout(() => this._playTone(440, 0.8, 'sawtooth', 0.25), 500);
  }

  bossDefeat() {
    this._playTone(523, 0.1, 'square', 0.25);
    setTimeout(() => this._playTone(659, 0.1, 'square', 0.25), 80);
    setTimeout(() => this._playTone(784, 0.1, 'square', 0.25), 160);
    setTimeout(() => this._playTone(1047, 0.1, 'square', 0.3), 240);
    setTimeout(() => this._playTone(1568, 0.6, 'square', 0.35), 320);
  }

  countdown() {
    this._playTone(1000, 0.12, 'square', 0.2);
  }

  countdownGo() {
    this._playTone(1200, 0.25, 'square', 0.3);
  }

  comboGain() {
    this._playTone(440, 0.05, 'square', 0.12);
    setTimeout(() => this._playTone(554, 0.05, 'square', 0.12), 40);
    setTimeout(() => this._playTone(659, 0.08, 'square', 0.15), 80);
  }

  comboDecay() {
    this._playTone(300, 0.15, 'sawtooth', 0.08);
    setTimeout(() => this._playTone(250, 0.3, 'sawtooth', 0.06), 150);
  }

  criticalHit() {
    this._playNoise(0.15, 0.3, 5000);
    this._playTone(1200, 0.1, 'square', 0.25);
    setTimeout(() => this._playTone(800, 0.15, 'sawtooth', 0.2), 80);
  }

  powerUp() {
    this._playRise(0.4, 0.2);
    setTimeout(() => this._playTone(1047, 0.15, 'sine', 0.2), 300);
  }

  milestone() {
    this._playTone(523, 0.1, 'sine', 0.2);
    setTimeout(() => this._playTone(659, 0.1, 'sine', 0.2), 80);
    setTimeout(() => this._playTone(784, 0.1, 'sine', 0.2), 160);
    setTimeout(() => this._playTone(1047, 0.1, 'sine', 0.25), 240);
    setTimeout(() => this._playTone(1319, 0.4, 'sine', 0.3), 320);
  }

  achievement() {
    this._playTone(523, 0.1, 'sine', 0.2);
    setTimeout(() => this._playTone(659, 0.1, 'sine', 0.2), 70);
    setTimeout(() => this._playTone(784, 0.1, 'sine', 0.2), 140);
    setTimeout(() => this._playTone(1047, 0.1, 'sine', 0.25), 210);
    setTimeout(() => this._playTone(1568, 0.5, 'sine', 0.3), 280);
  }

  dailyLogin() {
    this._playTone(523, 0.1, 'sine', 0.2);
    setTimeout(() => this._playTone(659, 0.1, 'sine', 0.2), 80);
    setTimeout(() => this._playTone(784, 0.15, 'sine', 0.25), 160);
    setTimeout(() => this._playTone(1047, 0.3, 'sine', 0.3), 240);
  }

  toggle(): boolean {
    this.enabled = !this.enabled;
    localStorage.setItem('sound_enabled', String(this.enabled));
    if (!this.enabled) {
      this.activeOscillators.forEach(osc => {
        try { osc.stop(); } catch {}
      });
      this.activeOscillators = [];
    }
    return this.enabled;
  }

  setVolume(v: number) {
    this.volume = Math.max(0, Math.min(1, v));
    localStorage.setItem('sound_volume', String(v));
    if (this.masterGain) {
      this.masterGain.gain.setValueAtTime(this.volume, this.ctx!.currentTime);
    }
  }
}

const soundEngine = new SoundEngine();
export default soundEngine;
