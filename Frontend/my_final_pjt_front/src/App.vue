<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-links">
        <RouterLink :to="{ name: 'home' }">Home</RouterLink> |
        <RouterLink :to="{ name: 'ArticleList' }">게시판</RouterLink> |
        <RouterLink :to="{ name: 'BankMap' }">은행찾기</RouterLink> |
        <RouterLink :to="{ name: 'FinancialProducts' }">금융상품</RouterLink> |
        <RouterLink to="/exchange-calculator">환율계산기</RouterLink>
        <template v-if="!store.isLogin">
          <RouterLink :to="{ name: 'SignUpView' }">회원가입</RouterLink> |
          <RouterLink :to="{ name: 'LogInView' }">로그인</RouterLink>
        </template>
        <template v-else>
          <RouterLink 
            :to="{ name: 'ProfileView', params: { username: store.user?.username } }"
          >
            프로필
          </RouterLink> |
          <a href="#" @click.prevent="logout">로그아웃</a>
        </template>
      </div>
    </nav>

    <RouterView />
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()

const logout = () => {
  store.logOut()
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.navbar {
  padding: 20px;
  background-color: #f8f9fa;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nav-links {
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}

.nav-links a {
  color: #2c3e50;
  text-decoration: none;
  padding: 10px;
  margin: 0 5px;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.nav-links a:hover {
  color: #42b983;
}

.router-link-active {
  color: #42b983 !important;
  font-weight: bold;
}

/* 전역 스타일 */
button {
  cursor: pointer;
  transition: opacity 0.3s;
}

button:hover {
  opacity: 0.8;
}

h1, h2, h3, h4, h5, h6 {
  color: #2c3e50;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .nav-links {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .nav-links a {
    display: block;
  }

  .nav-links span {
    display: none;
  }
}
</style>