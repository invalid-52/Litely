"""Legacy compatibility layer for hilite.me endpoints.

Preserves backward compatibility for scripts relying on GET/POST /api.
"""

from urllib.parse import unquote
from flask import request, make_response, render_template, Response

from litely.web import legacy_bp
from litely.core.document import CodeDocument, VisualizationSettings
from litely.services.highlighter import HighlightService


@legacy_bp.route("/api", methods=["GET", "POST"])
def legacy_api():
    """Legacy endpoint supporting old query/form parameters."""
    code = request.values.get("code", "")
    if not code:
        doc_text = (
            "# LITELY API Documentation (Legacy Compatibility)\n\n"
            "GET or POST to /api with parameters:\n"
            "* code: source code to format\n"
            "* lexer: language/lexer name (default: python)\n"
            "* style: theme/style name (default: github-dark)\n"
            "* linenos: if non-empty, includes line numbers\n\n"
            "Modern REST API v1 is available at: /api/v1/highlight\n"
        )
        response = make_response(doc_text)
        response.headers["Content-Type"] = "text/plain; charset=utf-8"
        return response

    lexer = request.values.get("lexer", "python")
    style = request.values.get("style", "github-dark")
    linenos = bool(request.values.get("linenos", ""))

    doc = CodeDocument(
        source=code,
        language=lexer,
        theme=style,
        visualization=VisualizationSettings(
            show_line_numbers=linenos,
            window_chrome="none",
            border_radius=4,
            padding=16,
        ),
    )

    result = HighlightService.highlight_document(doc)
    response = make_response(result["html"])
    response.headers["Content-Type"] = "text/html; charset=utf-8"
    return response
