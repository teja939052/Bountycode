/*
 * PlacementPro Service Worker
 * Enables offline support and caching for PWA
 */

const CACHE_NAME = 'placementpro-v1';
const STATIC_CACHE = 'placementpro-static-v1';
const DYNAMIC_CACHE = 'placementpro-dynamic-v1';

// Static assets to cache on install
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/favicon.ico',
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png',
];

// API routes to cache (for offline access)
const CACHEABLE_API_ROUTES = [
  '/api/problems/topics',
  '/api/problems/progress',
  '/api/daily/challenge',
  '/api/readiness/score',
  '/api/concepts',
];

// Install event - cache static assets
self.addEventListener('install', (event) => {
  console.log('[SW] Installing...');
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then((cache) => {
        console.log('[SW] Caching static assets');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => self.skipWaiting())
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cache) => {
          if (cache !== STATIC_CACHE && cache !== DYNAMIC_CACHE) {
            console.log('[SW] Deleting old cache:', cache);
            return caches.delete(cache);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }

  // Skip chrome extension requests
  if (!url.protocol.startsWith('http')) {
    return;
  }

  // Handle API requests
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(handleApiRequest(request));
    return;
  }

  // Handle static assets
  event.respondWith(handleStaticRequest(request));
});

// Handle API requests with cache-first strategy for cacheable routes
async function handleApiRequest(request) {
  const url = new URL(request.url);

  // Check if this API route should be cached
  const shouldCache = CACHEABLE_API_ROUTES.some(route => url.pathname.startsWith(route));

  if (shouldCache) {
    // Cache-first strategy
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      // Return cached response and update in background
      updateCache(request);
      return cachedResponse;
    }

    // Fetch from network and cache
    try {
      const response = await fetch(request);
      if (response.ok) {
        const cache = await caches.open(DYNAMIC_CACHE);
        cache.put(request, response.clone());
      }
      return response;
    } catch (error) {
      // Return offline fallback
      return new Response(
        JSON.stringify({ error: 'Offline', message: 'You are currently offline. Please check your connection.' }),
        { headers: { 'Content-Type': 'application/json' }, status: 503 }
      );
    }
  }

  // Network-first for other API requests
  try {
    const response = await fetch(request);
    return response;
  } catch (error) {
    // Return offline fallback
    return new Response(
      JSON.stringify({ error: 'Offline', message: 'You are currently offline.' }),
      { headers: { 'Content-Type': 'application/json' }, status: 503 }
    );
  }
}

// Handle static requests with cache-first strategy
async function handleStaticRequest(request) {
  const cachedResponse = await caches.match(request);
  if (cachedResponse) {
    return cachedResponse;
  }

  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(STATIC_CACHE);
      cache.put(request, response.clone());
    }
    return response;
  } catch (error) {
    // Return offline page for navigation requests
    if (request.mode === 'navigate') {
      const offlineResponse = await caches.match('/');
      if (offlineResponse) {
        return offlineResponse;
      }
    }
    return new Response('Offline', { status: 503 });
  }
}

// Update cache in background
async function updateCache(request) {
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(DYNAMIC_CACHE);
      cache.put(request, response);
    }
  } catch (error) {
    // Silently fail
  }
}

// Listen for messages from main thread
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }

  if (event.data && event.data.type === 'CACHE_PROBLEMS') {
    // Cache problems for offline access
    cacheProblems(event.data.problems);
  }
});

// Cache problems for offline access
async function cacheProblems(problems) {
  const cache = await caches.open(DYNAMIC_CACHE);
  for (const problem of problems) {
    const url = `/api/problems/${problem.id}`;
    const response = new Response(JSON.stringify(problem), {
      headers: { 'Content-Type': 'application/json' }
    });
    await cache.put(url, response);
  }
  console.log('[SW] Cached', problems.length, 'problems for offline access');
}

// Background sync for failed submissions
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-submissions') {
    event.waitUntil(syncSubmissions());
  }
});

// Sync failed submissions when back online
async function syncSubmissions() {
  const db = await openDB();
  const submissions = await db.getAll('pending-submissions');

  for (const submission of submissions) {
    try {
      await fetch(submission.url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(submission.data),
      });
      await db.delete('pending-submissions', submission.id);
      console.log('[SW] Synced submission:', submission.id);
    } catch (error) {
      console.log('[SW] Failed to sync submission:', submission.id);
    }
  }
}

// IndexedDB helper for offline storage
function openDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open('PlacementProOffline', 1);

    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve(request.result);

    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      if (!db.objectStoreNames.contains('pending-submissions')) {
        db.createObjectStore('pending-submissions', { keyPath: 'id', autoIncrement: true });
      }
      if (!db.objectStoreNames.contains('cached-code')) {
        db.createObjectStore('cached-code', { keyPath: 'key' });
      }
    };
  });
}

// Save code to IndexedDB (called from main thread)
self.addEventListener('message', async (event) => {
  if (event.data && event.data.type === 'SAVE_CODE') {
    const db = await openDB();
    const tx = db.transaction('cached-code', 'readwrite');
    const store = tx.objectStore('cached-code');
    store.put({
      key: event.data.key,
      code: event.data.code,
      language: event.data.language,
      timestamp: Date.now(),
    });
    await tx.complete;
    console.log('[SW] Code saved to IndexedDB');
  }

  if (event.data && event.data.type === 'LOAD_CODE') {
    const db = await openDB();
    const tx = db.transaction('cached-code', 'readonly');
    const store = tx.objectStore('cached-code');
    const request = store.get(event.data.key);
    request.onsuccess = () => {
      self.clients.matchAll().then(clients => {
        clients.forEach(client => {
          client.postMessage({
            type: 'CODE_LOADED',
            data: request.result,
          });
        });
      });
    };
  }
});
