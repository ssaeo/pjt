<template>
  <div v-if="article">
    <h1>{{ article.title }}</h1>
    <p>작성자: {{ article.user.username }}</p>
    <p>{{ article.content }}</p>

    <div v-if="store.user?.username === article.user.username" class="article-actions">
      <button @click="startEditing" v-if="!isEditing">수정</button>
      <button @click="deleteArticle">삭제</button>
    </div>

    <form v-if="isEditing" @submit.prevent="updateArticle">
      <div>
        <label for="edit-title">제목:</label>
        <input 
          type="text" 
          id="edit-title" 
          v-model="editData.title" 
          required
        >
      </div>
      
      <div>
        <label for="edit-content">내용:</label>
        <textarea 
          id="edit-content" 
          v-model="editData.content" 
          required
        ></textarea>
      </div>

      <button type="submit">저장</button>
      <button type="button" @click="cancelEdit">취소</button>
    </form>

    <div class="comments-section">
      <h2>댓글</h2>
      <form v-if="store.isLogin" @submit.prevent="submitComment">
        <textarea v-model="newComment" required></textarea>
        <button type="submit">댓글 작성</button>
      </form>

      <ul class="comments-list">
        <li v-for="comment in comments" :key="comment.id">
          <p>{{ comment.content }}</p>
          <p>작성자: {{ comment.user.username }}</p>
          <button 
            v-if="store.user?.username === comment.user.username"
            @click="deleteComment(comment.id)"
          >
            삭제
          </button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'

const route = useRoute()
const router = useRouter()
const store = useCounterStore()

const article = ref(null)
const comments = ref([])
const newComment = ref('')
const isEditing = ref(false)
const editData = ref({
  title: '',
  content: ''
})

onMounted(() => {
  store.getArticleDetail(route.params.id)
    .then((response) => {
      article.value = response
      return store.getComments(route.params.id)
    })
    .then((response) => {
      comments.value = response
    })
    .catch((err) => {
      console.log(err)
    })
})

const startEditing = () => {
  editData.value = {
    title: article.value.title,
    content: article.value.content
  }
  isEditing.value = true
}

const cancelEdit = () => {
  isEditing.value = false
}

const updateArticle = () => {
  store.updateArticle(route.params.id, editData.value)
    .then((response) => {
      article.value = response
      isEditing.value = false
    })
    .catch((err) => {
      console.log(err)
    })
}

const deleteArticle = () => {
  if (confirm('정말 삭제하시겠습니까?')) {
    store.deleteArticle(route.params.id)
      .then(() => {
        router.push({ name: 'ArticleList' })
      })
      .catch((err) => {
        console.log(err)
      })
  }
}

const submitComment = () => {
  store.createComment(route.params.id, newComment.value)
    .then((response) => {
      comments.value.unshift(response)
      newComment.value = ''
    })
    .catch((err) => {
      console.log(err)
    })
}

const deleteComment = (commentId) => {
  if (confirm('댓글을 삭제하시겠습니까?')) {
    store.deleteComment(route.params.id, commentId)
      .then(() => {
        comments.value = comments.value.filter(c => c.id !== commentId)
      })
      .catch((err) => {
        console.log(err)
      })
  }
}
</script>