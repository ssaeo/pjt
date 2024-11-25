<template>
  <v-app>
    <Navbar /> <!-- Navbar 컴포넌트 추가 -->

    <v-main>
      <v-container>
        <RouterView />
      </v-container>
    </v-main>

    <Footer class="footer"/>
  </v-app>
</template>

<script setup>
import { RouterView } from 'vue-router'
import Navbar from '@/components/Navbar.vue' // Navbar 컴포넌트 가져오기
import Footer from '@/components/Footer.vue' // Footer 컴포넌트 가져오기
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.footer {
  flex-shrink: 0;
}
</style>