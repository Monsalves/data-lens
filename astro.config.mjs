import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://monsalves.github.io',
  base: '/data-lens',
  trailingSlash: 'always',
  integrations: [
    starlight({
      title: 'Data Lens',
      description: 'Metodología y planificación para evaluar la capa de datos.',
      defaultLocale: 'root',
      locales: { root: { label: 'Español', lang: 'es' } },
      favicon: '/favicon.svg',
      customCss: ['./src/styles/custom.css'],
      sidebar: [
        { label: 'Inicio', slug: '' },
        { label: 'Metodología 1.4', slug: 'metodologia' },
        { label: 'Planificación', slug: 'planificacion' },
        { label: 'Entregables', slug: 'entregables' }
      ],
      social: [{ icon: 'github', label: 'Repositorio del proyecto', href: 'https://github.com/Monsalves/data-lens' }]
    })
  ]
});
