/**
 * LITELY Live Preview & Code Card Renderer
 * Hardened with AbortController cancellation, sequential request ID tracking,
 * smooth debouncing, and graceful error recovery without preview destruction.
 */

import { store, getApiBaseUrl } from './state.js';

class PreviewRenderer {
  constructor() {
    this.stageEl = null;
    this.viewportEl = null;
    this.loadingIndicator = null;
    this.debounceTimer = null;
    this.abortController = null;
    this.currentRequestId = 0;
    this.currentWordHtml = '';
    this.currentEmbeddableHtml = '';
    this.errorIndicator = null;
    this.initialized = false;
  }

  init() {
    if (this.initialized) return;
    this.stageEl = document.getElementById('previewStage');
    this.viewportEl = document.getElementById('previewViewport');
    this.loadingIndicator = document.getElementById('previewLoadingSpinner');
    this.errorIndicator = document.getElementById('previewErrorIndicator');

    if (!this.stageEl) return;
    this.initialized = true;

    // Subscribe to state changes
    store.subscribe((state, changeType) => {
      this.handleStateChange(state, changeType);
    });
  }

  handleStateChange(state, changeType) {
    if (changeType === 'visualization') {
      this.updateCardStyles(state);
    }

    clearTimeout(this.debounceTimer);
    this.debounceTimer = setTimeout(() => {
      this.fetchAndRenderHighlight(state);
    }, 120);
  }

  setError(message = '') {
    if (!this.errorIndicator) return;
    this.errorIndicator.textContent = message;
    this.errorIndicator.style.display = message ? 'inline-flex' : 'none';
  }

  setLoading(isLoading) {
    if (this.loadingIndicator) {
      this.loadingIndicator.style.display = isLoading ? 'inline-flex' : 'none';
    }
  }

  updateCardStyles(state) {
    if (!this.stageEl) this.stageEl = document.getElementById('previewStage');
    const s = state.document.visualization;

    if (this.stageEl) {
      this.stageEl.className = `litely-stage bg-preset-${s.background_value}`;
      this.stageEl.style.padding = `${s.padding + 16}px`;

      if (s.shadow === 'none') {
        this.stageEl.style.boxShadow = 'none';
      } else if (s.shadow === 'soft') {
        this.stageEl.style.setProperty('--shadow-card', '0 10px 25px -5px rgba(0, 0, 0, 0.3)');
      } else if (s.shadow === 'dramatic') {
        this.stageEl.style.setProperty('--shadow-card', '0 35px 70px -15px rgba(0, 0, 0, 0.8), 0 0 0 1px rgba(255, 255, 255, 0.15)');
      } else {
        this.stageEl.style.removeProperty('--shadow-card');
      }
    }

    const card = document.querySelector('.litely-card');
    if (card) {
      card.style.setProperty('--litely-font-size', `${s.font_size}px`);
      card.style.setProperty('--litely-line-height', s.line_height);
      card.style.setProperty('--litely-radius', `${s.border_radius}px`);
      card.style.fontFamily = `'${s.font_family}', monospace`;

      const lines = card.querySelectorAll('.litely-line-content');
      lines.forEach(l => {
        if (s.word_wrap) {
          l.classList.add('litely-wrap');
        } else {
          l.classList.remove('litely-wrap');
        }
      });

      const gutters = card.querySelectorAll('.litely-gutter');
      gutters.forEach(g => {
        g.style.display = s.show_line_numbers ? 'inline-block' : 'none';
      });

      const badge = card.querySelector('.litely-badge');
      if (badge) badge.style.display = s.show_language_badge ? 'inline-block' : 'none';

      const wm = card.querySelector('.litely-watermark');
      if (wm) wm.style.display = s.show_watermark ? 'block' : 'none';
    }
  }

  async fetchAndRenderHighlight(state) {
    if (!this.stageEl) this.stageEl = document.getElementById('previewStage');
    if (!this.stageEl) return;

    const source = state.document.source;
    if (!source || !source.trim()) {
      this.renderEmptyState();
      return;
    }

    // Cancel any previous in-flight request
    if (this.abortController) {
      this.abortController.abort();
    }
    this.abortController = new AbortController();
    const requestId = ++this.currentRequestId;

    this.setError('');
    this.setLoading(true);

    try {
      const response = await fetch(`${getApiBaseUrl()}/api/v1/highlight`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          code: source,
          language: state.ui.isAutoDetect ? 'auto' : state.document.language,
          filename: state.document.filename,
          theme: state.document.theme,
          visualization: state.document.visualization,
        }),
        signal: this.abortController.signal,
      });

      // Ignore stale responses
      if (requestId !== this.currentRequestId) {
        return;
      }

      if (!response.ok) {
        throw new Error(`Highlight API failed (${response.status})`);
      }

      const json = await response.json();
      if (json.success && json.data) {
        this.currentWordHtml = json.data.word_html || '';
        this.currentEmbeddableHtml = json.data.embeddable_html || '';

        // Update HTML output textarea in real time
        const htmlTextarea = document.getElementById('htmlOutputTextarea');
        if (htmlTextarea && json.data.embeddable_html) {
          htmlTextarea.value = json.data.embeddable_html;
        }

        this.renderCardHtml(json.data.html, json.data.theme_css, state);

        if (state.ui.isAutoDetect && json.data.language) {
          state.ui.detectedLanguage = json.data.language_name;
          const detectedBadge = document.getElementById('detectedLanguageBadge');
          if (detectedBadge) {
            detectedBadge.textContent = `Auto: ${json.data.language_name}`;
          }
        }
      } else {
        throw new Error(json.error?.message || 'Unable to render preview');
      }
    } catch (err) {
      if (err.name !== 'AbortError') {
        this.setError('Preview update failed — showing the last valid result.');
        console.warn('Highlight request error (preserving current preview):', err);
      }
    } finally {
      if (requestId === this.currentRequestId) {
        this.setLoading(false);
      }
    }
  }

  renderEmptyState() {
    if (!this.stageEl) return;
    this.stageEl.innerHTML = `
      <div class="litely-empty-preview">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="color: var(--text-muted); opacity: 0.6; margin-bottom: 0.75rem;"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>
        <p style="font-weight: 600; font-size: 0.95rem; color: var(--text-secondary); margin-bottom: 0.25rem;">No code to preview</p>
        <p style="font-size: 0.8rem; color: var(--text-muted);">Type or paste code in the editor, or pick a sample.</p>
      </div>
    `;
  }

  renderCardHtml(htmlMarkup, themeCss, state) {
    if (!this.stageEl) this.stageEl = document.getElementById('previewStage');
    if (!this.stageEl) return;

    let themeStyleEl = document.getElementById('litelyThemeStyle');
    if (!themeStyleEl) {
      themeStyleEl = document.createElement('style');
      themeStyleEl.id = 'litelyThemeStyle';
      document.head.appendChild(themeStyleEl);
    }
    themeStyleEl.textContent = themeCss || '';

    this.stageEl.innerHTML = htmlMarkup;
    this.updateCardStyles(state);
  }
}

export const preview = new PreviewRenderer();
