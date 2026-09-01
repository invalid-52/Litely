/**
 * LITELY Command Palette (Ctrl/Cmd + K)
 */

import { store } from './state.js';
import { exporter } from './export.js';
import { CODE_SAMPLES } from './samples.js';

class CommandPalette {
  constructor() {
    this.modal = null;
    this.input = null;
    this.resultsList = null;
    this.selectedIndex = 0;
    this.commands = [];
    this.filteredCommands = [];
    this.initialized = false;
  }

  init() {
    if (this.initialized) return;
    this.modal = document.getElementById('paletteModalBackdrop');
    this.input = document.getElementById('paletteSearchInput');
    this.resultsList = document.getElementById('paletteResultsList');

    this.registerCommands();
    this.bindEvents();
    this.initialized = true;
  }

  registerCommands() {
    this.commands = [
      // Quick Actions
      { id: 'copy-word', title: 'Copy for MS Word / Google Docs (with Line Numbers)', category: 'Clipboard', shortcut: '⌘⇧W', action: () => exporter.handleAction('copy-word') },
      { id: 'export-png', title: 'Export as PNG', category: 'Export', shortcut: '⌘⇧P', action: () => exporter.handleAction('png') },
      { id: 'export-svg', title: 'Export as SVG', category: 'Export', shortcut: '⌘⇧S', action: () => exporter.handleAction('svg') },
      { id: 'export-html', title: 'Export as HTML', category: 'Export', shortcut: '⌘⇧E', action: () => exporter.handleAction('html') },
      { id: 'copy-image', title: 'Copy Image to Clipboard', category: 'Clipboard', shortcut: '', action: () => exporter.handleAction('copy-image') },
      { id: 'copy-html', title: 'Copy Highlighted HTML', category: 'Clipboard', shortcut: '⌘⇧H', action: () => exporter.handleAction('copy-html') },
      { id: 'copy-code', title: 'Copy Raw Code', category: 'Clipboard', shortcut: '⌘⇧C', action: () => exporter.handleAction('copy-code') },

      // Dark Themes
      { id: 'theme-gh-dark', title: 'Theme: GitHub Dark', category: 'Theme', action: () => store.setTheme('github-dark') },
      { id: 'theme-dracula', title: 'Theme: Dracula', category: 'Theme', action: () => store.setTheme('dracula') },
      { id: 'theme-one-dark', title: 'Theme: One Dark Pro', category: 'Theme', action: () => store.setTheme('one-dark') },
      { id: 'theme-tokyo-night', title: 'Theme: Tokyo Night', category: 'Theme', action: () => store.setTheme('tokyo-night') },
      { id: 'theme-nord', title: 'Theme: Nord Arctic', category: 'Theme', action: () => store.setTheme('nord') },
      { id: 'theme-monokai', title: 'Theme: Monokai', category: 'Theme', action: () => store.setTheme('monokai') },
      { id: 'theme-catppuccin-mocha', title: 'Theme: Catppuccin Mocha', category: 'Theme', action: () => store.setTheme('catppuccin-mocha') },
      { id: 'theme-solarized-dark', title: 'Theme: Solarized Dark', category: 'Theme', action: () => store.setTheme('solarized-dark') },

      // Light Themes
      { id: 'theme-colorful', title: 'Theme: Colorful (Classic hilite.me)', category: 'Theme', action: () => store.setTheme('colorful') },
      { id: 'theme-friendly', title: 'Theme: Friendly Light', category: 'Theme', action: () => store.setTheme('friendly') },
      { id: 'theme-gh-light', title: 'Theme: GitHub Light', category: 'Theme', action: () => store.setTheme('github-light') },
      { id: 'theme-one-light', title: 'Theme: One Light', category: 'Theme', action: () => store.setTheme('one-light') },
      { id: 'theme-minimal-light', title: 'Theme: Minimal Light', category: 'Theme', action: () => store.setTheme('minimal-light') },
      { id: 'theme-vs', title: 'Theme: Visual Studio', category: 'Theme', action: () => store.setTheme('vs') },
      { id: 'theme-solarized-light', title: 'Theme: Solarized Light', category: 'Theme', action: () => store.setTheme('solarized-light') },
      { id: 'theme-catppuccin-latte', title: 'Theme: Catppuccin Latte', category: 'Theme', action: () => store.setTheme('catppuccin-latte') },

      // Languages
      { id: 'lang-python', title: 'Language: Python', category: 'Language', action: () => store.setLanguage('python', false) },
      { id: 'lang-typescript', title: 'Language: TypeScript', category: 'Language', action: () => store.setLanguage('typescript', false) },
      { id: 'lang-javascript', title: 'Language: JavaScript', category: 'Language', action: () => store.setLanguage('javascript', false) },
      { id: 'lang-rust', title: 'Language: Rust', category: 'Language', action: () => store.setLanguage('rust', false) },
      { id: 'lang-go', title: 'Language: Go', category: 'Language', action: () => store.setLanguage('go', false) },
      { id: 'lang-cpp', title: 'Language: C++', category: 'Language', action: () => store.setLanguage('cpp', false) },
      { id: 'lang-c', title: 'Language: C', category: 'Language', action: () => store.setLanguage('c', false) },
      { id: 'lang-csharp', title: 'Language: C#', category: 'Language', action: () => store.setLanguage('csharp', false) },
      { id: 'lang-java', title: 'Language: Java', category: 'Language', action: () => store.setLanguage('java', false) },
      { id: 'lang-kotlin', title: 'Language: Kotlin', category: 'Language', action: () => store.setLanguage('kotlin', false) },
      { id: 'lang-swift', title: 'Language: Swift', category: 'Language', action: () => store.setLanguage('swift', false) },
      { id: 'lang-sql', title: 'Language: SQL', category: 'Language', action: () => store.setLanguage('sql', false) },
      { id: 'lang-html', title: 'Language: HTML', category: 'Language', action: () => store.setLanguage('html', false) },
      { id: 'lang-css', title: 'Language: CSS', category: 'Language', action: () => store.setLanguage('css', false) },
      { id: 'lang-json', title: 'Language: JSON', category: 'Language', action: () => store.setLanguage('json', false) },
      { id: 'lang-yaml', title: 'Language: YAML', category: 'Language', action: () => store.setLanguage('yaml', false) },
      { id: 'lang-markdown', title: 'Language: Markdown', category: 'Language', action: () => store.setLanguage('markdown', false) },
      { id: 'lang-bash', title: 'Language: Bash / Shell', category: 'Language', action: () => store.setLanguage('bash', false) },
      { id: 'lang-dockerfile', title: 'Language: Dockerfile', category: 'Language', action: () => store.setLanguage('dockerfile', false) },

      // Toggles
      { id: 'toggle-linenos', title: 'Toggle Line Numbers', category: 'Options', action: () => store.setVisualization('show_line_numbers', !store.document.visualization.show_line_numbers) },
      { id: 'toggle-wrap', title: 'Toggle Word Wrap', category: 'Options', action: () => store.setVisualization('word_wrap', !store.document.visualization.word_wrap) },
      { id: 'toggle-badge', title: 'Toggle Language Badge', category: 'Options', action: () => store.setVisualization('show_language_badge', !store.document.visualization.show_language_badge) },
      { id: 'toggle-watermark', title: 'Toggle LITELY Watermark', category: 'Options', action: () => store.setVisualization('show_watermark', !store.document.visualization.show_watermark) },
      { id: 'toggle-customizer', title: 'Toggle Customizer Panel', category: 'Options', shortcut: '⌘/', action: () => window.litelyApp && window.litelyApp.toggleDrawer() },
      { id: 'reset-styles', title: 'Reset Customization Settings', category: 'Options', action: () => store.resetVisualization() },

      // Sample Snippets
      { id: 'sample-py', title: 'Insert Sample: Python Rate Limiter', category: 'Samples', action: () => this.loadSample('python') },
      { id: 'sample-ts', title: 'Insert Sample: TypeScript Transformer', category: 'Samples', action: () => this.loadSample('typescript') },
      { id: 'sample-rs', title: 'Insert Sample: Rust Concurrent Cache', category: 'Samples', action: () => this.loadSample('rust') },
      { id: 'sample-sql', title: 'Insert Sample: SQL Analytics Query', category: 'Samples', action: () => this.loadSample('sql') },
      { id: 'sample-go', title: 'Insert Sample: Go Worker Pool', category: 'Samples', action: () => this.loadSample('go') },
      { id: 'sample-js', title: 'Insert Sample: JavaScript Async Emitter', category: 'Samples', action: () => this.loadSample('javascript') },
    ];
  }

