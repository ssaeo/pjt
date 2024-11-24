<template>
  <v-container class="container" v-if="store.user">
    <v-card class="pa-5">
      <v-card-title class="title">
        <h1>{{ store.user.nickname }}님의 프로필 페이지</h1>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <v-row>
          <v-col cols="12" md="4" class="text-center">
            <v-avatar size="200">
              <v-img :src="profileImageUrl" alt="프로필 이미지"></v-img>
            </v-avatar>
          </v-col>
          <v-col cols="12" md="8">
            <v-list dense>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>아이디</v-list-item-title>
                  <v-list-item-subtitle>{{ store.user.username }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>닉네임</v-list-item-title>
                  <v-list-item-subtitle>{{ store.user.nickname || '미설정' }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>이메일</v-list-item-title>
                  <v-list-item-subtitle>{{ store.user.email || '미설정' }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>나이</v-list-item-title>
                  <v-list-item-subtitle>{{ store.user.age || '미설정' }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>주소</v-list-item-title>
                  <v-list-item-subtitle>{{ store.user.address || '미설정' }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-col>
        </v-row>
        <v-divider class="my-4"></v-divider>
        <h2>가입한 금융 상품</h2>
        <v-row>
          <v-col v-for="product in userFinancialProducts" :key="product.product.id" cols="12" md="6" lg="4">
            <v-card class="product-card" @click="selectProduct(product)">
              <v-card-title>
                <v-icon left>{{ product.type === 'deposit' ? 'mdi-bank' : 'mdi-piggy-bank' }}</v-icon>
                {{ product.product.fin_prdt_nm }}
              </v-card-title>
              <v-card-subtitle>{{ product.product.kor_co_nm }}</v-card-subtitle>
              <v-card-actions>
                <v-btn text color="primary" @click.stop="selectProduct(product)">자세히 보기</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
        <v-row justify="end" class="mt-4">
          <v-col cols="auto">
            <v-btn :style="{ backgroundColor: '#6c757d', color: 'white' }" @click="startEditing">정보 수정하기</v-btn>
            <v-btn :style="{ backgroundColor: '#dc3545', color: 'white' }" @click="confirmDelete">회원 탈퇴</v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- 상품 상세 모달 -->
    <v-dialog v-model="isDialogOpen" max-width="800">
      <v-card v-if="selectedProduct">
        <v-card-title class="headline grey lighten-3">
          <v-icon left>mdi-information-outline</v-icon>
          상품 상세 정보
        </v-card-title>
        <v-card-text>
          <v-list dense>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>상품명</v-list-item-title>
                <v-list-item-subtitle>{{ selectedProduct.product.fin_prdt_nm }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>은행명</v-list-item-title>
                <v-list-item-subtitle>{{ selectedProduct.product.kor_co_nm }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>가입 대상</v-list-item-title>
                <v-list-item-subtitle>{{ selectedProduct.product.join_member || '제한 없음' }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>가입 방법</v-list-item-title>
                <v-list-item-subtitle>{{ selectedProduct.product.join_way || '제한 없음' }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>우대 조건</v-list-item-title>
                <v-list-item-subtitle>{{ selectedProduct.product.spcl_cnd || '해당 없음' }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>상품 설명</v-list-item-title>
                <v-list-item-subtitle class="multiline">{{ selectedProduct.product.etc_note || '추가 정보 없음' }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>가입 제한</v-list-item-title>
                <v-list-item-subtitle>{{ getJoinDenyText(selectedProduct.product.join_deny) }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn color="red" @click="terminateProduct">
            <v-icon left>mdi-delete</v-icon>해지하기
          </v-btn>
          <v-btn color="grey" @click="closeModal">
            <v-icon left>mdi-cancel</v-icon>닫기
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRoute } from 'vue-router'

const route = useRoute()
const store = useCounterStore()
const isEditing = ref(false)
const editedUser = ref({})
const selectedImage = ref(null)
const selectedProduct = ref(null) // 선택된 상품
const isDialogOpen = ref(false) // 모달 열림 상태

// 프로필 이미지 URL 계산
const profileImageUrl = computed(() => {
  return store.user?.profile_img || `${import.meta.env.VITE_BACKEND_URL}/media/image/profile.png`
})

// 사용자가 가입한 금융 상품 목록
const userFinancialProducts = ref([])

onMounted(() => {
  store.getProfile(route.params.username)
  store.getMyFinancialProducts()
    .then((products) => {
      userFinancialProducts.value = products
    })
    .catch((err) => {
      console.error('가입한 금융 상품 조회 실패:', err)
    })
})

const selectProduct = (product) => {
  if (product && product.product) {
    selectedProduct.value = product
    isDialogOpen.value = true // 모달 열기
  } else {
    console.error('상품 선택 오류: 유효하지 않은 상품입니다.')
  }
}

const closeModal = () => {
  selectedProduct.value = null
  isDialogOpen.value = false // 모달 닫기
}

const terminateSelectedProduct = () => {
  if (selectedProduct.value && selectedProduct.value.product) {
    if (confirm(`정말 ${selectedProduct.value.product.fin_prdt_nm} 상품을 해지하시겠습니까?`)) {
      store.terminateProduct(selectedProduct.value.type, selectedProduct.value.product.id)
        .then(() => {
          alert('상품이 성공적으로 해지되었습니다.')
          // 해지된 상품을 목록에서 제거
          userFinancialProducts.value = userFinancialProducts.value.filter(
            (p) => p.product.id !== selectedProduct.value.product.id
          )
          closeModal()
        })
        .catch((error) => {
          console.error('상품 해지 실패:', error)
          alert('상품 해지에 실패했습니다. 다시 시도해 주세요.')
        })
    }
  } else {
    console.error('선택된 상품이 없습니다.')
  }
}

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

const formatRate = (rate) => {
  if (rate === undefined || rate === null || rate === -1) return '-'
  const parsedRate = parseFloat(rate)
  return isNaN(parsedRate) ? '-' : `${parsedRate}%`
}

const getJoinDenyText = (joinDeny) => {
  const denyTexts = {
    1: '제한 없음',
    2: '서민전용',
    3: '일부 제한',
  }
  return denyTexts[joinDeny] || '정보 없음'
}
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 3rem auto;
}

.title {
  color: #4b5320; /* 카키색 포인트 */
}

.v-card {
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.v-btn {
  margin-left: 8px;
}

.product-card {
  cursor: pointer;
  transition: transform 0.2s;
}

.product-card:hover {
  transform: scale(1.05);
}

.v-list-item-title {
  font-weight: bold;
}

.v-list-item-subtitle {
  color: #555;
}

.multiline {
  white-space: pre-wrap; /* 줄바꿈을 유지하여 텍스트를 표시 */
  overflow-wrap: break-word; /* 긴 단어를 줄바꿈 */
  word-wrap: break-word; /* 긴 단어를 줄바꿈 */
}
</style>