/**
 * lib/generator.js
 *
 * Generate a complete Thought Module directory from an extracted thread.
 *
 * Creates:
 *   {module-name}/index.html      ← Interactive calculator/explorer PWA
 *   {module-name}/whitepaper.html ← Full whitepaper
 *   {module-name}/calculator.js   ← Model logic (if applicable)
 */

import { mkdir, writeFile, readFile } from 'fs/promises';
import { join, dirname } from 'path';

const MODULE_TEMPLATES_DIR = new URL('../templates/', import.meta.url).pathname;

/**
 * Generate a safe directory slug from a title
 */
function slugify(title) {
  return title
    .toLowerCase()
    .replace(/[^a-z0-9가-힣]/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '')
    .slice(0, 40);
}

/**
 * Determine model type from content analysis
 */
function detectModelType(content, domains) {
  if (domains.includes('축구') || content.match(/축구|football|경기력|협회|선수|감독|전술|전략/i)) {
    return 'interactive-calculator';
  }
  if (content.match(/철학|7축|8축|ontology|존재|인식/i)) {
    return 'visual-explorer';
  }
  if (content.match(/금융|finance|투자|경제|ERP/i)) {
    return 'dashboard';
  }
  if (content.match(/음악|music|작곡|화성|BGM|가창/i)) {
    return 'player';
  }
  return 'article';
}

/**
 * Generate the index.html (landing/calculator page)
 */
async function generateIndexHtml(moduleData) {
  const { title, description, domains, score, modelType } = moduleData;

  return `<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title} — Thought Module ${moduleData.number}</title>
  <meta name="description" content="${description}">
  <meta name="theme-color" content="#050505">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #050505; --surface: #0a0a0f; --card: #0f0f15;
      --border: rgba(255,255,255,0.07); --text: #e8e8f0;
      --muted: rgba(255,255,255,0.5); --dim: rgba(255,255,255,0.12);
      --accent: #a855f7; --cyan: #22d3ee; --gold: #d4af37;
      --f-sans: 'Inter', -apple-system, sans-serif;
      --f-mono: 'JetBrains Mono', monospace;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: var(--f-sans); background: var(--bg); color: var(--text); min-height: 100vh; }
    nav { position:fixed; top:0; left:0; right:0; z-index:100; background:rgba(5,5,5,0.92); backdrop-filter:blur(12px); border-bottom:1px solid var(--border); padding:0 2rem; height:52px; display:flex; align-items:center; justify-content:space-between; }
    .nav-brand { font-size:.85rem; font-weight:600; color:var(--accent); letter-spacing:.05em; text-decoration:none; }
    .nav-links { display:flex; gap:1.5rem; list-style:none; }
    .nav-links a { color:var(--muted); font-size:.82rem; text-decoration:none; transition:color .2s; }
    .nav-links a:hover { color:var(--text); }
    .container { max-width:800px; margin:0 auto; padding:80px 1.5rem 100px; }
    .hero { text-align:center; padding:30px 0 40px; border-bottom:1px solid var(--border); margin-bottom:40px; }
    .hero-badge { display:inline-block; font-size:0.65rem; letter-spacing:0.15em; text-transform:uppercase; color:var(--accent); border:1px solid var(--accent); padding:0.2rem 0.7rem; border-radius:2rem; margin-bottom:1rem; }
    .hero h1 { font-size:clamp(1.4rem,4vw,2.2rem); font-weight:700; letter-spacing:-0.02em; margin-bottom:0.6rem; }
    .hero h1 em { color:var(--accent); font-style:normal; }
    .hero p { color:var(--muted); font-size:0.92rem; line-height:1.6; max-width:600px; margin:0 auto; }
    .hero-score { font-family:var(--f-mono); font-size:0.8rem; color:var(--gold); margin-top:1rem; }
    .section { margin-bottom:2rem; }
    .section h2 { font-size:1.1rem; font-weight:600; margin-bottom:0.8rem; color:var(--accent); }
    .section p { font-size:0.9rem; color:var(--muted); line-height:1.7; margin-bottom:0.8rem; }
    .placeholder { text-align:center; padding:60px 20px; color:var(--muted); font-size:0.9rem; border:1px dashed var(--border); border-radius:0.5rem; margin:2rem 0; }
    .btn-primary { display:inline-block; background:var(--accent); color:#fff; text-decoration:none; padding:0.6rem 1.4rem; border-radius:0.4rem; font-size:0.85rem; font-weight:600; transition:opacity .2s; }
    .btn-primary:hover { opacity:.85; }
    .btn-secondary { display:inline-block; border:1px solid var(--border); color:var(--text); text-decoration:none; padding:0.6rem 1.4rem; border-radius:0.4rem; font-size:0.85rem; font-weight:500; transition:border-color .2s; }
    .btn-secondary:hover { border-color:var(--accent); }
    .links-row { display:flex; gap:0.8rem; justify-content:center; margin-top:2rem; flex-wrap:wrap; }
    @media (max-width:600px) { .container { padding:70px 1rem 60px; } }
  </style>
</head>
<body>
<nav>
  <a class="nav-brand" href="../index.html">OrbitPrompt</a>
  <ul class="nav-links">
    <li><a href="../index.html">홈</a></li>
    <li><a href="../index.html#gallery">갤러리</a></li>
  </ul>
</nav>
<div class="container">
  <div class="hero">
    <div class="hero-badge">Thought Module ${moduleData.number} · ${modelType === 'interactive-calculator' ? 'Interactive Model' : modelType === 'visual-explorer' ? 'Visual Explorer' : 'Article'}</div>
    <h1><em>${title}</em></h1>
    <p>${description}</p>
    <div class="hero-score">${score ? '모델 점수: ' + score + '/100' : 'ParksyLog에서 추출한 사고 모듈'}</div>
    <div style="margin-top:1.2rem;">
      <a href="whitepaper.html" class="btn-secondary">📄 백서 읽기 →</a>
    </div>
  </div>
  <div class="placeholder">
    <p>🧪 이 모듈은 mcp-parksy-module-gallery에 의해 생성되었습니다.</p>
    <p style="font-size:0.8rem;margin-top:0.5rem;">${moduleData.source || 'ParksyLog 자동 추출'}</p>
  </div>
  <div class="section">
    <h2>모듈 정보</h2>
    <p><strong>도메인:</strong> ${domains.join(', ')}</p>
    <p><strong>생성일:</strong> ${new Date().toISOString().split('T')[0]}</p>
    <p><strong>출처:</strong> ${moduleData.source || 'ParksyLog'}</p>
    ${score ? '<p><strong>모델 점수:</strong> ' + score + '/100</p>' : ''}
  </div>
  <div class="links-row">
    <a href="../index.html" class="btn-secondary">← OrbitPrompt 홈</a>
  </div>
</div>
</body>
</html>`;
}

