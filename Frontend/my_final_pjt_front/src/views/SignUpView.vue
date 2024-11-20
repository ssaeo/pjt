<template>
  <div>
    <h1>회원가입</h1>
    <form @submit.prevent="signUp">
      <div>
        <label for="username">아이디: </label>
        <input type="text" id="username" v-model.trim="username" required>
      </div>

      <div>
        <label for="password">비밀번호: </label>
        <input type="password" id="password" v-model.trim="password" required>
      </div>

      <button type="submit">가입하기</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'

const username = ref('')
const password = ref('')

const store = useCounterStore()

const signUp = function () {
  const payload = {
    username: username.value,
    password: password.value
  }
  store.signUp(payload)
}
</script>