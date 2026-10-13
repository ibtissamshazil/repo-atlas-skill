#!/usr/bin/env python3
"""Print a safe, read-only inventory of a software repository."""

from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter, defaultdict
from pathlib import Path


SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "coverage",
    ".next",
    ".nuxt",
    "target",
    "bin",
    "obj",
}

MANIFEST_NAMES = {
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "bun.lock",
    "bun.lockb",
    "deno.json",
    "deno.jsonc",
    "pyproject.toml",
    "requirements.txt",
    "poetry.lock",
    "uv.lock",
    "Pipfile",
    "go.mod",
    "go.sum",
    "Cargo.toml",
    "Cargo.lock",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "settings.gradle",
    "settings.gradle.kts",
    "gradle.properties",
    "composer.json",
    "Gemfile",
    "mix.exs",
    "pubspec.yaml",
    "Package.swift",
    "Podfile",
    "CMakeLists.txt",
    "nuget.config",
    "Directory.Build.props",
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    "Makefile",
}

INSTRUCTION_NAMES = {
    "agents.md",
    "claude.md",
    "readme.md",
    "contributing.md",
    "architecture.md",
    "security.md",
}

ENTRYPOINT_NAMES = {
    "main.py",
    "app.py",
    "server.py",
    "manage.py",
    "index.js",
    "index.ts",
    "server.js",
    "server.ts",
    "main.go",
    "main.rs",
    "main.kt",
    "main.swift",
    "program.cs",
}

MANIFEST_SUFFIXES = {".csproj", ".fsproj", ".vbproj", ".sln", ".xcodeproj"}

BUCKETS = {
    "api-and-entrypoints": ("api", "route", "router", "controller", "main", "server", "app"),
    "data-and-schema": ("database", "db", "schema", "model", "migration", "repository"),
    "workers-and-jobs": ("worker", "listener", "queue", "consumer", "scheduler", "cron", "job", "task"),
    "ai-and-prompts": ("prompt", "llm", "inference", "embedding", "agent", "ai"),
    "frontend-and-static": ("frontend", "client", "web", "static", "public", "template", "dashboard"),
    "evaluation-and-tests": ("test", "spec", "eval", "benchmark", "fixture"),
    "operations": ("docker", "deploy", "infra", "config", "setting", "workflow", "script", "migration"),
}

ENV_FILE_NAMES = {".env.example", ".env.sample", ".env.template", "env.example"}
ENV_ASSIGNMENT = re.compile(r"^\s*(?:export\s+)?([A-Z][A-Z0-9_]{2,})\s*=", re.MULTILINE)
ENV_REFERENCES = (
    re.compile(r"(?:getenv|os\.getenv)\(\s*['\"]([A-Z][A-Z0-9_]{2,})['\"]"),
    re.compile(r"os\.environ(?:\.get)?\[?\(?\s*['\"]([A-Z][A-Z0-9_]{2,})['\"]"),
    re.compile(r"process\.env\.([A-Z][A-Z0-9_]{2,})"),
    re.compile(r"\$\{([A-Z][A-Z0-9_]{2,})(?::-[^}]*)?\}"),
)

