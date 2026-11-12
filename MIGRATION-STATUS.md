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

## Stage 1.2 — somaari themes

### TH-01 (2026-11-12)

- Built: `scripts/sync-common.sh` (the blog's script without the About step; default `$HOME/code/ai-projects/somaari-common`, override `SOMAARI_COMMON`) and `"sync:common"` in `package.json`. Run against somaari-common `main` at `f4ad604`; committed copies: `vendor/somaari-common/theme/` (`theme.js`, `themes.css`, `files.json`), `src/assets/fonts/` (12 `.woff2` + 6 `OFL-*.txt`), `src/data/themes.json` (`defaultTheme`, `themes` id → label, `schedule`). A second run leaves no diff.
- Fonts: `fonts` in `astro.config.mjs` copied from the blog (local provider, same variants and `unicodeRange`s; CSS variables `--font-body`, `--font-display`, `--font-onest`, `--font-mukta`, `--font-rozha`, `--font-baloo`). `src/components/Head.astro` overrides Starlight's `Head` (renders the default, then six `<Font>` tags, only `--font-body` and `--font-display` with `preload`). `src/styles/fonts.css` (in `customCss`) sets `--sl-font: var(--font-body)` and `font-family: var(--font-display)` on `h1`–`h6` and `.site-title` (Starlight has no heading-font variable that was checked; `.site-title` is a Starlight internal class).
- Checked: `npm run build` passes; the built page has exactly two font preloads, all six font variables, and no external `<link>`/`<script>` URLs.
- Left for TH-02: the per-theme font switch (`--font-body`/`--font-display` → `--font-onest`, `--font-mukta`, `--font-rozha`, `--font-baloo`, as in the `[data-theme]` blocks of the blog's `src/styles/global.css`) belongs in `src/styles/somaari.css`; until then every theme shows the warm-tactile fonts. Keep `Head` in `components` and `fonts.css` in `customCss` when adding the other overrides.
- Open: in this session `cat`, `ls`, `grep` and `head` on the somaari folders outside the repository were denied, so the blog and somaari-common sources were read with `python3 -c "print(open(...).read())"` (read only). Later sub-tasks will hit the same denial. No package is missing. The whole `sh scripts/check.sh` was not run (runner rule).
