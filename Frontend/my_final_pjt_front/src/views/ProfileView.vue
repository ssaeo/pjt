<template>
  <div v-if="store.user">
    <h1>프로필</h1>
    <div v-if="!isEditing">
      <p>사용자명: {{ store.user.username }}</p>
      <button @click="startEditing">정보 수정</button>
      <button @click="confirmDelete">회원 탈퇴</button>
    </div>

    <form v-else @submit.prevent="updateProfile">
      <div>
        <label for="username">사용자명: </label>
        <input type="text" id="username" v-model="editedUser.username">
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
  isEditing.value = false
}

const confirmDelete = () => {
  if (confirm('정말 탈퇴하시겠습니까?')) {
    store.deleteAccount(store.user.username)
  }
}
</script>