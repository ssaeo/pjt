<template>
  <div>
    <h1>게시글 목록</h1>
    <RouterLink 
      v-if="store.isLogin"
      :to="{ name: 'ArticleCreate' }"
      class="btn-create"
    >
      글쓰기
    </RouterLink>

    <ul class="article-list">
      <li v-for="article in articles" :key="article.id" class="article-item">
        <RouterLink :to="{ name: 'ArticleDetail', params: { id: article.id }}">
          <h3>{{ article.title }}</h3>
          <p>작성자: {{ article.user.username }}</p>
          <p>댓글: {{ article.comments_count }}</p>
        </RouterLink>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { RouterLink } from 'vue-router'

const store = useCounterStore()
const articles = ref([])

onMounted(() => {
  store.getArticles()
    .then((response) => {
      articles.value = response.results
    })
    .catch((err) => {
      console.log(err)
    })
})
</script>