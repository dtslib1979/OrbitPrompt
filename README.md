# OrbitPrompt

**Multiple query gen engine to AI**

A minimal, production-ready GitHub Pages prompt archive with searchable D1xP5x style tags.

## 🌐 Live Demo

Visit the live site at: `https://dtslib1979.github.io/OrbitPrompt/`

## 📁 Repository Structure

```
/ (root)
├── index.html              # Main search interface
├── generate-index.js       # Auto-indexing script
├── prompts/
│   ├── index.json         # Auto-generated file list
│   ├── D1xP1xL1xC1xE1.html  # Example prompt
│   └── D1xP5xL2xC3xE5.html  # Example prompt
└── README.md
```

## 🚀 GitHub Pages Setup

### Required Settings:

1. **Repository must be Public**
2. Navigate to **Settings** → **Pages**
3. Configure:
   - **Source:** Deploy from branch
   - **Branch:** `main`
   - **Folder:** `/ (root)`
4. Save and wait for deployment

## 📝 Adding New Prompts

1. Add your prompt file (`.html` or `.md`) to the `prompts/` directory
2. Run the indexing script:
   ```bash
   node generate-index.js
   ```
3. Commit and push changes

The script automatically:
- Scans the `prompts/` directory
- Generates `prompts/index.json` with all file names
- Excludes `index.json` and hidden files

## 🔍 Search Functionality

The main page (`index.html`) provides:
- Real-time search filtering
- Support for D1xP5x style tags
- Links to all prompt files
- Displays up to 50 results

## ✅ Validation Checklist

After setup, verify:
- [ ] GitHub Pages URL loads successfully
- [ ] `prompts/index.json` is valid JSON
- [ ] Clicking prompt links opens files correctly
- [ ] Search functionality works
- [ ] All commits pushed to main branch
