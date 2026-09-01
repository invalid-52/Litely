# LITELY — V1

> **Beautiful code. Instantly.**

LITELY is a modern, developer-focused platform for transforming source code into beautiful, readable, customizable, and exportable visual code artifacts.

---

## Features

- **Professional CodeMirror Editor**:
  - Live syntax highlighting for 30+ languages.
  - Line numbers, active line highlighting, bracket matching, and auto-closing brackets.
  - Tab indentation (4 spaces) & Shift+Tab unindent.
  - In-editor search & replace (<kbd>Ctrl+F</kbd> / <kbd>⌘F</kbd>).
  - Word wrap toggle, undo/redo history, and live line/char statistics.
- **Dual-Mode Editor (`[ Source Code ]` & `[ HTML Output ]`)**:
  - Direct live view of self-contained embeddable HTML with inline styles.
  - 1-click **Copy HTML Code** button and auto-select on click.
- **Universal Multi-Line Formatted Clipboard Engine**:
  - Specialized 2-column table clipboard payload with inlined Pygments token styles and matching line numbers.
  - Pastes formatted code with full colors and line numbers into **Microsoft Word**, **Google Docs**, **Outlook**, **Gmail**, **Notion**, and **Apple Pages**.
  - Dual-MIME (`text/html` + `text/plain`) architecture with synchronous clipboard event fallback.
- **Real-Time Live Preview**:
  - Debounced rendering protected by `AbortController` cancellation and request ID sequencing.
  - Zero-flicker updates preserving previous valid state during transient errors.
  - Selectable line numbers directly in the preview card (<kbd>user-select: text</kbd>).
- **Deterministic Language Detection**:
  - Multi-tier detection hierarchy: Explicit user selection &rarr; Filename extension &rarr; Shebang &rarr; Signature heuristics &rarr; Pygments lexer guess.
- **Curated Theme System**:
  - Dark & light theme families with visual swatches (*GitHub Dark, Dracula, One Dark, Nord, Tokyo Night, Monokai, Catppuccin Mocha, Solarized Dark/Light, Colorful Classic, Friendly Light, Visual Studio, One Light, Minimal Light*).
  - Independent **Application UI Dark/Light Theme** with `localStorage` persistence and `prefers-color-scheme` support.
- **Customization Controls**:
  - Typography: Monospace fonts (*JetBrains Mono, Fira Code, IBM Plex Mono, Source Code Pro, Menlo, Consolas*), font size, line height.
  - Layout: Card padding, border radius, elevation shadows (*None, Soft, Medium, Dramatic*).
  - Backgrounds: Solid, gradient presets (*Twilight, Midnight, Aurora, Sunset, Matrix, Carbon, Snow, Transparent*).
  - Window Chrome: macOS traffic lights, Windows controls, or minimal/none.
  - Code Options: Line numbers, word wrap, language badges, and watermarks.
- **High-Fidelity Export Pipeline**:
  - **PNG**: High-DPI (2x) raster export with font pre-warming (`document.fonts.ready`).
  - **SVG**: Valid XML vector card markup.
  - **HTML**: Standalone self-contained HTML files with embedded styling.
  - **Direct Clipboard Actions**: Copy Formatted, Copy Code, Copy HTML, Copy Image.
- **Developer Workflow**:
  - **Command Palette (`Ctrl/Cmd + K`)**: Keyboard-navigable fuzzy command execution.
  - **Keyboard Shortcuts (`?`)**: Quick actions for high-velocity power users.
  - **Drag & Drop**: Drop source code files (`.py`, `.ts`, `.rs`, `.go`, `.sql`, etc.) for instant parsing.
  - **Curated Sample Presets**: Jumpstart with sample snippets in Python, TypeScript, Rust, SQL, and Go.

---

## Architecture Pipeline

```text
INPUT (User Paste / File Drop / Preset / API)
  ↓
CodeDocument (source, language, filename, theme, visualization, metadata)
  ↓
Language Resolution (LanguageRegistry + Heuristic Detection)
  ↓
Syntax Highlighting Service (Pygments / Inlined Tokens)
  ↓
Visualization Configuration (Themes, Chrome, Typography, Backdrop)
  ↓
Live Preview Renderer (DOM Code Card + Window Chrome + Scaled Viewport)
  ↓
Export Engine (PNG @ High-DPI, Vector SVG, Standalone HTML, Dual-MIME Clipboard)
```

