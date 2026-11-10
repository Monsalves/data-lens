import { defineConfig } from 'vite'
import { parse, compileScript } from '@vue/compiler-sfc'

// Compilador SFC local. Usa @vue/compiler-sfc, incluido con Vue.
const vueSfc = {
  name: 'data-lens-vue-sfc',
  enforce: 'pre',
  transform(source, id) {
    if (!id.endsWith('.vue')) return null
    const { descriptor, errors } = parse(source, { filename: id })
    if (errors.length) throw errors[0]
    const script = compileScript(descriptor, { id: 'data-lens-app', inlineTemplate: true })
    return { code: script.content, map: null }
  },
}

export default defineConfig({
  plugins: [vueSfc],
  server: { host: '127.0.0.1', port: 5173 },
})
