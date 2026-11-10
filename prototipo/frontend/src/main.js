import { createApp } from 'vue'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import App from './App.vue'
import './style.css'

const vuetify = createVuetify({
  components,
  directives,
  icons: { defaultSet: 'mdi' },
  theme: {
    defaultTheme: 'dataLens',
    themes: {
      dataLens: {
        dark: false,
        colors: {
          primary: '#255ce8',
          secondary: '#00a8a0',
          background: '#f5f7fb',
          surface: '#ffffff',
          error: '#d6494f',
          warning: '#d98b16',
          success: '#23836e',
        },
      },
    },
  },
})

createApp(App).use(vuetify).mount('#app')
