import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'
import { ko } from 'vuetify/locale'
import axios from 'axios'
// axios 기본 설정
axios.defaults.baseURL = 'http://localhost:8000'  // Django 서버 주소

const vuetify = createVuetify({
  components,
  directives,
  locale: {
    locale: 'ko',
    messages: { ko }
  }
})

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(vuetify)

app.mount('#app')