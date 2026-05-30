/**
 * football-model/calculator.js
 * Φ-I-C-K-P 프레임워크 인터랙티브 계산기
 * 철학·인프라·컨텍스트→경기력 실시간 시뮬레이션
 */
(function() {
  'use strict';

  // ── DOM refs ──────────────────────────────────────────────
  const $ = id => document.getElementById(id);

  // Φ sliders
  const sA = $('slider-a'), sB = $('slider-b'), sC = $('slider-c');
  const vA = $('val-a'), vB = $('val-b'), vC = $('val-c');

  // I sliders
  const sIa = $('slider-ia'), sIb = $('slider-ib'), sIc = $('slider-ic');
  const vIa = $('val-ia'), vIb = $('val-ib'), vIc = $('val-ic');

  // C sliders
  const sCn = $('slider-cn'), sCj = $('slider-cj'), sCd = $('slider-cd');
  const vCn = $('val-cn'), vCj = $('val-cj'), vCd = $('val-cd');

  // S, λ, α
  const sS = $('slider-s'), sL = $('slider-lam'), sAphi = $('slider-aphi'), sAi = $('slider-ai');
  const vS = $('val-s'), vL = $('val-lam'), vAphi = $('val-aphi'), vAi = $('val-ai');

  // Outputs
  const outSync = $('out-sync');
  const outKbar = $('out-kbar');
  const outPerf = $('out-perf');
  const outTheta = $('out-theta');

  // Preset
  const presetSelect = $('preset-select');

  // ── State ─────────────────────────────────────────────────
  let animFrame = null;

  // ── Presets ───────────────────────────────────────────────
  const PRESETS = {
    germany: {
      label: '🇩🇪 독일',
      phi: [0.50, 0.20, 0.30],
      inf: [0.85, 0.40, 0.60],
      ctx: [0.30, 0.15, 0.85],
      s: 0.3, lam: 0.4, aphi: 0.15, ai: 0.10
    },
    spain: {
      label: '🇪🇸 스페인',
      phi: [0.15, 0.25, 0.60],
      inf: [0.40, 0.50, 0.90],
      ctx: [0.25, 0.10, 0.90],
      s: 0.4, lam: 0.6, aphi: 0.12, ai: 0.15
    },
    brazil: {
      label: '🇧🇷 브라질',
      phi: [0.10, 0.65, 0.25],
      inf: [0.30, 0.85, 0.50],
      ctx: [0.40, 0.20, 0.60],
      s: 0.7, lam: 0.8, aphi: 0.10, ai: 0.08
    },
    argentina: {
      label: '🇦🇷 아르헨티나',
      phi: [0.20, 0.55, 0.25],
      inf: [0.45, 0.75, 0.50],
      ctx: [0.50, 0.25, 0.55],
      s: 0.9, lam: 1.0, aphi: 0.10, ai: 0.08
    },
    korea: {
      label: '🇰🇷 한국',
      phi: [0.55, 0.15, 0.30],
      inf: [0.55, 0.25, 0.40],
      ctx: [0.70, 0.60, 0.50],
      s: 0.2, lam: 0.3, aphi: 0.20, ai: 0.12
    }
  };

  // ── Core model functions ──────────────────────────────────
  function norm(v) {
    return Math.sqrt(v.reduce((s, x) => s + x*x, 0));
  }

  function dot(a, b) {
    return a.reduce((s, x, i) => s + x * b[i], 0);
  }

  function sigmoid(x) {
    return 1 / (1 + Math.exp(-x));
  }

  function computeSync(phi, inf) {
    const d = dot(phi, inf);
    const n = norm(phi);
    return n > 0 ? d / n : 0;
  }

  function computeTheta(ctx) {
    const wC = [1.0, 0.8, -0.7]; // nationalism+, chaebol+, democracy-
    const b = 0.3;
    return sigmoid(dot(wC, ctx) - b);
  }

  function computeKbar(phi, ctx) {
    // θ(C_H)가 높을수록(통제 강함) K는 Φ에 가까워짐
    // θ(C_H)가 낮을수록(자율성 높음) K는 다양해질 수 있음
    // 평균적으로 K는 Φ 주변에 분포한다고 가정 (중심값)
    const th = computeTheta(ctx);
    // K 평균 ≈ Φ * (1 + noise), where noise ∝ (1-θ)
    const noise = (1 - th) * 0.15;
    const k = [
      Math.max(0, phi[0] + (Math.random() - 0.5) * noise * 2),
      Math.max(0, phi[1] + (Math.random() - 0.5) * noise * 2),
      Math.max(0, phi[2] + (Math.random() - 0.5) * noise * 2)
    ];
    const sum = k[0] + k[1] + k[2];
    if (sum > 0) { k[0] /= sum; k[1] /= sum; k[2] /= sum; }
    // 철학 순응도 = Φ · K (정규화된 K이므로 내적)
    return dot(phi, k);
  }

  function computePerformance(phi, inf, ctx, s, lam) {
    const sync = computeSync(phi, inf);
    // K̄: 여러 샘플 평균 (Monte Carlo)
    const N = 50;
    let kSum = 0;
    for (let i = 0; i < N; i++) {
      kSum += computeKbar(phi, ctx);
    }
    const kbar = kSum / N;
    const perf = sync * kbar * (1 + lam * s);
    return { sync, kbar, perf, theta: computeTheta(ctx) };
  }

  // ── Simplex projection ────────────────────────────────────
  function projectSimplex(v) {
    // proj_{Δ²}(v): a+b+c=1, 각 ≥0
    // 알고리즘: excess를 균등 분배
    let u = v.slice();
    const n = u.length;
    for (let iter = 0; iter < 100; iter++) {
      const sum = u.reduce((s, x) => s + x, 0);
      const diff = sum - 1;
      if (Math.abs(diff) < 1e-12) break;
      const excess = diff / n;
      let anyNegative = false;
      for (let i = 0; i < n; i++) {
        u[i] -= excess;
        if (u[i] < 0) { u[i] = 0; anyNegative = true; }
      }
      if (!anyNegative) break;
    }
    // Normalize to sum=1 exactly
    const sum = u.reduce((s, x) => s + x, 0);
    if (sum > 0) { u[0] /= sum; u[1] /= sum; u[2] /= sum; }
    return u;
  }

  // ── Get values from sliders ──────────────────────────────
  function getValues() {
    return {
      phi: [parseFloat(sA.value), parseFloat(sB.value), parseFloat(sC.value)],
      inf: [parseFloat(sIa.value), parseFloat(sIb.value), parseFloat(sIc.value)],
      ctx: [parseFloat(sCn.value), parseFloat(sCj.value), parseFloat(sCd.value)],
      s: parseFloat(sS.value),
      lam: parseFloat(sL.value),
      aphi: parseFloat(sAphi.value),
      ai: parseFloat(sAi.value)
    };
  }

  // ── Update Φ sliders (with normalization) ─────────────────
  function normalizePhi(changed) {
    let a = parseFloat(sA.value);
    let b = parseFloat(sB.value);
    let c = parseFloat(sC.value);
    const sum = a + b + c;
    if (sum === 0) { a = 1/3; b = 1/3; c = 1/3; }
    else if (Math.abs(sum - 1) > 0.001) {
      a /= sum; b /= sum; c /= sum;
    }
    sA.value = a; sB.value = b; sC.value = c;
    vA.textContent = a.toFixed(3);
    vB.textContent = b.toFixed(3);
    vC.textContent = c.toFixed(3);
  }

  // ── Render ────────────────────────────────────────────────
  function render() {
    const { phi, inf, ctx, s, lam } = getValues();
    const result = computePerformance(phi, inf, ctx, s, lam);

    outSync.textContent = result.sync.toFixed(4);
    outKbar.textContent = result.kbar.toFixed(4);
    outPerf.textContent = result.perf.toFixed(4);
    outTheta.textContent = result.theta.toFixed(4);

    // Update bar visualizations
    const barSync = document.getElementById('bar-sync');
    const barKbar = document.getElementById('bar-kbar');
    const barPerf = document.getElementById('bar-perf');
    const barTheta = document.getElementById('bar-theta');
    if (barSync) barSync.style.width = (result.sync * 100) + '%';
    if (barKbar) barKbar.style.width = (result.kbar * 100) + '%';
    if (barPerf) barPerf.style.width = Math.min(100, result.perf * 100) + '%';
    if (barTheta) barTheta.style.width = (result.theta * 100) + '%';
  }

  // ── Dynamic simulation ────────────────────────────────────
  let simRunning = false;

  function runSimulation() {
    if (simRunning) return;
    simRunning = true;
    const btn = $('sim-btn');
    if (btn) btn.textContent = '⏳ 시뮬레이션 중...';

    const canvas = document.getElementById('sim-canvas');
    if (!canvas) { simRunning = false; return; }
    const ctx = canvas.getContext('2d');
    const W = canvas.width, H = canvas.height;
    const pad = 40;
    const graphW = W - pad * 2, graphH = H - pad * 2;

    let { phi, inf, ctx:c, s, lam, aphi, ai } = getValues();
    const history = [];
    const steps = 30;

    // Run simulation
    for (let n = 0; n < steps; n++) {
      const { sync, kbar, perf } = computePerformance(phi, inf, c, s, lam);
      history.push({ phi: phi.slice(), inf: inf.slice(), sync, kbar, perf });

      // Gradient: P wrt phi (numerical approximation)
      const delta = 0.01;
      const baseP = perf;
      const gradPhi = phi.map((_, i) => {
        const phiUp = phi.slice(); phiUp[i] += delta;
        const pUp = computePerformance(phiUp, inf, c, s, lam).perf;
        return (pUp - baseP) / delta;
      });
      // Update phi with projection
      const phiNew = phi.map((v, i) => v + aphi * gradPhi[i]);
      phi = projectSimplex(phiNew);

      // Gradient: I wrt P (infrastructure investment based on performance)
      const baseInfP = perf;
      const gradI = inf.map((_, i) => {
        const iUp = inf.slice(); iUp[i] += delta;
        const pUp = computePerformance(phi, iUp, c, s, lam).perf;
        // Only if already invested (diminishing returns)
        return (pUp - baseInfP) / delta * (1 - inf[i]);
      });
      const infNew = inf.map((v, i) => v + ai * gradI[i]);
      inf = infNew.map(v => Math.min(1, Math.max(0, v)));
    }

    // Draw graph
    ctx.clearRect(0, 0, W, H);
    ctx.fillStyle = '#1a1a2e';
    ctx.fillRect(0, 0, W, H);

    // Grid
    ctx.strokeStyle = 'rgba(255,255,255,0.06)';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 5; i++) {
      const y = pad + graphH * (1 - i / 5);
      ctx.beginPath(); ctx.moveTo(pad, y); ctx.lineTo(pad + graphW, y);
      ctx.stroke();
    }

    // Labels
    ctx.fillStyle = 'rgba(255,255,255,0.3)';
    ctx.font = '10px monospace';
    for (let i = 0; i <= 5; i++) {
      const y = pad + graphH * (1 - i / 5);
      ctx.fillText((i / 5).toFixed(1), 4, y + 3);
    }

    // Plot lines
    const colors = {
      sync: '#a855f7',
      perf: '#facc15',
      kbar: '#22d3ee',
      phi_a: '#f97316',
      phi_b: '#10b981',
      phi_c: '#ec4899'
    };

    function plot(data, values, color, label) {
      ctx.strokeStyle = color;
      ctx.lineWidth = 2;
      ctx.beginPath();
      data.forEach((d, i) => {
        const x = pad + (i / (steps - 1)) * graphW;
        const y = pad + graphH * (1 - (values ? values[i] : d));
        i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
      });
      ctx.stroke();
    }

    // Performance & Sync
    const pData = history.map(d => d.perf);
    const sData = history.map(d => d.sync);
    const kData = history.map(d => d.kbar);
    // Normalize for display
    const maxVal = Math.max(...pData, ...sData, ...kData, 0.5);
    plot(history.map((d, i) => ({ val: d.perf / maxVal })), pData.map(v => v / maxVal), colors.perf, 'P 성능');
    plot(history.map((d, i) => ({ val: d.sync / maxVal })), sData.map(v => v / maxVal), colors.sync, 'Sync');
    plot(history.map((d, i) => ({ val: d.kbar / maxVal })), kData.map(v => v / maxVal), colors.kbar, 'K̄');

    // Legend
    ctx.font = '11px sans-serif';
    const legend = [
      { label: 'P 성능', color: colors.perf },
      { label: 'Sync', color: colors.sync },
      { label: 'K̄', color: colors.kbar }
    ];
    legend.forEach((l, i) => {
      const x = pad + 10 + i * 100;
      const y = pad + 15;
      ctx.fillStyle = l.color;
      ctx.fillRect(x, y - 5, 12, 3);
      ctx.fillStyle = 'rgba(255,255,255,0.6)';
      ctx.fillText(l.label, x + 16, y + 1);
    });

    ctx.fillStyle = 'rgba(255,255,255,0.2)';
    ctx.font = '9px monospace';
    ctx.fillText('시즌 →', W - pad - 50, H - pad + 15);

    simRunning = false;
    if (btn) btn.textContent = '▶ 시뮬레이션 실행';
    render();
  }

  // ── Preset loader ──────────────────────────────────────────
  function loadPreset(key) {
    const p = PRESETS[key];
    if (!p) return;

    const sum = p.phi[0] + p.phi[1] + p.phi[2];
    sA.value = p.phi[0] / sum; sB.value = p.phi[1] / sum; sC.value = p.phi[2] / sum;
    vA.textContent = (p.phi[0] / sum).toFixed(3);
    vB.textContent = (p.phi[1] / sum).toFixed(3);
    vC.textContent = (p.phi[2] / sum).toFixed(3);

    sIa.value = p.inf[0]; sIb.value = p.inf[1]; sIc.value = p.inf[2];
    vIa.textContent = p.inf[0].toFixed(2); vIb.textContent = p.inf[1].toFixed(2); vIc.textContent = p.inf[2].toFixed(2);

    sCn.value = p.ctx[0]; sCj.value = p.ctx[1]; sCd.value = p.ctx[2];
    vCn.textContent = p.ctx[0].toFixed(2); vCj.textContent = p.ctx[1].toFixed(2); vCd.textContent = p.ctx[2].toFixed(2);

    sS.value = p.s; vS.textContent = p.s.toFixed(1);
    sL.value = p.lam; vL.textContent = p.lam.toFixed(1);
    sAphi.value = p.aphi; vAphi.textContent = p.aphi.toFixed(2);
    sAi.value = p.ai; vAi.textContent = p.ai.toFixed(2);

    render();
  }

  // ── Event binding ─────────────────────────────────────────
  function init() {
    // Φ sliders with normalization
    sA.addEventListener('input', () => { normalizePhi('a'); render(); });
    sB.addEventListener('input', () => { normalizePhi('b'); render(); });
    sC.addEventListener('input', () => { normalizePhi('c'); render(); });

    // I sliders
    sIa.addEventListener('input', () => { vIa.textContent = parseFloat(sIa.value).toFixed(2); render(); });
    sIb.addEventListener('input', () => { vIb.textContent = parseFloat(sIb.value).toFixed(2); render(); });
    sIc.addEventListener('input', () => { vIc.textContent = parseFloat(sIc.value).toFixed(2); render(); });

    // C sliders
    sCn.addEventListener('input', () => { vCn.textContent = parseFloat(sCn.value).toFixed(2); render(); });
    sCj.addEventListener('input', () => { vCj.textContent = parseFloat(sCj.value).toFixed(2); render(); });
    sCd.addEventListener('input', () => { vCd.textContent = parseFloat(sCd.value).toFixed(2); render(); });

    // S, λ, α
    sS.addEventListener('input', () => { vS.textContent = parseFloat(sS.value).toFixed(1); render(); });
    sL.addEventListener('input', () => { vL.textContent = parseFloat(sL.value).toFixed(1); render(); });
    sAphi.addEventListener('input', () => { vAphi.textContent = parseFloat(sAphi.value).toFixed(2); });
    sAi.addEventListener('input', () => { vAi.textContent = parseFloat(sAi.value).toFixed(2); });

    // Preset
    presetSelect.addEventListener('change', () => loadPreset(presetSelect.value));

    // Sim button
    const simBtn = $('sim-btn');
    if (simBtn) simBtn.addEventListener('click', runSimulation);

    // Initial render
    loadPreset('korea');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