---

## Project Structure

```text
code_highlighter/
├── app.py                     # Application entry point
├── requirements.txt           # Python dependencies
├── litely/
│   ├── __init__.py            # Application factory (create_app)
│   ├── config.py              # Configuration limits & defaults
│   ├── core/
│   │   ├── document.py        # Canonical CodeDocument & Visualization models
│   │   ├── languages.py       # Centralized LanguageRegistry
│   │   └── themes.py          # Centralized ThemeRegistry & swatches
│   ├── services/
│   │   ├── highlighter.py     # Pygments syntax highlighting service
│   │   ├── detector.py        # Deterministic language detection
│   │   └── exporter.py        # Standalone HTML & SVG export generator
│   ├── api/
│   │   └── v1/
│   │       ├── routes.py      # REST API v1 endpoints
│   │       └── schemas.py     # Payload validation & standard response envelopes
│   └── web/
│       ├── routes.py          # Web UI routes
│       └── legacy.py          # Backward compatibility layer for legacy /api
├── static/
│   ├── css/
│   │   └── litely.css         # Design system & CodeMirror theme stylesheet
│   ├── vendor/
│   │   └── codemirror/        # Locally vendored CodeMirror core & language modes
│   └── js/
│       ├── app.js             # Main frontend application bootstrap
│       ├── state.js           # Observable state store
│       ├── editor.js          # CodeMirror editor controller
│       ├── preview.js         # Live preview & card renderer with AbortController
│       ├── export.js          # Export engine (PNG, SVG, HTML, Clipboard)
│       ├── palette.js         # Command palette (Cmd+K)
│       ├── dragdrop.js        # File drag & drop handler
│       ├── shortcuts.js       # Global keyboard shortcuts
│       ├── toast.js           # Toast notification manager
│       └── samples.js         # Curated sample snippets
├── templates/
│   ├── index.html             # Semantic application shell
│   └── api.txt                # Plain-text API reference
└── tests/                     # Automated test suite (41 test cases)
```

---

## Quickstart

### Prerequisites
- Python 3.10+

### Installation

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt
```

### Run Locally

```bash
python app.py
```
Open **http://127.0.0.1:5000** in your browser.

---

## REST API v1 Reference

### 1. Highlight Code
`POST /api/v1/highlight`

```json
{
  "code": "def hello():\n    print('Hello LITELY!')",
  "language": "python",
  "theme": "github-dark",
  "filename": "main.py",
  "visualization": {
    "font_family": "JetBrains Mono",
    "font_size": 14,
    "line_height": 1.5,
    "show_line_numbers": true,
    "padding": 32,
    "border_radius": 12,
    "window_chrome": "mac"
  }
}
```

### 2. Detect Language
`POST /api/v1/detect-language`

```json
{
  "code": "SELECT id, name FROM users;",
  "filename": "query.sql"
}
```

### 3. Export Artifact
`POST /api/v1/export`

```json
{
  "code": "fn main() { println!(\"LITELY\"); }",
  "language": "rust",
  "theme": "tokyo-night",
  "format": "html"
}
```

### 4. Health & Registries
- `GET /api/v1/languages` — List supported languages
- `GET /api/v1/themes` — List curated themes
- `GET /api/v1/health` — Service health probe

---

## Running Tests

Run the complete automated test suite with pytest:

```bash
pytest -v
```

---

## License
MIT
## Production deployment

LITELY includes a production WSGI entry point (`wsgi.py`), Gunicorn configuration, and a minimal Docker image.

### Local production-style run

```bash
pip install -r requirements.txt
FLASK_ENV=production SECRET_KEY="replace-with-a-random-secret" gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 30 wsgi:app
```

### Docker

```bash
docker build -t litely:1.0 .
docker run --rm -p 8000:8000 -e SECRET_KEY="replace-with-a-random-secret" litely:1.0
```

The application is a stateless Flask service with static frontend assets. Source code is never executed by the server. Clipboard image support depends on the browser and secure-context capabilities.

### Final verification

Install dependencies first, then run `pytest -v`. Also perform browser QA for paste/upload, editing, detection, customization, preview, PNG/SVG/HTML export, and clipboard behavior because browser APIs cannot be completely verified by server-side tests.

