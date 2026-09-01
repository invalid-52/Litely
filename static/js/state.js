/**
 * LITELY Reactive State Management Store
 */

const STORAGE_KEY = 'litely_state_v1';

const DEFAULT_SETTINGS = {
  font_family: 'JetBrains Mono',
  font_size: 14,
  line_height: 1.5,
  padding: 32,
  border_radius: 12,
  window_chrome: 'mac',
  background_type: 'preset',
  background_value: 'twilight',
  shadow: 'medium',
  show_line_numbers: true,
  show_language_badge: true,
  show_watermark: false,
  word_wrap: false,
  aspect_ratio: 'auto',
  highlight_lines: [],
};

class StateStore {
  constructor() {
    this.listeners = new Set();
    this.history = [];
    this.historyIndex = -1;

    // Load persisted state or defaults
    const persisted = this.loadPersisted();

    this.document = {
      source: persisted?.source || '',
      language: persisted?.language || 'python',
      filename: persisted?.filename || 'main.py',
      theme: persisted?.theme || 'github-dark',
      visualization: { ...DEFAULT_SETTINGS, ...(persisted?.visualization || {}) },
      source_type: 'text',
      metadata: {},
    };

    this.ui = {
      isAutoDetect: true,
      detectedLanguage: null,
      activeCustomizerTab: 'appearance',
      isLoading: false,
      isCommandPaletteOpen: false,
      isShortcutsModalOpen: false,
    };
  }

  loadPersisted() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  }

  savePersisted() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({
        source: this.document.source,
        language: this.document.language,
        filename: this.document.filename,
        theme: this.document.theme,
        visualization: this.document.visualization,
      }));
    } catch (e) {
      console.warn('Could not persist LITELY state:', e);
    }
  }

  subscribe(callback) {
    this.listeners.add(callback);
    return () => this.listeners.delete(callback);
  }

  notify(changeType) {
    this.savePersisted();
    for (const listener of this.listeners) {
      try {
        listener(this, changeType);
      } catch (err) {
        console.error('Error in state subscriber:', err);
      }
    }
  }

  // State Mutators
  setSource(source) {
    if (this.document.source === source) return;
    this.document.source = source;
    this.notify('source');
  }

  setLanguage(lang, isAuto = false) {
    this.document.language = lang;
    this.ui.isAutoDetect = isAuto;
    this.notify('language');
  }

  setFilename(name) {
    this.document.filename = name;
    this.notify('filename');
  }

  setTheme(themeId) {
    this.document.theme = themeId;
    this.notify('theme');
  }

  setVisualization(key, value) {
    this.document.visualization[key] = value;
    this.notify('visualization');
  }

  setBulkVisualization(newSettings) {
    this.document.visualization = { ...this.document.visualization, ...newSettings };
    this.notify('visualization');
  }

  resetVisualization() {
    this.document.visualization = { ...DEFAULT_SETTINGS };
    this.notify('visualization');
  }

  setUI(key, value) {
    this.ui[key] = value;
    this.notify('ui');
  }
}

export const store = new StateStore();
