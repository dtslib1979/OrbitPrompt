/**
 * gallery-store.js — OrbitPrompt Data Layer
 *
 * Centralized store for all data/*.json files.
 * All sections read from this store instead of fetching individually.
 *
 * Usage:
 *   import('./gallery-store.js').then(Store => Store.ready.then(() => { ... }));
 *   — or —
 *   <script src="assets/js/gallery-store.js"></script>
 *   <script> document.addEventListener('GalleryStoreReady', e => { ... }); </script>
 */

(function () {
  'use strict';

  const BASE = document.querySelector('script[src$="gallery-store.js"]')
    ?.getAttribute('src')?.replace('assets/js/gallery-store.js', '') || './';

  const DATA_FILES = {
    repos:      BASE + 'data/repos-registry.json',
    fab:        BASE + 'data/fab-manifest.json',
    phases:     BASE + 'data/phases.json',
    generators: BASE + 'data/generators.json',
  };

  const Store = {
    repos:      [],
    fab:        null,
    phases:     null,
    generators: [],
    modules:    [],   // populated by index.html's MODULES
    ready:      null, // Promise that resolves when all data loaded
    callbacks:  [],
    onReady(fn) { this.callbacks.push(fn); }
  };

  Store.ready = Promise.all(
    Object.entries(DATA_FILES).map(([key, url]) =>
      fetch(url)
        .then(r => r.json())
        .then(data => { Store[key] = data; })
        .catch(err => {
          console.warn(`[gallery-store] Failed to load ${key}:`, err.message);
        })
    )
  ).then(() => {
    // Compute derived stats
    const repoData = Array.isArray(Store.repos) ? Store.repos : [];
    Store.stats = {
      totalRepos:       repoData.length,
      tiers:            {},
      routes:           Store.fab?.routes ? Object.keys(Store.fab.routes).length : 0,
      generators:       Array.isArray(Store.generators?.generators) ? Store.generators.generators.length : 0,
      liveGenerators:   Array.isArray(Store.generators?.generators) ? Store.generators.generators.filter(g => g.status === 'live').length : 0,
      liveModules:      Store.modules.filter(m => m.status === 'live').length,
      totalModules:     Store.modules.length,
      phases:           Array.isArray(Store.phases?.parts) ? Store.phases.parts.length : 0,
      liveChapters:     0,
    };

    repoData.forEach(r => {
      const t = 'tier' + (r.tier || 3);
      Store.stats.tiers[t] = (Store.stats.tiers[t] || 0) + 1;
    });

    if (Array.isArray(Store.phases?.parts)) {
      Store.phases.parts.forEach(p => {
        if (Array.isArray(p.chapters)) {
          Store.stats.liveChapters += p.chapters.filter(c => c.status === 'live').length;
        }
      });
    }

    Store.stats.totalChapters = Store.phases?.parts?.reduce((acc, p) => acc + (p.chapters?.length || 0), 0) || 0;

    // Dispatch event
    const evt = new CustomEvent('GalleryStoreReady', { detail: Store });
    document.dispatchEvent(evt);

    // Run registered callbacks
    Store.callbacks.forEach(fn => fn(Store));
  });

  window.GalleryStore = Store;
})();
