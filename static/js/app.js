/**
 * LITELY Main Application Bootstrap & Orchestrator
 * Manages Progressive Disclosure Landing View, 2-Pane Workspace, and Collapsible Customizer Drawer.
 */

import { store } from './state.js';
import { preview } from './preview.js';
import { editor } from './editor.js';
import { exporter } from './export.js';
import { palette } from './palette.js';
import { dragDrop } from './dragdrop.js';
import { shortcuts } from './shortcuts.js';
import { CODE_SAMPLES } from './samples.js';

class LitelyApp {
  constructor() {
    this.landingView = null;
    this.workspaceView = null;
    this.customizerDrawer = null;
    this.customizerBackdrop = null;
    this.init();
  }

  init() {
    this.landingView = document.getElementById('landingView');
    this.workspaceView = document.getElementById('workspaceView');
    this.customizerDrawer = document.getElementById('customizerDrawer');
    this.customizerBackdrop = document.getElementById('customizerBackdrop');

    // 1. Initialize UI theme before rendering
    this.initAppTheme();

    // 2. Initialize sub-controllers
    editor.init();
    preview.init();
    exporter.init();
    palette.init();
    dragDrop.init();
    shortcuts.init();

    // 3. Initialize UI components & interactions
    this.initLandingInteractions();
    this.initCustomizerDrawer();
    this.initCustomizerTabs();
    this.initEditorTabs();
    this.initAppearanceControls();
    this.initTypographyControls();
    this.initLayoutControls();
    this.initCodeControls();
    this.initThemeModeToggle();
    this.initBrandHome();

    // 4. Always present Landing Screen first on page load
    this.openLanding();
    if (store.document.source && editor.cm) {
      editor.setValue(store.document.source);
    }
  }

  openLanding() {
    if (this.landingView) this.landingView.style.display = 'flex';
    if (this.workspaceView) this.workspaceView.style.display = 'none';
  }

  openWorkspace(initialCode = null, language = null, filename = null) {
    if (this.landingView) this.landingView.style.display = 'none';
    if (this.workspaceView) this.workspaceView.style.display = 'flex';

    if (initialCode !== null) {
      store.setSource(initialCode);
      if (language) store.setLanguage(language, false);
      if (filename) store.setFilename(filename);

      if (editor.cm) {
        editor.setValue(initialCode);
      }
    }

    if (editor.cm) {
      setTimeout(() => {
        editor.cm.refresh();
        editor.cm.focus();
      }, 50);
    }

    preview.fetchAndRenderHighlight(store);
  }

