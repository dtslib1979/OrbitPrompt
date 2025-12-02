#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const promptsDir = path.join(__dirname, 'prompts');

// Ensure prompts directory exists
if (!fs.existsSync(promptsDir)) {
  fs.mkdirSync(promptsDir, { recursive: true });
}

// Read all .html files in prompts directory
const files = fs.readdirSync(promptsDir)
  .filter(file => {
    // Include only .html files
    return file.endsWith('.html');
  })
  .sort(); // Sort alphabetically

// Write to index.json
const indexPath = path.join(promptsDir, 'index.json');
fs.writeFileSync(indexPath, JSON.stringify(files, null, 2));

console.log(`Generated index.json with ${files.length} files:`);
files.forEach(file => console.log(`  - ${file}`));
