#!/usr/bin/env python3
"""Validate a generated self-contained architecture HTML document."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


PLACEHOLDER = re.compile(r"\{\{[^{}]+\}\}")


class DocumentAudit(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.doctype = False
        self.ids: list[str] = []
        self.anchor_targets: list[str] = []
        self.tabs = 0
        self.panels = 0
        self.svgs = 0
        self.svg_titles = 0
        self.svg_descriptions = 0
        self.polygons = 0
        self.ellipses = 0
        self.external_assets: list[str] = []
        self._in_svg = 0

    def handle_decl(self, decl: str) -> None:
        if decl.lower().strip() == "doctype html":
            self.doctype = True

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._handle_tag(tag, dict(attrs))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._handle_tag(tag, dict(attrs))

    def handle_endtag(self, tag: str) -> None:
        if tag == "svg" and self._in_svg:
            self._in_svg -= 1

    def _handle_tag(self, tag: str, attrs: dict[str, str | None]) -> None:
        element_id = attrs.get("id")
        if element_id:
            self.ids.append(element_id)
        href = attrs.get("href")
        if href and href.startswith("#") and len(href) > 1:
            self.anchor_targets.append(href[1:])
        if attrs.get("role") == "tab":
            self.tabs += 1
        if attrs.get("role") == "tabpanel":
            self.panels += 1
        if tag == "svg":
            self.svgs += 1
            self._in_svg += 1
        elif self._in_svg and tag == "title":
            self.svg_titles += 1
        elif self._in_svg and tag == "desc":
            self.svg_descriptions += 1
        elif self._in_svg and tag == "polygon":
            self.polygons += 1
        elif self._in_svg and tag == "ellipse":
            self.ellipses += 1

        asset_url: str | None = None
        if tag in {"script", "img", "iframe", "video", "audio", "source"}:
            asset_url = attrs.get("src")
        elif tag == "link" and "stylesheet" in (attrs.get("rel") or "").lower():
            asset_url = attrs.get("href")
        if asset_url and urlparse(asset_url).scheme in {"http", "https"}:
            self.external_assets.append(asset_url)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html_file", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    path = args.html_file.resolve()
    if not path.is_file():
        print(f"ERROR: file not found: {path}")
        return 2

    source = path.read_text(encoding="utf-8")
    audit = DocumentAudit()
    audit.feed(source)

    errors: list[str] = []
    warnings: list[str] = []
    duplicates = sorted(value for value, count in Counter(audit.ids).items() if count > 1)
    missing_anchors = sorted(set(audit.anchor_targets) - set(audit.ids))

    if not audit.doctype:
        errors.append("missing <!doctype html>")
    if audit.tabs < 2 or audit.panels < 2:
        errors.append("expected at least two accessible tabs and two tab panels")
    if audit.svgs < 1:
        errors.append("no inline SVG architecture diagram found")
    if audit.svg_titles < audit.svgs or audit.svg_descriptions < audit.svgs:
        errors.append("every SVG needs a title and description")
    if duplicates:
        errors.append(f"duplicate IDs: {', '.join(duplicates)}")
    if missing_anchors:
        errors.append(f"broken fragment links: {', '.join(missing_anchors)}")
    if audit.external_assets:
        errors.append("network-loaded assets make the file non-self-contained: " + ", ".join(audit.external_assets))
    placeholders = sorted(set(PLACEHOLDER.findall(source)))
    if placeholders:
        errors.append("unresolved template placeholders: " + ", ".join(placeholders))
    if audit.polygons < 1:
        warnings.append("no SVG decision diamond detected")
    if audit.ellipses < 1:
        warnings.append("no SVG cylinder ellipse detected")
    if "@media print" not in source:
        warnings.append("no print stylesheet detected")
    if "keydown" not in source:
        warnings.append("no keyboard interaction handler detected")

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1

    print(
        "OK: "
        f"{audit.tabs} tabs, {audit.panels} panels, {audit.svgs} SVG diagram(s), "
        f"{audit.polygons} decision shape(s), {audit.ellipses} cylinder ellipse(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
