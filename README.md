````markdown
# 🌌 LITELY | Code Visualization & Developer Presentation Studio

**LITELY** is a lightweight developer-focused code visualization studio that transforms raw source code into polished, customizable, presentation-ready visuals.

Built around a simple idea:

> **Code should be easy to write, easy to style, and worth sharing.**

LITELY combines a browser-based code editor, automatic language detection, syntax highlighting, visual customization, live preview, rich clipboard support, and multi-format export into one focused workflow.

---

## 💡 Why I Built LITELY

Developers constantly need to share code across documentation, presentations, tutorials, portfolios, technical articles, classrooms, and social platforms.

The usual workflow is often:

```text
Open IDE
   ↓
Resize / clean the editor
   ↓
Take screenshot
   ↓
Crop it
   ↓
Fix formatting
   ↓
Try another tool
   ↓
Share
````

LITELY simplifies this into:

```text
Code
 ↓
Style
 ↓
Preview
 ↓
Export
 ↓
Share
```

The project focuses on removing the unnecessary gap between **writing code** and **presenting code professionally**.

---

## 🛑 Problem Statement

Code screenshots are convenient, but they are not always ideal.

Traditional approaches often introduce:

* IDE interface clutter
* Inconsistent visual styling
* Poor portability
* Difficult resizing
* Loss of selectable text
* Manual formatting work
* Separate tools for editing, styling, and exporting

LITELY provides a single workspace where the source code remains the source of truth while its presentation can be customized independently.

---

## 🎯 Solution

LITELY turns source code into a configurable visual document.

```text
                 SOURCE
                    │
                    ▼
          ┌─────────────────┐
          │   CodeMirror    │
          │     Editor      │
          └────────┬────────┘
                   │
                   ▼
          Language Detection
                   │
                   ▼
          Syntax Highlighting
                   │
                   ▼
         Visual Configuration
                   │
                   ▼
              Live Preview
                   │
          ┌────────┼────────┐
          ▼        ▼        ▼
         PNG      SVG      HTML
          │        │        │
          └────────┼────────┘
                   ▼
          Copy / Export / Share
```

---

## 🚀 Core Features

### 🧑‍💻 Advanced Code Editing

LITELY provides a CodeMirror-powered editor with:

* Syntax highlighting
* Line numbers
* Active-line highlighting
* Bracket matching
* Automatic bracket closing
* Tab indentation
* Undo / Redo
* Search and Replace
* Word wrapping
* Line statistics
* Character statistics
* Keyboard shortcuts

---

### 🔎 Automatic Language Detection

LITELY can determine the programming language from multiple sources instead of relying on a single detection method.

```text
Manual Selection
       │
       ▼
File Extension
       │
       ▼
Shebang Detection
       │
       ▼
Syntax Signatures
       │
       ▼
Lexer Detection
       │
       ▼
Language + Confidence
```

This is particularly useful when importing source files directly.

---

### 🎨 Visual Code Customization

The source code and its visual representation are treated separately.

Customize:

### Themes

* GitHub Dark
* Dracula
* One Dark
* Tokyo Night
* Nord
* Monokai
* Catppuccin
* Solarized
* GitHub Light
* Visual Studio
* One Light
* Friendly
* Minimal Light

### Fonts

* JetBrains Mono
* Fira Code
* IBM Plex Mono
* Source Code Pro
* Menlo
* Consolas

### Layout

* Font size
* Line height
* Padding
* Border radius
* Shadow / elevation
* Window chrome
* Line numbers
* Word wrapping
* Language badge
* Watermark

### Background

* Solid backgrounds
* Gradients
* Transparent backgrounds

---

## 👀 Live Preview

LITELY provides an interactive preview while the code and visual configuration are being changed.

The preview pipeline uses debounced rendering and request cancellation to reduce unnecessary rendering work during rapid editing.

This helps prevent stale preview requests from replacing newer results.

---

## 📁 Drag & Drop

Source files can be dropped directly into LITELY.

For example:

```text
main.py
app.js
server.go
query.sql
index.html
program.rs
```

The application uses available file information and source-code characteristics to determine the appropriate language before loading the document.

---

## 📋 Rich Clipboard

LITELY supports both plain and rich clipboard output.

```text
text/plain
     +
