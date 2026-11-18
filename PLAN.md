# Somaari site improvements: book

Part C of `somaari-website/somaari-site-improvements-plan.md` (in the somaari-website folder). Shared files
are already in the repo: `scripts/fetch-network.mjs` (from somaari-site), a committed `network.json`
fallback, and reference copies of somaari-site's `partials.mjs`, `nav.js` and `style.css` in
`vendor/somaari-site/` (see its README).

### Shared header and footer
- [ ] [moderate] Override Starlight's `Header` and `Footer` in `astro.config.mjs` (`components: { Header, Footer }`) with the shared Somaari header, "Somaari sites" switcher and footer built from `network.json`, with Book highlighted (site id `book`). Keep Starlight's search, sidebar, theme picker (`ThemeSelect`) and mobile menu.
    Run `node scripts/fetch-network.mjs` before `astro build` in the `build` script so the build uses the live copy and falls back to the committed one.
    Build the markup the way `header(network, "book")` and `footer(network)` in `vendor/somaari-site/partials.mjs` do, with full `https://somaari.in/...` URLs; port styles from `vendor/somaari-site/style.css` onto the `--sl-color-*` and somaari tokens, and the switcher behaviour from `vendor/somaari-site/nav.js` as a bundled (not `is:inline`) script so the CSP in `public/_headers` needs no new hash. Keep the copyright and licence line in the footer. Update CLAUDE.md's layout notes.
- [ ] [simple] Link to Docs and the somaari.in apps from the footer (if the shared footer does not already).

### Theme and page details
- [ ] [moderate] Read and write the theme cookie on `.somaari.in` in `src/components/ThemeProvider.astro`, as somaari-common's `public/theme/theme.js` does (cookie `somaari-theme`, `Domain=somaari.in` only on somaari.in hosts, the cookie wins over localStorage, "auto" means no saved choice, try/catch when cookies are blocked); apply it to the colour variables only.
    ThemeProvider's script is inline, so after changing it run `sh scripts/check.sh` and paste the new hash it prints into the CSP in `public/_headers`.
- [ ] [moderate] Show a "somaari / book / <chapter>" breadcrumb above each page title, and a "Last updated" date taken from git on each page (Starlight's `lastUpdated: true`).
- [ ] [simple] Publish `stats.json` at the site root at build time: `{ "chapters": N }`, N = the number of chapter pages in the sidebar (Chapter 0 to Chapter 6 today), counted from the config or content, not hard-coded. somaari.in's "Explore Somaari" row reads it.

### UI polish
- [ ] [simple] Friendly 404 page with links to all sites (from `network.json`).
- [ ] [moderate] Contrast (WCAG AA), 44 px tap targets, no sideways scroll at 360 px, visible focus outlines, alt text, reduce-motion.

### SEO
- [ ] [simple] `sitemap.xml`, `robots.txt`, canonical URLs, OG and Twitter tags, title pattern "Page · Somaari Book". Keep what `scripts/check_site.py` checks passing.
- [ ] [simple] Add `Book` JSON-LD on the home page.

### Manual
- [ ] [manual] Preview the branch (`npm run build && npm run preview`) on phone and desktop; click through the switcher and footer links.
- [ ] [manual] Merge the branch into `main` and push; CI (`site.yml`) deploys book.somaari.in.