  initLandingInteractions() {
    // 1. Paste Code Card
    const pasteCard = document.getElementById('landingPasteCard');
    if (pasteCard) {
      pasteCard.addEventListener('click', () => {
        // Try reading clipboard if supported, else open workspace preserving state or ready to type
        if (navigator.clipboard && navigator.clipboard.readText) {
          navigator.clipboard.readText().then((clipText) => {
            if (clipText && clipText.trim().length > 0) {
              this.openWorkspace(clipText, null, 'main.py');
              editor.triggerAutoDetect(clipText, 'main.py');
            } else {
              this.openWorkspace(store.document.source ? null : '', 'python', 'main.py');
            }
          }).catch(() => {
            // If clipboard permission is denied, open workspace without wiping existing content or fake success
            this.openWorkspace(store.document.source ? null : '', 'python', 'main.py');
          });
        } else {
          this.openWorkspace(store.document.source ? null : '', 'python', 'main.py');
        }
      });
      pasteCard.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          pasteCard.click();
        }
      });
    }

    // 2. Upload File Card
    const uploadCard = document.getElementById('landingUploadCard');
    const fileInput = document.getElementById('fileUploadInput');
    if (uploadCard && fileInput) {
      uploadCard.addEventListener('click', () => {
        fileInput.click();
      });
      uploadCard.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          uploadCard.click();
        }
      });
    }

    // 3. Landing Sample Chips
    document.querySelectorAll('.sample-chip').forEach((chip) => {
      chip.addEventListener('click', () => {
        const sampleKey = chip.getAttribute('data-sample');
        const s = CODE_SAMPLES[sampleKey];
        if (s) {
          store.setTheme(s.theme);
          this.openWorkspace(s.code, s.language, s.filename);
        }
      });
    });
  }

  initBrandHome() {
    const brandHomeBtn = document.getElementById('brandHomeBtn');
    if (brandHomeBtn) {
      brandHomeBtn.addEventListener('click', () => {
        // Toggle or return to landing
        this.openLanding();
      });
    }
  }

  initCustomizerDrawer() {
    const toggleBtn = document.getElementById('toggleCustomizerBtn');
    const closeBtn = document.getElementById('closeCustomizerBtn');

    if (toggleBtn && this.customizerDrawer) {
      toggleBtn.addEventListener('click', () => {
        this.toggleDrawer();
      });
    }

    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        this.closeDrawer();
      });
    }

    if (this.customizerBackdrop) {
      this.customizerBackdrop.addEventListener('click', () => {
        this.closeDrawer();
      });
    }

    // Close on ESC
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.customizerDrawer && this.customizerDrawer.classList.contains('open')) {
        this.closeDrawer();
      }
      // Shortcut Ctrl+/ or Cmd+/ to toggle customizer
      if ((e.ctrlKey || e.metaKey) && e.key === '/') {
        e.preventDefault();
        this.toggleDrawer();
      }
    });
  }

  toggleDrawer() {
    if (!this.customizerDrawer) return;
    const isOpen = this.customizerDrawer.classList.contains('open');
    if (isOpen) this.closeDrawer();
    else this.openDrawer();
  }

  openDrawer() {
    if (this.customizerDrawer) this.customizerDrawer.classList.add('open');
    if (this.customizerBackdrop) this.customizerBackdrop.classList.add('open');
  }

  closeDrawer() {
    if (this.customizerDrawer) this.customizerDrawer.classList.remove('open');
    if (this.customizerBackdrop) this.customizerBackdrop.classList.remove('open');
  }

  initAppTheme() {
    try {
      const saved = localStorage.getItem('litely_app_theme');
      if (saved === 'light') {
        document.body.classList.add('light-mode');
      } else if (saved === 'dark') {
        document.body.classList.remove('light-mode');
      } else {
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
          document.body.classList.add('light-mode');
        }
      }
    } catch (e) {
      console.warn('Could not read localStorage for app theme:', e);
    }
  }

  initThemeModeToggle() {
    const toggles = [
      document.getElementById('appThemeModeToggle'),
      document.getElementById('landingAppThemeToggle'),
    ];

    toggles.forEach((btn) => {
      if (btn) {
        btn.addEventListener('click', () => {
          document.body.classList.toggle('light-mode');
          const isLight = document.body.classList.contains('light-mode');
          try {
            localStorage.setItem('litely_app_theme', isLight ? 'light' : 'dark');
          } catch (e) {
            console.warn('Could not save app theme to localStorage:', e);
          }
        });
      }
    });
  }

  initCustomizerTabs() {
    const tabs = document.querySelectorAll('.customizer-tab');
    const sections = {
      appearance: document.getElementById('tabSectionAppearance'),
      typography: document.getElementById('tabSectionTypography'),
      layout: document.getElementById('tabSectionLayout'),
      code: document.getElementById('tabSectionCode'),
    };

    tabs.forEach((tab) => {
      tab.addEventListener('click', () => {
        const target = tab.getAttribute('data-tab');
        tabs.forEach(t => {
          t.classList.remove('active');
          t.setAttribute('aria-selected', 'false');
        });
        tab.classList.add('active');
        tab.setAttribute('aria-selected', 'true');

        Object.keys(sections).forEach((k) => {
          if (sections[k]) {
            sections[k].style.display = (k === target) ? 'flex' : 'none';
          }
        });
      });
    });
  }

  initEditorTabs() {
    const tabSource = document.getElementById('editorTabSource');
    const tabHtml = document.getElementById('editorTabHtml');
    const containerSource = document.getElementById('sourceEditorContainer');
    const containerHtml = document.getElementById('htmlOutputContainer');
    const htmlTextarea = document.getElementById('htmlOutputTextarea');

    if (tabSource && tabHtml && containerSource && containerHtml) {
      tabSource.addEventListener('click', () => {
        tabSource.classList.add('active');
        tabHtml.classList.remove('active');
        containerSource.style.display = 'flex';
        containerHtml.style.display = 'none';
        if (editor.cm) editor.cm.refresh();
      });

      tabHtml.addEventListener('click', () => {
        tabHtml.classList.add('active');
        tabSource.classList.remove('active');
        containerHtml.style.display = 'flex';
        containerSource.style.display = 'none';

        if (htmlTextarea && preview.currentEmbeddableHtml) {
          htmlTextarea.value = preview.currentEmbeddableHtml;
        }
      });
    }

    if (htmlTextarea) {
      htmlTextarea.addEventListener('click', () => {
        htmlTextarea.select();
      });
    }
  }

  initAppearanceControls() {
    const themeOptions = document.querySelectorAll('.theme-card-option');
    themeOptions.forEach((opt) => {
      opt.addEventListener('click', () => {
        const themeId = opt.getAttribute('data-theme-id');
        themeOptions.forEach(o => o.classList.remove('active'));
        opt.classList.add('active');
        store.setTheme(themeId);
      });
    });

    const bgBtns = document.querySelectorAll('.bg-preset-btn');
    bgBtns.forEach((btn) => {
      btn.addEventListener('click', () => {
        const bgVal = btn.getAttribute('data-bg');
        bgBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        store.setVisualization('background_value', bgVal);
      });
    });

    const chromeBtns = document.querySelectorAll('[data-chrome]');
    chromeBtns.forEach((btn) => {
      btn.addEventListener('click', () => {
        const val = btn.getAttribute('data-chrome');
        chromeBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        store.setVisualization('window_chrome', val);
      });
    });
  }

  initTypographyControls() {
    const fontSelect = document.getElementById('fontFamilySelect');
    if (fontSelect) {
      fontSelect.value = store.document.visualization.font_family;
      fontSelect.addEventListener('change', () => {
        store.setVisualization('font_family', fontSelect.value);
      });
    }

    const fontSizeSlider = document.getElementById('fontSizeSlider');
    const fontSizeBadge = document.getElementById('fontSizeBadge');
    if (fontSizeSlider) {
      fontSizeSlider.value = store.document.visualization.font_size;
      if (fontSizeBadge) fontSizeBadge.textContent = `${fontSizeSlider.value}px`;

      fontSizeSlider.addEventListener('input', () => {
        const val = parseInt(fontSizeSlider.value, 10);
        if (fontSizeBadge) fontSizeBadge.textContent = `${val}px`;
        store.setVisualization('font_size', val);
      });
    }

    const lineHeightSlider = document.getElementById('lineHeightSlider');
    const lineHeightBadge = document.getElementById('lineHeightBadge');
    if (lineHeightSlider) {
      lineHeightSlider.value = store.document.visualization.line_height;
      if (lineHeightBadge) lineHeightBadge.textContent = `${lineHeightSlider.value}x`;

      lineHeightSlider.addEventListener('input', () => {
        const val = parseFloat(lineHeightSlider.value);
        if (lineHeightBadge) lineHeightBadge.textContent = `${val}x`;
        store.setVisualization('line_height', val);
      });
    }
  }

  initLayoutControls() {
    const paddingSlider = document.getElementById('paddingSlider');
    const paddingBadge = document.getElementById('paddingBadge');
    if (paddingSlider) {
      paddingSlider.value = store.document.visualization.padding;
      if (paddingBadge) paddingBadge.textContent = `${paddingSlider.value}px`;

      paddingSlider.addEventListener('input', () => {
        const val = parseInt(paddingSlider.value, 10);
        if (paddingBadge) paddingBadge.textContent = `${val}px`;
        store.setVisualization('padding', val);
      });
    }

    const radiusSlider = document.getElementById('radiusSlider');
    const radiusBadge = document.getElementById('radiusBadge');
    if (radiusSlider) {
      radiusSlider.value = store.document.visualization.border_radius;
      if (radiusBadge) radiusBadge.textContent = `${radiusSlider.value}px`;

      radiusSlider.addEventListener('input', () => {
        const val = parseInt(radiusSlider.value, 10);
        if (radiusBadge) radiusBadge.textContent = `${val}px`;
        store.setVisualization('border_radius', val);
      });
    }

    const shadowBtns = document.querySelectorAll('[data-shadow]');
    shadowBtns.forEach((btn) => {
      btn.addEventListener('click', () => {
        const val = btn.getAttribute('data-shadow');
        shadowBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        store.setVisualization('shadow', val);
      });
    });
  }

  initCodeControls() {
    const toggles = [
      { id: 'toggleLineNumbers', key: 'show_line_numbers' },
      { id: 'toggleWordWrap', key: 'word_wrap' },
      { id: 'toggleLanguageBadge', key: 'show_language_badge' },
      { id: 'toggleWatermark', key: 'show_watermark' },
    ];

    toggles.forEach(({ id, key }) => {
      const toggleEl = document.getElementById(id);
      if (toggleEl) {
        toggleEl.addEventListener('click', () => {
          toggleEl.classList.toggle('active');
          const isActive = toggleEl.classList.contains('active');
          toggleEl.setAttribute('aria-checked', isActive ? 'true' : 'false');
          store.setVisualization(key, isActive);
        });
      }
    });
  }
}

// Global bootstrap
function startApp() {
  window.litelyApp = new LitelyApp();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', startApp);
} else {
  startApp();
}
