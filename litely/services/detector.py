"""Deterministic and heuristic language detection service.

Uses fast local signature matching, shebang detection, extension resolution,
and Pygments lexer heuristics without external AI API calls.
"""

import re
from typing import Dict, Any, Optional
from pygments.lexers import guess_lexer, TextLexer

from litely.core.languages import LanguageRegistry
from litely.core.document import LanguageInfo


class LanguageDetectionService:
    """Service for identifying code snippet programming languages."""

    @classmethod
    def detect(cls, code: str, filename: Optional[str] = None) -> Dict[str, Any]:
        """Detect language from code content and optional filename."""
        if not code or not code.strip():
            return {
                "detected": False,
                "language_id": None,
                "language_name": "Unknown",
                "confidence": 0.0,
                "reason": "Empty source code",
            }

        clean_code = code.strip()

        # 1. Check filename extension if provided
        if filename:
            dot_idx = filename.rfind(".")
            if dot_idx != -1:
                ext = filename[dot_idx:].lower()
                lang_by_ext = LanguageRegistry.get_by_extension(ext)
                if lang_by_ext:
                    return {
                        "detected": True,
                        "language_id": lang_by_ext.id,
                        "language_name": lang_by_ext.display_name,
                        "confidence": 0.95,
                        "reason": f"Matched file extension '{ext}'",
                    }

        # 2. Check Shebang line
        first_line = clean_code.splitlines()[0] if clean_code else ""
        if first_line.startswith("#!"):
            for lang in LanguageRegistry.list_all():
                for pat in lang.shebang_patterns:
                    if pat.lower() in first_line.lower():
                        return {
                            "detected": True,
                            "language_id": lang.id,
                            "language_name": lang.display_name,
                            "confidence": 0.9,
                            "reason": f"Matched shebang pattern '{pat}'",
                        }

        # 3. Signature keyword scoring
        best_lang: Optional[LanguageInfo] = None
        best_score = 0
        code_sample = clean_code[:5000]  # Analyze first 5k characters for speed

        for lang in LanguageRegistry.list_all():
            score = 0
            for kw in lang.signature_keywords:
                if kw in code_sample:
                    score += 1
            if score > best_score:
                best_score = score
                best_lang = lang

        # If keyword score is distinct and strong enough
        if best_lang and best_score >= 1:
            confidence = min(0.65 + (best_score * 0.08), 0.94)
            return {
                "detected": True,
                "language_id": best_lang.id,
                "language_name": best_lang.display_name,
                "confidence": round(confidence, 2),
                "reason": f"Matched {best_score} syntax signatures",
            }

        # 4. Pygments guess_lexer fallback
        try:
            guessed_lexer = guess_lexer(clean_code)
            if guessed_lexer and not isinstance(guessed_lexer, TextLexer):
                matched = LanguageRegistry.get(guessed_lexer.aliases[0] if guessed_lexer.aliases else guessed_lexer.name)
                if matched:
                    return {
                        "detected": True,
                        "language_id": matched.id,
                        "language_name": matched.display_name,
                        "confidence": 0.70,
                        "reason": f"Pygments lexer inference '{guessed_lexer.name}'",
                    }
        except Exception:
            pass

        # 5. Unknown / low confidence
        return {
            "detected": False,
            "language_id": None,
            "language_name": "Unknown",
            "confidence": 0.0,
            "reason": "Low confidence. Please select language manually.",
        }
