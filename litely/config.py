"""LITELY Configuration Module.

Defines default settings, limits, and runtime constants.
"""

import os
from typing import Dict, Any


class Config:
    """Base application configuration."""

    APP_NAME: str = "LITELY"
    TAGLINE: str = "Beautiful code. Instantly."
    VERSION: str = "1.0.0"

    # Security & limits
    MAX_CONTENT_LENGTH: int = 1 * 1024 * 1024  # 1 MB max request payload
    MAX_CODE_LENGTH: int = 200_000  # 200k characters max for code snippets
    DEFAULT_TIMEOUT_SECONDS: int = 10

    # Default CodeDocument settings
    DEFAULT_LANGUAGE: str = "python"
    DEFAULT_THEME: str = "github-dark"
    DEFAULT_FONT_FAMILY: str = "JetBrains Mono"
    DEFAULT_FONT_SIZE: int = 14
    DEFAULT_LINE_HEIGHT: float = 1.5
    DEFAULT_PADDING: int = 32
    DEFAULT_BORDER_RADIUS: int = 12
    DEFAULT_WINDOW_CHROME: str = "mac"  # "mac" | "windows" | "minimal" | "none"
    DEFAULT_BACKGROUND_TYPE: str = "preset"  # "preset" | "solid" | "gradient" | "transparent"
    DEFAULT_BACKGROUND_VALUE: str = "twilight"
    DEFAULT_SHADOW: str = "medium"  # "none" | "soft" | "medium" | "dramatic"
    DEFAULT_SHOW_LINE_NUMBERS: bool = True
    DEFAULT_SHOW_LANGUAGE_BADGE: bool = True
    DEFAULT_SHOW_WATERMARK: bool = False
    DEFAULT_WORD_WRAP: bool = False

    # Server configuration
    JSON_SORT_KEYS: bool = False
    # LITELY V1 does not use server-side sessions. Generate a per-process fallback
    # for local development; production deployments should still provide SECRET_KEY.
    SECRET_KEY: str = os.getenv("SECRET_KEY") or os.urandom(32).hex()


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG: bool = True
    TESTING: bool = False


class TestingConfig(Config):
    """Testing environment configuration."""
    DEBUG: bool = False
    TESTING: bool = True


class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG: bool = False
    TESTING: bool = False


config_by_name: Dict[str, Any] = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
