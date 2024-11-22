<template>
  <div v-if="store.user">
    <h1>프로필</h1>
    <div v-if="!isEditing">
      <p>아이디: {{ store.user.username }}</p>
      <p>이메일: {{ store.user.email }}</p>
      <p>나이: {{ store.user.age }}</p>
      <p>주소: {{ store.user.address }}</p>
      <p>가입한 금융 상품: {{ store.user.fin_products }}</p>
      <img :src="getProfileImageUrl(store.user.profile_img)" alt="프로필 이미지" />
      <button @click="startEditing">정보 수정</button>
      <button @click="confirmDelete">회원 탈퇴</button>
    </div>

    <form v-else @submit.prevent="updateProfile">
      <div>
        <label for="username">아이디: </label>
        <input type="text" id="username" v-model="editedUser.username" />
      </div>
      <div>
        <label for="email">이메일: </label>
        <input type="email" id="email" v-model="editedUser.email" />
      </div>
      <div>
        <label for="age">나이: </label>
        <input type="number" id="age" v-model="editedUser.age" />
      </div>
      <div>
        <label for="address">주소: </label>
        <input type="text" id="address" v-model="editedUser.address" />
      </div>
      <button type="submit">저장</button>
      <button type="button" @click="cancelEdit">취소</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRoute } from 'vue-router'

const route = useRoute()
const store = useCounterStore()
const isEditing = ref(false)
const editedUser = ref({})

onMounted(() => {
  store.getProfile(route.params.username)
})

const startEditing = () => {
  editedUser.value = { ...store.user }
  isEditing.value = true
}

const cancelEdit = () => {
  isEditing.value = false
}

const updateProfile = () => {
  store.updateProfile(store.user.username, editedUser.value)
    .then(() => {
      return store.getProfile(route.params.username) // 업데이트 후 프로필 새로고침
    })
    .then(() => {
      isEditing.value = false
    })
    .catch((error) => {
      console.error('프로필 업데이트 실패:', error)
    })
}

const confirmDelete = () => {
  if (confirm('정말 탈퇴하시겠습니까?')) {
    store.deleteAccount(store.user.username)
      .catch((error) => {
        console.error('회원 탈퇴 실패:', error)
      })
  }
}

// 프로필 이미지 URL 생성 함수
const getProfileImageUrl = (path) => {
  return `${import.meta.env.VITE_BACKEND_URL}/media/${path}`
}
</script>