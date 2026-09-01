"""Canonical CodeDocument and visualization configuration models.

Designed to serve as the unified domain model across V1 and future V2-V5 roadmaps.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, Optional, List
import time


@dataclass
class VisualizationSettings:
    """Settings controlling the visual rendering of the code artifact."""

    font_family: str = "JetBrains Mono"
    font_size: int = 14
    line_height: float = 1.5
    padding: int = 32
    border_radius: int = 12
    window_chrome: str = "mac"  # "mac" | "windows" | "minimal" | "none"
    background_type: str = "preset"  # "preset" | "solid" | "gradient" | "transparent"
    background_value: str = "twilight"
    shadow: str = "medium"  # "none" | "soft" | "medium" | "dramatic"
    show_line_numbers: bool = True
    start_line_number: int = 1
    show_language_badge: bool = True
    show_watermark: bool = False
    word_wrap: bool = False
    highlight_lines: List[int] = field(default_factory=list)
    aspect_ratio: str = "auto"  # "auto" | "16:9" | "4:3" | "1:1" | "full"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> "VisualizationSettings":
        """Build settings from untrusted input with strict, renderer-safe normalization."""
        if not isinstance(data, dict):
            return cls()

        defaults = cls()
        fonts = {
            "JetBrains Mono", "Fira Code", "IBM Plex Mono", "Source Code Pro",
            "Menlo", "Monaco", "Consolas", "Courier New",
        }
        enums = {
            "window_chrome": {"mac", "windows", "minimal", "none"},
            "background_type": {"preset", "solid", "gradient", "transparent"},
            "shadow": {"none", "soft", "medium", "dramatic"},
            "aspect_ratio": {"auto", "16:9", "4:3", "1:1", "full"},
        }

        def bounded_int(value, lo, hi, fallback):
            try:
                return max(lo, min(hi, int(value)))
            except (TypeError, ValueError):
                return fallback

        def bounded_float(value, lo, hi, fallback):
            try:
                return max(lo, min(hi, float(value)))
            except (TypeError, ValueError):
                return fallback

        def safe_bool(value, fallback):
            if isinstance(value, bool):
                return value
            if isinstance(value, str):
                if value.strip().lower() in {"true", "1", "yes", "on"}: return True
                if value.strip().lower() in {"false", "0", "no", "off"}: return False
            if isinstance(value, (int, float)):
                return bool(value)
            return fallback

        raw_font = str(data.get("font_family", defaults.font_family))
        font_family = raw_font if raw_font in fonts else defaults.font_family

        backgrounds = {
            "twilight", "midnight", "aurora", "sunset", "matrix", "carbon", "snow", "transparent",
        }
        background_value = str(data.get("background_value", defaults.background_value)).lower()
        if background_value not in backgrounds:
            background_value = defaults.background_value

        result = cls(
            font_family=font_family,
            font_size=bounded_int(data.get("font_size"), 11, 32, defaults.font_size),
            line_height=bounded_float(data.get("line_height"), 1.1, 2.5, defaults.line_height),
            padding=bounded_int(data.get("padding"), 8, 120, defaults.padding),
            border_radius=bounded_int(data.get("border_radius"), 0, 40, defaults.border_radius),
            window_chrome=str(data.get("window_chrome", defaults.window_chrome)).lower()
                if str(data.get("window_chrome", defaults.window_chrome)).lower() in enums["window_chrome"]
                else defaults.window_chrome,
            background_type=str(data.get("background_type", defaults.background_type)).lower()
                if str(data.get("background_type", defaults.background_type)).lower() in enums["background_type"]
                else defaults.background_type,
            background_value=background_value,
            shadow=str(data.get("shadow", defaults.shadow)).lower()
                if str(data.get("shadow", defaults.shadow)).lower() in enums["shadow"]
                else defaults.shadow,
            show_line_numbers=safe_bool(data.get("show_line_numbers"), defaults.show_line_numbers),
            start_line_number=bounded_int(data.get("start_line_number"), 1, 1_000_000, defaults.start_line_number),
            show_language_badge=safe_bool(data.get("show_language_badge"), defaults.show_language_badge),
            show_watermark=safe_bool(data.get("show_watermark"), defaults.show_watermark),
            word_wrap=safe_bool(data.get("word_wrap"), defaults.word_wrap),
            highlight_lines=[n for n in (data.get("highlight_lines") or [])
                             if isinstance(n, int) and 1 <= n <= 1_000_000][:500],
            aspect_ratio=str(data.get("aspect_ratio", defaults.aspect_ratio)).lower()
                if str(data.get("aspect_ratio", defaults.aspect_ratio)).lower() in enums["aspect_ratio"]
                else defaults.aspect_ratio,
        )
        return result


@dataclass
class CodeDocument:
    """Canonical representation of a code document in LITELY.

    Serves as the single source of truth passed through the rendering pipeline.
    """

    source: str
    language: str = "python"
    filename: Optional[str] = "main.py"
    theme: str = "github-dark"
    visualization: VisualizationSettings = field(default_factory=VisualizationSettings)
    source_type: str = "text"  # "text" | "upload" | future "ocr" | future "url"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not isinstance(self.visualization, VisualizationSettings):
            if isinstance(self.visualization, dict):
                self.visualization = VisualizationSettings.from_dict(self.visualization)
            else:
                self.visualization = VisualizationSettings()
        
        # Populate basic metadata
        lines = self.source.splitlines()
        self.metadata.setdefault("line_count", len(lines))
        self.metadata.setdefault("char_count", len(self.source))
        self.metadata.setdefault("created_at", int(time.time()))

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CodeDocument":
        source = data.get("code") or data.get("source", "")
        language = data.get("language") or data.get("lexer", "python")
        filename = data.get("filename") or (data.get("title") if data.get("title") else "snippet")
        theme = data.get("theme") or data.get("style", "github-dark")
        
        # Handle settings whether flat or nested
        raw_settings = data.get("visualization") or data.get("settings") or {}
        if not isinstance(raw_settings, dict):
            raw_settings = {}
        
        # Support flat top-level legacy keys
        if "linenos" in data and "show_line_numbers" not in raw_settings:
            raw_settings["show_line_numbers"] = bool(data["linenos"] and str(data["linenos"]).lower() not in ("0", "false"))
        if "fontSize" in data and "font_size" not in raw_settings:
            raw_settings["font_size"] = int(data["fontSize"])

        vis = VisualizationSettings.from_dict(raw_settings)
        source_type = data.get("source_type", "text")
        metadata = data.get("metadata", {})

        return cls(
            source=source,
            language=language,
            filename=filename,
            theme=theme,
            visualization=vis,
            source_type=source_type,
            metadata=metadata,
        )


@dataclass
class LanguageInfo:
    """Metadata describing a supported language."""

    id: str
    display_name: str
    category: str
    extensions: List[str]
    aliases: List[str]
    lexer_name: str
    shebang_patterns: List[str] = field(default_factory=list)
    signature_keywords: List[str] = field(default_factory=list)
    popular: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ThemeInfo:
    """Metadata describing a curated theme."""

    id: str
    display_name: str
    category: str  # "dark" | "light"
    background: str
    foreground: str
    accent: str
    pygments_style: str
    swatches: List[str] = field(default_factory=list)
    popular: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