/**
 * Generate the whitepaper.html (markdown → styled HTML)
 */
async function generateWhitepaperHtml(moduleData, rawContent) {
  const { title, description, domains, score, scoreBreakdown } = moduleData;

  const sections = rawContent
    ? rawContent.split('\n## ').filter(Boolean).map(s => {
        const lines = s.split('\n');
        const heading = lines[0].replace(/^#+\s*/, '');
        const body = lines.slice(1).join('\n').trim();
        return { heading, body };
      }).filter(s => s.body.length > 50)
    : [];

  return `<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title} — 백서</title>
  <meta name="description" content="${description}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root { --bg:#050505; --surface:#0a0a0a; --card:#0f0f0f; --border:rgba(255,255,255,0.06); --text:#f0f0f0; --muted:rgba(255,255,255,0.55); --dim:rgba(255,255,255,0.15); --accent:#a855f7; --cyan:#22d3ee; --gold:#d4af37; --f-sans:'Inter',-apple-system,sans-serif; --f-mono:'JetBrains Mono',monospace; }
    * { margin:0; padding:0; box-sizing:border-box; }
    body { font-family:var(--f-sans); background:var(--bg); color:var(--text); line-height:1.8; }
    nav { position:fixed; top:0; left:0; right:0; z-index:100; background:rgba(5,5,5,0.92); backdrop-filter:blur(12px); border-bottom:1px solid var(--border); padding:0 2rem; height:52px; display:flex; align-items:center; justify-content:space-between; }
    .nav-brand { font-size:.85rem; font-weight:600; color:var(--accent); letter-spacing:.05em; text-decoration:none; }
    .nav-links { display:flex; gap:1.5rem; list-style:none; }
    .nav-links a { color:var(--muted); font-size:.82rem; text-decoration:none; transition:color .2s; }
    .nav-links a:hover { color:var(--text); }
    .container { max-width:800px; margin:0 auto; padding:80px 2rem 120px; }
    .wp-hero { text-align:center; padding:40px 0 50px; border-bottom:1px solid var(--border); margin-bottom:50px; }
    .wp-label { font-family:var(--f-mono); font-size:0.65rem; letter-spacing:0.2em; text-transform:uppercase; color:var(--accent); margin-bottom:1.2rem; }
    .wp-hero h1 { font-size:clamp(1.6rem,4vw,2.4rem); font-weight:700; letter-spacing:-0.02em; margin-bottom:0.8rem; }
    .wp-hero .subtitle { font-size:0.95rem; color:var(--muted); margin-bottom:1rem; }
    .wp-score { display:inline-block; background:var(--gold); color:#000; font-size:0.7rem; font-weight:700; padding:0.2rem 0.7rem; border-radius:2rem; font-family:var(--f-mono); }
    .section { margin-bottom:3rem; }
    .section h2 { font-size:1.3rem; font-weight:600; margin-bottom:1rem; padding-bottom:0.4rem; border-bottom:1px solid var(--border); color:var(--gold); }
    .section h3 { font-size:1rem; font-weight:600; margin:1.2rem 0 0.5rem; color:var(--accent); }
    .section p { font-size:0.92rem; color:var(--muted); margin-bottom:0.8rem; }
    .section p strong { color:var(--text); }
    .info-box { background:var(--card); border:1px solid var(--border); border-radius:0.5rem; padding:1.2rem; margin:1rem 0; }
    .back-link { display:inline-block; margin-top:2rem; font-size:0.85rem; color:var(--accent); text-decoration:none; }
    .back-link:hover { text-decoration:underline; }
    @media (max-width:600px) { .container { padding:70px 1.2rem 80px; } }
  </style>
</head>
<body>
<nav>
  <a class="nav-brand" href="../index.html">OrbitPrompt</a>
  <ul class="nav-links">
    <li><a href="../index.html">홈</a></li>
    <li><a href="index.html">모듈</a></li>
  </ul>
</nav>
<div class="container">
  <div class="wp-hero">
    <div class="wp-label">Thought Module ${moduleData.number} · Whitepaper</div>
    <h1>${title}</h1>
    <div class="subtitle">${description}</div>
    ${score ? '<div><span class="wp-score">' + score + ' / 100</span></div>' : ''}
  </div>

  ${sections.length > 0 ? sections.map(s => '<section class="section"><h2>' + s.heading + '</h2><p>' + s.body.replace(/\n/g, '</p><p>') + '</p></section>').join('\n') : `
  <section class="section">
    <h2>모듈 개요</h2>
    <p>이 백서는 <strong>${title}</strong>에 관한 철학적 사고에서 수학적 모델링, 인터랙티브 앱으로의 출판 과정을 기록합니다.</p>
    <p><strong>도메인:</strong> ${domains.join(', ')}</p>
    <p>자세한 내용은 대화 로그 원본을 참조하세요.</p>
  </section>
  <section class="section">
    <h2>출처</h2>
    <p>이 모듈은 ${moduleData.source || 'ParksyLog 대화 로그'}에서 자동 추출되었습니다.</p>
  </section>
  ${score && scoreBreakdown ? '<section class="section"><h2>모델 평가</h2>' + Object.entries(scoreBreakdown).map(([k, v]) => '<div class="info-box"><strong>' + k + ':</strong> ' + v + '/20</div>').join('') + '</section>' : ''}
  `}

  <a href="index.html" class="back-link">← 모듈 홈으로 돌아가기</a>
</div>
</body>
</html>`;
}

/**
 * Generate a basic calculator.js (model scaffold)
 */
function generateCalculatorJs(moduleData) {
  const { title } = moduleData;
  return `/**
 * ${title} — Model Calculator
 * Auto-generated by mcp-parksy-module-gallery
 *
 * Edit this file to implement your interactive model logic.
 */

(function() {
  'use strict';

  // ── DOM refs ──────────────────────────────────────────────
  // (Replace with your actual slider/input selectors)

  // ── Model parameters ──────────────────────────────────────
  // Define your model's variables here

  // ── Core functions ────────────────────────────────────────
  // Implement your model logic

  // ── Rendering ─────────────────────────────────────────────
  function render() {
    // Update output displays
  }

  // ── Initialize ────────────────────────────────────────────
  document.addEventListener('DOMContentLoaded', () => {
    render();
  });

})();
`;
}

/**
 * Generate a complete module directory
 */
export async function generateModule(moduleData, rawContent = '', outputBaseDir) {
  const slug = slugify(moduleData.title);
  const moduleDir = join(outputBaseDir, slug);

  await mkdir(moduleDir, { recursive: true });

  const modelType = moduleData.modelType || detectModelType(rawContent || '', moduleData.domains || []);

  const enriched = {
    ...moduleData,
    modelType,
    number: moduleData.number || '??',
    source: moduleData.source || 'ParksyLog 자동 추출'
  };

  // Generate files
  const indexHtml = await generateIndexHtml(enriched);
  await writeFile(join(moduleDir, 'index.html'), indexHtml, 'utf-8');

  const whitepaperHtml = await generateWhitepaperHtml(enriched, rawContent);
  await writeFile(join(moduleDir, 'whitepaper.html'), whitepaperHtml, 'utf-8');

  const calculatorJs = generateCalculatorJs(enriched);
  await writeFile(join(moduleDir, 'calculator.js'), calculatorJs, 'utf-8');

  return {
    slug,
    path: slug,
    fullPath: moduleDir,
    files: ['index.html', 'whitepaper.html', 'calculator.js'],
    number: enriched.number
  };
}
