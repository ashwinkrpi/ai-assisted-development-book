// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://book.somaari.in',
  integrations: [
    starlight({
      title: 'AI Assisted Development Book',
    }),
  ],
});
