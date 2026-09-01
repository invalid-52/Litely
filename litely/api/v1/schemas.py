"""Request validation, schema checking, and standard JSON response envelopes.
"""

from typing import Dict, Any, Tuple, Optional
from flask import jsonify, Response

from litely.config import Config


class APIResponse:
    """Standardized API response helper."""

    @staticmethod
    def success(data: Any, status_code: int = 200) -> Tuple[Response, int]:
        return jsonify({
            "success": True,
            "data": data,
            "error": None,
        }), status_code

    @staticmethod
    def error(
        code: str,
        message: str,
        status_code: int = 400,
        details: Optional[Any] = None,
    ) -> Tuple[Response, int]:
        return jsonify({
            "success": False,
            "data": None,
            "error": {
                "code": code,
                "message": message,
                "details": details,
            },
        }), status_code


def validate_highlight_request(payload: Optional[Dict[str, Any]]) -> Tuple[bool, Optional[str]]:
    """Validate incoming payload for code highlighting."""
    if not isinstance(payload, dict):
        return False, "Request body must be a valid JSON object."

    code = payload.get("code") or payload.get("source")
    if code is None:
        return False, "Field 'code' is required."

    if not isinstance(code, str):
        return False, "Field 'code' must be a string."

    if len(code) > Config.MAX_CODE_LENGTH:
        return False, f"Code length exceeds maximum allowed limit of {Config.MAX_CODE_LENGTH} characters."

    return True, None


def validate_detection_request(payload: Optional[Dict[str, Any]]) -> Tuple[bool, Optional[str]]:
    """Validate incoming payload for language detection."""
    if not isinstance(payload, dict):
        return False, "Request body must be a valid JSON object."

    code = payload.get("code") or payload.get("source")
    if code is None:
        return False, "Field 'code' is required."

    if not isinstance(code, str):
        return False, "Field 'code' must be a string."

    return True, None


def validate_export_request(payload: Optional[Dict[str, Any]]) -> Tuple[bool, Optional[str]]:
    """Validate incoming export payload."""
    is_valid, error = validate_highlight_request(payload)
    if not is_valid:
        return is_valid, error

    export_format = str(payload.get("format", "html")).lower()
    allowed_formats = {"html", "svg", "raw", "json"}
    if export_format not in allowed_formats:
        return False, f"Unsupported export format '{export_format}'. Allowed: {', '.join(allowed_formats)}."

    return True, None
