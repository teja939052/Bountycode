const CACHE_VERSION = "bountycode-cache-v3";
const CORE_CACHE = `${CACHE_VERSION}-core`;
const RUNTIME_CACHE = `${CACHE_VERSION}-runtime`;
const PRECACHE_URLS = ["/"];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches
      .open(CORE_CACHE)
      .then((cache) => cache.addAll(PRECACHE_URLS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(
          keys
            .filter((key) => !key.startsWith(CACHE_VERSION))
            .map((key) => caches.delete(key))
        )
      )
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const { request } = event;
  if (request.method !== "GET") return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;
  if (url.pathname.startsWith("/api")) return;

  if (request.mode === "navigate") {
    event.respondWith(
      fetch(request)
        .then((response) => {
          const clone = response.clone();
          caches.open(CORE_CACHE).then((cache) => cache.put("/", clone));
          return response;
        })
        .catch(() =>
          caches.match(request).then((cached) => cached || caches.match("/"))
        )
    );
    return;
  }

  // Immutable hashed build assets (/assets/*.hash.js|css|...) are safe to serve
  // cache-first. Everything else (Vite dev modules, unhashed files) must go to
  // the network first so code changes are never masked by a stale cache.
  const isHashedAsset = /\.[a-f0-9]{8,}\.(js|css|png|jpe?g|gif|svg|woff2?|webp)$/.test(url.pathname);

  event.respondWith(
    (isHashedAsset ? caches.match(request) : Promise.resolve(null)).then((cached) => {
      if (cached) return cached;
      return fetch(request)
        .then((response) => {
          if (response.ok) {
            const clone = response.clone();
            caches.open(RUNTIME_CACHE).then((cache) => cache.put(request, clone));
          }
          return response;
        })
        .catch(() => caches.match("/"));
    })
  );
});

self.addEventListener("push", (event) => {
  let data = {};
  try {
    data = event.data ? event.data.json() : {};
  } catch (err) {
    data = { body: event.data ? event.data.text() : "New update available" };
  }
  const title = data.title || "BountyCode";
  const options = {
    body: data.body || "",
    icon: data.icon || "/icon.svg",
    badge: data.badge || "/icon.svg",
  };
  event.waitUntil(self.registration.showNotification(title, options));
});
