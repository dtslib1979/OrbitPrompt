<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="철학을 코드로 — OrbitPrompt 사고 시스템">
<title>OrbitPrompt</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Inter:wght@400;500&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#0A1A0F;--bg2:#0D2214;--bg3:#112A18;--gold:#EEC864;--gold2:rgba(238,200,100,.45);--gold3:rgba(238,200,100,.1);--ink1:#FFFFFF;--ink2:rgba(255,255,255,.5);--ink3:rgba(255,255,255,.25);--purple:#a855f7;--cyan:#22d3ee;--green:#4ade80;--line:rgba(255,255,255,.04);--chalk:rgba(255,255,255,.02)}
html,body{background:var(--bg);color:var(--ink1);font-family:'Inter',sans-serif;min-height:100vh;overflow:hidden}
body::before{content:'';position:fixed;inset:0;background:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.1'/%3E%3C/svg%3E");pointer-events:none;z-index:0}
body::after{content:'';position:fixed;inset:0;background:radial-gradient(circle at 30% 30%, rgba(238,200,100,.03) 0%, transparent 50%),radial-gradient(circle at 70% 70%, rgba(34,211,238,.02) 0%, transparent 50%);pointer-events:none;z-index:0}

/* ── FULLSCREEN GRAPH ── */
#graphWrap{position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:1}
#graphSvg{width:100%;height:100%;display:block;cursor:grab;background:transparent;transform-style:preserve-3d;transform-origin:center center}
#graphSvg:active{cursor:grabbing}
.edge{fill:none;stroke-width:.8;stroke-linecap:round;opacity:.12;transition:opacity .3s}
.edge:hover,.edge.highlight{opacity:.6}
.node-dot{transition:r .2s,opacity .2s;cursor:pointer}
.node-dot:hover{r:6;opacity:1}
.node-label{font-family:'JetBrains Mono',monospace;font-size:8.5px;fill:rgba(255,255,255,.35);letter-spacing:.04em;pointer-events:none;transition:opacity .3s;text-anchor:middle;dominant-baseline:middle}
.node-group:hover .node-label{opacity:1;fill:rgba(255,255,255,.7)}
.node-group:hover .node-dot{filter:brightness(1.5)}
.center-label{font-family:'Cormorant Garamond',serif;font-size:15px;fill:var(--gold);font-style:italic;text-anchor:middle;pointer-events:none;opacity:.8}

/* ── SIDE LABEL (hub names) ── */
.hub-label{font-family:'JetBrains Mono',monospace;font-size:7px;fill:rgba(255,255,255,.15);letter-spacing:.12em;text-anchor:middle;pointer-events:none;text-transform:uppercase}

/* ── OVERLAY UI ── */
.header{position:fixed;top:0;left:0;right:0;z-index:100;padding:20px 28px;display:flex;align-items:center;justify-content:space-between;pointer-events:none}
.header .logo{pointer-events:auto;font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.2em;color:var(--gold2);text-decoration:none}
.header .nav-links{pointer-events:auto;display:flex;gap:24px}
.header .nav-links a{font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.12em;color:var(--ink3);text-decoration:none;transition:color .2s}
.header .nav-links a:hover{color:var(--ink2)}
.header .nav-links a.hot{color:var(--gold2)}

.footer{position:fixed;bottom:0;left:0;right:0;z-index:100;padding:16px 28px;display:flex;justify-content:center;gap:24px;flex-wrap:wrap;pointer-events:none}
.footer a{pointer-events:auto;font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.08em;color:var(--ink3);text-decoration:none;transition:color .2s}
.footer a:hover{color:var(--ink2)}

/* ── TITLE BOX ── */
.title-box{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);z-index:50;text-align:center;pointer-events:none;opacity:0;animation:fadeIn 2s ease 1s forwards}
.title-box .kicker{font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.25em;color:var(--gold2);margin-bottom:12px}
.title-box h1{font-family:'Cormorant Garamond',serif;font-size:28px;font-weight:400;line-height:1.2;letter-spacing:-.02em;color:#fff;margin-bottom:4px}
.title-box h1 em{font-style:italic;color:var(--gold)}
.title-box .sub{font-size:11px;color:var(--ink2);margin-top:8px}

@keyframes fadeIn{to{opacity:1}}

@media(max-width:700px){
  .header .nav-links{display:none}
  .footer{justify-content:center;gap:12px;padding:10px 16px}
  .footer a{font-size:7px}
  .title-box h1{font-size:22px}
}
</style>
</head>
<body>

<div class="header">
  <a class="logo" href="/">ORBITPROMPT</a>
  <div class="nav-links">
    <a class="hot" href="why.html">WHY</a>
    <a href="whitepaper.html">백서</a>
    <a href="philosophy.html">철학</a>
    <a href="humanity-finger.html">휴머니티</a>
  </div>
</div>

<div class="title-box">
  <div class="kicker">Φ-I-C-K-P-7AXIS · THOUGHT SYSTEM</div>
  <h1>칠판 위에 쓰는 <em>철학</em></h1>
  <div class="sub">그래프의 노드를 클릭하면 이동합니다 · 드래그로 회전</div>
</div>

<div id="graphWrap">
  <svg id="graphSvg" viewBox="-500 -500 1000 1000" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="ggold"><stop offset="0%" stop-color="#EEC864" stop-opacity=".3"/><stop offset="100%" stop-color="#EEC864" stop-opacity="0"/></radialGradient>
      <radialGradient id="gpurp"><stop offset="0%" stop-color="#a855f7" stop-opacity=".3"/><stop offset="100%" stop-color="#a855f7" stop-opacity="0"/></radialGradient>
      <radialGradient id="gcyan"><stop offset="0%" stop-color="#22d3ee" stop-opacity=".3"/><stop offset="100%" stop-color="#22d3ee" stop-opacity="0"/></radialGradient>
      <radialGradient id="ggrn"><stop offset="0%" stop-color="#4ade80" stop-opacity=".25"/><stop offset="100%" stop-color="#4ade80" stop-opacity="0"/></radialGradient>
      <radialGradient id="gwht"><stop offset="0%" stop-color="#fff" stop-opacity=".2"/><stop offset="100%" stop-color="#fff" stop-opacity="0"/></radialGradient>
      <filter id="glow"><feGaussianBlur stdDeviation="1.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    </defs>
  </svg>
</div>

<div class="footer">
  <a href="identity.html">정체성</a>
  <a href="humility.html">겸손</a>
  <a href="docs/JUSTIFICATION-REPORT.md">정당성</a>
  <a href="docs/AI-MISSIONARY-PLUGIN-WHITEPAPER.md">미셔너</a>
  <a href="archive.html">Archive</a>
  <a href="map.html">Map</a>
  <a href="https://github.com/dtslib1979/OrbitPrompt">GitHub</a>
</div>

<script>
const GOLD='#EEC864', PUR='#a855f7', CYAN='#22d3ee', GRN='#4ade80', WHT='#fff';
const GLOW={gold:'url(#glow)',pur:'url(#glow)',cyan:'url(#glow)',grn:'url(#glow)',arch:null};

// ── DATA ──
const HUBS = [
  {id:'phi', label:'철학',    color:GOLD, glow:GLOW.gold},
  {id:'mod', label:'모듈',    color:PUR,  glow:GLOW.pur},
  {id:'mcp', label:'MCP',    color:CYAN, glow:GLOW.cyan},
  {id:'gen', label:'생성기',  color:GRN,  glow:GLOW.grn},
  {id:'arch',label:'아카이브',color:WHT,  glow:null},
];

const LEAVES = [
  // 철학
  {hub:'phi', label:'WHY',     sub:'존재 이유',    href:'why.html',           color:GOLD},
  {hub:'phi', label:'백서',     sub:'Whitepaper',   href:'whitepaper.html',    color:GOLD},
  {hub:'phi', label:'7축 철학', sub:'Φ7',           href:'philosophy.html',    color:GOLD},
  {hub:'phi', label:'휴머니티', sub:'5 Fingers',    href:'humanity-finger.html',color:GOLD},
  // 모듈
  {hub:'mod', label:'축구 모델', sub:'98pts',       href:'football-model/index.html',            color:PUR},
  {hub:'mod', label:'WC2026',   sub:'예측기',      href:'football-model/wc2026-predictor.html', color:PUR},
  {hub:'mod', label:'선거 MCP', sub:'100pts',      href:'boards/election-gallery.html',         color:PUR},
  {hub:'mod', label:'달러 시스템',sub:'DSI',        href:'boards/dollar-system-whitepaper.html', color:PUR},
  // MCP
  {hub:'mcp', label:'정치 MCP',  sub:'parksy-pol',  href:'political-mcp/index.html',        color:CYAN},
  {hub:'mcp', label:'금융 MCP',  sub:'parksy-fin',  href:'parksy-finance-mcp/index.html',   color:CYAN},
  {hub:'mcp', label:'달러 MCP',  sub:'parksy-dollar',href:'dollar-system-mcp/WHITEPAPER.md',color:CYAN},
  {hub:'mcp', label:'교육 MCP',  sub:'edu',         href:'edu-mcp/mcp/server.py',           color:CYAN},
  {hub:'mcp', label:'Media MCP', sub:'v2.0',        href:'media-mcp/mcp/server.py',         color:CYAN},
  // 생성기
  {hub:'gen', label:'칠판',     sub:'Chalkboard',   href:'prompts/chalkboard/index.html',              color:GRN},
  {hub:'gen', label:'Identity', sub:'Engine',       href:'prompts/identity/index.html',                color:GRN},
  {hub:'gen', label:'Broadcast',sub:'방송',         href:'prompts/broadcast/parksy-brain-season.html', color:GRN},
  {hub:'gen', label:'PWA',      sub:'Generator',    href:'prompts/apk/index.html',                     color:GRN},
  // 아카이브
  {hub:'arch',label:'Archive',  sub:'전체 작업물',  href:'archive.html',  color:WHT},
  {hub:'arch',label:'Map',      sub:'레포 지도',    href:'map.html',      color:WHT},
  {hub:'arch',label:'Links',    sub:'외부링크',    href:'links/index.html',color:WHT},
  {hub:'arch',label:'정당성',   sub:'Justification',href:'docs/JUSTIFICATION-REPORT.md', color:WHT},
  {hub:'arch',label:'미셔너',   sub:'AI Missionary',href:'docs/AI-MISSIONARY-PLUGIN-WHITEPAPER.md',color:WHT},
];

// ── 3D ORBIT COORDINATES ──
// 각 리프 노드를 허브 주변 궤도에 3D 회전 배치
function orbitPos(hubAngle, hubDist, leafIndex, totalLeaves, orbitTilt) {
  const angle = (leafIndex / totalLeaves) * Math.PI * 2 + hubAngle;
  const x = Math.cos(angle) * hubDist;
  const y = Math.sin(angle) * hubDist * Math.cos(orbitTilt);
  return {x, y};
}

const HUBS_3D = [
  {id:'phi',   x:-280, y:-150, label:'철학',    color:GOLD},
  {id:'mod',   x:320,  y:-100, label:'모듈',    color:PUR},
  {id:'mcp',   x:280,  y:170,  label:'MCP',    color:CYAN},
  {id:'gen',   x:-300, y:180,  label:'생성기',  color:GRN},
  {id:'arch',  x:-400, y:40,   label:'아카이브',color:WHT},
];

// 각 허브별 리프 노드들 궤도 좌표 계산
const hubsById = {};
HUBS.forEach(h => hubsById[h.id] = h);

const NODES = [];
const EDGES = [];

HUBS_3D.forEach(hub => {
  const leaves = LEAVES.filter(l => l.hub === hub.id);
  const glowRad = 80;
  
  // Center dot glow
  NODES.push({type:'hubGlow', x:hub.x, y:hub.y, r:glowRad, color:hub.color});
  // Hub center
  NODES.push({type:'hub', x:hub.x, y:hub.y, r:6, color:hub.color, label:hub.label});
  
  leaves.forEach((leaf, i) => {
    const total = leaves.length;
    const angle = (i / total) * Math.PI * 2 - Math.PI/2 + (hub.id === 'phi' ? 0.3 : hub.id === 'mod' ? 0.5 : hub.id === 'mcp' ? 0.7 : hub.id === 'gen' ? 0.2 : 0.4);
    const dist = 45 + (i % 3) * 12;
    const lx = hub.x + Math.cos(angle) * dist;
    const ly = hub.y + Math.sin(angle) * dist * 0.7;
    
    NODES.push({type:'leaf', x:lx, y:ly, r:3, color:leaf.color, label:leaf.label, href:leaf.href, hubId:hub.id});
    EDGES.push({x1:hub.x, y1:hub.y, x2:lx, y2:ly, color:leaf.color, hubId:hub.id});
  });
  
  // Inter-hub edges
  HUBS_3D.forEach(other => {
    if (hub.id < other.id) {
      EDGES.push({x1:hub.x, y1:hub.y, x2:other.x, y2:other.y, color:'rgba(255,255,255,.03)', hubId:'all'});
    }
  });
});

// ── RENDER ──
const svg = document.getElementById('graphSvg');
const NS = 'http://www.w3.org/2000/svg';

function el(tag, attrs) {
  const e = document.createElementNS(NS, tag);
  for (const [k, v] of Object.entries(attrs || {})) e.setAttribute(k, v);
  return e;
}

// Edges
EDGES.forEach(edge => {
  const line = el('line', {
    x1:edge.x1, y1:edge.y1, x2:edge.x2, y2:edge.y2,
    class:edge+' edge-'+edge.hubId, stroke:edge.color || 'rgba(255,255,255,.03)'
  });
  svg.appendChild(line);
});

// Hover edge highlighter class
function highlightEdges(hubId) {
  document.querySelectorAll('.edge').forEach(e => e.classList.remove('highlight'));
  document.querySelectorAll(`.edge-${hubId}`).forEach(e => e.classList.add('highlight'));
}

// Nodes
NODES.forEach(node => {
  if (node.type === 'hubGlow') {
    const g = el('circle', {cx:node.x, cy:node.y, r:node.r, fill:'none', stroke:node.color, 'stroke-width':.5, opacity:.12});
    svg.appendChild(g);
    return;
  }
  
  if (node.type === 'hub') {
    const g = document.createElementNS(NS, 'g');
    g.setAttribute('class', `node-group hub-group-${node.label}`);
    
    const dot = el('circle', {cx:node.x, cy:node.y, r:node.r, class:'node-dot', fill:node.color, filter:'url(#glow)', opacity:.8});
    g.appendChild(dot);
    
    // Ring
    const ring = el('circle', {cx:node.x, cy:node.y, r:node.r+6, fill:'none', stroke:node.color, 'stroke-width':.5, opacity:.2});
    g.appendChild(ring);
    
    // Label
    const txt = el('text', {x:node.x, y:node.y+18, class:'hub-label', fill:node.color});
    txt.textContent = node.label;
    g.appendChild(txt);
    
    g.addEventListener('mouseenter', () => {
      document.querySelectorAll(`.edge`).forEach(e => e.style.opacity = '.06');
      document.querySelectorAll(`.edge-${node.label}`).forEach(e => e.style.opacity = '.5');
    });
    g.addEventListener('mouseleave', () => {
      document.querySelectorAll(`.edge`).forEach(e => e.style.opacity = '');
    });
    
    svg.appendChild(g);
    return;
  }
  
  if (node.type === 'leaf') {
    const a = document.createElementNS(NS, 'a');
    a.setAttributeNS('http://www.w3.org/1999/xlink', 'href', node.href);
    a.setAttribute('href', node.href);
    a.setAttribute('class', `node-group edge-${node.hubId}`);
    
    const dot = el('circle', {cx:node.x, cy:node.y, r:node.r, class:'node-dot', fill:node.color, opacity:.5});
    a.appendChild(dot);
    
    const label = el('text', {x:node.x, y:node.y+12, class:'node-label', fill:node.color});
    label.textContent = node.label;
    a.appendChild(label);
    
    svg.appendChild(a);
  }
});

// Center label (OrbitPrompt)
const center = el('text', {x:0, y:0, class:'center-label'});
center.textContent = 'OrbitPrompt';
svg.appendChild(center);

// ── DRAG TO ROTATE (simplified 2D transform) ──
let isDragging = false, startX, startY, angleX = 0, angleY = 0;
const wrap = document.getElementById('graphWrap');

wrap.addEventListener('mousedown', e => {
  isDragging = true; startX = e.clientX; startY = e.clientY;
});
window.addEventListener('mousemove', e => {
  if (!isDragging) return;
  const dx = e.clientX - startX, dy = e.clientY - startY;
  angleX += dy * 0.003; angleY += dx * 0.003;
  svg.style.transform = `rotateX(${angleX}rad) rotateY(${angleY}rad)`;
  startX = e.clientX; startY = e.clientY;
});
window.addEventListener('mouseup', () => { isDragging = false; });

// ── ANIMATED PULSE ──
let pulse = 0;
setInterval(() => {
  pulse = (pulse + 0.02) % (Math.PI * 2);
  const hubs = document.querySelectorAll('.hub-group-철학, .hub-group-모듈, .hub-group-MCP, .hub-group-생성기, .hub-group-아카이브');
  hubs.forEach((g, i) => {
    const dot = g.querySelector('circle');
    if (dot) {
      const phase = 1 + Math.sin(pulse + i * 0.8) * 0.15;
      dot.setAttribute('r', (phase * 6).toString());
    }
  });
}, 50);

console.log('✅ OrbitPrompt Graph — Obsidian-style');
</script>
</body>
</html>
