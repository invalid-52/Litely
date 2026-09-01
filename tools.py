"""Legacy tools compatibility shim.

Redirects legacy hilite_me calls to litely.services.highlighter.HighlightService.
"""

from litely.core.document import CodeDocument, VisualizationSettings
from litely.services.highlighter import HighlightService


def hilite_me(code, lexer, options, style, linenos, divstyles=""):
    """Legacy wrapper function."""
    doc = CodeDocument(
        source=code or "",
        language=lexer or "python",
        theme=style or "github-dark",
        visualization=VisualizationSettings(
            show_line_numbers=bool(linenos),
            window_chrome="none",
        ),
    )
    res = HighlightService.highlight_document(doc)
    return res["html"]


def get_default_style():
    return "padding: 16px;"


def insert_line_numbers(html):
    return html


def cmp(a, b):
    return (a > b) - (a < b)