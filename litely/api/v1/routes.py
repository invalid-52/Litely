"""REST API v1 endpoint implementations for LITELY.
"""

from typing import Dict, Any
from flask import request, Response
from werkzeug.utils import secure_filename

from litely.api.v1 import api_v1_bp
from litely.api.v1.schemas import (
    APIResponse,
    validate_highlight_request,
    validate_detection_request,
    validate_export_request,
)
from litely.config import Config
from litely.core.document import CodeDocument
from litely.core.languages import LanguageRegistry
from litely.core.themes import ThemeRegistry
from litely.services.highlighter import HighlightService
from litely.services.detector import LanguageDetectionService
from litely.services.exporter import ExportService


@api_v1_bp.route("/health", methods=["GET"])
def health_check():
    """Service health and capability probe."""
    return APIResponse.success({
        "status": "healthy",
        "service": Config.APP_NAME,
        "version": Config.VERSION,
        "languages_count": len(LanguageRegistry.list_all()),
        "themes_count": len(ThemeRegistry.list_all()),
    })


@api_v1_bp.route("/languages", methods=["GET"])
def list_languages():
    """Retrieve all supported languages with metadata."""
    popular_only = request.args.get("popular", "").lower() in ("true", "1")
    if popular_only:
        langs = LanguageRegistry.list_popular()
    else:
        langs = LanguageRegistry.list_all()

    data = [l.to_dict() for l in langs]
    return APIResponse.success({"languages": data, "total": len(data)})


@api_v1_bp.route("/themes", methods=["GET"])
def list_themes():
    """Retrieve all curated themes categorized by dark/light with color swatches."""
    dark_themes = [t.to_dict() for t in ThemeRegistry.list_dark()]
    light_themes = [t.to_dict() for t in ThemeRegistry.list_light()]

    return APIResponse.success({
        "dark": dark_themes,
        "light": light_themes,
        "total": len(dark_themes) + len(light_themes),
    })


@api_v1_bp.route("/detect-language", methods=["POST"])
def detect_language():
    """Detect programming language using shebang, signatures, and lexer analysis."""
    payload = request.get_json(silent=True)
    is_valid, error_msg = validate_detection_request(payload)
    if not is_valid:
        return APIResponse.error("INVALID_PAYLOAD", error_msg or "Invalid request")

    code = payload.get("code") or payload.get("source", "")
    filename = payload.get("filename")

    result = LanguageDetectionService.detect(code, filename)
    return APIResponse.success(result)


@api_v1_bp.route("/highlight", methods=["POST"])
def highlight_code():
    """Render syntax-highlighted HTML for a CodeDocument."""
    payload = request.get_json(silent=True)
    is_valid, error_msg = validate_highlight_request(payload)
    if not is_valid:
        return APIResponse.error("INVALID_PAYLOAD", error_msg or "Invalid request")

    # If language is set to 'auto', detect first
    req_lang = payload.get("language") or payload.get("lexer")
    code = payload.get("code") or payload.get("source", "")
    filename = payload.get("filename")

    if not req_lang or str(req_lang).lower() in ("auto", "detect", "auto-detect"):
        detect_res = LanguageDetectionService.detect(code, filename)
        if detect_res.get("detected") and detect_res.get("language_id"):
            payload["language"] = detect_res["language_id"]
        else:
            payload["language"] = "text"

    doc = CodeDocument.from_dict(payload)
    result = HighlightService.highlight_document(doc)

    return APIResponse.success(result)


@api_v1_bp.route("/export", methods=["POST"])
def export_artifact():
    """Export code document to standalone HTML, SVG, or raw format."""
    payload = request.get_json(silent=True)
    is_valid, error_msg = validate_export_request(payload)
    if not is_valid:
        return APIResponse.error("INVALID_PAYLOAD", error_msg or "Invalid request")

    # If language is set to 'auto', detect first
    req_lang = payload.get("language") or payload.get("lexer")
    code = payload.get("code") or payload.get("source", "")
    filename = payload.get("filename")

    if not req_lang or str(req_lang).lower() in ("auto", "detect", "auto-detect"):
        detect_res = LanguageDetectionService.detect(code, filename)
        if detect_res.get("detected") and detect_res.get("language_id"):
            payload["language"] = detect_res["language_id"]
        else:
            payload["language"] = "text"

    doc = CodeDocument.from_dict(payload)
    export_format = str(payload.get("format", "html")).lower()

    if export_format == "html":
        content = ExportService.export_standalone_html(doc)
        mimetype = "text/html"
        filename = f"{doc.filename or 'code'}.html"
    elif export_format == "svg":
        content = ExportService.export_svg(doc)
        mimetype = "image/svg+xml"
        filename = f"{doc.filename or 'code'}.svg"
    elif export_format == "raw":
        content = doc.source
        mimetype = "text/plain"
        filename = f"{doc.filename or 'code'}.txt"
    else:
        return APIResponse.error("INVALID_FORMAT", f"Unsupported format: {export_format}")

    # Return download or JSON depending on query param
    if request.args.get("download", "").lower() in ("1", "true"):
        safe_name = secure_filename(filename) or f"code.{export_format}"
        return Response(
            content,
            mimetype=mimetype,
            headers={
                "Content-Disposition": f'attachment; filename="{safe_name}"',
                "X-Content-Type-Options": "nosniff",
            },
        )

    return APIResponse.success({
        "format": export_format,
        "filename": filename,
        "content": content,
        "mimetype": mimetype,
    })
