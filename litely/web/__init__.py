"""LITELY Web UI Package."""

from flask import Blueprint

web_bp = Blueprint("web", __name__)
legacy_bp = Blueprint("legacy", __name__)

from litely.web import routes, legacy  # noqa: E402, F401

__all__ = ["web_bp", "legacy_bp"]
