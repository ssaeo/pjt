import { createApp } from 'vue'
import { createPinia } from 'pinia'

import axios from 'axios'
// axios 기본 설정
axios.defaults.baseURL = 'http://localhost:8000'  // Django 서버 주소

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
