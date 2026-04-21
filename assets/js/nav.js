(function () {
  // Compute root path based on URL depth under /OrbitPrompt/
  const parts = window.location.pathname.split('/').filter(Boolean);
  const repoIdx = parts.indexOf('OrbitPrompt');
  const depth = repoIdx >= 0 ? parts.length - repoIdx - 1 : 0;
  const root = depth <= 0 ? './' : '../'.repeat(depth);

  // Current page label for breadcrumb
  const page = document.title.split('—')[0].trim();

  const style = document.createElement('style');
  style.textContent = `
    #orbit-nav {
      position: sticky; top: 0; z-index: 200;
      background: rgba(10,10,10,0.96);
      backdrop-filter: blur(8px);
      border-bottom: 1px solid rgba(255,255,255,0.07);
      height: 44px;
      display: flex; align-items: center; justify-content: space-between;
      padding: 0 20px;
      font-family: 'SF Mono','Fira Mono','JetBrains Mono',monospace;
    }
    #orbit-nav a { text-decoration: none; transition: color .15s; }
    .orbit-nav-brand { font-size: 12px; color: #e8d5b7; font-weight: 600; }
    .orbit-nav-links { display: flex; gap: 18px; list-style: none; margin: 0; padding: 0; }
    .orbit-nav-links a { font-size: 11px; color: #666; }
    .orbit-nav-links a:hover { color: #a0a0a0; }
    .orbit-nav-sep { color: #333; font-size: 10px; }
    @media (max-width: 480px) {
      .orbit-nav-links li:nth-child(n+4) { display: none; }
    }
  `;

  const nav = document.createElement('nav');
  nav.id = 'orbit-nav';
  nav.innerHTML = `
    <a href="${root}" class="orbit-nav-brand">OrbitPrompt</a>
    <ul class="orbit-nav-links">
      <li><a href="${root}#generators">Generators</a></li>
      <li><a href="${root}whitepaper.html">Whitepaper</a></li>
      <li><a href="${root}archive.html">Archive</a></li>
      <li><a href="${root}links/">Links</a></li>
      <li><a href="https://github.com/dtslib1979/OrbitPrompt" target="_blank" rel="noopener">GitHub</a></li>
    </ul>
  `;

  document.head.appendChild(style);
  document.body.insertBefore(nav, document.body.firstChild);
})();
