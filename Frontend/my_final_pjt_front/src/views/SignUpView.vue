<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card
          class="container"
          elevation="8"
          max-width="500"
          rounded="lg"
        >
          <h1 class="title">회원가입</h1>

          <form @submit.prevent="signUp" class="form">
            <v-text-field
              variant="outlined"
              color="#26A69A"
              label="아이디"
              v-model="state.username"
              :error-messages="errors.username ? [errors.username] : []"
              @blur="validateUsername"
            ></v-text-field>

            <v-text-field
              variant="outlined"
              color="#26A69A"
              label="닉네임"
              v-model="state.name"
              :error-messages="errors.name ? [errors.name] : []"
              @blur="validateName"
            ></v-text-field>

            <v-text-field
              variant="outlined"
              color="#26A69A"
              label="이메일"
              v-model="state.email"
              :error-messages="errors.email ? [errors.email] : []"
              @blur="validateEmail"
            ></v-text-field>

            <v-text-field
              variant="outlined"
              color="#26A69A"
              :append-icon="show1 ? 'mdi-eye-off' : 'mdi-eye'"
              :type="show1 ? 'text' : 'password'"
              label="비밀번호"
              v-model="state.password1"
              @click:append="show1 = !show1"
              :error-messages="errors.password1 ? [errors.password1] : []"
              @blur="validatePassword1"
            ></v-text-field>

            <v-text-field
              variant="outlined"
              color="#26A69A"
              :append-icon="show2 ? 'mdi-eye-off' : 'mdi-eye'"
              :type="show2 ? 'text' : 'password'"
              label="비밀번호 확인"
              v-model="state.password2"
              @click:append="show2 = !show2"
              :error-messages="errors.password2 ? [errors.password2] : []"
              @blur="validatePassword2"
            ></v-text-field>

            <div class="checkbox">
              <p class="warning">{{ errorAgree }}</p>
              <v-checkbox
                color="#26A69A"
                label="(필수) 약관 동의"
                value="service"
                v-model="selected"
              ></v-checkbox>
              <v-checkbox
                color="#26A69A"
                label="(필수) 약관 동의"
                value="info"
                v-model="selected"
              ></v-checkbox>
              <v-checkbox
                color="#26A69A"
                v-model="isAgreeAll"
              >
                <template v-slot:label>
                  <span class="color">전체 동의</span>
                </template>
              </v-checkbox>
            </div>

            <v-btn
              block
              variant="flat"
              color="#26A69A"
              @click.prevent="signUp"
            >
              가입하기
            </v-btn>
          </form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
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
    errors.value.username = '값을 입력해주세요.'
  } else if (!/^[a-zA-Z0-9]+$/.test(state.value.username)) {
    errors.value.username = '영문과 숫자만 입력해주세요'
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
    errors.value.name = '값을 입력해주세요.'
  } else if (state.value.name.length > 20) {
    errors.value.name = '20자 이하로 입력해야합니다.'
  } else {
    errors.value.name = ''
  }
}

const validateEmail = () => {
  if (!state.value.email) {
    errors.value.email = '값을 입력해주세요.'
  } else if (!/\S+@\S+\.\S+/.test(state.value.email)) {
    errors.value.email = '유효한 이메일 주소가 아닙니다.'
  } else if (state.value.email.length > 100) {
    errors.value.email = '100자 이하로 입력해야합니다.'
  } else {
    errors.value.email = ''
  }
}

const validatePassword1 = () => {
  if (!state.value.password1) {
    errors.value.password1 = '값을 입력해주세요.'
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
    errors.value.password2 = '값을 입력해주세요.'
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
        password: state.value.password1,
      }
      
      console.log('회원가입 요청 데이터:', payload)
      
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
  background-color: #FFFFFF;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.title {
  text-align: center; /* 가운데 정렬 */
  color: #26A69A; /* 색상 변경 */
  margin-bottom: 2rem; /* 아래쪽 간격 추가 */
}

form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 3rem; /* h1과 form 사이의 간격 추가 */
}

.checkbox {
  margin: 1rem 0;
  text-align: left;
  display: flex;
  flex-direction: column;
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