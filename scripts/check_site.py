#!/usr/bin/env python3
"""Check the built site (dist/) against the MkDocs site it replaces (PC-01, PC-02).

Standard library only. Run after `npm run build` (scripts/check.sh does this).

(a) Every page path of MIGRATION-PLAN.md section 2.2 exists in dist/.
(b) Every heading in src/content/docs/ has, on its built page, the anchor MkDocs
    made: the explicit `{#id}`, or else Python-Markdown's `toc` default slugify
    of the heading text. Fix a mismatch with an explicit `{#id}` in the source.
(c) No built HTML or CSS loads an http(s):// URL through <link href>,
    <script src>, <img src> or CSS url().
(d) Site files: robots.txt points at the sitemap; sitemap <loc>s and each
    page's canonical URL use SITE.
(e) The Content-Security-Policy in _headers allows no inline script except by
    hash, and its hashes are exactly those of the inline scripts in dist/ (one
    of them the somaari theme script). It allows Cloudflare Web Analytics.
(f) The Pagefind index holds a glossary term, and the glossary page's search
    fragment contains it.

Exit status 1 and one line per problem if anything fails.
"""

import base64
import gzip
import hashlib
import html
import json
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

SITE = "https://book.somaari.in"
SITEMAP = f"{SITE}/sitemap-index.xml"

# Cloudflare Web Analytics: the beacon script and where it reports.
ANALYTICS = {"script-src": "https://static.cloudflareinsights.com", "connect-src": "https://cloudflareinsights.com"}

# A glossary term that Pagefind indexes unstemmed (Pagefind stores word stems,
# e.g. "hallucination" as "hallucin").
SEARCH_TERM = "rlhf"
SEARCH_PAGE = "/glossary/"

# <script type> values a browser runs (and CSP checks); others, such as JSON-LD, are data.
JS_TYPES = {"", "module", "text/javascript", "application/javascript"}

# Pages that are not part of the MkDocs site, so they have no anchors to keep.
NOT_FROM_MKDOCS = {"404.md"}

# <link rel> values that name a URL without loading it.
NON_LOADING_RELS = {"canonical", "alternate", "author", "license", "help", "me", "sitemap", "next", "prev", "search"}

HEADING = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$")
EXPLICIT_ID = re.compile(r"\s*\{#([^}\s]+)\}\s*$")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
EXTERNAL = re.compile(r"^\s*(?:https?:)?//", re.IGNORECASE)
CSS_URL = re.compile(r"url\(\s*['\"]?([^'\")]+)")


