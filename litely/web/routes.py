"""Web UI route handler for LITELY V1.
"""

from flask import render_template, request, current_app
from litely.web import web_bp
from litely.core.languages import LanguageRegistry
from litely.core.themes import ThemeRegistry
from litely.config import Config


@web_bp.route("/", methods=["GET"])
def index():
    """Render the primary LITELY application shell."""
    languages = [l.to_dict() for l in LanguageRegistry.list_all()]
    popular_languages = [l.to_dict() for l in LanguageRegistry.list_popular()]
    dark_themes = [t.to_dict() for t in ThemeRegistry.list_dark()]
    light_themes = [t.to_dict() for t in ThemeRegistry.list_light()]

    return render_template(
        "index.html",
        app_name=Config.APP_NAME,
        tagline=Config.TAGLINE,
        version=Config.VERSION,
        languages=languages,
        popular_languages=popular_languages,
        dark_themes=dark_themes,
        light_themes=light_themes,
    )
