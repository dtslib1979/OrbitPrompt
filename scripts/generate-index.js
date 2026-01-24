#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const promptsDir = path.join(__dirname, '..', 'prompts');
const categories = ['broadcast', 'engine', 'guide'];

const index = {};

categories.forEach(cat => {
  const catDir = path.join(promptsDir, cat);
  if (fs.existsSync(catDir)) {
    index[cat] = fs.readdirSync(catDir)
      .filter(f => f.endsWith('.html'))
      .sort();
  }
});

const indexPath = path.join(promptsDir, 'index.json');
fs.writeFileSync(indexPath, JSON.stringify(index, null, 2) + '\n');

console.log('Generated index.json:');
Object.entries(index).forEach(([cat, files]) => {
  console.log(`  ${cat}/: ${files.length} files`);
  files.forEach(f => console.log(`    - ${f}`));
});
