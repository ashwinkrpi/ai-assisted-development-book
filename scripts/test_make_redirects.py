#!/usr/bin/env python3
"""Unit tests for scripts/make_redirects.py: the files written and the URLs in them."""

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_redirects  # noqa: E402

SCRIPT = Path(__file__).resolve().parent / "make_redirects.py"

EXPECTED = {
    "index.html": "https://book.somaari.in/",
    "00-before-you-begin/index.html": "https://book.somaari.in/00-before-you-begin/",
    "01-foundations/01-introduction/index.html":
        "https://book.somaari.in/01-foundations/01-introduction/",
    "01-foundations/02-why-ai-is-transforming-software-development/index.html":
        "https://book.somaari.in/01-foundations/02-why-ai-is-transforming-software-development/",
    "01-foundations/03-understanding-large-language-models/index.html":
        "https://book.somaari.in/01-foundations/03-understanding-large-language-models/",
    "01-foundations/04-ai-assisted-software-development-lifecycle/index.html":
        "https://book.somaari.in/01-foundations/04-ai-assisted-software-development-lifecycle/",
    "01-foundations/05-building-your-ai-assisted-development-environment/index.html":
        "https://book.somaari.in/01-foundations/05-building-your-ai-assisted-development-environment/",
    "01-foundations/06-your-first-ai-assisted-software-project/index.html":
        "https://book.somaari.in/01-foundations/06-your-first-ai-assisted-software-project/",
    "glossary/index.html": "https://book.somaari.in/glossary/",
    "404.html": "https://book.somaari.in/",
}


class MakeRedirectsTest(unittest.TestCase):
    def test_writes_one_page_per_path_and_404(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, str(SCRIPT), tmp],
                                    capture_output=True, text=True, check=True)
            self.assertIn("wrote 10 pages", result.stdout)
            files = sorted(p.relative_to(tmp).as_posix() for p in Path(tmp).rglob("*") if p.is_file())
            self.assertEqual(files, sorted(EXPECTED))
            for rel, new_url in EXPECTED.items():
                with self.subTest(rel=rel):
                    text = Path(tmp, rel).read_text(encoding="utf-8")
                    self.assertNotIn("$NEW", text)
                    self.assertIn(f'<link rel="canonical" href="{new_url}">', text)
                    self.assertIn(f'<meta http-equiv="refresh" content="0; url={new_url}">', text)
                    self.assertIn(f'location.replace("{new_url}" + location.hash);', text)
                    self.assertIn(f'<a href="{new_url}">{new_url}</a>', text)
                    self.assertIn('<meta name="robots" content="noindex">', text)
                    # Only the new site is referenced.
                    urls = set(re.findall(r'https?://[^"<\s]+', text))
                    self.assertEqual(urls, {new_url})

    def test_usage_error_without_outdir(self):
        self.assertEqual(make_redirects.main(["make_redirects.py"]), 2)


if __name__ == "__main__":
    unittest.main()
