"""Centralized Language Registry for LITELY.

Provides lookup, alias resolution, extension mapping, and heuristic keywords.
"""

from typing import Dict, List, Optional
from litely.core.document import LanguageInfo


class LanguageRegistry:
    """Registry managing all supported languages in LITELY."""

    _LANGUAGES: Dict[str, LanguageInfo] = {
        "python": LanguageInfo(
            id="python",
            display_name="Python",
            category="Programming",
            extensions=[".py", ".pyw", ".pyi", ".ipynb"],
            aliases=["py", "python3", "python2"],
            lexer_name="python",
            shebang_patterns=["python", "python3"],
            signature_keywords=["def ", "import ", "elif ", "self", "from ", "print(", "__init__", "class ", "lambda "],
            popular=True,
        ),
        "javascript": LanguageInfo(
            id="javascript",
            display_name="JavaScript",
            category="Web",
            extensions=[".js", ".mjs", ".cjs"],
            aliases=["js", "node"],
            lexer_name="javascript",
            shebang_patterns=["node"],
            signature_keywords=["const ", "let ", "var ", "function", "=>", "console.log", "export default", "require("],
            popular=True,
        ),
        "typescript": LanguageInfo(
            id="typescript",
            display_name="TypeScript",
            category="Web",
            extensions=[".ts", ".mts", ".cts"],
            aliases=["ts"],
            lexer_name="typescript",
            signature_keywords=["interface ", "type ", "enum ", ": string", ": number", ": boolean", "export interface", "readonly "],
            popular=True,
        ),
        "jsx": LanguageInfo(
            id="jsx",
            display_name="React JSX",
            category="Web",
            extensions=[".jsx"],
            aliases=["react-js"],
            lexer_name="jsx",
            signature_keywords=["className=", "<div", "useState", "useEffect", "React.", "</", "/>"],
            popular=True,
        ),
        "tsx": LanguageInfo(
            id="tsx",
            display_name="React TSX",
            category="Web",
            extensions=[".tsx"],
            aliases=["react-ts"],
            lexer_name="tsx",
            signature_keywords=["FC<", "React.FC", "className=", "useState<", "</", "/>"],
            popular=True,
        ),
        "rust": LanguageInfo(
            id="rust",
            display_name="Rust",
            category="Systems",
            extensions=[".rs"],
            aliases=["rs"],
            lexer_name="rust",
            signature_keywords=["fn ", "let mut ", "pub fn ", "impl ", "struct ", "match ", "println!", "Result<", "Option<", "&self"],
            popular=True,
        ),
        "go": LanguageInfo(
            id="go",
            display_name="Go",
            category="Systems",
            extensions=[".go"],
            aliases=["golang"],
            lexer_name="go",
            signature_keywords=["package ", "func ", "fmt.Println", "import (", "chan ", "goroutine", "type struct", ":="],
            popular=True,
        ),
        "cpp": LanguageInfo(
            id="cpp",
            display_name="C++",
            category="Systems",
            extensions=[".cpp", ".cc", ".cxx", ".hpp", ".h++", ".hh"],
            aliases=["c++", "cplusplus"],
            lexer_name="cpp",
            signature_keywords=["#include <", "std::", "cout <<", "nullptr", "namespace ", "template<", "auto ", "class "],
            popular=True,
        ),
        "c": LanguageInfo(
            id="c",
            display_name="C",
            category="Systems",
            extensions=[".c", ".h"],
            aliases=["clang"],
            lexer_name="c",
            signature_keywords=["#include <stdio.h>", "printf(", "malloc(", "int main(", "size_t ", "struct ", "NULL"],
            popular=True,
        ),
        "csharp": LanguageInfo(
            id="csharp",
            display_name="C#",
            category="Programming",
            extensions=[".cs"],
            aliases=["c#", "cs", "dotnet"],
            lexer_name="csharp",
            signature_keywords=["using System;", "namespace ", "public class ", "Console.WriteLine", "async Task", "var "],
            popular=True,
        ),
        "java": LanguageInfo(
            id="java",
            display_name="Java",
            category="Programming",
            extensions=[".java", ".jav"],
            aliases=["jvm"],
            lexer_name="java",
            signature_keywords=["public class ", "public static void main", "System.out.println", "import java.", "@Override"],
            popular=True,
        ),
        "kotlin": LanguageInfo(
            id="kotlin",
            display_name="Kotlin",
            category="Programming",
            extensions=[".kt", ".kts"],
            aliases=["kt"],
            lexer_name="kotlin",
            signature_keywords=["fun ", "val ", "var ", "println(", "companion object", "data class "],
            popular=True,
        ),
        "swift": LanguageInfo(
            id="swift",
            display_name="Swift",
            category="Mobile",
            extensions=[".swift"],
            aliases=[],
            lexer_name="swift",
            signature_keywords=["import SwiftUI", "import Foundation", "func ", "var body: some View", "guard let "],
            popular=True,
        ),
        "sql": LanguageInfo(
            id="sql",
            display_name="SQL",
            category="Data",
            extensions=[".sql", ".pgsql", ".mysql"],
            aliases=["mysql", "postgresql", "postgres", "sqlite"],
            lexer_name="sql",
            signature_keywords=["SELECT ", "FROM ", "WHERE ", "INSERT INTO ", "CREATE TABLE ", "INNER JOIN ", "GROUP BY "],
            popular=True,
        ),
        "html": LanguageInfo(
            id="html",
            display_name="HTML",
            category="Web",
            extensions=[".html", ".htm", ".xhtml"],
            aliases=["xhtml"],
            lexer_name="html",
            signature_keywords=["<!DOCTYPE html>", "<html", "<head>", "<body", "<div", "<span", "<p>"],
            popular=True,
        ),
        "css": LanguageInfo(
            id="css",
            display_name="CSS",
            category="Web",
            extensions=[".css"],
            aliases=["styles"],
            lexer_name="css",
            signature_keywords=["@media", "@import", "display:", "margin:", "padding:", "background-color:", ":root"],
            popular=True,
        ),
        "scss": LanguageInfo(
            id="scss",
            display_name="SCSS / Sass",
            category="Web",
            extensions=[".scss", ".sass"],
            aliases=["sass"],
            lexer_name="scss",
            signature_keywords=["$primary:", "@include ", "@mixin ", "&:hover", "@extend "],
            popular=False,
        ),
        "json": LanguageInfo(
            id="json",
            display_name="JSON",
            category="Config / Data",
            extensions=[".json", ".jsonc", ".geojson"],
            aliases=["jsonc"],
            lexer_name="json",
            signature_keywords=['": "', '": {', '": [', '": true', '": false', '": null', '":\n', '{\n  "', '},\n  {'],
            popular=True,
        ),
        "yaml": LanguageInfo(
            id="yaml",
            display_name="YAML",
            category="Config / Data",
            extensions=[".yaml", ".yml"],
            aliases=["yml"],
            lexer_name="yaml",
            signature_keywords=["apiVersion:", "version:", "services:", "steps:", "image:", "name:", "- "],
            popular=True,
        ),
        "toml": LanguageInfo(
            id="toml",
            display_name="TOML",
            category="Config / Data",
            extensions=[".toml"],
            aliases=[],
            lexer_name="toml",
            signature_keywords=["[package]", "[tool.poetry]", "[dependencies]", "version = "],
            popular=False,
        ),
        "markdown": LanguageInfo(
            id="markdown",
            display_name="Markdown",
            category="Documentation",
            extensions=[".md", ".markdown", ".mdown"],
            aliases=["md"],
            lexer_name="markdown",
            signature_keywords=["# ", "## ", "### ", "```", "* ", "- [ ]", "[link]("],
            popular=True,
        ),
        "bash": LanguageInfo(
            id="bash",
            display_name="Bash / Shell",
            category="Scripting",
            extensions=[".sh", ".bash", ".zsh"],
            aliases=["sh", "shell", "zsh"],
            lexer_name="bash",
            shebang_patterns=["bash", "sh", "zsh"],
            signature_keywords=["#!/bin/bash", "#!/bin/sh", "echo ", "export ", "if [", "fi", "chmod ", "curl "],
            popular=True,
        ),
        "dockerfile": LanguageInfo(
            id="dockerfile",
            display_name="Dockerfile",
            category="DevOps",
            extensions=["Dockerfile", ".dockerfile"],
            aliases=["docker"],
            lexer_name="docker",
            signature_keywords=["FROM ", "RUN ", "CMD ", "ENTRYPOINT ", "COPY ", "WORKDIR ", "EXPOSE ", "ENV "],
            popular=True,
        ),
        "php": LanguageInfo(
            id="php",
            display_name="PHP",
            category="Web",
            extensions=[".php", ".phtml"],
            aliases=["php8", "php7"],
            lexer_name="php",
            signature_keywords=["<?php", "$_GET", "$_POST", "echo ", "public function ", "namespace ", "use "],
            popular=True,
        ),
        "ruby": LanguageInfo(
            id="ruby",
            display_name="Ruby",
            category="Programming",
            extensions=[".rb", "Gemfile", "Rakefile"],
            aliases=["rb", "rails"],
            lexer_name="ruby",
            shebang_patterns=["ruby"],
            signature_keywords=["def ", "end", "puts ", "class ", "require '", "attr_accessor", "do |"],
            popular=False,
        ),
        "lua": LanguageInfo(
            id="lua",
            display_name="Lua",
            category="Scripting",
            extensions=[".lua"],
            aliases=[],
            lexer_name="lua",
            signature_keywords=["function ", "local ", "then", "end", "print(", "nil"],
            popular=False,
        ),
        "graphql": LanguageInfo(
            id="graphql",
            display_name="GraphQL",
            category="Web",
            extensions=[".graphql", ".gql"],
            aliases=["gql"],
            lexer_name="graphql",
            signature_keywords=["query ", "mutation ", "type Query", "type Mutation", "schema {", "fragment "],
            popular=False,
        ),
        "dart": LanguageInfo(
            id="dart",
            display_name="Dart",
            category="Mobile",
            extensions=[".dart"],
            aliases=["flutter"],
            lexer_name="dart",
            signature_keywords=["import 'package:flutter", "Widget build", "StatefulWidget", "StatelessWidget"],
            popular=False,
        ),
        "r": LanguageInfo(
            id="r",
            display_name="R",
            category="Data",
            extensions=[".r", ".R"],
            aliases=["R"],
            lexer_name="r",
            signature_keywords=["library(", "ggplot(", "data.frame(", "<-", "%>%"],
            popular=False,
        ),
    }

    # Index for fast lookup by alias and extension
    _ALIAS_MAP: Dict[str, str] = {}
    _EXT_MAP: Dict[str, str] = {}

    @classmethod
    def initialize(cls):
        """Build lookup indexes."""
        cls._ALIAS_MAP.clear()
        cls._EXT_MAP.clear()

        for lang_id, info in cls._LANGUAGES.items():
            cls._ALIAS_MAP[lang_id.lower()] = lang_id
            for alias in info.aliases:
                cls._ALIAS_MAP[alias.lower()] = lang_id
            for ext in info.extensions:
                cls._EXT_MAP[ext.lower()] = lang_id

    @classmethod
    def get(cls, language_id: str) -> Optional[LanguageInfo]:
        """Retrieve LanguageInfo by id or alias."""
        if not cls._ALIAS_MAP:
            cls.initialize()
        resolved_id = cls._ALIAS_MAP.get(str(language_id).lower().strip())
        if resolved_id:
            return cls._LANGUAGES.get(resolved_id)
        return None

    @classmethod
    def get_by_extension(cls, extension: str) -> Optional[LanguageInfo]:
        """Retrieve LanguageInfo by file extension (e.g. '.py')."""
        if not cls._EXT_MAP:
            cls.initialize()
        ext = extension.lower() if extension.startswith(".") else f".{extension.lower()}"
        lang_id = cls._EXT_MAP.get(ext)
        if lang_id:
            return cls._LANGUAGES.get(lang_id)
        return None

    @classmethod
    def resolve_lexer_name(cls, language_id: str) -> str:
        """Get Pygments lexer name from language identifier or alias."""
        info = cls.get(language_id)
        if info:
            return info.lexer_name
        return language_id or "text"

    @classmethod
    def list_all(cls) -> List[LanguageInfo]:
        """List all supported languages."""
        return list(cls._LANGUAGES.values())

    @classmethod
    def list_popular(cls) -> List[LanguageInfo]:
        """List popular/frequently used languages."""
        return [lang for lang in cls._LANGUAGES.values() if lang.popular]


# Auto-initialize indexes on load
LanguageRegistry.initialize()
