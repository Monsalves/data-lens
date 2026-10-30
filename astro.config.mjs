import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://monsalves.github.io',
  base: '/data-lens',
  trailingSlash: 'always',
  redirects: {
    '/metodologia/': 'https://github.com/Monsalves/data-lens/blob/main/metodologia/Marco_Trabajo_Datos_v1_4.md',
    '/entregables/': 'https://github.com/Monsalves/data-lens'
  }
});
