export function registerServiceWorker() {
  if (!('serviceWorker' in navigator)) return;

  if (import.meta.env.DEV) {
    // Dev must never be SW-controlled: unregister any stale service worker
    // (e.g. left over from a production build) and purge all its caches so the
    // dev server always serves fresh modules.
    navigator.serviceWorker.getRegistrations().then((regs) => {
      regs.forEach((reg) => reg.unregister());
    });
    if (window.caches) {
      window.caches.keys().then((keys) => keys.forEach((key) => window.caches.delete(key)));
    }
    return;
  }

  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/service-worker.js').then(
      (reg) => console.log('SW registered:', reg.scope),
      (err) => console.log('SW failed:', err)
    );
  });
}

export function isPwaInstalled() {
  return window.matchMedia('(display-mode: standalone)').matches;
}
