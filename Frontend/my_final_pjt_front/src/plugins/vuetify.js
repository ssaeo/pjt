// src/plugins/vuetify.js
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi'

// Vuetify 인스턴스를 생성합니다.
export default createVuetify({
  theme: {
    defaultTheme: 'light', // 기본 테마를 라이트 모드로 설정
    themes: {
      light: {
        colors: {
          primary: '#26A69A',
          secondary: '#b0bec5',
          // 기타 색상 설정
        },
      },
      dark: {
        colors: {
          primary: '#26A69A',
          secondary: '#b0bec5',
          // 기타 색상 설정
        },
      },
    },
  },
})