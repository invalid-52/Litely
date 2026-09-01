/**
 * LITELY Keyboard Shortcuts Manager & Help Modal
 */

import { palette } from './palette.js';
import { exporter } from './export.js';
import { preview } from './preview.js';
import { store } from './state.js';

class ShortcutsManager {
  constructor() {
    this.shortcutsModal = null;
    this.initialized = false;
  }

  init() {
    if (this.initialized) return;
    this.shortcutsModal = document.getElementById('shortcutsModalBackdrop');
    this.bindGlobalShortcuts();

    const openShortcutsBtn = document.getElementById('openShortcutsBtn');
    if (openShortcutsBtn) {
      openShortcutsBtn.addEventListener('click', () => this.openModal());
    }

    if (this.shortcutsModal) {
      this.shortcutsModal.addEventListener('click', (e) => {
        if (e.target === this.shortcutsModal) this.closeModal();
      });
    }
    this.initialized = true;
  }

  bindGlobalShortcuts() {
    document.addEventListener('keydown', (e) => {
      const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
      const mod = isMac ? e.metaKey : e.ctrlKey;
      const activeTag = document.activeElement ? document.activeElement.tagName.toLowerCase() : '';
      const isInputFocused = activeTag === 'textarea' || activeTag === 'input';

      // Cmd / Ctrl + K: Command Palette
      if (mod && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        palette.open();
        return;
      }

      // Cmd / Ctrl + Enter: Force preview refresh
      if (mod && e.key === 'Enter') {
        e.preventDefault();
        preview.fetchAndRenderHighlight(store);
        return;
      }

      // Cmd / Ctrl + Shift + W: Copy for Word / Docs
      if (mod && e.shiftKey && e.key.toLowerCase() === 'w') {
        e.preventDefault();
        exporter.handleAction('copy-word');
        return;
      }

      // Cmd / Ctrl + Shift + C: Copy raw code
      if (mod && e.shiftKey && e.key.toLowerCase() === 'c') {
        e.preventDefault();
        exporter.handleAction('copy-code');
        return;
      }

      // Cmd / Ctrl + Shift + H: Copy highlighted HTML
      if (mod && e.shiftKey && e.key.toLowerCase() === 'h') {
        e.preventDefault();
        exporter.handleAction('copy-html');
        return;
      }

      // Cmd / Ctrl + Shift + P: Export PNG
      if (mod && e.shiftKey && e.key.toLowerCase() === 'p') {
        e.preventDefault();
        exporter.handleAction('png');
        return;
      }

      // Cmd / Ctrl + Shift + S: Export SVG
      if (mod && e.shiftKey && e.key.toLowerCase() === 's') {
        e.preventDefault();
        exporter.handleAction('svg');
        return;
      }

      // Escape: Close modals
      if (e.key === 'Escape') {
        palette.close();
        this.closeModal();
        const exportMenu = document.getElementById('exportMenuDropdown');
        if (exportMenu) exportMenu.classList.remove('open');
        return;
      }

      // ? key: Open shortcuts modal when not editing text
      if (e.key === '?' && !isInputFocused && !mod) {
        e.preventDefault();
        this.openModal();
      }
    });
  }

  openModal() {
    if (!this.shortcutsModal) this.shortcutsModal = document.getElementById('shortcutsModalBackdrop');
    if (!this.shortcutsModal) return;
    this.shortcutsModal.classList.add('open');
  }

  closeModal() {
    if (!this.shortcutsModal) this.shortcutsModal = document.getElementById('shortcutsModalBackdrop');
    if (!this.shortcutsModal) return;
    this.shortcutsModal.classList.remove('open');
  }
}

export const shortcuts = new ShortcutsManager();
