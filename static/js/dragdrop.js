/**
 * LITELY Drag and Drop File Handler
 */

import { store, getApiBaseUrl } from './state.js';
import { toast } from './toast.js';

class DragDropHandler {
  constructor() {
    this.initialized = false;
  }

  init() {
    if (this.initialized) return;

    const dropzones = [
      document.getElementById('codeEditorPane'),
      document.body,
    ];

    dropzones.forEach((zone) => {
      if (!zone) return;

      zone.addEventListener('dragover', (e) => {
        e.preventDefault();
        e.stopPropagation();
        zone.classList.add('drag-active');
      });

      zone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        e.stopPropagation();
        zone.classList.remove('drag-active');
      });

      zone.addEventListener('drop', (e) => {
        e.preventDefault();
        e.stopPropagation();
        zone.classList.remove('drag-active');

        const files = e.dataTransfer.files;
        if (files && files.length > 0) {
          if (files.length > 1) {
            toast.info('Multiple files detected: loading the first file.');
          }
          this.loadFile(files[0]);
        }
      });
    });

    const fileInput = document.getElementById('fileUploadInput');
    const uploadBtn = document.getElementById('uploadFileBtn');

    if (uploadBtn && fileInput) {
      uploadBtn.addEventListener('click', () => fileInput.click());
      fileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files.length > 0) {
          this.loadFile(e.target.files[0]);
        }
      });
    }

    this.initialized = true;
  }

  loadFile(file) {
    if (!file) return;

    if (file.size > 1024 * 1024) {
      toast.error('File size exceeds 1MB limit.');
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      const content = e.target.result;
      const filename = file.name;

      if (window.litelyApp && window.litelyApp.openWorkspace) {
        window.litelyApp.openWorkspace(content, null, filename);
      } else {
        store.setFilename(filename);
        store.setSource(content);
      }

      const dotIdx = filename.lastIndexOf('.');
      if (dotIdx !== -1) {
        fetch(`${getApiBaseUrl()}/api/v1/detect-language`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ code: content, filename }),
        })
          .then(res => res.json())
          .then(json => {
            if (json.success && json.data && json.data.detected) {
              store.setLanguage(json.data.language_id, false);
            }
          })
          .catch(() => {});
      }

      toast.success(`Loaded file: ${filename}`);
    };

    reader.onerror = () => {
      toast.error('Failed to read file.');
    };

    reader.readAsText(file);
  }
}

export const dragDrop = new DragDropHandler();
