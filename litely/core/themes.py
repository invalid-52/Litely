"""Centralized Theme Registry for LITELY.

Curated themes with color tokens, swatches, categories, and Pygments mappings.
"""

from typing import Dict, List, Optional
from litely.core.document import ThemeInfo


class ThemeRegistry:
    """Registry managing curated syntax themes in LITELY."""

    _THEMES: Dict[str, ThemeInfo] = {
        # DARK THEMES
        "github-dark": ThemeInfo(
            id="github-dark",
            display_name="GitHub Dark",
            category="dark",
            background="#0d1117",
            foreground="#c9d1d9",
            accent="#58a6ff",
            pygments_style="github-dark",
            swatches=["#0d1117", "#ff7b72", "#79c0ff", "#7ee787", "#ffa657"],
            popular=True,
        ),
        "dracula": ThemeInfo(
            id="dracula",
            display_name="Dracula",
            category="dark",
            background="#282a36",
            foreground="#f8f8f2",
            accent="#bd93f9",
            pygments_style="dracula",
            swatches=["#282a36", "#ff79c6", "#bd93f9", "#50fa7b", "#f1fa8c"],
            popular=True,
        ),
        "one-dark": ThemeInfo(
            id="one-dark",
            display_name="One Dark",
            category="dark",
            background="#282c34",
            foreground="#abb2bf",
            accent="#61afef",
            pygments_style="one-dark",
            swatches=["#282c34", "#e06c75", "#61afef", "#98c379", "#e5c07b"],
            popular=True,
        ),
        "tokyo-night": ThemeInfo(
            id="tokyo-night",
            display_name="Tokyo Night",
            category="dark",
            background="#1a1b26",
            foreground="#a9b1d6",
            accent="#7aa2f7",
            pygments_style="nord-darker",
            swatches=["#1a1b26", "#f7768e", "#7aa2f7", "#9ece6a", "#e0af68"],
            popular=True,
        ),
        "nord": ThemeInfo(
            id="nord",
            display_name="Nord",
            category="dark",
            background="#2e3440",
            foreground="#d8dee9",
            accent="#88c0d0",
            pygments_style="nord",
            swatches=["#2e3440", "#bf616a", "#88c0d0", "#a3be8c", "#ebcb8b"],
            popular=True,
        ),
        "monokai": ThemeInfo(
            id="monokai",
            display_name="Monokai",
            category="dark",
            background="#272822",
            foreground="#f8f8f2",
            accent="#a6e22e",
            pygments_style="monokai",
            swatches=["#272822", "#f92672", "#66d9ef", "#a6e22e", "#fd971f"],
            popular=True,
        ),
        "catppuccin-mocha": ThemeInfo(
            id="catppuccin-mocha",
            display_name="Catppuccin Mocha",
            category="dark",
            background="#1e1e2e",
            foreground="#cdd6f4",
            accent="#cba6f7",
            pygments_style="dracula",
            swatches=["#1e1e2e", "#f38ba8", "#89b4fa", "#a6e3a1", "#fab387"],
            popular=True,
        ),
        "solarized-dark": ThemeInfo(
            id="solarized-dark",
            display_name="Solarized Dark",
            category="dark",
            background="#002b36",
            foreground="#839496",
            accent="#268bd2",
            pygments_style="solarized-dark",
            swatches=["#002b36", "#dc322f", "#268bd2", "#859900", "#b58900"],
            popular=False,
        ),
        # LIGHT THEMES
        "colorful": ThemeInfo(
            id="colorful",
            display_name="Colorful (Classic)",
            category="light",
            background="#ffffff",
            foreground="#111827",
            accent="#008800",
            pygments_style="colorful",
            swatches=["#ffffff", "#008800", "#0e84b5", "#bb8844", "#aa22ff"],
            popular=True,
        ),
        "friendly": ThemeInfo(
            id="friendly",
            display_name="Friendly Light",
            category="light",
            background="#f8f9fa",
            foreground="#24292e",
            accent="#007020",
            pygments_style="friendly",
            swatches=["#f8f9fa", "#007020", "#4070a0", "#207070", "#b00040"],
            popular=True,
        ),
        "github-light": ThemeInfo(
            id="github-light",
            display_name="GitHub Light",
            category="light",
            background="#ffffff",
            foreground="#24292f",
            accent="#0969da",
            pygments_style="friendly",
            swatches=["#ffffff", "#cf222e", "#0550ae", "#116329", "#953800"],
            popular=True,
        ),
        "one-light": ThemeInfo(
            id="one-light",
            display_name="One Light",
            category="light",
            background="#fafafa",
            foreground="#383a42",
            accent="#4078f2",
            pygments_style="tango",
            swatches=["#fafafa", "#e45649", "#4078f2", "#50a14f", "#c18401"],
            popular=True,
        ),
        "minimal-light": ThemeInfo(
            id="minimal-light",
            display_name="Minimal Light",
            category="light",
            background="#f8f9fa",
            foreground="#212529",
            accent="#228be6",
            pygments_style="default",
            swatches=["#f8f9fa", "#e03131", "#1971c2", "#2f9e44", "#f08c00"],
            popular=True,
        ),
        "vs": ThemeInfo(
            id="vs",
            display_name="Visual Studio",
            category="light",
            background="#ffffff",
            foreground="#000000",
            accent="#0000ff",
            pygments_style="vs",
            swatches=["#ffffff", "#0000ff", "#2b91af", "#a31515", "#008000"],
            popular=False,
        ),
        "solarized-light": ThemeInfo(
            id="solarized-light",
            display_name="Solarized Light",
            category="light",
            background="#fdf6e3",
            foreground="#657b83",
            accent="#268bd2",
            pygments_style="solarized-light",
            swatches=["#fdf6e3", "#cb4b16", "#268bd2", "#859900", "#b58900"],
            popular=False,
        ),
        "catppuccin-latte": ThemeInfo(
            id="catppuccin-latte",
            display_name="Catppuccin Latte",
            category="light",
            background="#eff1f5",
            foreground="#4c4f69",
            accent="#8839ef",
            pygments_style="manni",
            swatches=["#eff1f5", "#d20f39", "#1e66f5", "#40a02b", "#fe640b"],
            popular=False,
        ),
    }

    @classmethod
    def get(cls, theme_id: str) -> Optional[ThemeInfo]:
        """Get ThemeInfo by ID."""
        return cls._THEMES.get(str(theme_id).lower().strip())

    @classmethod
    def resolve(cls, theme_id: str) -> ThemeInfo:
        """Get ThemeInfo or fallback to default github-dark."""
        info = cls.get(theme_id)
        if not info:
            return cls._THEMES["github-dark"]
        return info

    @classmethod
    def list_all(cls) -> List[ThemeInfo]:
        """List all themes."""
        return list(cls._THEMES.values())

    @classmethod
    def list_dark(cls) -> List[ThemeInfo]:
        """List dark themes."""
        return [t for t in cls._THEMES.values() if t.category == "dark"]

    @classmethod
    def list_light(cls) -> List[ThemeInfo]:
        """List light themes."""
        return [t for t in cls._THEMES.values() if t.category == "light"]
