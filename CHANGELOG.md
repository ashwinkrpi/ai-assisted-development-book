# Changelog

## Unreleased

### Site

- The site moves from MkDocs Material on GitHub Pages to Astro Starlight on Cloudflare at https://book.somaari.in/, styled with the somaari themes and self-hosted fonts. Every page path and heading anchor stays the same.
- The old GitHub Pages URLs redirect to the matching pages on the new site, keeping the `#anchor`.
- The book source moves from `chapters/` to `src/content/docs/`. Preview with `npm run dev`; `sh scripts/check.sh` replaces `mkdocs build --strict`. `mkdocs.yml` is removed.

### Licensing

- From this commit, book content is licensed under CC BY-NC-SA 4.0. Copies obtained earlier under CC BY 4.0 (including v1.0.0) keep the rights granted at that time.
- Code (`examples/`, `scripts/`, CI and tooling) stays under the MIT License. Code listings in the chapters that also appear in `examples/` are additionally available under MIT.
- Commercial use of the book content, including print or ebook editions, requires written permission from the author.

See [LICENSE](LICENSE) for the full terms.

## v1.0.0 — 2026-10-03

- First release of Volume 1 (Part 1: Foundations), Chapters 0–6 and the glossary.