def legacy_slugify(text):
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
            anchor = legacy_slugify(heading_text(text))
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
    """Collects element ids, the external URLs a page loads, its canonical URL
    and the text of its inline scripts."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.external = []
        self.canonical = []
        self.inline_scripts = []
        self._in_style = False
        self._script = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "script" and a.get("src") is None and (a.get("type") or "").lower() in JS_TYPES:
            self._script = []
        url = None
        if tag == "link":
            rels = set((a.get("rel") or "").lower().split())
            if "canonical" in rels:
                self.canonical.append(a.get("href") or "")
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
        if tag == "script" and self._script is not None:
            self.inline_scripts.append("".join(self._script))
            self._script = None

    def handle_data(self, data):
        if self._in_style:
            self.external += css_external(data)
        if self._script is not None:
            self._script.append(data)


def css_external(css):
    return [f"url() {u}" for u in CSS_URL.findall(css) if EXTERNAL.match(u)]


def read_exact(path):
    """File text with line endings kept, so script hashes match the served bytes."""
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def scan(path):
    parser = PageScan()
    parser.feed(read_exact(path))
    parser.close()
    return parser


def csp_hash(script):
    """The CSP source expression that allows one inline script."""
    digest = hashlib.sha256(script.encode("utf-8")).digest()
    return "'sha256-" + base64.b64encode(digest).decode("ascii") + "'"


def csp_directives(headers_text, path="/*"):
    """The Content-Security-Policy directives of one path rule in a _headers file."""
    current = None
    for line in headers_text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line[0].isspace():
            current = line.strip()
            continue
        name, _, value = line.strip().partition(":")
        if current == path and name.strip().lower() == "content-security-policy":
            directives = {}
            for part in value.split(";"):
                words = part.split()
                if words:
                    directives[words[0].lower()] = words[1:]
            return directives
    return None


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


def check_site_files(dist):
    errors = []
    robots = dist / "robots.txt"
    lines = robots.read_text(encoding="utf-8").splitlines() if robots.is_file() else []
    if f"Sitemap: {SITEMAP}" not in lines:
        errors.append(f"(d) robots.txt has no line `Sitemap: {SITEMAP}`")
    sitemaps = sorted(dist.glob("sitemap*.xml"))
    if not (dist / "sitemap-index.xml").is_file():
        errors.append("(d) missing sitemap-index.xml")
    for path in sitemaps:
        for loc in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", path.read_text(encoding="utf-8")):
            if not loc.startswith(SITE + "/"):
                errors.append(f"(d) {path.name}: <loc> {loc} is not on {SITE}")
    for page in PAGE_PATHS:
        built = dist / page.lstrip("/") / "index.html"
        if not built.is_file():
            continue  # reported by (a)
        canonical = scan(built).canonical
        if canonical != [SITE + page]:
            errors.append(f"(d) {page}: canonical {canonical} is not [{SITE + page!r}]")
    return errors


def check_csp(dist):
    errors = []
    headers = dist / "_headers"
    directives = csp_directives(read_exact(headers)) if headers.is_file() else None
    if directives is None:
        return ["(e) _headers has no Content-Security-Policy for /*"]
    script_src = directives.get("script-src", [])
    if "'self'" not in script_src:
        errors.append("(e) script-src lacks 'self'")
    for bad in ("'unsafe-inline'", "'unsafe-eval'"):
        if bad in script_src:
            errors.append(f"(e) script-src allows {bad}")
    for directive, source in ANALYTICS.items():
        if source not in directives.get(directive, []):
            errors.append(f"(e) {directive} lacks {source} (Cloudflare Web Analytics)")

    allowed = {s for s in script_src if s.startswith("'sha256-")}
    used, theme = {}, False
    for path in sorted(dist.rglob("*.html")):
        for script in scan(path).inline_scripts:
            used.setdefault(csp_hash(script), (path.relative_to(dist), script))
            theme = theme or "somaari-theme" in script
    if not theme:
        errors.append("(e) no inline somaari theme script found in dist/")
    for digest, (path, script) in sorted(used.items()):
        if digest not in allowed:
            start = " ".join(script.split())[:60]
            errors.append(f"(e) inline script in {path} is not allowed by script-src; "
                          f"add or update its hash in public/_headers: {digest} ({start}…)")
    for digest in sorted(allowed - set(used)):
        errors.append(f"(e) script-src hash {digest} matches no inline script in dist/; remove it")
    return errors


def check_search(dist, term=SEARCH_TERM, page=SEARCH_PAGE):
    """Pagefind files are gzip; inside, words are CBOR text strings (one length byte when short)."""
    errors = []
    pagefind = dist / "pagefind"
    if not (pagefind / "pagefind-entry.json").is_file():
        return ["(f) no Pagefind index in dist/pagefind/"]
    word = term.encode("utf-8")
    cbor_word = bytes([0x60 + len(word)]) + word  # needs len(word) < 24
    if not any(cbor_word in gzip.decompress(p.read_bytes()) for p in pagefind.glob("index/*.pf_index")):
        errors.append(f"(f) Pagefind index has no word {term!r}")
    found = False
    for path in pagefind.glob("fragment/*.pf_fragment"):
        data = gzip.decompress(path.read_bytes())
        fragment = json.loads(data[data.index(b"{"):])
        if fragment.get("url") == page:
            found = term.lower() in fragment.get("content", "").lower()
            break
    if not found:
        errors.append(f"(f) Pagefind has no fragment for {page} containing {term!r}")
    return errors


def main(docs=DOCS, dist=DIST):
    if not dist.is_dir():
        print(f"check_site: {dist} not found; run `npm run build` first.")
        return 1
    errors = (check_paths(dist) + check_anchors(docs, dist) + check_external(dist)
              + check_site_files(dist) + check_csp(dist) + check_search(dist))
    for error in errors:
        print(error)
    if errors:
        print(f"check_site: {len(errors)} problem(s).")
        return 1
    print(f"check_site: {len(PAGE_PATHS)} paths, heading anchors, external loads, "
          f"robots/sitemap/canonical, CSP script hashes and search OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
