/**
 * OrbitPrompt Topics Loader
 *
 * 오늘의 주제를 자동 생성하는 시스템
 *
 * Usage:
 *   await TopicsLoader.init();
 *   const topic = TopicsLoader.getTodaysTopic('math-tutor');
 *   const random = TopicsLoader.getRandomTopic('music-curation');
 */

const TopicsLoader = {
  index: null,
  cache: {},
  loaded: false,

  /**
   * Initialize - load topics index
   */
  async init() {
    if (this.loaded) return this;

    try {
      const basePath = this._getBasePath();
      const indexRes = await fetch(`${basePath}topics/index.json`);
      this.index = await indexRes.json();
      this.loaded = true;
      console.log('[TopicsLoader] Initialized:', this.index.stats);
      return this;
    } catch (e) {
      console.error('[TopicsLoader] Failed to init:', e);
      return null;
    }
  },

  /**
   * Load topics for a specific category
   */
  async loadCategory(categoryId) {
    if (this.cache[categoryId]) return this.cache[categoryId];

    const category = this.index?.categories?.find(c => c.id === categoryId);
    if (!category) {
      console.warn(`[TopicsLoader] Category not found: ${categoryId}`);
      return null;
    }

    try {
      const basePath = this._getBasePath();
      const res = await fetch(`${basePath}topics/${category.file}`);
      const data = await res.json();
      this.cache[categoryId] = data;
      return data;
    } catch (e) {
      console.error(`[TopicsLoader] Failed to load ${categoryId}:`, e);
      return null;
    }
  },

  /**
   * Get today's topic based on date seed
   * Same day = same topic (deterministic)
   */
  async getTodaysTopic(categoryId) {
    const data = await this.loadCategory(categoryId);
    if (!data?.topics?.length) return null;

    // Use date as seed for consistent daily selection
    const today = new Date();
    const seed = today.getFullYear() * 10000 + (today.getMonth() + 1) * 100 + today.getDate();
    const index = seed % data.topics.length;

    return data.topics[index];
  },

  /**
   * Get random topic
   */
  async getRandomTopic(categoryId) {
    const data = await this.loadCategory(categoryId);
    if (!data?.topics?.length) return null;

    const index = Math.floor(Math.random() * data.topics.length);
    return data.topics[index];
  },

  /**
   * Get all topics for a category
   */
  async getAllTopics(categoryId) {
    const data = await this.loadCategory(categoryId);
    return data?.topics || [];
  },

  /**
   * Search topics by keyword
   */
  async searchTopics(query, categoryId = null) {
    const categories = categoryId
      ? [categoryId]
      : this.index?.categories?.map(c => c.id) || [];

    const results = [];
    const q = query.toLowerCase();

    for (const catId of categories) {
      const data = await this.loadCategory(catId);
      if (!data?.topics) continue;

      const matches = data.topics.filter(t =>
        t.title?.toLowerCase().includes(q) ||
        t.titleEn?.toLowerCase().includes(q) ||
        t.keywords?.some(k => k.toLowerCase().includes(q))
      );

      results.push(...matches.map(m => ({ ...m, category: catId })));
    }

    return results;
  },

  /**
   * Get topic by ID
   */
  async getTopicById(categoryId, topicId) {
    const data = await this.loadCategory(categoryId);
    return data?.topics?.find(t => t.id === topicId) || null;
  },

  /**
   * Get category info
   */
  getCategoryInfo(categoryId) {
    return this.index?.categories?.find(c => c.id === categoryId) || null;
  },

  /**
   * Get all categories
   */
  getCategories() {
    return this.index?.categories || [];
  },

  /**
   * Format topic for display
   */
  formatTopic(topic, lang = 'ko') {
    if (!topic) return null;

    const isEn = lang === 'en';
    return {
      title: isEn ? topic.titleEn : topic.title,
      unit: isEn ? (topic.unitEn || topic.unit) : topic.unit,
      intro: topic.outline?.intro,
      main: topic.outline?.main,
      outro: topic.outline?.outro,
      difficulty: topic.difficulty,
      keywords: topic.keywords
    };
  },

  /**
   * Calculate base path
   */
  _getBasePath() {
    const path = window.location.pathname;
    // Handle different depths
    if (path.includes('/prompts/broadcast/')) {
      return '../../';
    } else if (path.includes('/prompts/')) {
      return '../';
    }
    return './';
  }
};

// Global export
window.TopicsLoader = TopicsLoader;
