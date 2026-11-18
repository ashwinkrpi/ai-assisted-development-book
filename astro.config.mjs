// @ts-check
import { readFileSync } from 'node:fs';
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightLinksValidator from 'starlight-links-validator';
import remarkCustomHeadingId from 'remark-custom-heading-id';
import mermaid from 'astro-mermaid';

// Each somaari theme's color-scheme (light or dark), read from the synced themes.css.
const themesCss = readFileSync(new URL('./public/theme/themes.css', import.meta.url), 'utf8');
const themeSchemes = [...themesCss.matchAll(/:root\[data-theme="([a-z-]+)"\]\s*\{\s*color-scheme:\s*(light|dark)/g)];
const themeSelectors = (scheme) =>
  themeSchemes.filter((m) => m[2] === scheme).map((m) => `[data-theme="${m[1]}"]`);
const lightThemesSelector = `:is(${[':not([data-theme])', ...themeSelectors('light')].join(',')})`;
const darkThemesSelector = `:is(${themeSelectors('dark').join(',')})`;

export default defineConfig({
  site: 'https://book.somaari.in',
  // Emit every bundled script as a file under /_astro/ instead of inlining small ones, so the
  // CSP in public/_headers needs hashes only for the few `is:inline` scripts (PC-02).
  vite: {
    build: { assetsInlineLimit: 0 },
  },
  // `### Agent {#agent}` in the glossary keeps the id `agent` (as MkDocs attr_list did),
  // and the `{#…}` text is removed from the heading.
  markdown: {
    remarkPlugins: [remarkCustomHeadingId],
  },
  integrations: [
    // Draws the `mermaid` fences in the browser (decision 3). It must come before Starlight.
    // src/styles/somaari.css colors the diagrams from the somaari tokens (LT-03).
    mermaid(),
    starlight({
      title: 'AI Assisted Development Book',
      // Fails the build on a broken internal link or heading anchor.
      plugins: [starlightLinksValidator()],
      // Head.astro links somaari-common's themes.css (tokens and fonts); fonts.css points Starlight
      // at --font and --font-display.
      // ThemeProvider and ThemeSelect replace Starlight's light/dark logic with the somaari themes;
      // somaari.css maps the somaari tokens onto --sl-color-*.
      // SocialIcons adds the Somaari link before the GitHub icon. Header adds the shared Somaari site
      // links and "Somaari sites" switcher; Footer adds the shared footer and the copyright line
      // (both built from network.json).
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/ashwinkrpi/ai-assisted-development-book' },
      ],
      components: {
        Head: './src/components/Head.astro',
        Header: './src/components/Header.astro',
        SocialIcons: './src/components/SocialIcons.astro',
        Footer: './src/components/Footer.astro',
        ThemeProvider: './src/components/ThemeProvider.astro',
        ThemeSelect: './src/components/ThemeSelect.astro',
      },
      customCss: ['./src/styles/fonts.css', './src/styles/somaari.css'],
      // Code blocks follow the color-scheme of the active somaari theme. The dark code theme is
      // the base; the light one applies to the light somaari themes and when there is no
      // data-theme (no JavaScript: rangoli).
      expressiveCode: {
        useStarlightDarkModeSwitch: false,
        useDarkModeMediaQuery: false,
        themeCssSelector: (theme) => (theme.type === 'light' ? lightThemesSelector : darkThemesSelector),
        // Keep `# tests/…` first lines in the code, so blocks stay byte-identical to examples/.
        frames: { extractFileNameFromCode: false },
      },
      // The labels and order of the MkDocs `nav`; previous/next links follow this order.
      sidebar: [
        { label: 'Home', link: '/' },
        { label: 'Chapter 0 — Before You Begin', slug: '00-before-you-begin' },
        {
          label: 'Part 1 — Foundations',
          items: [
            { label: 'Chapter 1 — Introduction', slug: '01-foundations/01-introduction' },
            { label: 'Chapter 2 — Why AI Is Transforming Software Development', slug: '01-foundations/02-why-ai-is-transforming-software-development' },
            { label: 'Chapter 3 — Understanding Large Language Models', slug: '01-foundations/03-understanding-large-language-models' },
            { label: 'Chapter 4 — The AI-Assisted Development Lifecycle', slug: '01-foundations/04-ai-assisted-software-development-lifecycle' },
            { label: 'Chapter 5 — Building Your Development Environment', slug: '01-foundations/05-building-your-ai-assisted-development-environment' },
            { label: 'Chapter 6 — Your First AI-Assisted Project', slug: '01-foundations/06-your-first-ai-assisted-software-project' },
          ],
        },
        { label: 'Glossary', slug: 'glossary' },
      ],
      // On-page contents: "On this page" is Starlight's English label; levels 2–3 as in MkDocs.
      tableOfContents: { minHeadingLevel: 2, maxHeadingLevel: 3 },
    }),
  ],
});
