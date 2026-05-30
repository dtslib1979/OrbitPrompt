#!/usr/bin/env node

/**
 * mcp-parksy-module-gallery — MCP Server
 *
 * Tools:
 *   scan_for_modules   — Scan ParksyLog captures for module-worthy threads
 *   generate_module    — Generate a complete Thought Module directory from content
 *   publish_module     — Register a module in the OrbitPrompt gallery index.html
 *
 * JSON-RPC over stdio (MCP protocol)
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { scanDirectory, scanLogFile } from './lib/scanner.js';
import { generateModule } from './lib/generator.js';
import { publishModule, unpublishModule, updateGalleryStats } from './lib/publisher.js';
import { readFile } from 'fs/promises';
import { join, dirname } from 'path';

const GALLERY_DIR = process.env.ORBIT_GALLERY_DIR || join(dirname(new URL(import.meta.url).pathname), '..');

const server = new Server(
  { name: 'mcp-parksy-module-gallery', version: '0.1.0' },
  { capabilities: { tools: {} } }
);

/**
 * List available tools
 */
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: 'scan_for_modules',
      description: 'Scan ParksyLog capture files for module-worthy conversation threads. Returns scored list of potential modules.',
      inputSchema: {
        type: 'object',
        properties: {
          dirPath: {
            type: 'string',
            description: 'Directory containing ParksyLog_*.md files (default: PARKSY_LOGS_DIR env or ~/aider-workspace/parksy-logs)'
          },
          minScore: {
            type: 'number',
            description: 'Minimum score threshold (0-100, default: 60)',
            default: 60
          }
        }
      }
    },
    {
      name: 'generate_module',
      description: 'Generate a complete Thought Module directory from extracted content. Creates index.html, whitepaper.html, and calculator.js.',
      inputSchema: {
        type: 'object',
        properties: {
          title: { type: 'string', description: 'Module title' },
          description: { type: 'string', description: 'Short description' },
          domains: {
            type: 'array', items: { type: 'string' },
            description: 'Domain tags (e.g. 축구, 철학, 금융, 음악, 기술, AI)'
          },
          rawContent: { type: 'string', description: 'Raw markdown content for whitepaper parsing' },
          score: { type: 'number', description: 'Module quality score 0-100' },
          id: { type: 'string', description: 'Unique module ID (slug, auto-generated from title if empty)' },
          status: {
            type: 'string', enum: ['live', 'building', 'planned'],
            description: 'Module status', default: 'live'
          },
          source: { type: 'string', description: 'Source identifier' },
          outputBaseDir: { type: 'string', description: 'Output directory (default: gallery dir)' }
        },
        required: ['title', 'description']
      }
    },
    {
      name: 'publish_module',
      description: 'Register a generated Thought Module in the OrbitPrompt gallery index.html. Adds entry to MODULES array and updates stats.',
      inputSchema: {
        type: 'object',
        properties: {
          id: { type: 'string', description: 'Module ID (must match generated module)' },
          title: { type: 'string', description: 'Module title' },
          description: { type: 'string', description: 'Module description' },
          domain: { type: 'string', description: 'Domain (축구, 철학, 금융, 음악, 기술, AI, 준비중)' },
          icon: { type: 'string', description: 'Emoji icon' },
          tags: { type: 'array', items: { type: 'string' }, description: 'Tech tags' },
          score: { type: 'number', description: 'Score 0-100' },
          number: { type: 'number', description: 'Module number (auto if empty)' },
          fromLog: { type: 'string', description: 'Source log filename' },
          path: { type: 'string', description: 'Relative path to index.html' },
          whitepaper: { type: 'string', description: 'Relative path to whitepaper.html' },
          status: { type: 'string', enum: ['live', 'building', 'planned'], default: 'live' }
        },
        required: ['id', 'title', 'domain']
      }
    },
    {
      name: 'unpublish_module',
      description: 'Remove a module from the gallery by ID.',
      inputSchema: {
        type: 'object',
        properties: {
          id: { type: 'string', description: 'Module ID to remove' }
        },
        required: ['id']
      }
    },
    {
      name: 'scan_log_file',
      description: 'Scan a single ParksyLog markdown file for module potential.',
      inputSchema: {
        type: 'object',
        properties: {
          filePath: { type: 'string', description: 'Path to ParksyLog_*.md file' }
        },
        required: ['filePath']
      }
    }
  ]
}));

/**
 * Handle tool calls
 */
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'scan_for_modules': {
        const dirPath = args?.dirPath;
        const minScore = args?.minScore || 60;
        const results = await scanDirectory(dirPath);
        if (results.error) {
          return {
            content: [{ type: 'text', text: `Error: ${results.error}` }],
            isError: true
          };
        }
        const filtered = results.filter(r => r.score >= minScore);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({ count: filtered.length, modules: filtered }, null, 2)
          }]
        };
      }

      case 'generate_module': {
        const { title, description, domains, rawContent, score, id, status, source, outputBaseDir } = args;
        const moduleData = {
          id: id || title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/-+/g, '-').replace(/^-|-$/g, ''),
          title,
          description,
          domains: domains || ['철학'],
          score: score || 0,
          status: status || 'live',
          source: source || 'ParksyLog 자동 추출'
        };
        const baseDir = outputBaseDir || GALLERY_DIR;
        const result = await generateModule(moduleData, rawContent || '', baseDir);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              success: true,
              slug: result.slug,
              path: result.path,
              fullPath: result.fullPath,
              files: result.files
            }, null, 2)
          }]
        };
      }

      case 'publish_module': {
        const { id, title, description, domain, icon, tags, score, number, fromLog, path, whitepaper, status } = args;
        const moduleEntry = {
          id,
          icon: icon || '◇',
          domain: domain || '준비중',
          number: number || 1,
          title,
          desc: description || '',
          tags: tags || [],
          score: score || 0,
          maxScore: 100,
          status: status || 'live',
          fromLog: fromLog || '',
          path: path || `${id}/index.html`,
          whitepaper: whitepaper || `${id}/whitepaper.html`
        };
        const result = await publishModule(moduleEntry);
        if (result.success) {
          await updateGalleryStats();
        }
        return {
          content: [{
            type: 'text',
            text: JSON.stringify(result, null, 2)
          }]
        };
      }

      case 'unpublish_module': {
        const { id: removeId } = args;
        const result = await unpublishModule(removeId);
        if (result.success) {
          await updateGalleryStats();
        }
        return {
          content: [{
            type: 'text',
            text: JSON.stringify(result, null, 2)
          }]
        };
      }

      case 'scan_log_file': {
        const { filePath } = args;
        const result = await scanLogFile(filePath);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify(result, null, 2)
          }]
        };
      }

      default:
        return {
          content: [{ type: 'text', text: `Unknown tool: ${name}` }],
          isError: true
        };
    }
  } catch (err) {
    return {
      content: [{ type: 'text', text: `Error: ${err.message}` }],
      isError: true
    };
  }
});

/**
 * Start the server
 */
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('mcp-parksy-module-gallery server running on stdio');
}

main().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
