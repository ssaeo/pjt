<template>
  <div>
    <!-- <v-img
      class="mx-auto my-6"
      max-width="228"
      src="https://cdn.vuetifyjs.com/docs/images/logos/vuetify-logo-v3-slim-text-light.svg"
    ></v-img> -->
    
    <v-card
      class="mx-auto pa-12 pb-8 mt-15"
      elevation="8"
      max-width="448"
      rounded="lg"
    >
      <h1>로그인</h1>
      <div class="text-subtitle-1 text-medium-emphasis mt-5">아이디</div>

      <v-text-field
        density="compact"
        placeholder="아이디"
        prepend-inner-icon="mdi-account-outline"
        variant="outlined"
        v-model="username"
        color="teal-lighten-1"
        required
      ></v-text-field>

      <div class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
        비밀번호

        <!-- <a
          class="text-caption text-decoration-none text-blue"
          href="#"
          rel="noopener noreferrer"
          target="_blank"
        >
          비밀번호를 잊으셨나요?</a> -->
      </div>

      <v-text-field
        :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
        :type="visible ? 'text' : 'password'"
        density="compact"
        placeholder="비밀번호 입력"
        prepend-inner-icon="mdi-lock-outline"
        variant="outlined"
        v-model="password"
        color="teal-lighten-1"
        @click:append-inner="visible = !visible"
        required
      ></v-text-field>

      <v-btn
        class="mt-5 mb-8"
        color="#26A69A"
        size="large"
        variant="tonal"
        block
        @click="logIn"
        
      >
        로그인
      </v-btn>

      <v-card-text class="text-center">
        <a
          class="text-teal-lighten-1 text-decoration-none"
          href="#"
          @click.prevent="goToSignUp"
        >
          회원가입 <v-icon icon="mdi-chevron-right"></v-icon>
        </a>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import axios from 'axios'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const visible = ref(false)

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

const goToSignUp = () => {
  router.push({ name: 'SignUpView' })  // 회원가입 페이지로 이동
}
</script>

<style scoped>
.container {
  width: 100%;
  max-width: 500px;
  margin: 3rem auto;
  padding: 2rem;
  background-color: #FAFAFA;
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
  background-color: #26A69A;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

form button:hover {
  background-color: #26A69A;
}
</style>