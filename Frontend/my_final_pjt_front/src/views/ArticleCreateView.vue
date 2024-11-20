<template>
  <div>
    <h1>게시글 작성</h1>
    <form @submit.prevent="submitArticle">
      <div>
        <label for="title">제목:</label>
        <input 
          type="text" 
          id="title" 
          v-model="articleData.title" 
          required
        >
      </div>
      
      <div>
        <label for="content">내용:</label>
        <textarea 
          id="content" 
          v-model="articleData.content" 
          required
        ></textarea>
      </div>

      <button type="submit">작성하기</button>
      <button type="button" @click="$router.go(-1)">취소</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'

const router = useRouter()
const store = useCounterStore()

const articleData = ref({
  title: '',
  content: ''
})

const submitArticle = () => {
  store.createArticle(articleData.value)
    .then(() => {
      router.push({ name: 'ArticleList' })
    })
    .catch((err) => {
      console.log(err)
    })
}
</script>