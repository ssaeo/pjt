<template>
  <div class="container">
    <h1>Sign up to <span class="color">MYFI</span></h1>

    <div class="checkbox">
      <p class="warning" v-text="errorAgree"></p>
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

    <form @submit.prevent="signUp" @keypress.enter="signUp">
      <div>
        <label>아이디</label>
        <input type="text" v-model="state.value.username" @input="v$.value.username.$touch" @blur="v$.value.username.$touch">
        <span v-if="v$.value.username?.$error">{{ v$.value.username.$errors[0].$message }}</span>
      </div>

      <div>
        <label>닉네임</label>
        <input type="text" v-model="state.value.name" @input="v$.value.name.$touch" @blur="v$.value.name.$touch">
        <span v-if="v$.value.name?.$error">{{ v$.value.name.$errors[0].$message }}</span>
      </div>

      <div>
        <label>이메일</label>
        <input type="email" v-model="state.value.email" @input="v$.value.email.$touch" @blur="v$.value.email.$touch">
        <span v-if="v$.value.email?.$error">{{ v$.value.email.$errors[0].$message }}</span>
      </div>

      <div>
        <label>비밀번호</label>
        <input :type="show1 ? 'text' : 'password'" v-model="state.value.password1" @click="show1 = !show1" @input="v$.value.password1.$touch" @blur="v$.value.password1.$touch">
        <span v-if="v$.value.password1?.$error">{{ v$.value.password1.$errors[0].$message }}</span>
      </div>

      <div>
        <label>비밀번호 확인</label>
        <input :type="show2 ? 'text' : 'password'" v-model="state.value.password2" @click="show2 = !show2" @input="v$.value.password2.$touch" @blur="v$.value.password2.$touch">
        <span v-if="v$.value.password2?.$error">{{ v$.value.password2.$errors[0].$message }}</span>
      </div>

      <button type="submit">Sign up</button>
    </form>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useCounterStore } from '@/stores/counter'
import useVuelidate from '@vuelidate/core'
import { email, required, minLength, maxLength, alphaNum, sameAs, helpers } from '@vuelidate/validators'

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

const rules = {
  username: { 
    required: helpers.withMessage('필수 정보입니다.', required),
    alphaNum: helpers.withMessage('영어 대소문자와 숫자만 입력가능합니다.', alphaNum),
    minLength: helpers.withMessage('5자 이상 입력해야합니다.', minLength(5)),
    maxLength: helpers.withMessage('20자 이하로 입력해야합니다.', maxLength(20))
  },
  name: { 
    required: helpers.withMessage('필수 정보입니다.', required),
    maxLength: helpers.withMessage('20자 이하로 입력해야합니다.', maxLength(20))
  },
  email: {
    required: helpers.withMessage('필수 정보입니다.', required),
    email: helpers.withMessage('이메일 주소가 정확한지 확인해 주세요.', email),
    maxLength: helpers.withMessage('100자 이하로 입력해야합니다.', maxLength(100))
  },
  password1: { 
    required: helpers.withMessage('필수 정보입니다.', required),
    minLength: helpers.withMessage('8~16자의 영문 대/소문자, 숫자, 특수문자를 사용해 주세요. 특수문자는 *!@#$%^&만 사용가능합니다.', minLength(8)),
    maxLength: helpers.withMessage('8~16자의 영문 대/소문자, 숫자, 특수문자를 사용해 주세요. 특수문자는 *!@#$%^&만 사용가능합니다.', maxLength(16)),
    containspasswordrequirement: helpers.withMessage(
      '8~16자의 영문 대/소문자, 숫자, 특수문자를 사용해 주세요. 특수문자는 *!@#$%^&만 사용가능합니다.', 
      (value) => /(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])/.test(value)
    )
  },
  password2: { 
    required: helpers.withMessage('필수 정보입니다.', required),
    sameAsPassword: helpers.withMessage('비밀번호가 일치하지 않습니다.',
      sameAs(computed(() => state.value.password1))
    )
  }
}

const v$ = useVuelidate(rules, state)

const signUp = function () {
  v$.value.$validate()
  
  if (selected.value.length !== checkList.length) {
    errorAgree.value = '약관에 동의하셔야 합니다.'
  } else {
    errorAgree.value = 'ㅤ'
    if (!v$.value.$error){
      const payload = {
        username: state.value.username,
        name: state.value.name,
        email: state.value.email,
        password1: state.value.password1,
        password2: state.value.password2,
      }
      userStore.signUp(payload)
    }
  }
}
</script>

<style scoped>
.container {
  width: 500px;
  margin: 3rem auto;
  padding: 2rem;
  text-align: center;
}

.checkbox {
  margin: 1rem 0;
}

form * {
  text-align: start;
  margin: 0.6rem 0;
}

.warning {
  color: #b00020;
  font-size: 12px;
  margin: 0 0 0 15px;
}
</style>