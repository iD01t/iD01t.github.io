const V = 'v1.0.0';
const ASSETS = [
  '/', '/ebooks.html','/audiobooks.html','/book.html',
  '/assets/css/site.css','/assets/js/app.js','/manifest.webmanifest'
];
self.addEventListener('install', e=>{
  e.waitUntil(caches.open(V).then(c=>c.addAll(ASSETS)).then(()=>self.skipWaiting()));
});
self.addEventListener('activate', e=>{
  e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==V).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));
});
self.addEventListener('fetch', e=>{
  const {request} = e;
  if (request.method !== 'GET') return;
  e.respondWith(
    caches.match(request).then(r => r || fetch(request).then(resp=>{
      const copy = resp.clone();
      caches.open(V).then(c=>c.put(request, copy)).catch(()=>{});
      return resp;
    }).catch(()=>caches.match('/')) )
  );
});