  loadSample(sampleKey) {
    const s = CODE_SAMPLES[sampleKey];
    if (s) {
      store.setLanguage(s.language, false);
      store.setFilename(s.filename);
      store.setTheme(s.theme);
      store.setSource(s.code);
    }
  }

  bindEvents() {
    const openBtn = document.getElementById('openPaletteBtn');
    if (openBtn) {
      openBtn.addEventListener('click', () => this.open());
    }

    if (!this.modal || !this.input) return;

    this.input.addEventListener('input', () => {
      this.filter(this.input.value);
    });

    this.input.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        this.selectedIndex = Math.min(this.selectedIndex + 1, this.filteredCommands.length - 1);
        this.renderResults();
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        this.selectedIndex = Math.max(this.selectedIndex - 1, 0);
        this.renderResults();
      } else if (e.key === 'Enter') {
        e.preventDefault();
        this.executeSelected();
      } else if (e.key === 'Escape') {
        this.close();
      }
    });

    this.modal.addEventListener('click', (e) => {
      if (e.target === this.modal) this.close();
    });
  }

  open() {
    if (!this.modal) this.modal = document.getElementById('paletteModalBackdrop');
    if (!this.input) this.input = document.getElementById('paletteSearchInput');
    if (!this.resultsList) this.resultsList = document.getElementById('paletteResultsList');
    if (!this.modal || !this.input) return;

    this.modal.classList.add('open');
    this.input.value = '';
    this.filter('');
    setTimeout(() => this.input.focus(), 50);
  }

  close() {
    if (!this.modal) return;
    this.modal.classList.remove('open');
  }

  filter(query) {
    const q = query.toLowerCase().trim();
    if (!q) {
      this.filteredCommands = [...this.commands];
    } else {
      this.filteredCommands = this.commands.filter(
        cmd => cmd.title.toLowerCase().includes(q) || cmd.category.toLowerCase().includes(q)
      );
    }
    this.selectedIndex = 0;
    this.renderResults();
  }

  renderResults() {
    if (!this.resultsList) return;
    this.resultsList.innerHTML = '';

    if (this.filteredCommands.length === 0) {
      const empty = document.createElement('div');
      empty.style.cssText = 'padding: 1rem; text-align: center; color: var(--text-muted);';
      empty.textContent = 'No commands found.';
      this.resultsList.appendChild(empty);
      return;
    }

    this.filteredCommands.forEach((cmd, idx) => {
      const item = document.createElement('div');
      item.className = `palette-item ${idx === this.selectedIndex ? 'selected' : ''}`;
      
      const leftDiv = document.createElement('div');
      leftDiv.className = 'palette-item-left';

      const catSpan = document.createElement('span');
      catSpan.style.fontSize = '0.75rem';
      catSpan.style.fontWeight = '600';
      catSpan.style.color = 'var(--brand-accent)';
      catSpan.textContent = cmd.category;

      const titleSpan = document.createElement('span');
      titleSpan.textContent = cmd.title;

      leftDiv.appendChild(catSpan);
      leftDiv.appendChild(titleSpan);
      item.appendChild(leftDiv);

      if (cmd.shortcut) {
        const scSpan = document.createElement('span');
        scSpan.className = 'palette-item-shortcut';
        scSpan.textContent = cmd.shortcut;
        item.appendChild(scSpan);
      }

      item.addEventListener('click', () => {
        this.selectedIndex = idx;
        this.executeSelected();
      });

      this.resultsList.appendChild(item);
    });

    const selectedEl = this.resultsList.children[this.selectedIndex];
    if (selectedEl) {
      selectedEl.scrollIntoView({ block: 'nearest' });
    }
  }

  executeSelected() {
    const cmd = this.filteredCommands[this.selectedIndex];
    if (cmd && cmd.action) {
      cmd.action();
      this.close();
    }
  }
}

export const palette = new CommandPalette();
