<template>
  <div class="container">
    <GoToBack :goName="{ name: 'ArticleDetail', params: { id: postId }, query: { page: pageNum }}" />
    <h1>게시글 수정하기</h1>
    <v-form class="my-5">
      <v-text-field
        variant="outlined"
        color="#1089FF"
        label="제목"
        v-model="state.title"
        :error-messages="v$.title.$errors.map(e => e.$message)"
        @input="v$.title.$touch"
        @blur="v$.title.$touch"
        @keypress.enter.prevent="updatePost"
      ></v-text-field>
      <v-textarea
        variant="outlined"
        color="#1089FF"
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
        color="#1089FF"
        @click.prevent="updatePost"
      >
        게시물 수정하기
      </v-btn>
    </v-form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
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

const route = useRoute()
const router = useRouter()
const store = useCounterStore()

const postId = route.params.id
const pageNum = route.query.page

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

onMounted(() => {
  store.getArticleDetail(postId)
    .then((res) => {
      state.value.title = res.title
      state.value.content = res.content
    })
    .catch((err) => {
      console.log(err)
    })
})

const updatePost = () => {
  v$.value.$validate()

  if (!v$.value.$error) {
    store.updateArticle(postId, state.value)
      .then((res) => {
        router.push({ name: 'ArticleDetail', params: { id: res.id }, query: { page: pageNum } })
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
</style>