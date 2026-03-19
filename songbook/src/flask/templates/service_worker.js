self.addEventListener('install', function(event) {
  console.log('[Service Worker] Installing Service Worker ...', event);
});
self.addEventListener('activate', function(event) {
  console.log('[Service Worker] Activating Service Worker ...', event);
});
self.addEventListener('fetch', function(event) {
  console.log('[Service Worker] Fetching something ...', event);
});

const cacheName = "HK_Cache";
const precachedResources = ["/", "/app.js", "/static/style.css", {{songPaths}}];

async function precache() {
  const cache = await caches.open(cacheName);
  return cache.addAll(precachedResources);
}

self.addEventListener("install", (event) => {
  event.waitUntil(precache());
});

async function cacheFirstWithRefresh(request) {
  const fetchResponsePromise = fetch(request).then(async (networkResponse) => {
    if (networkResponse.ok) {
      const cache = await caches.open("HK_Cache");
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  });

  return (await caches.match(request)) || (await fetchResponsePromise);
}

self.addEventListener("fetch", (event) => {
  event.respondWith(cacheFirstWithRefresh(event.request));
});
