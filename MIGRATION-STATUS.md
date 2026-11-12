# Migration status

Short notes per sub-task, newest last. The next session reads this instead of the code.

## Stage 1.1 — Setup check and build script

### SU-01 (2026-11-12)

- Built: `scripts/check.sh` (Appendix A.1), `.node-version` (`24`), minimal `astro.config.mjs` (Starlight, title "AI Assisted Development Book", `site: 'https://book.somaari.in'`), `src/content.config.ts` (`docsLoader()` + `docsSchema()`), temporary page `src/content/docs/theme-sample.md`. `npm run build` passes and writes `dist/theme-sample/index.html`.
- CR-03 baseline: `python3 scripts/check_examples.py` prints `Checked 10 code blocks, 0 mismatches.` (still globbing `chapters/`).
- Installed versions (`package-lock.json`): `astro` 7.4.4, `@astrojs/starlight` 0.42.8, `@astrojs/markdown-remark` 7.3.5, `astro-mermaid` 2.2.0, `mermaid` 12.2.0, `remark-custom-heading-id` 2.0.0, `starlight-links-validator` 0.27.0, `wrangler` 4.155.0. No package is missing.
- Open, for later stages: Expressive Code still strips the `# tests/test_sample.py` first line into a block title (file-name extraction is not off yet); the `mermaid` block renders as plain code (`astro-mermaid` not wired in); there is no `index` page yet, so the build warns `Entry docs → 404 was not found` and the `i18n` collection is empty (both warnings only).
- Not run: the whole `sh scripts/check.sh` (runner rule: only affected checks; `check_examples.py` and `npm run build` were run separately and pass).

### Verify (2026-11-12): Stage 1.1 verified, Done when met

- Checked: `scripts/check.sh` matches Appendix A.1 line for line; `python3 scripts/check_examples.py` prints `Checked 10 code blocks, 0 mismatches.`; `npm run build` passes and writes `dist/theme-sample/index.html`; the block count and the eight package versions above match a fresh run and `package-lock.json`. There are no `scripts/test_*.py` yet. The whole `sh scripts/check.sh` was not run (runner rule; it runs at the end of the plan).
- Added by this stage: `scripts/check.sh`, `.node-version`, `astro.config.mjs`, `src/content.config.ts`, `src/content/docs/theme-sample.md`. No fixes were needed at verify. `node_modules/`, `dist/`, `.astro/` and `site/` are ignored and untracked (BD-04).
- Built sample page contains: both headings, the link, `python`, `text` and `mermaid` code blocks, the table and the note aside.
- Review in a browser before merging (not visible to a headless session): the sample page is readable in Starlight's default light and dark themes at desktop and phone width; the aside, table and code blocks look right; search opens.
- Open issues (unchanged, for later stages): the `# tests/test_sample.py` line is shown as a block title, not as code; the `mermaid` block is plain code; build warnings for the missing `index`/404 entry and the empty `i18n` collection.
