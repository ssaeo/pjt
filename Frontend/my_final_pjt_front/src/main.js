import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// 카카오맵 API 로드
const script = document.createElement('script')
script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${import.meta.env.VITE_KAKAO_MAP_API_KEY}&autoload=false`
script.async = true

// Vue 앱 생성
const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.use(router)

// 카카오맵 API 로드 후 앱 마운트
script.onload = () => {
  kakao.maps.load(() => {
    app.mount('#app')
  })
}

document.head.appendChild(script)