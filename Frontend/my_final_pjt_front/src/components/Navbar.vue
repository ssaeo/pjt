<template>
  <v-app-bar app color="white" flat>
    <v-toolbar-title>
      <RouterLink :to="{ name: 'home' }" class="brand">
        <img src="@/assets/logo.png" alt="logo" class="logo" /> <!-- 로고 이미지 추가 -->
        FIPL
      </RouterLink>
    </v-toolbar-title>

    <v-tabs
      v-model="activeTab"
      background-color="white"
      slider-color="#26A69A"
      show-arrows
      class="nav-tabs"
    >
      <v-tab
        v-for="link in links"
        :key="link.name"
        :to="link.to"
        :value="link.name"
      >
        {{ link.label }}
      </v-tab>
    </v-tabs>

    <v-spacer></v-spacer>
    <v-spacer></v-spacer>
    <v-spacer></v-spacer>
    <v-spacer></v-spacer>
    <v-spacer></v-spacer>
    <v-spacer></v-spacer>

    <template v-if="!store.isLogin">
      <v-btn text :to="{ name: 'LogInView' }" class="auth-btn">로그인</v-btn>
      <v-btn text :to="{ name: 'SignUpView' }" class="auth-btn">회원가입</v-btn>
    </template>
    <template v-else>
      <v-btn text :to="{ name: 'ProfileView', params: { username: store.user?.username } }" class="auth-btn">
        프로필
      </v-btn>
      <v-btn text @click.prevent="logout" class="auth-btn">로그아웃</v-btn>
    </template>
  </v-app-bar>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const activeTab = ref('home')

const links = [
  { name: 'BankMap', label: '은행찾기', to: { name: 'BankMap' } },
  { name: 'ExchangeCalculator', label: '환율계산기', to: '/exchange-calculator' },
  { name: 'FinancialProducts', label: '금융상품', to: { name: 'FinancialProducts' } },
  { name: 'ArticleList', label: '게시판', to: { name: 'ArticleList' } }
]

const logout = () => {
  store.logOut()
}
</script>

<style scoped>
.brand {
  color: #26A69A;
  font-weight: bold;
  text-decoration: none;
  display: flex;
  align-items: center; /* 로고와 텍스트를 수직 가운데 정렬 */
}

.logo {
  height: 40px; /* 로고 이미지의 높이 설정 */
  margin-right: 8px; /* 로고와 텍스트 사이의 간격 */
}

.nav-tabs {
  color: #26A69A;
}

.v-tab {
  color: #26A69A;
}

.auth-btn {
  color: #26A69A;
}

.v-app-bar {
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>