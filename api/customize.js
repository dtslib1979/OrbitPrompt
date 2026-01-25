/**
 * OrbitPrompt Branch Customization API
 *
 * 브랜치가 템플릿을 커스터마이징할 때 사용하는 스크립트
 *
 * Usage (in branch's HTML):
 *
 * <script src="https://dtslib1979.github.io/OrbitPrompt/api/customize.js"></script>
 * <script>
 *   OrbitCustomize.init({
 *     branch: 'koosy',
 *     colors: {
 *       primary: '#ff6b6b',
 *       accent: '#ffd93d',
 *       bg: '#1a1a2e'
 *     },
 *     logo: 'https://koosy.kr/logo.png',
 *     font: 'Noto Sans KR'
 *   });
 * </script>
 */

const OrbitCustomize = {
  config: null,

  /**
   * Initialize customization
   * @param {Object} options - Branch customization options
   */
  init(options = {}) {
    this.config = {
      branch: options.branch || 'default',
      colors: {
        primary: options.colors?.primary || '#58a6ff',
        accent: options.colors?.accent || '#a371f7',
        bg: options.colors?.bg || '#0d1117',
        surface: options.colors?.surface || '#161b22',
        text: options.colors?.text || '#e6edf3',
        muted: options.colors?.muted || '#8b949e'
      },
      logo: options.logo || null,
      font: options.font || null,
      watermark: options.watermark !== false
    };

    this.applyStyles();
    this.injectBranding();
    this.logActivation();

    return this;
  },

  /**
   * Apply CSS custom properties
   */
  applyStyles() {
    const root = document.documentElement;
    const { colors, font } = this.config;

    // Apply color variables
    root.style.setProperty('--brand-primary', colors.primary);
    root.style.setProperty('--brand-accent', colors.accent);
    root.style.setProperty('--brand-bg', colors.bg);
    root.style.setProperty('--brand-surface', colors.surface);
    root.style.setProperty('--brand-text', colors.text);
    root.style.setProperty('--brand-muted', colors.muted);

    // Map to common variable names used in templates
    root.style.setProperty('--accent', colors.primary);
    root.style.setProperty('--bg', colors.bg);
    root.style.setProperty('--surface', colors.surface);
    root.style.setProperty('--text', colors.text);
    root.style.setProperty('--text-muted', colors.muted);
    root.style.setProperty('--gradient-start', colors.primary);
    root.style.setProperty('--gradient-end', colors.accent);

    // Apply font if specified
    if (font) {
      root.style.setProperty('--brand-font', font);
      document.body.style.fontFamily = `'${font}', -apple-system, BlinkMacSystemFont, sans-serif`;
    }
  },

  /**
   * Inject branch logo/branding
   */
  injectBranding() {
    const { branch, logo, watermark } = this.config;

    // Add logo if provided
    if (logo) {
      const existingLogo = document.querySelector('.branch-logo');
      if (!existingLogo) {
        const logoEl = document.createElement('img');
        logoEl.className = 'branch-logo';
        logoEl.src = logo;
        logoEl.alt = `${branch} logo`;
        logoEl.style.cssText = `
          position: fixed;
          top: 1rem;
          left: 1rem;
          height: 32px;
          width: auto;
          z-index: 100;
          opacity: 0.8;
        `;
        document.body.appendChild(logoEl);
      }
    }

    // Add watermark
    if (watermark) {
      const existingWatermark = document.querySelector('.branch-watermark');
      if (!existingWatermark) {
        const wmEl = document.createElement('div');
        wmEl.className = 'branch-watermark';
        wmEl.innerHTML = `
          <span style="opacity: 0.3; font-size: 0.7rem;">
            Powered by <a href="https://dtslib1979.github.io/OrbitPrompt" style="color: inherit;">OrbitPrompt</a>
            ${branch !== 'default' ? ` · ${branch.toUpperCase()}` : ''}
          </span>
        `;
        wmEl.style.cssText = `
          position: fixed;
          bottom: 0.5rem;
          right: 0.5rem;
          z-index: 100;
          color: var(--brand-muted, #8b949e);
        `;
        document.body.appendChild(wmEl);
      }
    }
  },

  /**
   * Log activation for analytics
   */
  logActivation() {
    console.log(`%c[OrbitPrompt] Branch "${this.config.branch}" activated`,
      'color: #58a6ff; font-weight: bold;');
    console.log('Config:', this.config);
  },

  /**
   * Get current configuration
   */
  getConfig() {
    return this.config;
  },

  /**
   * Update colors dynamically
   */
  setColors(colors) {
    Object.assign(this.config.colors, colors);
    this.applyStyles();
  },

  /**
   * Preset themes for branches
   */
  presets: {
    koosy: {
      colors: {
        primary: '#ff6b6b',
        accent: '#ffd93d',
        bg: '#1a1a2e'
      }
    },
    gohsy: {
      colors: {
        primary: '#4ecdc4',
        accent: '#44a08d',
        bg: '#0f1419'
      }
    },
    lotus: {
      colors: {
        primary: '#e91e63',
        accent: '#9c27b0',
        bg: '#0a0a0a'
      }
    },
    'tango-magenta': {
      colors: {
        primary: '#e91e63',
        accent: '#ffd54f',
        bg: '#0a0008'
      }
    },
    artrew: {
      colors: {
        primary: '#ff9800',
        accent: '#ff5722',
        bg: '#121212'
      }
    },
    papafly: {
      colors: {
        primary: '#2196f3',
        accent: '#03a9f4',
        bg: '#0d1117'
      }
    }
  },

  /**
   * Apply preset theme
   * @param {string} branchName - Name of the branch
   */
  applyPreset(branchName) {
    const preset = this.presets[branchName];
    if (preset) {
      this.init({
        branch: branchName,
        ...preset
      });
    } else {
      console.warn(`[OrbitPrompt] No preset found for "${branchName}"`);
    }
  }
};

// Global export
window.OrbitCustomize = OrbitCustomize;

// Auto-detect branch from URL parameter
(function autoInit() {
  const params = new URLSearchParams(window.location.search);
  const branch = params.get('branch');

  if (branch && OrbitCustomize.presets[branch]) {
    OrbitCustomize.applyPreset(branch);
  }
})();
