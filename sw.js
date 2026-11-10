var V="pc-v62",A=["./","./index.html","./manifest.json"];
self.addEventListener("install",function(e){e.waitUntil(caches.open(V).then(function(c){return c.addAll(A);}));});
self.addEventListener("activate",function(e){e.waitUntil(caches.keys().then(function(ks){return Promise.all(ks.filter(function(k){return k!=V;}).map(function(k){return caches.delete(k);}));}).then(function(){return self.clients.claim();}));});
self.addEventListener("message",function(e){if(e.data=="skip")self.skipWaiting();});
self.addEventListener("fetch",function(e){if(e.request.method!="GET")return;var u=new URL(e.request.url);if(u.origin!=location.origin)return;
// cache first: the app opens at once on a weak gym signal; the network copy refreshes the cache in the background and a new version arrives through the update prompt
e.respondWith(caches.match(e.request,{ignoreSearch:true}).then(function(hit){var net=fetch(e.request).then(function(r){if(r.ok){var c=r.clone();caches.open(V).then(function(x){x.put(e.request,c);});}return r;}).catch(function(){return hit||caches.match("./");});return hit||net;}));});