text/html
```

This allows highlighted code to be pasted into compatible applications while retaining its formatting.

Unlike an image-only workflow, the resulting code can remain selectable and reusable.

Useful for:

* Documentation
* Presentations
* Emails
* Tutorials
* Technical articles
* Notes
* Knowledge bases

---

## 📤 Multi-Format Export

LITELY supports multiple output formats for different workflows.

| Output        | Best For                        |
| ------------- | ------------------------------- |
| **PNG**       | Presentations, posts, tutorials |
| **SVG**       | Scalable graphics               |
| **HTML**      | Web content and embeds          |
| **RAW**       | Original source                 |
| **Clipboard** | Fast sharing and rich pasting   |

---

## 🧩 Code → HTML

LITELY can generate a portable HTML representation of highlighted source code.

```text
Source Code
     ↓
Language
     ↓
Syntax Tokens
     ↓
Theme
     ↓
Visual Configuration
     ↓
Standalone HTML
```

This allows the generated representation to be reused outside the application.

---

## ⌨️ Keyboard-First Workflow

Common actions are accessible through keyboard shortcuts.

### Command Palette

```text
Ctrl / Cmd + K
```

### Search

```text
Ctrl / Cmd + F
```

### Shortcut Reference

```text
?
```

The goal is to keep the workflow fast and minimize unnecessary navigation.

---

## 🧪 Built-in Samples

LITELY includes ready-to-use source examples so users can immediately explore the application.

Examples include:

* Python
* TypeScript
* Rust
* SQL
* Go

---

# 🏗️ System Architecture

```text
                  ┌──────────────────┐
                  │      USER        │
                  └────────┬─────────┘
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
           Paste        File Drop      Samples
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                    Code Document
                           │
                           ▼
                  Language Detection
                           │
                           ▼
                  Syntax Highlighting
                           │
                           ▼
                 Visualization Engine
                           │
                           ▼
                      Live Preview
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
             PNG          SVG          HTML
              │            │            │
              └────────────┼────────────┘
                           ▼
                   Clipboard / Export
