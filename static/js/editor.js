/**
 * LITELY CodeMirror Code Editor Controller
 * Provides syntax highlighting, line numbers, search, bracket matching,
 * tab indentation, selection, undo/redo, and bidirectional state synchronization.
 */

import { store, getApiBaseUrl } from './state.js';

// Map LITELY language IDs to CodeMirror mode configurations
const MODE_MAP = {
  python: 'python',
  javascript: 'javascript',
  typescript: { name: 'javascript', typescript: true },
  jsx: { name: 'javascript', jsx: true },
  tsx: { name: 'javascript', typescript: true, jsx: true },
  rust: 'rust',
  go: 'go',
  sql: 'sql',
  c: 'text/x-csrc',
  cpp: 'text/x-c++src',
  java: 'text/x-java',
  csharp: 'text/x-csharp',
  kotlin: 'text/x-kotlin',
  dart: 'text/x-dart',
  html: 'htmlmixed',
  xml: 'xml',
  css: 'css',
  scss: 'css',
  sass: 'css',
  markdown: 'markdown',
  json: { name: 'javascript', json: true },
};

class CodeEditor {
  constructor() {
    this.cm = null;
    this.container = null;
    this.lineCountEl = null;
    this.charCountEl = null;
    this.filenameInput = null;
    this.languageSelect = null;
    this.initialized = false;
    this.detectAbortController = null;
  }

  init() {
    if (this.initialized) return;

    this.container = document.getElementById('sourceEditorContainer');
    this.lineCountEl = document.getElementById('editorLineCount');
    this.charCountEl = document.getElementById('editorCharCount');
    this.filenameInput = document.getElementById('filenameInput');
    this.languageSelect = document.getElementById('languageSelect');

    if (!this.container) return;

    // Check if CodeMirror is loaded globally
    if (typeof window.CodeMirror !== 'undefined') {
      this.initCodeMirror();
    } else {
      // Fallback: poll or wait
      const checkCm = setInterval(() => {
        if (typeof window.CodeMirror !== 'undefined') {
          clearInterval(checkCm);
          this.initCodeMirror();
        }
      }, 50);
    }
  }

  initCodeMirror() {
    if (this.initialized) return;

    const initialCode = store.document.source || '';
    const initialMode = this.resolveMode(store.document.language);

    this.cm = window.CodeMirror(this.container, {
      value: initialCode,
      mode: initialMode,
      theme: 'litely',
      lineNumbers: true,
      styleActiveLine: true,
      matchBrackets: true,
      autoCloseBrackets: true,
      lineWrapping: store.document.visualization.word_wrap || false,
      tabSize: 4,
      indentUnit: 4,
      indentWithTabs: false,
      extraKeys: {
        Tab: (cm) => {
          if (cm.somethingSelected()) {
            cm.indentSelection('add');
          } else {
            cm.replaceSelection('    ', 'end', '+input');
          }
        },
        'Shift-Tab': (cm) => {
          cm.indentSelection('subtract');
        },
      },
    });

    this.initialized = true;

    // Set initial stats
    this.updateStats(initialCode);

    if (this.filenameInput && store.document.filename) {
      this.filenameInput.value = store.document.filename;
    }
    if (this.languageSelect && store.document.language) {
      this.languageSelect.value = store.ui.isAutoDetect ? 'auto' : store.document.language;
    }

    this.bindEvents();

    // Subscribe to central state changes
    store.subscribe((state, changeType) => {
      if (changeType === 'source') {
        const currentVal = this.cm.getValue();
        if (currentVal !== state.document.source) {
          this.cm.setValue(state.document.source || '');
          this.updateStats(state.document.source || '');
        }
      }
      if (changeType === 'language') {
        const mode = this.resolveMode(state.document.language);
        this.cm.setOption('mode', mode);
        if (this.languageSelect) {
          this.languageSelect.value = state.ui.isAutoDetect ? 'auto' : state.document.language;
        }
      }
      if (changeType === 'filename' && this.filenameInput) {
        if (this.filenameInput.value !== state.document.filename) {
          this.filenameInput.value = state.document.filename;
        }
      }
      if (changeType === 'visualization') {
        this.cm.setOption('lineWrapping', state.document.visualization.word_wrap);
      }
    });

    // Initial resize refresh
    setTimeout(() => this.cm.refresh(), 100);
  }

  resolveMode(langId) {
    if (!langId) return 'python';
    const key = langId.toLowerCase().trim();
    return MODE_MAP[key] || 'python';
  }

  bindEvents() {
    // CodeMirror change event
    this.cm.on('change', () => {
      const code = this.cm.getValue();
      this.updateStats(code);
      store.setSource(code);

      if (store.ui.isAutoDetect) {
        this.triggerAutoDetect(code);
      }
    });

    // Filename input
    if (this.filenameInput) {
      this.filenameInput.addEventListener('input', () => {
        const name = this.filenameInput.value.trim() || 'snippet';
        store.setFilename(name);

        // Extension detection if auto-detect enabled
        if (store.ui.isAutoDetect) {
          const dotIdx = name.lastIndexOf('.');
          if (dotIdx !== -1) {
            this.triggerAutoDetect(this.cm.getValue(), name);
          }
        }
      });
    }

    // Language selector dropdown
    if (this.languageSelect) {
      this.languageSelect.addEventListener('change', () => {
        const selected = this.languageSelect.value;
        if (selected === 'auto') {
          store.setLanguage(store.document.language || 'python', true);
          this.triggerAutoDetect(this.cm.getValue());
        } else {
          store.setLanguage(selected, false);
          const detectedBadge = document.getElementById('detectedLanguageBadge');
          if (detectedBadge) {
            detectedBadge.textContent = `Manual: ${this.languageSelect.options[this.languageSelect.selectedIndex]?.text || selected}`;
          }
        }
      });
    }
  }

  updateStats(text) {
    if (!text) {
      if (this.lineCountEl) this.lineCountEl.textContent = '0 lines';
      if (this.charCountEl) this.charCountEl.textContent = '0 chars';
      return;
    }
    const lines = text.split('\n').length;
    const chars = text.length;

    if (this.lineCountEl) this.lineCountEl.textContent = `${lines} ${lines === 1 ? 'line' : 'lines'}`;
    if (this.charCountEl) this.charCountEl.textContent = `${chars} chars`;
  }

  async triggerAutoDetect(code, filename = null) {
    if (!code || code.trim().length < 4) return;

    if (this.detectAbortController) {
      this.detectAbortController.abort();
    }
    this.detectAbortController = new AbortController();

    try {
      const res = await fetch(`${getApiBaseUrl()}/api/v1/detect-language`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          code,
          filename: filename || store.document.filename,
        }),
        signal: this.detectAbortController.signal,
      });

      const data = await res.json();
      if (data.success && data.data && data.data.detected && store.ui.isAutoDetect) {
        store.ui.detectedLanguage = data.data.language_name;
        store.setLanguage(data.data.language_id, true);

        const detectedBadge = document.getElementById('detectedLanguageBadge');
        if (detectedBadge) {
          detectedBadge.textContent = `Auto: ${data.data.language_name}`;
        }
      }
    } catch (err) {
      if (err.name !== 'AbortError') {
        console.warn('Auto-detect error:', err);
      }
    }
  }

  getValue() {
    return this.cm ? this.cm.getValue() : '';
  }

  setValue(val) {
    if (this.cm) {
      this.cm.setValue(val);
      this.updateStats(val);
    }
  }

  refresh() {
    if (this.cm) this.cm.refresh();
  }
}

export const editor = new CodeEditor();
