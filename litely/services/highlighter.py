"""Syntax highlighting service powered by Pygments.

Generates high-precision HTML token trees, inline CSS variables, embeddable HTML, and Microsoft Word / Rich Text tables.
"""

import html
import re
from typing import Dict, Any, Optional, Tuple, List

from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound

from litely.core.document import CodeDocument, VisualizationSettings
from litely.core.languages import LanguageRegistry
from litely.core.themes import ThemeRegistry


class HighlightService:
    """Service for rendering syntax-highlighted code artifacts."""

    @classmethod
    def highlight_document(cls, doc: CodeDocument) -> Dict[str, Any]:
        """Highlight a canonical CodeDocument and return structured result."""
        # 1. Resolve language & lexer
        lang_info = LanguageRegistry.get(doc.language)
        lexer_name = lang_info.lexer_name if lang_info else doc.language

        try:
            lexer = get_lexer_by_name(lexer_name, stripnl=False, ensurenl=False)
        except (ClassNotFound, ValueError):
            lexer = TextLexer(stripnl=False, ensurenl=False)

        # 2. Resolve theme
        theme_info = ThemeRegistry.resolve(doc.theme)
        pygments_style = theme_info.pygments_style

        # 3. Format tokens to class-based HTML
        try:
            formatter = HtmlFormatter(
                style=pygments_style,
                nowrap=True,
                classprefix="tok-",
            )
            raw_highlighted = highlight(doc.source, lexer, formatter)
            theme_css = formatter.get_style_defs(".litely-code")
        except Exception:
            formatter = HtmlFormatter(nowrap=True, classprefix="tok-")
            raw_highlighted = highlight(doc.source, TextLexer(), formatter)
            theme_css = ""

        # 4. Format tokens with full INLINE styles for Word / Rich Text paste
        try:
            formatter_inlined = HtmlFormatter(
                style=pygments_style,
                nowrap=True,
                noclasses=True,
            )
            raw_inlined = highlight(doc.source, lexer, formatter_inlined)
        except Exception:
            formatter_inlined = HtmlFormatter(nowrap=True, noclasses=True)
            raw_inlined = highlight(doc.source, TextLexer(), formatter_inlined)

        # 5. Process lines for DOM card view
        lines_html, total_lines = cls._process_lines(
            raw_highlighted=raw_highlighted,
            settings=doc.visualization,
        )

        # 6. Generate rich HTML specifically optimized for MS Word / Google Docs / Rich Text
        word_html = cls.generate_rich_html_for_word(
            raw_inlined=raw_inlined,
            doc=doc,
            theme_info=theme_info,
        )

        # 7. Generate embeddable HTML string (standalone embed with inline styles)
        embeddable_html = cls.generate_embeddable_html(
            raw_inlined=raw_inlined,
            doc=doc,
            theme_info=theme_info,
        )

        # 8. Build full standalone HTML card snippet
        card_html = cls._build_code_card_html(
            doc=doc,
            lines_html=lines_html,
            total_lines=total_lines,
            theme_info=theme_info,
            lang_info=lang_info,
        )

        return {
            "html": card_html,
            "raw_html": raw_highlighted,
            "theme_css": theme_css,
            "word_html": word_html,
            "embeddable_html": embeddable_html,
            "total_lines": total_lines,
            "language": lang_info.id if lang_info else doc.language,
            "language_name": lang_info.display_name if lang_info else doc.language.title(),
            "theme": theme_info.id,
            "theme_name": theme_info.display_name,
            "theme_info": theme_info.to_dict(),
        }

    @classmethod
    def generate_embeddable_html(
        cls,
        raw_inlined: str,
        doc: CodeDocument,
        theme_info: Any,
    ) -> str:
        """Generate a complete standalone embeddable HTML block with inline CSS."""
        s = doc.visualization
        normalized = raw_inlined.replace("\r\n", "\n").replace("\r", "\n")
        raw_lines = normalized.split("\n")
        if len(raw_lines) > 1 and raw_lines[-1] == "":
            raw_lines = raw_lines[:-1]
        if not raw_lines:
            raw_lines = [""]

        bg = theme_info.background
        fg = theme_info.foreground
        gutter_fg = "#6e7681" if theme_info.category == "dark" else "#8c959f"
        border_col = "rgba(255,255,255,0.15)" if theme_info.category == "dark" else "rgba(0,0,0,0.15)"
        font = s.font_family
        font_size = s.font_size
        line_height = s.line_height
        padding = s.padding
        radius = s.border_radius
        wrap_style = "pre-wrap" if s.word_wrap else "pre"

        pre_styles = f"margin: 0; line-height: {line_height}; font-family: '{font}', Consolas, 'Courier New', monospace; font-size: {font_size}px;"

        if s.show_line_numbers:
            start_line = s.start_line_number
            numbers = "\n".join(str(start_line + i) for i in range(len(raw_lines)))
            table_html = (
                f'<table style="border-collapse: collapse; width: 100%; border: none; margin: 0; padding: 0;">\n'
                f'  <tr>\n'
                f'    <td style="text-align: right; padding-right: 14px; padding-left: 4px; vertical-align: top; border-right: 1px solid {border_col}; width: 1%; white-space: nowrap; user-select: text;">\n'
                f'      <pre style="{pre_styles} color: {gutter_fg}; user-select: text;">{numbers}</pre>\n'
                f'    </td>\n'
                f'    <td style="padding-left: 14px; vertical-align: top; width: 99%;">\n'
                f'      <pre style="{pre_styles} color: {fg}; white-space: {wrap_style};">{raw_inlined}</pre>\n'
                f'    </td>\n'
                f'  </tr>\n'
                f'</table>'
            )
            body_content = table_html
        else:
            body_content = f'<pre style="{pre_styles} color: {fg}; white-space: {wrap_style};">{raw_inlined}</pre>'

        wrapper_style = (
            f"background: {bg}; color: {fg}; "
            f"border-radius: {radius}px; padding: {padding}px; "
            f"overflow: auto; border: 1px solid {border_col}; "
            f"font-family: '{font}', Consolas, 'Courier New', monospace;"
        )

        return f"<!-- HTML generated using LITELY -->\n<div style=\"{wrapper_style}\">\n{body_content}\n</div>"

    @classmethod
    def generate_rich_html_for_word(
        cls,
        raw_inlined: str,
        doc: CodeDocument,
        theme_info: Any,
    ) -> str:
        """Generate a pristine, multi-line table-based HTML block with inlined styles for MS Word and Google Docs."""
        s = doc.visualization
        normalized = raw_inlined.replace("\r\n", "\n").replace("\r", "\n")
        raw_lines = normalized.split("\n")
        if len(raw_lines) > 1 and raw_lines[-1] == "":
            raw_lines = raw_lines[:-1]
        if not raw_lines:
            raw_lines = [""]

        bg = theme_info.background
        fg = theme_info.foreground
        gutter_fg = "#6e7681" if theme_info.category == "dark" else "#8c959f"
        border_col = "#d0d7de" if theme_info.category == "light" else "#30363d"
        font = "Consolas, 'Courier New', 'JetBrains Mono', monospace"
        font_size = "10.5pt"
        line_height = "1.35"
        wrap_style = "pre-wrap" if s.word_wrap else "pre"

        pre_styles = f"margin: 0; line-height: {line_height}; font-family: {font}; font-size: {font_size};"

        if s.show_line_numbers:
            start_line = s.start_line_number
            max_digits = len(str(start_line + len(raw_lines) - 1))
            fmt = f"%{max_digits}d"
            numbers = "\n".join(fmt % (start_line + i) for i in range(len(raw_lines)))

            full_table = (
                f'<table style="background-color: {bg}; color: {fg}; border: 1px solid {border_col}; '
                f'border-collapse: collapse; width: 100%; margin: 8pt 0; border-radius: 6px; '
                f'font-family: {font}; font-size: {font_size}; line-height: {line_height};">\n'
                f'  <tbody>\n'
                f'    <tr>\n'
                f'      <td style="color: {gutter_fg}; text-align: right; padding: 6pt 10pt 6pt 8pt; '
                f'border-right: 1px solid {border_col}; vertical-align: top; width: 1%; white-space: nowrap; user-select: text;">\n'
                f'        <pre style="{pre_styles} color: {gutter_fg}; user-select: text;">{numbers}</pre>\n'
                f'      </td>\n'
                f'      <td style="padding: 6pt 10pt 6pt 12pt; vertical-align: top; width: 99%; color: {fg};">\n'
                f'        <pre style="{pre_styles} color: {fg}; white-space: {wrap_style};">{raw_inlined}</pre>\n'
                f'      </td>\n'
                f'    </tr>\n'
                f'  </tbody>\n'
                f'</table>'
            )
            return full_table
        else:
            return (
                f'<div style="background-color: {bg}; color: {fg}; padding: 8pt 12pt; '
                f'border: 1px solid {border_col}; border-radius: 6px; font-family: {font}; '
                f'font-size: {font_size}; line-height: {line_height};">\n'
                f'  <pre style="{pre_styles} color: {fg}; white-space: {wrap_style};">{raw_inlined}</pre>\n'
                f'</div>'
            )

    @classmethod
    def _process_lines(
        cls,
        raw_highlighted: str,
        settings: VisualizationSettings,
    ) -> Tuple[str, int]:
        """Split highlighted tokens into structured individual line containers."""
        normalized = raw_highlighted.replace("\r\n", "\n").replace("\r", "\n")
        raw_lines = normalized.split("\n")
        
        if len(raw_lines) > 1 and raw_lines[-1] == "":
            raw_lines = raw_lines[:-1]
        
        if not raw_lines:
            raw_lines = [""]

        total_lines = len(raw_lines)
        start_line = settings.start_line_number
        highlight_set = set(settings.highlight_lines)

        processed = []
        for idx, line_content in enumerate(raw_lines):
            line_num = start_line + idx
            is_highlighted = line_num in highlight_set
            hl_class = " litely-line-highlight" if is_highlighted else ""
            
            safe_content = line_content if line_content else "&#160;"

            line_markup = (
                f'<div class="litely-line{hl_class}" data-line="{line_num}">'
            )
            if settings.show_line_numbers:
                line_markup += f'<span class="litely-gutter">{line_num}</span>'
            
            wrap_class = " litely-wrap" if settings.word_wrap else ""
            line_markup += f'<span class="litely-line-content{wrap_class}">{safe_content}</span>'
            line_markup += '</div>'
            processed.append(line_markup)

        return "".join(processed), total_lines

    @classmethod
    def _build_code_card_html(
        cls,
        doc: CodeDocument,
        lines_html: str,
        total_lines: int,
        theme_info: Any,
        lang_info: Optional[Any],
    ) -> str:
        """Construct the complete semantic DOM markup for the code card."""
        s = doc.visualization
        filename = html.escape(doc.filename or "snippet")
        lang_display = lang_info.display_name if lang_info else doc.language.title()
        
        chrome_html = ""
        if s.window_chrome == "mac":
            chrome_html = (
                '<div class="litely-window-controls mac" aria-hidden="true">'
                '<span class="litely-dot close"></span>'
                '<span class="litely-dot minimize"></span>'
                '<span class="litely-dot maximize"></span>'
                '</div>'
            )
        elif s.window_chrome == "windows":
            chrome_html = (
                '<div class="litely-window-controls windows" aria-hidden="true">'
                '<span class="litely-win-btn win-min">―</span>'
                '<span class="litely-win-btn win-max">□</span>'
                '<span class="litely-win-btn win-close">✕</span>'
                '</div>'
            )

        badge_html = ""
        if s.show_language_badge:
            badge_html = f'<span class="litely-badge">{html.escape(lang_display)}</span>'

        title_bar = ""
        if s.window_chrome != "none" or filename or s.show_language_badge:
            title_bar = (
                f'<div class="litely-card-header">'
                f'{chrome_html}'
                f'<div class="litely-card-title">{filename}</div>'
                f'{badge_html}'
                f'</div>'
            )

        watermark_html = ""
        if s.show_watermark:
            watermark_html = '<div class="litely-watermark">LITELY</div>'

        card_html = (
            f'<!-- LITELY V1 Code Artifact -->\n'
            f'<div class="litely-card theme-{theme_info.id}" '
            f'data-theme="{theme_info.id}" '
            f'style="--litely-font-size: {s.font_size}px; --litely-line-height: {s.line_height}; '
            f'--litely-radius: {s.border_radius}px; --litely-bg: {theme_info.background}; '
            f'--litely-fg: {theme_info.foreground}; font-family: \'{s.font_family}\', monospace;">\n'
            f'{title_bar}\n'
            f'<pre class="litely-code-body"><code class="litely-code">{lines_html}</code></pre>\n'
            f'{watermark_html}\n'
            f'</div>'
        )

        return card_html
