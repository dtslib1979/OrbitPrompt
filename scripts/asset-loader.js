/**
 * OrbitPrompt Asset Loader v1.0
 *
 * 3개 스튜디오(image, audio, experience)의 에셋을 통합 로드
 *
 * 사용법:
 *   await AssetLoader.init();
 *   const bg = AssetLoader.getAsset('image', 'backgrounds', 'chalkboard-dark');
 *   const allMathAssets = AssetLoader.getByTag('image', 'math');
 */

const AssetLoader = {
  sources: null,
  cache: {},
  loaded: false,

  /**
   * 초기화: sources.json 로드 → 각 스튜디오 manifest fetch
   */
  async init() {
    if (this.loaded) return this.cache;

    try {
      // 1. sources.json 로드
      const sourcesUrl = this._getBasePath() + 'config/sources.json';
      this.sources = await fetch(sourcesUrl).then(r => r.json());

      // 2. 각 스튜디오 manifest 병렬 로드
      const loadPromises = Object.entries(this.sources.studios).map(
        async ([type, studio]) => {
          try {
            const manifest = await fetch(studio.manifest).then(r => r.json());
            this.cache[type] = manifest;
            console.log(`✓ ${studio.name} 연결됨`);
            return { type, success: true };
          } catch (e) {
            console.warn(`✗ ${studio.name} 연결 실패:`, e.message);
            this.cache[type] = null;
            return { type, success: false };
          }
        }
      );

      await Promise.all(loadPromises);
      this.loaded = true;

      return this.cache;
    } catch (e) {
      console.error('AssetLoader 초기화 실패:', e);
      return null;
    }
  },

  /**
   * 특정 에셋 가져오기
   * @param {string} studioType - 'image' | 'audio' | 'experience'
   * @param {string} category - 'thumbnails', 'bgm', 'designTokens' 등
   * @param {string} id - 에셋 ID
   * @returns {string|object|null} - URL 또는 객체
   */
  getAsset(studioType, category, id) {
    const studio = this.cache[studioType];
    if (!studio) return null;

    // experience 스튜디오는 구조가 다름
    if (studioType === 'experience') {
      if (category === 'designTokens') {
        return studio.designTokens?.[id] || studio.designTokens;
      }
      if (category === 'exports') {
        const exportPath = studio.exports?.[id];
        return exportPath ? studio.baseUrl + exportPath : null;
      }
      return null;
    }

    // image, audio 스튜디오
    const assets = studio.assets?.[category];
    if (!assets) return null;

    const asset = assets.find(a => a.id === id);
    if (!asset) return null;

    return studio.baseUrl + asset.url;
  },

  /**
   * 태그로 에셋 검색
   * @param {string} studioType - 'image' | 'audio'
   * @param {string} tag - 검색할 태그
   * @returns {Array} - 매칭된 에셋 목록
   */
  getByTag(studioType, tag) {
    const studio = this.cache[studioType];
    if (!studio || !studio.assets) return [];

    const results = [];
    for (const [category, assets] of Object.entries(studio.assets)) {
      if (!Array.isArray(assets)) continue;

      assets
        .filter(a => a.tags?.includes(tag))
        .forEach(a => {
          results.push({
            ...a,
            category,
            fullUrl: studio.baseUrl + a.url
          });
        });
    }
    return results;
  },

  /**
   * 디자인 토큰 가져오기 (tango-magenta)
   * @param {string} tokenType - 'timing' | 'colors' | 'easing'
   * @returns {object|null}
   */
  getDesignTokens(tokenType) {
    const studio = this.cache.experience;
    if (!studio || !studio.designTokens) return null;

    return tokenType
      ? studio.designTokens[tokenType]
      : studio.designTokens;
  },

  /**
   * 연결 상태 확인
   * @returns {object} - 각 스튜디오 연결 상태
   */
  getStatus() {
    return {
      loaded: this.loaded,
      studios: Object.fromEntries(
        Object.keys(this.sources?.studios || {}).map(type => [
          type,
          {
            connected: this.cache[type] !== null,
            name: this.sources?.studios[type]?.name
          }
        ])
      )
    };
  },

  /**
   * base path 계산 (상대 경로 지원)
   */
  _getBasePath() {
    const path = window.location.pathname;
    const depth = (path.match(/\//g) || []).length - 1;
    return depth > 0 ? '../'.repeat(depth) : './';
  }
};

// 글로벌 노출
window.AssetLoader = AssetLoader;
