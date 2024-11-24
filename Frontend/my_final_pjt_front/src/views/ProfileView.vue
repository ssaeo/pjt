<template>
  <div class="container" v-if="store.user">
    <h1>프로필</h1>
    <div v-if="!isEditing">
      <!-- 이미지 표시 부분 -->
      <img 
        :src="profileImageUrl" 
        alt="프로필 이미지" 
        class="profile-image"
      />
      <!-- 나머지 프로필 정보 표시 -->
      <p>아이디: {{ store.user.username }}</p>
      <p>이메일: {{ store.user.email || '미설정' }}</p>
      <p>나이: {{ store.user.age || '미설정' }}</p>
      <p>주소: {{ store.user.address || '미설정' }}</p>
      <p>가입한 금융 상품: {{ store.user.fin_products || '없음' }}</p>
      <button @click="startEditing">정보 수정</button>
      <button @click="confirmDelete">회원 탈퇴</button>
    </div>

    <form v-else @submit.prevent="updateProfile">
      <div>
        <label for="username">아이디: </label>
        <input type="text" id="username" v-model="editedUser.username" disabled />
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
      <div>
        <label for="profile_img">프로필 이미지: </label>
        <input type="file" id="profile_img" @change="handleImageChange" accept="image/*" />
      </div>
      <button type="submit">저장</button>
      <button type="button" @click="cancelEdit">취소</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRoute } from 'vue-router'

const route = useRoute()
const store = useCounterStore()
const isEditing = ref(false)
const editedUser = ref({})
const selectedImage = ref(null)

// 프로필 이미지 URL 계산
const profileImageUrl = computed(() => {
  return store.user?.profile_img || `${import.meta.env.VITE_BACKEND_URL}/media/image/profile.png`
})

const startEditing = () => {
  editedUser.value = { ...store.user }
  isEditing.value = true
}

const handleImageChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    selectedImage.value = file
  }
}

const updateProfile = () => {
  const formData = new FormData()
  
  // 변경된 데이터만 FormData에 추가
  Object.keys(editedUser.value).forEach(key => {
    if (editedUser.value[key] !== store.user[key] && editedUser.value[key] !== null) {
      formData.append(key, editedUser.value[key])
    }
  })

  // 프로필 이미지 추가
  if (selectedImage.value) {
    formData.append('profile_img', selectedImage.value)
  }

  store.updateProfile(store.user.username, formData)
    .then(() => {
      return store.getProfile(route.params.username)
    })
    .then(() => {
      isEditing.value = false
    })
    .catch((error) => {
      console.error('프로필 업데이트 실패:', error)
    })
}

const cancelEdit = () => {
  isEditing.value = false
}

const confirmDelete = () => {
  if (confirm('정말 탈퇴하시겠습니까?')) {
    store.deleteAccount(store.user.username)
  }
}

onMounted(() => {
  store.getProfile(route.params.username)
})
</script>

<style scoped>
.container {
  width: 100%;
  max-width: 600px;
  margin: 3rem auto;
  padding: 2rem;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.profile-image {
  width: 200px;
  height: 200px;
  object-fit: cover;
  border-radius: 50%;
  margin-bottom: 20px;
}

form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

form div {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

form label {
  font-weight: bold;
  margin-bottom: 0.5rem;
}

form input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

form button {
  padding: 0.75rem;
  background-color: #1089FF;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

form button:hover {
  background-color: #0a6dc2;
}
</style>