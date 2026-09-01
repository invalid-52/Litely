/**
 * LITELY High-Fidelity Export Engine
 * Supports PNG (2x/3x DPI), Vector SVG, Standalone HTML, and Direct Clipboard Actions.
 * Includes specialized Rich-Text Word & Google Docs clipboard formatter with line numbers.
 */

import { store, getApiBaseUrl } from './state.js';
import { preview } from './preview.js';
import { toast } from './toast.js';

class ExportManager {
  constructor() {
    this.initialized = false;
  }

  init() {
    if (this.initialized) return;

    // Bind export button triggers
    const exportBtn = document.getElementById('exportMenuBtn');
    const exportMenu = document.getElementById('exportMenuDropdown');

    if (exportBtn && exportMenu) {
      exportBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        exportMenu.classList.toggle('open');
      });

      document.addEventListener('click', () => {
        exportMenu.classList.remove('open');
      });
    }

    // Bind action items
    document.querySelectorAll('[data-export-action]').forEach((item) => {
      item.addEventListener('click', (e) => {
        const action = e.currentTarget.getAttribute('data-export-action');
        this.handleAction(action);
      });
    });

    this.initialized = true;
  }

  async handleAction(action) {
    const code = store.document.source;
    if (!code || !code.trim()) {
      toast.error('Please paste or enter code before exporting.');
      return;
    }

    const filename = store.document.filename || 'code-snippet';
    const baseName = filename.replace(/\.[^/.]+$/, '');

    try {
      if (action === 'png') {
        toast.info('Rendering high-resolution PNG...');
        await this.exportPNG(`${baseName}.png`);
        toast.success('PNG exported successfully!');
      } else if (action === 'svg') {
        toast.info('Generating SVG vector card...');
        await this.exportSVG(`${baseName}.svg`);
        toast.success('SVG exported successfully!');
      } else if (action === 'html') {
        await this.exportHTML(`${baseName}.html`);
        toast.success('HTML exported successfully!');
      } else if (action === 'copy-word') {
        await this.copyForWordOrDocs();
        toast.success('All lines formatted & copied! Paste directly into Word, Docs, or Email.');
      } else if (action === 'copy-image') {
        toast.info('Rendering image to clipboard...');
        await this.copyImageToClipboard();
        toast.success('Image copied to clipboard!');
      } else if (action === 'copy-html') {
        await this.copyEmbeddableHtml();
        toast.success('Embeddable HTML code copied to clipboard!');
      } else if (action === 'copy-code') {
        await this.copyRawCode();
        toast.success('All source code lines copied to clipboard!');
      }
    } catch (err) {
      console.error('Export action failed:', err);
      toast.error('Failed to complete action: ' + err.message);
    }
  }

  async getWordCompatibleHtml() {
    if (preview.currentWordHtml) {
      return preview.currentWordHtml;
    }

    const res = await fetch(`${getApiBaseUrl()}/api/v1/highlight`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        code: store.document.source,
        language: store.ui.isAutoDetect ? 'auto' : store.document.language,
        filename: store.document.filename,
        theme: store.document.theme,
        visualization: store.document.visualization,
      }),
    });
    const json = await res.json();
    if (json.success && json.data && json.data.word_html) {
      preview.currentWordHtml = json.data.word_html;
      preview.currentEmbeddableHtml = json.data.embeddable_html || '';
      return json.data.word_html;
    }
    throw new Error('Could not generate formatted HTML');
  }

  async copyEmbeddableHtml() {
    let htmlCode = preview.currentEmbeddableHtml;
    if (!htmlCode) {
      await this.getWordCompatibleHtml();
      htmlCode = preview.currentEmbeddableHtml || preview.currentWordHtml;
    }
    if (!htmlCode) throw new Error('No HTML code generated');

    await navigator.clipboard.writeText(htmlCode);
  }

  async copyForWordOrDocs() {
    const code = store.document.source;
    if (!code || !code.trim()) throw new Error('Editor is empty');

    const wordHtml = await this.getWordCompatibleHtml();

    // Strategy 1: Modern navigator.clipboard.write with ClipboardItem (HTML + Plain Text)
    if (navigator.clipboard && navigator.clipboard.write && typeof ClipboardItem !== 'undefined') {
      try {
        const htmlBlob = new Blob([wordHtml], { type: 'text/html' });
        const textBlob = new Blob([code], { type: 'text/plain' });
        await navigator.clipboard.write([
          new ClipboardItem({
            'text/html': htmlBlob,
            'text/plain': textBlob,
          }),
        ]);
        return;
      } catch (clipErr) {
        console.warn('ClipboardItem write failed, falling back to copy event listener:', clipErr);
      }
    }

    // Strategy 2: Event Listener Copy with full HTML + Text payload
    let copySuccessful = false;
    const copyListener = (e) => {
      e.preventDefault();
      if (e.clipboardData) {
        e.clipboardData.setData('text/html', wordHtml);
        e.clipboardData.setData('text/plain', code);
        copySuccessful = true;
      }
    };

    document.addEventListener('copy', copyListener);
    try {
      document.execCommand('copy');
    } catch (e) {
      console.warn('execCommand copy failed:', e);
    }
    document.removeEventListener('copy', copyListener);

    // Strategy 3: Pure plain text fallback
    if (!copySuccessful) {
      await navigator.clipboard.writeText(code);
    }
  }

  async exportPNG(filename = 'litely-code.png', scale = 2) {
    try {
      const canvas = await this.renderDirectToCanvas(scale);
      await new Promise((resolve, reject) => {
        canvas.toBlob((blob) => {
          if (blob) {
            this.downloadBlob(blob, filename);
            resolve();
          } else {
            reject(new Error('Canvas blob generation failed'));
          }
        }, 'image/png');
      });
    } catch (err) {
      console.warn('Canvas export failed, falling back to SVG vector download:', err);
      // Fallback: download high-quality SVG vector card
      await this.exportSVG(filename.replace(/\.png$/, '.svg'));
    }
  }

  async exportSVG(filename = 'litely-code.svg') {
    const res = await fetch(`${getApiBaseUrl()}/api/v1/export`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...store.document,
        format: 'svg',
      }),
    });

    const json = await res.json();
    if (!json.success || !json.data) throw new Error(json.error?.message || 'SVG generation failed');

    const blob = new Blob([json.data.content], { type: 'image/svg+xml;charset=utf-8' });
    this.downloadBlob(blob, filename);
  }

  async exportHTML(filename = 'litely-code.html') {
    const res = await fetch(`${getApiBaseUrl()}/api/v1/export`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...store.document,
        format: 'html',
      }),
    });

    const json = await res.json();
    if (!json.success || !json.data) throw new Error(json.error?.message || 'HTML generation failed');

    const blob = new Blob([json.data.content], { type: 'text/html;charset=utf-8' });
    this.downloadBlob(blob, filename);
  }

  async copyImageToClipboard() {
    if (!navigator.clipboard || !navigator.clipboard.write) {
      throw new Error('Direct image clipboard is not supported in this browser.');
    }

    const canvas = await this.renderDirectToCanvas(2);
    const blob = await new Promise((resolve, reject) => {
      canvas.toBlob((b) => {
        if (b) resolve(b);
        else reject(new Error('Canvas image creation failed'));
      }, 'image/png');
    });

    await navigator.clipboard.write([
      new ClipboardItem({ 'image/png': blob }),
    ]);
  }

  async copyRawCode() {
    const code = store.document.source;
    if (!code) throw new Error('Editor is empty');

    await navigator.clipboard.writeText(code);
  }

  async renderDirectToCanvas(scale = 2) {
    if (document.fonts && document.fonts.ready) {
      try { await document.fonts.ready; } catch (_) {}
    }

    const cardEl = document.querySelector('.litely-card');
    const stageEl = document.getElementById('previewStage');
    const lines = Array.from(document.querySelectorAll('.litely-line'));

    const vis = store.document.visualization || {};
    const fontSize = Number(vis.font_size) || 14;
    const lineHeightMult = Number(vis.line_height) || 1.5;
    const lineHeight = fontSize * lineHeightMult;
    const fontFamily = vis.font_family ? `"${vis.font_family}", JetBrains Mono, monospace` : 'JetBrains Mono, monospace';
    const stagePad = Number(vis.padding) || 48;
    const cardRadius = Number(vis.border_radius) || 12;
    const showLineNumbers = vis.show_line_numbers !== false;
    const showWatermark = !!vis.show_watermark;
    const showBadge = vis.show_language_badge !== false;
    const windowChrome = vis.window_chrome || 'mac';
    const headerHeight = windowChrome !== 'none' ? 38 : 16;
    const filename = store.document.filename || 'code-snippet';
    const langInfo = store.document.language || 'code';

    // Measure text width using an offscreen canvas
    const measureCanvas = document.createElement('canvas');
    const mctx = measureCanvas.getContext('2d');
    mctx.font = `400 ${fontSize}px ${fontFamily}`;

    let maxCodeLineWidth = 300;
    lines.forEach((line) => {
      const contentEl = line.querySelector('.litely-line-content');
      const text = contentEl ? contentEl.textContent : line.textContent;
      const w = mctx.measureText(text).width;
      if (w > maxCodeLineWidth) maxCodeLineWidth = w;
    });

    const numDigits = Math.max(String(lines.length).length, 1);
    const gutterWidth = showLineNumbers ? (numDigits * (fontSize * 0.65) + 24) : 0;
    const cardContentWidth = maxCodeLineWidth + gutterWidth + 48;
    const cardWidth = Math.max(cardContentWidth, 480);
    const cardHeight = headerHeight + (Math.max(lines.length, 1) * lineHeight) + 32;

    const stageWidth = cardWidth + (stagePad * 2);
    const stageHeight = cardHeight + (stagePad * 2);

    const canvas = document.createElement('canvas');
    canvas.width = stageWidth * scale;
    canvas.height = stageHeight * scale;
    const ctx = canvas.getContext('2d');
    ctx.scale(scale, scale);

    // 1. Stage Background
    const bgPreset = vis.background_preset || 'twilight';
    this.paintStageBackground(ctx, bgPreset, stageWidth, stageHeight);

    // 2. Card Outer Shadow
    const cardX = stagePad;
    const cardY = stagePad;
    const shadowType = vis.shadow || 'medium';

    if (shadowType !== 'none') {
      ctx.save();
      ctx.shadowColor = 'rgba(0, 0, 0, 0.55)';
      ctx.shadowBlur = shadowType === 'dramatic' ? 45 : shadowType === 'soft' ? 18 : 30;
      ctx.shadowOffsetY = shadowType === 'dramatic' ? 22 : shadowType === 'soft' ? 8 : 14;
      ctx.fillStyle = '#0d1117';
      ctx.beginPath();
      if (ctx.roundRect) {
        ctx.roundRect(cardX, cardY, cardWidth, cardHeight, cardRadius);
      } else {
        ctx.rect(cardX, cardY, cardWidth, cardHeight);
      }
      ctx.fill();
      ctx.restore();
    }

    // 3. Card Background
    let cardBg = '#0d1117';
    if (cardEl) {
      const computed = window.getComputedStyle(cardEl);
      if (computed.backgroundColor && computed.backgroundColor !== 'transparent') {
        cardBg = computed.backgroundColor;
      }
    }

    ctx.save();
    ctx.fillStyle = cardBg;
    ctx.beginPath();
    if (ctx.roundRect) {
      ctx.roundRect(cardX, cardY, cardWidth, cardHeight, cardRadius);
    } else {
      ctx.rect(cardX, cardY, cardWidth, cardHeight);
    }
    ctx.fill();

    // Border
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.09)';
    ctx.lineWidth = 1;
    ctx.stroke();
    ctx.restore();

    // 4. Window Chrome Header
    if (windowChrome !== 'none') {
      ctx.save();
      // Divider
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(cardX, cardY + headerHeight);
      ctx.lineTo(cardX + cardWidth, cardY + headerHeight);
      ctx.stroke();

      if (windowChrome === 'mac') {
        // macOS dots (Close, Minimize, Maximize)
        const dotY = cardY + (headerHeight / 2);
        const dots = [
          { x: cardX + 16, color: '#ff5f56' },
          { x: cardX + 30, color: '#ffbd2e' },
          { x: cardX + 44, color: '#27c93f' },
        ];
        dots.forEach((d) => {
          ctx.fillStyle = d.color;
          ctx.beginPath();
          ctx.arc(d.x, dotY, 5, 0, Math.PI * 2);
          ctx.fill();
        });
      } else if (windowChrome === 'windows') {
        // Windows buttons
        ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
        ctx.font = '10px sans-serif';
        ctx.fillText('―', cardX + cardWidth - 48, cardY + 22);
        ctx.fillText('□', cardX + cardWidth - 32, cardY + 22);
        ctx.fillText('✕', cardX + cardWidth - 16, cardY + 22);
      }

      // Title in center
      ctx.font = `500 12px ${fontFamily}`;
      ctx.fillStyle = 'rgba(255, 255, 255, 0.65)';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(filename, cardX + (cardWidth / 2), cardY + (headerHeight / 2));

      // Badge in top right
      if (showBadge) {
        const badgeText = langInfo.toUpperCase();
        ctx.font = '700 9px monospace';
        const bw = ctx.measureText(badgeText).width + 12;
        const bx = cardX + cardWidth - bw - 14;
        const by = cardY + 10;
        ctx.fillStyle = 'rgba(255, 255, 255, 0.08)';
        ctx.beginPath();
        if (ctx.roundRect) ctx.roundRect(bx, by, bw, 18, 4);
        else ctx.rect(bx, by, bw, 18);
        ctx.fill();
        ctx.fillStyle = 'rgba(255, 255, 255, 0.75)';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(badgeText, bx + (bw / 2), by + 9);
      }
      ctx.restore();
    }

    // 5. Code Lines & Highlighted Tokens
    ctx.save();
    const codeStartY = cardY + headerHeight + 20;

    lines.forEach((lineEl, idx) => {
      const lineY = codeStartY + (idx * lineHeight);

      // Line Number Gutter
      if (showLineNumbers) {
        ctx.font = `400 ${fontSize * 0.9}px ${fontFamily}`;
        ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
        ctx.textAlign = 'right';
        ctx.textBaseline = 'middle';
        ctx.fillText(String(idx + 1), cardX + 18 + gutterWidth - 14, lineY);
      }

      // Code Tokens
      const contentEl = lineEl.querySelector('.litely-line-content');
      let tokenX = cardX + 18 + gutterWidth;
      ctx.font = `400 ${fontSize}px ${fontFamily}`;
      ctx.textAlign = 'left';
      ctx.textBaseline = 'middle';

      if (contentEl && contentEl.childNodes.length > 0) {
        contentEl.childNodes.forEach((node) => {
          const text = node.textContent;
          if (!text) return;

          if (node.nodeType === Node.ELEMENT_NODE) {
            const compColor = window.getComputedStyle(node).color;
            ctx.fillStyle = compColor || '#e6edf3';
          } else {
            ctx.fillStyle = '#e6edf3';
          }
          ctx.fillText(text, tokenX, lineY);
          tokenX += ctx.measureText(text).width;
        });
      } else {
        const text = lineEl.textContent;
        ctx.fillStyle = '#e6edf3';
        ctx.fillText(text, tokenX, lineY);
      }
    });

    // 6. Watermark
    if (showWatermark) {
      ctx.font = `700 9px ${fontFamily}`;
      ctx.fillStyle = 'rgba(255, 255, 255, 0.35)';
      ctx.textAlign = 'right';
      ctx.textBaseline = 'alphabetic';
      ctx.fillText('LITELY', cardX + cardWidth - 14, cardY + cardHeight - 10);
    }
    ctx.restore();

    return canvas;
  }

  paintStageBackground(ctx, preset, width, height) {
    if (preset === 'transparent') {
      ctx.clearRect(0, 0, width, height);
      return;
    }

    ctx.save();
    let bg;
    if (preset === 'midnight') {
      bg = ctx.createLinearGradient(0, 0, width, height);
      bg.addColorStop(0, '#0f172a');
      bg.addColorStop(1, '#1e293b');
    } else if (preset === 'aurora') {
      bg = ctx.createLinearGradient(0, 0, width, height);
      bg.addColorStop(0, '#059669');
      bg.addColorStop(0.5, '#0284c7');
      bg.addColorStop(1, '#4f46e5');
    } else if (preset === 'sunset') {
      bg = ctx.createLinearGradient(0, 0, width, height);
      bg.addColorStop(0, '#f43f5e');
      bg.addColorStop(0.5, '#d946ef');
      bg.addColorStop(1, '#6366f1');
    } else if (preset === 'matrix') {
      bg = ctx.createLinearGradient(0, 0, width, height);
      bg.addColorStop(0, '#022c22');
      bg.addColorStop(0.5, '#064e3b');
      bg.addColorStop(1, '#020617');
    } else if (preset === 'carbon') {
      bg = '#18181b';
    } else if (preset === 'snow') {
      bg = ctx.createLinearGradient(0, 0, width, height);
      bg.addColorStop(0, '#f8fafc');
      bg.addColorStop(1, '#e2e8f0');
    } else {
      // Default: Twilight radial gradient
      bg = ctx.createRadialGradient(width * 0.2, height * 0.2, 10, width * 0.5, height * 0.5, Math.max(width, height));
      bg.addColorStop(0, '#3b82f6');
      bg.addColorStop(0.4, '#6366f1');
      bg.addColorStop(1, '#1e1b4b');
    }

    ctx.fillStyle = bg;
    if (ctx.roundRect) {
      ctx.beginPath();
      ctx.roundRect(0, 0, width, height, 14);
      ctx.fill();
    } else {
      ctx.fillRect(0, 0, width, height);
    }
    ctx.restore();
  }

  downloadBlob(blob, filename) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => {
      if (a.parentNode) a.parentNode.removeChild(a);
      URL.revokeObjectURL(url);
    }, 1000);
  }
}

export const exporter = new ExportManager();
