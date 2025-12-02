#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const promptsDir = path.join(__dirname, 'prompts');

// Ensure prompts directory exists
if (!fs.existsSync(promptsDir)) {
  fs.mkdirSync(promptsDir, { recursive: true });
}

// Read all files in prompts directory
const files = fs.readdirSync(promptsDir)
  .filter(file => {
    // Exclude index.json and hidden files
    return file !== 'index.json' && !file.startsWith('.');
  })
  .sort(); // Sort alphabetically

// Write to index.json
const indexPath = path.join(promptsDir, 'index.json');
fs.writeFileSync(indexPath, JSON.stringify(files, null, 2));

console.log(`Generated index.json with ${files.length} files:`);
files.forEach(file => console.log(`  - ${file}`));
