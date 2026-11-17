#!/usr/bin/env python3
"""Write the redirect pages for the old GitHub Pages site (DC-02).

Usage: python3 scripts/make_redirects.py OUTDIR

Standard library only. For every page path of MIGRATION-PLAN.md section 2.2,
writes OUTDIR/<path>index.html, plus OUTDIR/404.html, from the template in
Appendix A.3. Published on the gh-pages branch (LA-04), they send
https://ashwinkrpi.github.io/ai-assisted-development-book/<path> to
https://book.somaari.in/<path>, keeping the #anchor; any unknown path gets
404.html, which sends readers to the home page.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_site import PAGE_PATHS, SITE  # noqa: E402

TEMPLATE = """\
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>This book has moved</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="$NEW">
<meta http-equiv="refresh" content="0; url=$NEW">
<script>location.replace("$NEW" + location.hash);</script>
</head>
<body>
<p>This book has moved to <a href="$NEW">$NEW</a>.</p>
</body>
</html>
"""


def page(new_url):
    """The redirect page for one new URL."""
    return TEMPLATE.replace("$NEW", new_url)


def redirects():
    """(relative file path, new URL) for every page, then 404.html."""
    pairs = [(Path(path.strip("/"), "index.html"), SITE + path) for path in PAGE_PATHS]
    pairs.append((Path("404.html"), SITE + "/"))
    return pairs


def write(outdir):
    """Write all redirect pages under outdir; return the files written."""
    written = []
    for rel, new_url in redirects():
        target = Path(outdir, rel)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page(new_url), encoding="utf-8")
        written.append(target)
    return written


def main(argv):
    if len(argv) != 2:
        print("usage: make_redirects.py OUTDIR", file=sys.stderr)
        return 2
    files = write(argv[1])
    print(f"make_redirects: wrote {len(files)} pages to {argv[1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
