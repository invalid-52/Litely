"""LITELY Application Package.

Beautiful code visualization and syntax highlighting platform.
"""

from typing import Optional
from flask import Flask, jsonify

from litely.config import config_by_name, Config


def create_app(config_name: Optional[str] = None) -> Flask:
    """Application factory for LITELY."""
    if not config_name:
        config_name = "default"

    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )

    # Load configuration
    cfg = config_by_name.get(config_name, Config)
    app.config.from_object(cfg)

    # Register blueprints
    from litely.api.v1 import api_v1_bp
    from litely.web import web_bp, legacy_bp

    app.register_blueprint(api_v1_bp)
    app.register_blueprint(web_bp)
    app.register_blueprint(legacy_bp)

    @app.after_request
    def add_security_headers(response):
        response.headers.setdefault(
            "Content-Security-Policy",
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com data:; "
            "img-src 'self' blob: data:; "
            "connect-src 'self'; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "frame-ancestors 'none'"
        )
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        return response

    # Global error handlers
    @app.errorhandler(413)
    def request_entity_too_large(error):
        return jsonify({
            "success": False,
            "data": None,
            "error": {
                "code": "PAYLOAD_TOO_LARGE",
                "message": f"Payload exceeds maximum allowed size ({Config.MAX_CONTENT_LENGTH // (1024 * 1024)} MB).",
            }
        }), 413

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "The requested resource was not found.",
            }
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "data": None,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Something went wrong while processing your request. Please try again.",
            }
        }), 500

    return app


__version__ = Config.VERSION
__all__ = ["create_app"]