TEXT_SUFFIXES = {
    ".c",
    ".cc",
    ".cpp",
    ".cs",
    ".css",
    ".dart",
    ".ex",
    ".exs",
    ".go",
    ".h",
    ".html",
    ".java",
    ".js",
    ".json",
    ".jsx",
    ".kt",
    ".kts",
    ".md",
    ".php",
    ".ps1",
    ".py",
    ".rb",
    ".rs",
    ".scala",
    ".sh",
    ".sql",
    ".swift",
    ".tf",
    ".tfvars",
    ".toml",
    ".ts",
    ".tsx",
    ".vue",
    ".xml",
    ".yaml",
    ".yml",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root")
    parser.add_argument("--max-files", type=int, default=10_000, help="Safety limit")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown")
    return parser.parse_args()


def walk_files(root: Path, max_files: int) -> tuple[list[Path], bool]:
    files: list[Path] = []
    truncated = False
    for current, dirs, names in os.walk(root):
        dirs[:] = sorted(directory for directory in dirs if directory not in SKIP_DIRS)
        for name in sorted(names):
            path = Path(current) / name
            try:
                if path.is_symlink() or not path.is_file():
                    continue
            except OSError:
                continue
            files.append(path)
            if len(files) >= max_files:
                truncated = True
                return files, truncated
    return files, truncated


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def read_small_text(path: Path) -> str | None:
    try:
        if path.stat().st_size > 512_000:
            return None
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None


def build_inventory(root: Path, max_files: int) -> dict[str, object]:
    files, truncated = walk_files(root, max_files)
    extensions: Counter[str] = Counter()
    manifests: list[str] = []
    instructions: list[str] = []
    entrypoints: list[str] = []
    buckets: dict[str, list[str]] = defaultdict(list)
    env_names: set[str] = set()

    for path in files:
        rel = relative(path, root)
        lower_rel = rel.lower()
        lower_name = path.name.lower()
        suffix = path.suffix.lower() or "[no extension]"
        extensions[suffix] += 1

        if path.name in MANIFEST_NAMES or path.suffix.lower() in MANIFEST_SUFFIXES:
            manifests.append(rel)
        if lower_name in INSTRUCTION_NAMES:
            instructions.append(rel)
        if lower_name in ENTRYPOINT_NAMES or lower_name.startswith(("cli.", "worker.", "listener.")):
            entrypoints.append(rel)

        tokens = set(re.split(r"[^a-z0-9]+", lower_rel))
        for bucket, keywords in BUCKETS.items():
            if any(keyword in tokens for keyword in keywords):
                buckets[bucket].append(rel)

        should_scan = path.suffix.lower() in TEXT_SUFFIXES or lower_name in ENV_FILE_NAMES
        if not should_scan:
            continue
        text = read_small_text(path)
        if text is None:
            continue
        if lower_name in ENV_FILE_NAMES:
            env_names.update(ENV_ASSIGNMENT.findall(text))
        for pattern in ENV_REFERENCES:
            env_names.update(pattern.findall(text))

    return {
        "root": str(root),
        "file_count": len(files),
        "truncated": truncated,
        "top_extensions": extensions.most_common(20),
        "instructions": sorted(instructions),
        "manifests": sorted(manifests),
        "entrypoints": sorted(entrypoints),
        "architecture_hints": {key: sorted(values)[:60] for key, values in sorted(buckets.items())},
        "environment_variable_names": sorted(env_names),
    }


def markdown_list(values: list[str], empty: str = "None detected") -> str:
    return "\n".join(f"- `{value}`" for value in values) if values else f"- {empty}"


def print_markdown(data: dict[str, object]) -> None:
    print("# Repository inventory\n")
    print(f"- Root: `{data['root']}`")
    print(f"- Files inspected: {data['file_count']}")
    print(f"- Truncated: {'yes' if data['truncated'] else 'no'}")
    print("\nThis is a discovery aid. Verify every architecture claim in source.\n")

    for title, key in (
        ("Repository instructions", "instructions"),
        ("Manifests and build files", "manifests"),
        ("Likely entry points", "entrypoints"),
    ):
        print(f"## {title}\n")
        print(markdown_list(data[key]))
        print()

    print("## File types\n")
    for suffix, count in data["top_extensions"]:
        print(f"- `{suffix}`: {count}")

    print("\n## Architecture hints\n")
    for bucket, paths in data["architecture_hints"].items():
        print(f"### {bucket}\n")
        print(markdown_list(paths))
        print()

    print("## Environment variable names\n")
    print(markdown_list(data["environment_variable_names"]))


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        raise SystemExit(f"Repository root is not a directory: {root}")
    if args.max_files < 1:
        raise SystemExit("--max-files must be at least 1")
    data = build_inventory(root, args.max_files)
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print_markdown(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
