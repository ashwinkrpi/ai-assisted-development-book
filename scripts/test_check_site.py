#!/usr/bin/env python3
"""Unit tests for scripts/check_site.py. Self-contained: they do not need dist/."""

import gzip
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_site  # noqa: E402

GLOSSARY = check_site.DOCS / "glossary.md"


class SlugifyTest(unittest.TestCase):
    def test_matches_python_markdown_toc(self):
        cases = {
            "6.1 Step 1 — Project Structure": "61-step-1-project-structure",
            "LLM (large language model)": "llm-large-language-model",
            "Hands-On Lab: Tokens, Context, and Hallucination in Practice":
                "hands-on-lab-tokens-context-and-hallucination-in-practice",
            "Part 1: Foundations of AI-Assisted Software Development":
                "part-1-foundations-of-ai-assisted-software-development",
        }
        for text, slug in cases.items():
            self.assertEqual(check_site.mkdocs_slugify(text), slug)

    def test_headings_skip_code_and_take_explicit_ids(self):
        md = "---\ntitle: X\n---\n## A *b*\n```markdown\n## Not a heading\n```\n### Agent {#agent}\n## A b\n"
        self.assertEqual([a for a, _ in check_site.expected_anchors(md)], ["a-b", "agent", "a-b_1"])


class AnchorCheckTest(unittest.TestCase):
    """Deleting one glossary {#id} in a scratch copy makes the check fail."""

    def run_check(self, glossary_text):
        ids = [a for a, _ in check_site.expected_anchors(GLOSSARY.read_text(encoding="utf-8"))]
        with tempfile.TemporaryDirectory() as tmp:
            docs, dist = Path(tmp, "docs"), Path(tmp, "dist")
            docs.mkdir()
            (docs / "glossary.md").write_text(glossary_text, encoding="utf-8")
            page = dist / "glossary" / "index.html"
            page.parent.mkdir(parents=True)
            page.write_text("".join(f'<h3 id="{i}">x</h3>' for i in ids), encoding="utf-8")
            return check_site.check_anchors(docs, dist)

    def test_real_glossary_passes(self):
        self.assertEqual(self.run_check(GLOSSARY.read_text(encoding="utf-8")), [])

    def test_deleted_glossary_id_fails(self):
        text = GLOSSARY.read_text(encoding="utf-8")
        self.assertIn(" {#llm}", text)
        errors = self.run_check(text.replace(" {#llm}", "", 1))
        self.assertEqual(len(errors), 1)
        self.assertIn('id="llm-large-language-model"', errors[0])


class ExternalLoadTest(unittest.TestCase):
    def test_flags_loads_but_not_canonical(self):
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp, "index.html")
            page.write_text(
                '<link rel="canonical" href="https://book.somaari.in/">'
                '<link rel="stylesheet" href="https://cdn.example/a.css">'
                '<script src="/local.js"></script><img src="//cdn.example/i.png">'
                '<style>a{background:url("https://cdn.example/b.png")}</style>',
                encoding="utf-8",
            )
            self.assertEqual(len(check_site.check_external(Path(tmp))), 3)


THEME_SCRIPT = "(function(){localStorage.getItem('somaari-theme')})();"


def headers_with(*sources):
    return ("# comment\n/*\n  X-Content-Type-Options: nosniff\n"
            f"  Content-Security-Policy: default-src 'self'; script-src 'self' {' '.join(sources)} "
            "https://static.cloudflareinsights.com; connect-src 'self' https://cloudflareinsights.com\n"
            "/_astro/*\n  Cache-Control: immutable\n")


class CspTest(unittest.TestCase):
    """A change to the theme script fails the check until public/_headers has its new hash."""

    def run_check(self, headers, script):
        with tempfile.TemporaryDirectory() as tmp:
            dist = Path(tmp)
            (dist / "_headers").write_text(headers, encoding="utf-8")
            (dist / "index.html").write_text(
                f'<script>{script}</script><script type="module" src="/_astro/a.js"></script>'
                '<script type="application/ld+json">{}</script>', encoding="utf-8")
            return check_site.check_csp(dist)

    def test_hash_of_theme_script_passes(self):
        self.assertEqual(self.run_check(headers_with(check_site.csp_hash(THEME_SCRIPT)), THEME_SCRIPT), [])

    def test_changed_theme_script_fails(self):
        changed = THEME_SCRIPT.replace("getItem", "removeItem")
        errors = self.run_check(headers_with(check_site.csp_hash(THEME_SCRIPT)), changed)
        self.assertEqual(len(errors), 2)  # new script not allowed, old hash unused
        self.assertIn(check_site.csp_hash(changed), errors[0])

    def test_unsafe_inline_fails(self):
        errors = self.run_check(headers_with("'unsafe-inline'", check_site.csp_hash(THEME_SCRIPT)), THEME_SCRIPT)
        self.assertEqual(errors, ["(e) script-src allows 'unsafe-inline'"])

    def test_real_headers_file(self):
        csp = check_site.csp_directives((check_site.ROOT / "public" / "_headers").read_text(encoding="utf-8"))
        self.assertIn("'self'", csp["script-src"])
        self.assertNotIn("'unsafe-inline'", csp["script-src"])
        for directive, source in check_site.ANALYTICS.items():
            self.assertIn(source, csp[directive])


class SearchTest(unittest.TestCase):
    def test_finds_glossary_term_in_pagefind_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            pagefind = Path(tmp, "pagefind")
            (pagefind / "index").mkdir(parents=True)
            (pagefind / "fragment").mkdir()
            (pagefind / "pagefind-entry.json").write_text("{}", encoding="utf-8")
            word = check_site.SEARCH_TERM.encode()
            (pagefind / "index" / "en_1.pf_index").write_bytes(
                gzip.compress(b"pagefind_dcd\x82" + bytes([0x60 + len(word)]) + word))
            fragment = {"url": "/glossary/", "content": f"Glossary. {check_site.SEARCH_TERM.upper()} means …"}
            (pagefind / "fragment" / "en_1.pf_fragment").write_bytes(
                gzip.compress(b"pagefind_dcd" + json.dumps(fragment).encode()))
            self.assertEqual(check_site.check_search(Path(tmp)), [])
            self.assertEqual(len(check_site.check_search(Path(tmp), term="zebra")), 2)


if __name__ == "__main__":
    unittest.main()