```

---

# 🔌 REST API

LITELY includes a versioned REST API under:

```text
/api/v1
```

## Health Check

```http
GET /api/v1/health
```

Provides application/service status and capability information.

---

## Languages

```http
GET /api/v1/languages
```

Retrieve supported language metadata.

### Popular Languages

```http
GET /api/v1/languages?popular=true
```

---

## Themes

```http
GET /api/v1/themes
```

Retrieve available theme definitions.

---

## Language Detection

```http
POST /api/v1/detect-language
```

Example:

```json
{
  "code": "SELECT id, name FROM users;",
  "filename": "query.sql"
}
```

---

## Code Highlighting

```http
POST /api/v1/highlight
```

Example:

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

The API can provide:

* Highlighted HTML
* Theme information
* Language metadata
* Clipboard-ready HTML
* Embeddable HTML
* Document statistics

---

## Export API

```http
POST /api/v1/export
```

Server-side export formats include:

```text
HTML
SVG
RAW
```

PNG rendering and browser clipboard workflows are handled client-side.

---

# 🔐 Security & Reliability

LITELY treats submitted source code as **data**.

Submitted programs are not executed by the application.

The application also applies request and source-size limits to prevent unnecessarily large requests.

Current limits include:

```text
Maximum request payload: 1 MB
Maximum source-code length: 200,000 characters
```

API responses use a consistent structure:

```json
{
  "success": true,
  "data": {},
  "error": null
}
```

This keeps client-side API handling predictable across successful and failed requests.

---

# 🧪 Testing

LITELY includes automated tests covering core application behavior.

Run the test suite:

```bash
pytest -v
```

---

# 🛠️ Technology Stack

### Frontend

* HTML5
* CSS3
* JavaScript
* CodeMirror

### Backend

* Python
* Flask
* Pygments
* Gunicorn

### Rendering & Export

* Pygments tokenization
* DOM rendering
* Canvas-based PNG generation
* SVG generation
* HTML generation
* Browser Clipboard APIs

### Testing

* pytest

### Deployment

* Docker
* Gunicorn
* Render

---

# 📂 Repository Structure

```text
LITELY/
│
├── app.py
├── wsgi.py
├── requirements.txt
├── Dockerfile
├── Procfile
├── runtime.txt
│
├── litely/
│   ├── api/
│   │   └── v1/
│   │       ├── routes.py
│   │       └── schemas.py
│   │
│   ├── core/
│   │   ├── document.py
│   │   ├── languages.py
│   │   └── themes.py
│   │
│   ├── services/
│   │   ├── detector.py
│   │   ├── exporter.py
│   │   └── highlighter.py
│   │
│   └── web/
│       ├── routes.py
│       └── legacy.py
│
├── static/
│   ├── css/
│   ├── js/
│   ├── vendor/
│   │   └── codemirror/
│   └── assets/
│
├── templates/
│
└── tests/
```

---

# 💻 Local Development

## Requirements

* Python 3.10+
* pip

### Clone

```bash
git clone <YOUR_REPOSITORY_URL>
cd LITELY
```

### Create Virtual Environment

#### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

# 🐳 Docker

Build:

```bash
docker build -t litely .
```

Run:

```bash
docker run --rm -p 8000:8000 litely
```

Open:

```text
http://localhost:8000
```

---

# 🚀 Production

LITELY includes a WSGI entry point and can run with Gunicorn.

```bash
FLASK_ENV=production \
SECRET_KEY="replace-with-a-random-secret" \
gunicorn \
  --bind 0.0.0.0:8000 \
  --workers 2 \
  --timeout 30 \
  wsgi:app
```

---

# 🎯 Use Cases

### Developers

Create polished code visuals for:

* GitHub documentation
* Technical blogs
* Presentations
* Developer communities
* Architecture discussions

### Students

Present:

* Programming assignments
* Algorithms
* Coding solutions
* Project implementations
* Technical demonstrations

### Educators

Create code examples for:

* Lessons
* Workshops
* Tutorials
* Course material

### Technical Writers

Generate consistent code representations for:

* Documentation
* Guides
* Tutorials
* Knowledge bases

### Content Creators

Create code visuals for:

* Articles
* Videos
* Presentations
* Social content
* Developer education

---

# 📐 Design Principles

## Code First

The original source remains the source of truth.

Visual styling should not require modifying the underlying code.

## Fast Workflow

The journey from source code to finished visual should take seconds.

## Presentation Without a Design Tool

Developers should not need a graphics editor to create a professional-looking code visual.

## Portable Output

Generated results should remain useful outside LITELY.

```text
PNG
SVG
HTML
RAW
CLIPBOARD
```

## Developer-Centric

Editing, detection, highlighting, styling, exporting, and keyboard workflows are treated as parts of one developer experience.

---

# 🗺️ Roadmap

* [ ] Custom theme builder
* [ ] Additional language detection improvements
* [ ] More export presets
* [ ] Shareable code links
* [ ] Saved snippets
* [ ] Public/private snippet collections
* [ ] Browser extension
* [ ] VS Code integration
* [ ] Team workspaces
* [ ] API authentication
* [ ] Usage analytics
* [ ] Additional editor integrations

---

# 🌐 Live Demo

**[https://litely.onrender.com/](https://litely.onrender.com/)**

Open LITELY and turn your next piece of code into something worth sharing.

---

# ⭐ Project Highlights

```text
Developer-focused editor
        +
Automatic language detection
        +
Syntax highlighting
        +
Custom visual themes
        +
Live preview
        +
Rich clipboard
        +
PNG / SVG / HTML / RAW export
        +
REST API
        +
Docker deployment
        +
Automated testing
```

---

## LITELY

### Beautiful code. Instantly.

**Write it. Style it. Share it.**

```
```
