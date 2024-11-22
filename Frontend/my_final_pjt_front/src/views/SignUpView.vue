<template>
  <div class="container">
    <h1>회원가입</h1>

    <div class="checkbox">
      <p class="warning">{{ errorAgree }}</p>
      <label>
        <input type="checkbox" value="service" v-model="selected">
        (필수) 서비스 이용약관 동의
      </label>
      <label>
        <input type="checkbox" value="info" v-model="selected">
        (필수) 개인정보 처리 동의
      </label>
      <label>
        <input type="checkbox" v-model="isAgreeAll">
        <span class="color">전체 동의</span>
      </label>
    </div>

    <form @submit.prevent="signUp">
      <div>
        <label>아이디</label>
        <input type="text" v-model="state.username" @blur="validateUsername" :class="{ 'invalid': errors.username }">
        <span class="error" v-if="errors.username">{{ errors.username }}</span>
      </div>

      <div>
        <label>닉네임</label>
        <input type="text" v-model="state.name" @blur="validateName" :class="{ 'invalid': errors.name }">
        <span class="error" v-if="errors.name">{{ errors.name }}</span>
      </div>

      <div>
        <label>이메일</label>
        <input type="email" v-model="state.email" @blur="validateEmail" :class="{ 'invalid': errors.email }">
        <span class="error" v-if="errors.email">{{ errors.email }}</span>
      </div>

      <div>
        <label>비밀번호</label>
        <input :type="show1 ? 'text' : 'password'" v-model="state.password1" @blur="validatePassword1" :class="{ 'invalid': errors.password1 }">
        <span class="error" v-if="errors.password1">{{ errors.password1 }}</span>
      </div>

      <div>
        <label>비밀번호 확인</label>
        <input :type="show2 ? 'text' : 'password'" v-model="state.password2" @blur="validatePassword2" :class="{ 'invalid': errors.password2 }">
        <span class="error" v-if="errors.password2">{{ errors.password2 }}</span>
      </div>

      <button type="submit">Sign up</button>
    </form>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useCounterStore } from '@/stores/counter'

const userStore = useCounterStore()

const checkList = ['service', 'info']
const selected = ref([])
const show1 = ref(false)
const show2 = ref(false)

const isAgreeAll = computed({
  get() {
    return checkList.length === selected.value.length
  },
  set(e) {
    selected.value = e ? checkList : []
  }  
})

const errorAgree = ref('ㅤ')

const state = ref({
  username: '',
  name: '',
  email: '',
  password1: '',
  password2: '',
})

const errors = ref({
  username: '',
  name: '',
  email: '',
  password1: '',
  password2: '',
})

const validateUsername = () => {
  if (!state.value.username) {
    errors.value.username = '필수 정보입니다.'
  } else if (!/^[a-zA-Z0-9]+$/.test(state.value.username)) {
    errors.value.username = '영어 대소문자와 숫자만 입력가능합니다.'
  } else if (state.value.username.length < 5) {
    errors.value.username = '5자 이상 입력해야합니다.'
  } else if (state.value.username.length > 20) {
    errors.value.username = '20자 이하로 입력해야합니다.'
  } else {
    errors.value.username = ''
  }
}

const validateName = () => {
  if (!state.value.name) {
    errors.value.name = '필수 정보입니다.'
  } else if (state.value.name.length > 20) {
    errors.value.name = '20자 이하로 입력해야합니다.'
  } else {
    errors.value.name = ''
  }
}

const validateEmail = () => {
  if (!state.value.email) {
    errors.value.email = '필수 정보입니다.'
  } else if (!/\S+@\S+\.\S+/.test(state.value.email)) {
    errors.value.email = '이메일 주소가 정확한지 확인해 주세요.'
  } else if (state.value.email.length > 100) {
    errors.value.email = '100자 이하로 입력해야합니다.'
  } else {
    errors.value.email = ''
  }
}

const validatePassword1 = () => {
  if (!state.value.password1) {
    errors.value.password1 = '필수 정보입니다.'
  } else if (state.value.password1.length < 8 || state.value.password1.length > 16) {
    errors.value.password1 = '8~16자의 영문 대/소문자, 숫자, 특수문자를 사용해 주세요. 특수문자는 *!@#$%^&만 사용가능합니다.'
  } else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])/.test(state.value.password1)) {
    errors.value.password1 = '8~16자의 영문 대/소문자, 숫자, 특수문자를 사용해 주세요. 특수문자는 *!@#$%^&만 사용가능합니다.'
  } else {
    errors.value.password1 = ''
  }
}

const validatePassword2 = () => {
  if (!state.value.password2) {
    errors.value.password2 = '필수 정보입니다.'
  } else if (state.value.password2 !== state.value.password1) {
    errors.value.password2 = '비밀번호가 일치하지 않습니다.'
  } else {
    errors.value.password2 = ''
  }
}

const signUp = function () {
  validateUsername()
  validateName()
  validateEmail()
  validatePassword1()
  validatePassword2()
  
  if (selected.value.length !== checkList.length) {
    errorAgree.value = '약관에 동의하셔야 합니다.'
  } else {
    errorAgree.value = 'ㅤ'
    if (!Object.values(errors.value).some(error => error)) {
      const payload = {
        username: state.value.username,
        name: state.value.name,
        email: state.value.email,
        password: state.value.password1,  // 서버가 기대하는 필드명 확인
      }
      
      console.log('회원가입 요청 데이터:', payload)  // 요청 데이터 확인
      
      userStore.signUp(payload)
    }
  }
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

.checkbox {
  margin: 1rem 0;
  text-align: left;
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

form input.invalid {
  border-color: red;
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

.warning {
  color: #b00020;
  font-size: 12px;
  margin: 0 0 0 15px;
}

.error {
  color: red;
  font-size: 12px;
  margin-top: 0.5rem;
}
</style>