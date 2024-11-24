<template>
  <div class="container">
    <h1>로그인</h1>
    <form @submit.prevent="logIn">
      <div>
        <label for="username">아이디: </label>
        <input type="text" id="username" v-model.trim="username" required>
      </div>

      <div>
        <label for="password">비밀번호: </label>
        <input type="password" id="password" v-model.trim="password" required>
      </div>

      <button type="submit">로그인</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import axios from 'axios'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')

const store = useCounterStore()
const router = useRouter()

const API_URL = 'http://127.0.0.1:8000'  // API URL 설정

const logIn = function () {
  axios({
    method: 'post',
    url: `${API_URL}/accounts/login/`,
    data: {
      username: username.value,
      password: password.value
    }
  })
    .then((res) => {
      console.log('로그인 성공:', res.data)
      store.token = res.data.token  // store에 token 저장
      store.user = res.data.user    // store에 user 정보 저장
      router.push({ 
        name: 'ProfileView', 
        params: { username: res.data.user.username } 
      })
    })
    .catch((err) => {
      console.log('로그인 실패:', err.response?.data)
      alert(err.response?.data?.error || '로그인에 실패했습니다.')
    })
}
</script>

<style scoped>
.container {
  width: 100%;
  max-width: 500px;
  margin: 3rem auto;
  padding: 2rem;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

form div {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

form label {
  font-weight: bold;
  margin-bottom: 0.5rem;
}

form input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

form button {
  padding: 0.75rem;
  background-color: #1089FF;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

form button:hover {
  background-color: #0a6dc2;
}
</style>