<template>
  <div class="container">
    <GoToBack :goName="{ name: 'ArticleList', query: { page: 1 } }" />
    <h1 class="title">글 쓰기</h1>
    <v-form class="my-5">
      <v-text-field
        variant="outlined"
        color="#26A69A"
        label="제목"
        v-model="state.title"
        :error-messages="v$.title.$errors.map(e => e.$message)"
        @input="v$.title.$touch"
        @blur="v$.title.$touch"
        @keypress.enter="createPost"
      ></v-text-field>
      <v-textarea
        variant="outlined"
        color="#26A69A"
        label="내용"
        v-model="state.content"
        auto-grow
        rows="15"
        row-height="25"
        shaped
        :error-messages="v$.content.$errors.map(e => e.$message)"
        @input="v$.content.$touch"
        @blur="v$.content.$touch"
      ></v-textarea>
      <v-btn
        block
        variant="flat"
        color="#26A69A"
        @click.prevent="createPost"
      >
        작성완료
      </v-btn>
    </v-form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import { useVuelidate } from '@vuelidate/core'
import { required, maxLength, helpers } from '@vuelidate/validators'

const initialState = {
  title: '',
  content: ''
}

const state = ref({
  ...initialState
})

const router = useRouter()
const store = useCounterStore()

const rules = {
  title: {
    required: helpers.withMessage('필수 정보입니다.', required),
    maxLength: helpers.withMessage('300자 이하로 입력해야합니다.', maxLength(300))
  },
  content: {
    required: helpers.withMessage('필수 정보입니다.', required),
    maxLength: helpers.withMessage('10000자 이하로 입력해야합니다.', maxLength(10000))
  }
}

const v$ = useVuelidate(rules, state)

const createPost = () => {
  v$.value.$validate()

  if (!v$.value.$error) {
    store.createArticle(state.value)
      .then((res) => {
        router.push({ name: 'ArticleDetail', params: { id: res.id }, query: { page: 1 } })
      })
      .catch((err) => {
        console.log(err)
      })
  }
}
</script>

<style scoped>
.container {
  width: 1000px;
  margin: 2rem auto;
}

.title {
  text-align: center; /* 가운데 정렬 */
  color: #26A69A; /* 색상 변경 */
  margin-bottom: 2rem; /* 아래쪽 간격 추가 */
}
</style>