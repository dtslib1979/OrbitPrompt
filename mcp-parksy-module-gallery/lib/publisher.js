/**
 * lib/publisher.js
 *
 * Register a generated Thought Module in the OrbitPrompt gallery index.html.
 *
 * Reads index.html, finds the MODULES array, inserts a new entry,
 * and writes the updated file back.
 */

import { readFile, writeFile } from 'fs/promises';
import { join } from 'path';

const GALLERY_INDEX = join(process.env.ORBIT_GALLERY_DIR || process.cwd(), '..', 'index.html');

/**
 * Parse the MODULES array from index.html
 */
function parseModulesArray(html) {
  const match = html.match(/const MODULES\s*=\s*\[([\s\S]*?)\];/);
  if (!match) return { html, modules: [], start: match?.index ?? -1, end: -1 };
  return { html, modules: match[1], start: match.index, end: match.index + match[0].length };
}

/**
 * Build a JS object literal string for a module entry
 */
function buildModuleEntry(data) {
  const tags = (data.tags || []).map(t => `'${t.replace(/'/g, "\\'")}'`).join(', ');
  return `  { id: '${data.id}', icon: '${data.icon || '◇'}', domain: '${data.domain}', number: '${String(data.number).padStart(2, '0')}', title: '${data.title.replace(/'/g, "\\'")}', desc: '${(data.desc || '').replace(/'/g, "\\'")}', tags: [${tags}], score: ${data.score || 0}, maxScore: ${data.maxScore || 100}, status: '${data.status || 'live'}', fromLog: '${data.fromLog || ''}', path: '${data.path || ''}', whitepaper: '${data.whitepaper || ''}' }`;
}

/**
 * Publish a module: insert into index.html MODULES array
 */
export async function publishModule(moduleData, galleryPath) {
  const indexPath = galleryPath || GALLERY_INDEX;
  let html = await readFile(indexPath, 'utf-8');

  const parsed = parseModulesArray(html);
  if (!parsed.modules) {
    return { success: false, error: 'Could not find MODULES array in index.html' };
  }

  // Check for duplicate
  const idMatch = new RegExp(`id:\\s*'${moduleData.id}'`);
  if (idMatch.test(parsed.modules)) {
    return { success: false, error: `Module with id '${moduleData.id}' already exists` };
  }

  const entry = buildModuleEntry(moduleData);
  let newModules;
  if (parsed.modules.trim().length === 0) {
    newModules = `\n${entry}\n`;
  } else {
    newModules = parsed.modules.trimEnd() + `,\n${entry}\n`;
  }

  const before = html.slice(0, parsed.start);
  const after = html.slice(parsed.end);
  html = `${before}const MODULES = [\n${newModules}];${after}`;

  await writeFile(indexPath, html, 'utf-8');
  return { success: true, path: indexPath, moduleId: moduleData.id };
}

/**
 * Remove a module from the gallery by id
 */
export async function unpublishModule(moduleId, galleryPath) {
  const indexPath = galleryPath || GALLERY_INDEX;
  let html = await readFile(indexPath, 'utf-8');

  const entryRegex = new RegExp(`\\s{2}\\{ id: '${moduleId}',[\\s\\S]*?\\},?\\n?`);
  const newHtml = html.replace(entryRegex, '');
  if (newHtml === html) {
    return { success: false, error: `Module '${moduleId}' not found in gallery` };
  }

  // Clean up trailing comma before ] if needed
  const cleaned = newHtml.replace(/,\n\];/, '\n];');
  await writeFile(indexPath, cleaned, 'utf-8');
  return { success: true, moduleId };
}

/**
 * Update gallery stats: count live modules
 */
export async function updateGalleryStats(galleryPath) {
  const indexPath = galleryPath || GALLERY_INDEX;
  const html = await readFile(indexPath, 'utf-8');

  const liveMatch = html.match(/status:\s*'live'/g);
  const liveCount = liveMatch ? liveMatch.length : 0;

  // Update the stat-modules element if it exists in the HTML
  const statRegex = /(<span id="stat-modules">)(\d+)(<\/span>)/;
  const updated = html.replace(statRegex, `$1${liveCount}$3`);

  if (updated !== html) {
    await writeFile(indexPath, updated, 'utf-8');
  }

  return { liveCount };
}
