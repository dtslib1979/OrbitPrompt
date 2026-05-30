/**
 * lib/scanner.js
 *
 * Scan ParksyLog capture files for module-worthy conversation threads.
 *
 * A "module-worthy thread" is a coherent sub-conversation (~100+ exchanges,
 * clear topic, formalizable model, score potential >60).
 *
 * Integration:
 *   - Reads from parksy-audiolog MCP (parksy_audiolog_list_units)
 *   - Or reads from local parksy-logs repo
 *   - Or accepts raw markdown content
 */

import { readFile, readdir, stat } from 'fs/promises';
import { join, basename } from 'path';

const PARKSY_LOGS_DIR = process.env.PARKSY_LOGS_DIR || join(process.env.HOME || '/root', 'aider-workspace', 'parksy-logs');

/**
 * Score a thread for "module potential"
 *
 * Criteria (each 0-20):
 *   - topicClarity: Is there a clear, bounded subject?
 *   - modelPotential: Can the discussion be formalized into equations/structures?
 *   - complexity: Deep enough to warrant a full module (not trivial)?
 *   - completeness: Has the discussion reached a conclusion?
 *   - originality: Is this a novel framework, not just retelling?
 */
function scoreModulePotential(content) {
  const signals = {
    // Mathematical model signals
    formula: (content.match(/[=+\-*/^∫∑∏∂Δ∇ΦΙΚθλασ]|formula|equation|model|수식/g) || []).length,
    framework: (content.match(/framework|프레임워크|ㅍㅍ|paradigm|패러다임/g) || []).length,
    score: (content.match(/score|\d+\/100|점수|평가/g) || []).length,
    structure: (content.match(/계산기|calculator|시뮬레이션|simulation|interactive|인터랙티브/g) || []).length,
    philosophy: (content.match(/철학|philosophy|ontology|인식|축\s*\d|7축|8축/g) || []).length,
    // Engagement signals
    turns: (content.match(/---|user:|assistant:|human:|ai:/gi) || []).length,
    depth: content.length
  };

  const topicClarity = Math.min(20, Math.round(signals.framework * 5 + signals.philosophy * 3));
  const modelPotential = Math.min(20, Math.round(signals.formula * 3 + signals.structure * 5));
  const complexity = Math.min(20, Math.round(signals.turns / 20 + signals.depth / 5000));
  const completeness = Math.min(20, Math.round(signals.score * 8 + (content.includes('결론') || content.includes('conclusion') || content.includes('완료') ? 10 : 0)));
  const originality = Math.min(20, Math.round(signals.framework * 5 + (signals.formula + signals.structure > 10 ? 10 : 0)));

  const total = topicClarity + modelPotential + complexity + completeness + originality;
  return {
    total: Math.min(100, total),
    breakdown: { topicClarity, modelPotential, complexity, completeness, originality }
  };
}

/**
 * Extract topic/title from the first meaningful H1/H2 or first 100 chars
 */
function extractTitle(content) {
  const h1 = content.match(/^#\s+(.+)$/m);
  if (h1) return h1[1].trim();
  const h2 = content.match(/^##\s+(.+)$/m);
  if (h2) return h2[1].trim();
  const firstLine = content.split('\n')[0]?.trim();
  if (firstLine && firstLine.length < 120) return firstLine;
  return content.slice(0, 80).trim() + '...';
}

/**
 * Extract domain tags from content (축구, 철학, 금융, 음악, 기술, etc.)
 */
function extractDomain(content) {
  const domains = [];
  if (content.match(/축구|football|soccer|협회|경기력|선수|감독|월드컵|K리그/i)) domains.push('축구');
  if (content.match(/철학|philosophy|존재|인식|윤리|형이상학|7축|ontology/i)) domains.push('철학');
  if (content.match(/금융|finance|투자|주식|경제|ERP|자본|회계|원장|P&L/i)) domains.push('금융');
  if (content.match(/음악|music|노래|작곡|화성|멜로디|BGM|싱어|가창/i)) domains.push('음악');
  if (content.match(/기술|tech|개발|프로그래밍|코드|architecture|MCP|API|파이프라인/i)) domains.push('기술');
  if (content.match(/AI|인공지능|딥러닝|모델|training|데이터셋|파인튜닝/i)) domains.push('AI');
  if (domains.length === 0) domains.push('철학');
  return domains;
}

/**
 * Scan a single ParksyLog markdown file
 */
export async function scanLogFile(filePath) {
  const content = await readFile(filePath, 'utf-8');
  const score = scoreModulePotential(content);
  const fileName = basename(filePath);

  return {
    fileName,
    path: filePath,
    title: extractTitle(content),
    domains: extractDomain(content),
    score: score.total,
    scoreBreakdown: score.breakdown,
    length: content.length,
    turnEstimate: Math.round((content.match(/\n---\n/g) || []).length),
    moduleWorthy: score.total >= 60
  };
}

/**
 * Scan a directory for all ParksyLog files
 */
export async function scanDirectory(dirPath = PARKSY_LOGS_DIR) {
  try {
    const files = await readdir(dirPath);
    const mdFiles = files.filter(f => f.startsWith('ParksyLog_') && f.endsWith('.md'));

    const results = [];
    for (const f of mdFiles) {
      try {
        const result = await scanLogFile(join(dirPath, f));
        results.push(result);
      } catch (e) {
        // skip unreadable files
      }
    }
    return results.sort((a, b) => b.score - a.score);
  } catch (e) {
    return { error: `Cannot read directory: ${dirPath}`, message: e.message };
  }
}

/**
 * Extract a specific sub-thread from a log (by line range or topic marker)
 */
export function extractThread(content, options = {}) {
  const lines = content.split('\n');
  const sections = [];
  let currentSection = { title: '', lines: [], startLine: 0 };

  lines.forEach((line, i) => {
    if (line.startsWith('## ') || line.startsWith('---')) {
      if (currentSection.lines.length > 10) {
        sections.push({ ...currentSection });
      }
      currentSection = {
        title: line.replace(/^##\s+/, '').replace(/^---+$/, 'Section'),
        lines: [],
        startLine: i
      };
    }
    currentSection.lines.push(line);
  });
  if (currentSection.lines.length > 10) {
    sections.push({ ...currentSection });
  }

  return sections.map(s => ({
    title: s.title,
    startLine: s.startLine,
    content: s.lines.join('\n'),
    score: scoreModulePotential(s.lines.join('\n'))
  })).filter(s => s.score.total >= 50);
}
