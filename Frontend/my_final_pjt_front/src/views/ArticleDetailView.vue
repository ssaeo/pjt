<template>
  <div v-if="article" class="container">
    <GoToBack :goName="{ name: 'ArticleList', query: { page: pageNum } }" />
    <header>
      <div class="d-flex justify-space-between align-center">
        <h1>{{ article.title }}</h1>
        <div class="d-flex">
          <p class="mr-2 text-h7">작성자 :</p>
          <v-avatar size="x-small">
            <v-img
              cover
              :src="`${store.API_URL}${article.user.profile_img}`"
              alt="profile-img"
            ></v-img>
          </v-avatar>
          <p class="ml-1 text-h7">{{ article.user.name }}</p>
        </div>
      </div>
      <div class="d-flex justify-space-between">
        <div class="left">
          <span class="text-h7">작성일 : {{ formatDate(article.created_at) }}</span>
          <span class="text-h7 ml-3">수정일 : {{ formatDate(article.updated_at) }}</span>
        </div>
        <div class="right">
          <span class="text-h7">조회수: {{ article.views }}</span>
        </div>
      </div>
    </header>
    <v-divider class="my-3"></v-divider>

    <main class="position-relative" style="min-height: 200px;">
      <article class="text-h5 my-10">
        <div v-html="article.content"></div>
      </article>
      <div v-if="isPostedUser" class="edit-buttons">
        <v-btn
          class="edit-btn"
          size="small"
          :to="{ name: 'ArticleUpdate', params: { id: article.id }, query: { page: pageNum }}"
        >수정</v-btn>
        <v-btn
          class="delete-btn"
          size="small"
          @click.prevent="deleteArticle"
        >삭제</v-btn>
      </div>
    </main>
    <v-divider class="my-3"></v-divider>

    <h3 class="mb-5">댓글</h3>
    <div v-if="store.isLogin" class="my-4">
      <v-form
        class="d-flex align-center"
        @submit.prevent="createComment"
      >
        <v-text-field
          label="댓글을 입력해주세요."
          color="#26A69A"
          variant="outlined"
          v-model="newComment"
        ></v-text-field>
        <v-btn
          color="#26A69A"
          variant="tonal"
          size="large"
          class="mb-5 ml-3"
          @click.prevent="createComment"
        >
          댓글 작성
        </v-btn>
      </v-form>
    </div>

    <div v-if="comments.length > 0" class="comment-container" v-for="comment in comments" :key="comment.id">
      <div class="upper d-flex align-center mb-2">
        <v-avatar size="x-small">
          <v-img
            cover
            :src="`${store.API_URL}${comment.user.profile_img}`"
            alt="profile-img"
          ></v-img>
        </v-avatar>
        <p class="ml-1 text-h7">{{ comment.user.name }}</p>
      </div>
      <div class="lower mt-1 mb-10 text-h7 d-flex justify-space-between align-start">
        <p class="comment-left" v-html="comment.content"></p>
        <div v-if="store.user && comment.user.username === store.user.username" class="right">
          <v-btn
            class="edit-btn"
            size="small"
            @click="editComment(comment.id, comment.content)"
          >수정</v-btn>
          <v-btn
            class="delete-btn"
            size="small"
            @click="deleteComment(comment.id)"
          >삭제</v-btn>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import GoToBack from '@/components/GoToBack.vue'

const route = useRoute()
const router = useRouter()
const store = useCounterStore()

const article = ref(null)
const comments = ref([])
const newComment = ref('')
const isPostedUser = ref(false)
const pageNum = route.query.page

const formatDate = (dateString) => {
  const options = { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric', 
    hour: '2-digit', 
    minute: '2-digit', 
    second: '2-digit' 
  }
  return new Date(dateString).toLocaleString(undefined, options)
}

onMounted(() => {
  store.getArticleDetail(route.params.id)
    .then((response) => {
      article.value = response
      article.value.content = response.content.replaceAll("\n", "<br />")
      if (article.value.user && store.user && article.value.user.username === store.user.username) {
        isPostedUser.value = true
      }
      return store.getComments(route.params.id)
    })
    .then((response) => {
      comments.value = response
    })
    .catch((err) => {
      console.log(err)
    })
})

const deleteArticle = () => {
  if (confirm('정말 삭제하시겠습니까?')) {
    store.deleteArticle(route.params.id)
      .then(() => {
        router.push({ name: 'ArticleList', query: { page: pageNum } })
      })
      .catch((err) => {
        console.log(err)
      })
  }
}

const createComment = () => {
  store.createComment(route.params.id, newComment.value)
    .then((response) => {
      comments.value.push(response)
      newComment.value = ''
    })
    .catch((err) => {
      console.log(err)
    })
}

const deleteComment = (commentId) => {
  if (confirm('정말 삭제하시겠습니까?')) {
    store.deleteComment(route.params.id, commentId)
      .then(() => {
        comments.value = comments.value.filter((comment) => comment.id !== commentId)
      })
      .catch((err) => {
        console.log(err)
      })
  }
}

const editComment = (commentId, currentContent) => {
  const newContent = prompt('댓글을 수정하세요:', currentContent)
  if (newContent !== null && newContent !== currentContent) {
    store.updateComment(route.params.id, commentId, newContent)
      .then((updatedComment) => {
        const index = comments.value.findIndex(comment => comment.id === commentId)
        if (index !== -1) {
          comments.value[index] = updatedComment
        }
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
  position: relative;
}

.comment-left {
  width: 880px;
}

.right {
  width: 120px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.ml-3 {
  margin-left: 1rem;
}

.edit-buttons {
  position: absolute;
  right: 0;
  bottom: 20px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.edit-btn {
  background-color: #4CAF50; /* 수정 버튼 색상 */
  color: white;
  border-radius: 5px;
  margin-right: 5px;
  transition: background-color 0.3s;
}

.edit-btn:hover {
  background-color: #45a049; /* 수정 버튼 호버 색상 */
}

.delete-btn {
  background-color: #f44336; /* 삭제 버튼 색상 */
  color: white;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.delete-btn:hover {
  background-color: #e53935; /* 삭제 버튼 호버 색상 */
}
</style>