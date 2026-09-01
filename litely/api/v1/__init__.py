"""LITELY API v1 Module."""

from flask import Blueprint

api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")

from litely.api.v1 import routes  # noqa: E402, F401

__all__ = ["api_v1_bp"]
