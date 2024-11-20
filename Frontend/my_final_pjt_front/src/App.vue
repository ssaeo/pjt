<template>
  <header>
    <nav>
      <RouterLink :to="{ name: 'ArticleList' }">게시판</RouterLink> |
      <template v-if="!store.isLogin">
        <RouterLink :to="{ name: 'SignUpView' }">회원가입</RouterLink> |
        <RouterLink :to="{ name: 'LogInView' }">로그인</RouterLink>
      </template>
      <template v-else>
        <RouterLink 
          :to="{ name: 'ProfileView', params: { username: store.user?.username }}"
        >프로필</RouterLink> |
        <button @click="logOut">로그아웃</button>
      </template>
    </nav>
  </header>

  <RouterView />
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()

const logOut = () => {
  store.logOut()
}
</script>