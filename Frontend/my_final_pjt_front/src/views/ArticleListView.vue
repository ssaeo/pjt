<template>
  <v-container class="container">
    <div class="header d-flex justify-space-between align-end mb-4">
      <h1>게시글 목록</h1>
      <v-btn
        variant="flat"
        color="#26A69A"
        :to="{ name: 'ArticleCreate' }"
      >작성하기</v-btn>
    </div>
    <table class="elevation-6 mb-4">
      <thead class="table-header">
        <tr>
          <th class="left-align">번호</th>
          <th class="center-align">제목</th>
          <th class="right-align">글쓴이</th>
          <th class="right-align">조회수</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in articles" :key="item.id" @click="clickTr(item)">
          <td class="number-align">{{ item.id }}</td>
          <td class="center-align">{{ item.title }} [{{ item.comments_count }}]</td>
          <td class="right-align">
            <v-avatar size="small">
              <v-img
                cover
                :src="`${store.API_URL}${item.user.profile_img}`"
                alt="profile-img"
              ></v-img>
            </v-avatar>
            {{ item.user.name }}
          </td>
          <td class="views-align">{{ item.views }}</td>
        </tr>
      </tbody>
    </table>
    <v-pagination
      v-model="page"
      :length="totalPages"
      :total-visible="6"
      color="#26A69A"
      rounded="circle"
    ></v-pagination>
  </v-container>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const router = useRouter()
const page = ref(1)
const articles = ref([])
const totalPages = ref(1)

watch(page, () => {
  fetchArticles()
  window.scrollTo({ left: 0, top: 0, behavior: "smooth" })
  router.push({ name: 'ArticleList', query: { page: page.value } })
})

const fetchArticles = () => {
  store.getArticles(page.value)
    .then((response) => {
      articles.value = response.results
      totalPages.value = Math.ceil(response.count / 10) // assuming 10 articles per page
    })
    .catch((err) => {
      console.log(err)
    })
}

const clickTr = (item) => {
  console.log('Clicked item:', item); // 디버깅을 위해 item 객체 출력
  if (item && item.id) {
    router.push({ name: 'ArticleDetail', params: { id: item.id }, query: { page: page.value } })
  } else {
    console.error('Missing required param "id"')
  }
}

onMounted(() => {
  fetchArticles()
})
</script>

<style scoped>
.container {
  max-width: 1000px;
  margin: 2rem auto;
}

.header {
  margin-bottom: 2rem; /* 글쓰기 버튼과 게시글 목록 사이의 간격 */
}

.elevation-6 {
  border-radius: 5px;
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 2rem; /* 게시글 목록과 페이지네이션 사이의 간격 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 테이블에 그림자 추가 */
}

.table-header {
  background-color: #26A69A; /* 헤더 배경색 설정 */
  color: white; /* 헤더 텍스트 색상 */
}

th, td {
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

.left-align {
  text-align: left;
}

.center-align {
  text-align: center;
}

.right-align {
  text-align: right;
}

.number-align {
  text-align: left;
  padding-left: 20px; /* 번호를 조금 더 오른쪽으로 */
}

.views-align {
  text-align: right;
  padding-right: 20px; /* 조회수를 조금 더 왼쪽으로 */
}

tbody > tr {
  transition: 200ms;
  cursor: pointer;
}

tbody > tr:hover {
  background-color: rgb(247, 250, 253);
}
</style>