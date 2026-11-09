import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://monsalves.github.io',
  base: '/data-lens',
  trailingSlash: 'always',
  redirects: { '/entregables/': '/data-lens/' }
});
