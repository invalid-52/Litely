"""Export engine for generating standalone HTML, SVG vector cards, and raw snippets.
"""

import html
from typing import Dict, Any

from litely.core.document import CodeDocument
from litely.services.highlighter import HighlightService
from litely.core.themes import ThemeRegistry


class ExportService:
    """Service for packaging code artifacts into exportable file formats."""

    @classmethod
    def export_standalone_html(cls, doc: CodeDocument) -> str:
        """Create a complete standalone HTML document with embedded CSS."""
        highlight_res = HighlightService.highlight_document(doc)
        theme_info = ThemeRegistry.resolve(doc.theme)
        s = doc.visualization

        # Base CSS needed for standalone rendering
        base_css = f"""
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #0f1117;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 2rem;
        }}
        .litely-card {{
            background: {theme_info.background};
            color: {theme_info.foreground};
            border-radius: {s.border_radius}px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(255, 255, 255, 0.1);
            overflow: hidden;
            font-family: '{s.font_family}', 'JetBrains Mono', monospace;
            font-size: {s.font_size}px;
            line-height: {s.line_height};
            max-width: 100%;
        }}
        .litely-card-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px 18px;
            background: rgba(255, 255, 255, 0.04);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            user-select: none;
        }}
        .litely-window-controls {{
            display: flex;
            gap: 8px;
        }}
        .litely-dot {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
            display: inline-block;
        }}
        .litely-dot.close {{ background: #ff5f56; }}
        .litely-dot.minimize {{ background: #ffbd2e; }}
        .litely-dot.maximize {{ background: #27c93f; }}
        .litely-card-title {{
            font-size: 13px;
            font-weight: 500;
            color: rgba(255, 255, 255, 0.7);
            text-align: center;
            flex-grow: 1;
        }}
        .litely-badge {{
            font-size: 11px;
            font-weight: 600;
            padding: 2px 8px;
            border-radius: 6px;
            background: rgba(255, 255, 255, 0.1);
            color: rgba(255, 255, 255, 0.8);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .litely-code-body {{
            padding: {s.padding}px;
            overflow-x: auto;
            margin: 0;
            white-space: {'pre-wrap' if s.word_wrap else 'pre'};
        }}
        .litely-line {{
            display: flex;
            min-height: 1.5em;
        }}
        .litely-line-highlight {{
            background: rgba(255, 255, 255, 0.08);
            margin: 0 -{s.padding}px;
            padding: 0 {s.padding}px;
        }}
        .litely-gutter {{
            display: inline-block;
            width: 3.2em;
            text-align: right;
            padding-right: 1.5em;
            color: rgba(255, 255, 255, 0.3);
            user-select: none;
            flex-shrink: 0;
        }}
        .litely-line-content {{
            flex-grow: 1;
        }}
        .litely-watermark {{
            padding: 6px 16px;
            text-align: right;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 1px;
            color: rgba(255, 255, 255, 0.25);
            border-top: 1px solid rgba(255, 255, 255, 0.05);
        }}
        {highlight_res['theme_css']}
        """

        doc_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(doc.filename or 'LITELY Code Artifact')}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600;700&family=Source+Code+Pro:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
{base_css}
    </style>
</head>
<body>
{highlight_res['html']}
</body>
</html>"""
        return doc_html

    @classmethod
    def export_svg(cls, doc: CodeDocument) -> str:
        """Create a standalone SVG vector code card for GitHub READMEs / Markdown."""
        highlight_res = HighlightService.highlight_document(doc)
        theme_info = ThemeRegistry.resolve(doc.theme)
        s = doc.visualization
        
        # Calculate dynamic height based on lines
        total_lines = highlight_res.get("total_lines", 1)
        line_height_px = int(s.font_size * s.line_height)
        content_height = (total_lines * line_height_px) + (s.padding * 2) + 50
        width = 800
        height = max(content_height, 120)

        # SVG markup using foreignObject for exact high-fidelity CSS and font rendering
        svg_markup = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <foreignObject width="100%" height="100%">
        <div xmlns="http://www.w3.org/1999/xhtml">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&amp;display=swap');
                *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
                .litely-svg-frame {{
                    width: 100%;
                    min-height: {height}px;
                    padding: 24px;
                    background: transparent;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-family: '{s.font_family}', 'JetBrains Mono', monospace;
                }}
                .litely-card {{
                    width: 100%;
                    background: {theme_info.background};
                    color: {theme_info.foreground};
                    border-radius: {s.border_radius}px;
                    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
                    overflow: hidden;
                    font-size: {s.font_size}px;
                    line-height: {s.line_height};
                }}
                .litely-card-header {{
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    padding: 10px 16px;
                    background: rgba(255, 255, 255, 0.05);
                    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
                }}
                .litely-window-controls {{ display: flex; gap: 6px; }}
                .litely-dot {{ width: 10px; height: 10px; border-radius: 50%; display: inline-block; }}
                .litely-dot.close {{ background: #ff5f56; }}
                .litely-dot.minimize {{ background: #ffbd2e; }}
                .litely-dot.maximize {{ background: #27c93f; }}
                .litely-card-title {{ font-size: 12px; color: rgba(255, 255, 255, 0.7); text-align: center; flex-grow: 1; }}
                .litely-badge {{ font-size: 10px; font-weight: 600; padding: 2px 6px; border-radius: 4px; background: rgba(255, 255, 255, 0.1); color: rgba(255, 255, 255, 0.8); text-transform: uppercase; }}
                .litely-code-body {{ padding: {s.padding}px; overflow: hidden; margin: 0; }}
                .litely-line {{ display: flex; }}
                .litely-gutter {{ width: 3em; text-align: right; padding-right: 1.2em; color: rgba(255, 255, 255, 0.3); flex-shrink: 0; }}
                .litely-line-content {{ flex-grow: 1; }}
                {highlight_res['theme_css']}
            </style>
            <div class="litely-svg-frame">
                {highlight_res['html']}
            </div>
        </div>
    </foreignObject>
</svg>"""
        return svg_markup
