#!/usr/bin/env python3
"""Check the built site (dist/) against the MkDocs site it replaces (PC-01).

Standard library only. Run after `npm run build` (scripts/check.sh does this).

(a) Every page path of MIGRATION-PLAN.md section 2.2 exists in dist/.
(b) Every heading in src/content/docs/ has, on its built page, the anchor MkDocs
    made: the explicit `{#id}`, or else Python-Markdown's `toc` default slugify
    of the heading text. Fix a mismatch with an explicit `{#id}` in the source.
(c) No built HTML or CSS loads an http(s):// URL through <link href>,
    <script src>, <img src> or CSS url().

Exit status 1 and one line per problem if anything fails.
"""

import html
import re
import sys
import unicodedata
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "src" / "content" / "docs"
DIST = ROOT / "dist"

# MIGRATION-PLAN.md section 2.2.
PAGE_PATHS = [
    "/",
    "/00-before-you-begin/",
    "/01-foundations/01-introduction/",
    "/01-foundations/02-why-ai-is-transforming-software-development/",
    "/01-foundations/03-understanding-large-language-models/",
    "/01-foundations/04-ai-assisted-software-development-lifecycle/",
    "/01-foundations/05-building-your-ai-assisted-development-environment/",
    "/01-foundations/06-your-first-ai-assisted-software-project/",
    "/glossary/",
]

# Pages that are not part of the MkDocs site, so they have no anchors to keep.
NOT_FROM_MKDOCS = {"404.md"}

# <link rel> values that name a URL without loading it.
NON_LOADING_RELS = {"canonical", "alternate", "author", "license", "help", "me", "sitemap", "next", "prev", "search"}

HEADING = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$")
EXPLICIT_ID = re.compile(r"\s*\{#([^}\s]+)\}\s*$")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
EXTERNAL = re.compile(r"^\s*(?:https?:)?//", re.IGNORECASE)
CSS_URL = re.compile(r"url\(\s*['\"]?([^'\")]+)")


def mkdocs_slugify(text):
    """Python-Markdown `toc` default slugify (markdown.extensions.toc.slugify)."""
    value = unicodedata.normalize("NFKD", text)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[-\s]+", "-", value)


def heading_text(markdown):
    """The plain text of an inline Markdown heading, as toc sees it."""
    text = re.sub(r"`([^`]*)`", r"\1", markdown)  # code spans
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)  # links and images
    text = re.sub(r"<[^>]+>", "", text)  # inline HTML
    text = re.sub(r"(\*{1,3}|_{1,3})(\S.*?\S|\S)\1", r"\2", text)  # emphasis
    return html.unescape(text)


def expected_anchors(markdown):
    """The anchors MkDocs makes for the ATX headings of one page, in order.

    Skips fenced code blocks and front matter; repeats get toc's `_N` suffix.
    """
    lines = markdown.splitlines()
    if lines and lines[0].strip() == "---":
        for end in range(1, len(lines)):
            if lines[end].strip() == "---":
                lines = lines[end + 1:]
                break
    anchors, seen, fence = [], set(), None
    for line in lines:
        m = FENCE.match(line)
        if fence:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and not line.strip()[len(m.group(1)):]:
                fence = None
            continue
        if m:
            fence = m.group(1)
            continue
        m = HEADING.match(line)
        if not m:
            continue
        text = m.group(2)
        explicit = EXPLICIT_ID.search(text)
        if explicit:
            anchor = explicit.group(1)
        else:
            anchor = mkdocs_slugify(heading_text(text))
            base, n = anchor, 1
            while anchor in seen:
                anchor = f"{base}_{n}"
                n += 1
        seen.add(anchor)
        anchors.append((anchor, line.strip()))
    return anchors


def built_page(dist, source):
    """dist/…/index.html for a source page under src/content/docs/."""
    rel = source.with_suffix("")
    if rel.name == "index":
        rel = rel.parent
    return dist / rel / "index.html"


class PageScan(HTMLParser):
    """Collects element ids and the external URLs a page loads."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.external = []
        self._in_style = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        url = None
        if tag == "link":
            rels = set((a.get("rel") or "").lower().split())
            if not rels or not rels <= NON_LOADING_RELS:
                url = a.get("href")
        elif tag in ("script", "img"):
            url = a.get("src")
        if url and EXTERNAL.match(url):
            self.external.append(f"<{tag}> {url}")
        if a.get("style"):
            self.external += css_external(a["style"])
        self._in_style = tag == "style"

    def handle_endtag(self, tag):
        self._in_style = False

    def handle_data(self, data):
        if self._in_style:
            self.external += css_external(data)


def css_external(css):
    return [f"url() {u}" for u in CSS_URL.findall(css) if EXTERNAL.match(u)]


def scan(path):
    parser = PageScan()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    return parser


def check_paths(dist):
    errors = []
    for path in PAGE_PATHS:
        if not (dist / path.lstrip("/") / "index.html").is_file():
            errors.append(f"(a) missing page: {path}")
    return errors


def check_anchors(docs, dist):
    errors = []
    for source in sorted(docs.rglob("*.md")):
        rel = source.relative_to(docs)
        if str(rel) in NOT_FROM_MKDOCS:
            continue
        page = built_page(dist, rel)
        if not page.is_file():
            errors.append(f"(b) no built page for {rel}: {page.relative_to(dist)}")
            continue
        ids = scan(page).ids
        for anchor, line in expected_anchors(source.read_text(encoding="utf-8")):
            if anchor not in ids:
                errors.append(f"(b) {rel}: no id=\"{anchor}\" on the built page for `{line}`")
    return errors


def check_external(dist):
    errors = []
    for path in sorted(dist.rglob("*.html")):
        for item in scan(path).external:
            errors.append(f"(c) {path.relative_to(dist)} loads {item}")
    for path in sorted(dist.rglob("*.css")):
        for item in css_external(path.read_text(encoding="utf-8")):
            errors.append(f"(c) {path.relative_to(dist)} loads {item}")
    return errors


def main(docs=DOCS, dist=DIST):
    if not dist.is_dir():
        print(f"check_site: {dist} not found; run `npm run build` first.")
        return 1
    errors = check_paths(dist) + check_anchors(docs, dist) + check_external(dist)
    for error in errors:
        print(error)
    if errors:
        print(f"check_site: {len(errors)} problem(s).")
        return 1
    print(f"check_site: {len(PAGE_PATHS)} paths, heading anchors and external loads OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
