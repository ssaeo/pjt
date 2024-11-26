<template>
  <v-container class="container" v-if="store.user">
    <v-card class="pa-5 elevation-2">
      <v-card-title class="title">
        <h1>
          <span class="user-name">{{ store.user.name }}</span>님의 프로필 페이지
        </h1>
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
              <v-list-item v-for="(value, key) in userInfo" :key="key">
                <v-row class="align-center">
                  <v-col cols="4">
                    <v-list-item-title>{{ key }}</v-list-item-title>
                  </v-col>
                  <v-col cols="8">
                    <v-list-item-subtitle>{{ value }}</v-list-item-subtitle>
                  </v-col>
                </v-row>
              </v-list-item>
            </v-list>
          </v-col>
        </v-row>
        <v-divider class="my-4"></v-divider>
        <h2>가입한 금융 상품</h2>
        <v-row>
          <v-col v-for="product in userFinancialProducts" :key="product.product.id" cols="12" md="6" lg="4">
            <v-card class="product-card elevation-1" @click="selectProduct(product)">
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

        <!-- 가입한 상품 금리 -->
        <v-divider class="my-4"></v-divider>
        <h2 class="mb-4">가입한 상품 금리</h2>
        <v-row class="mb-4 d-flex align-center">
          <v-col cols="auto" class="d-flex align-center">
            <v-select
              v-model="selectedMonth"
              :items="[1, 3, 6, 12, 24, 36]"
              label="저축 기간 (단위: 개월)"
              variant="outlined"
              color="teal-lighten-1"
              class="small-select"
              :style="{ width: '200px' }" 
            ></v-select>
          </v-col>
        </v-row>
        <bar-chart
          :labels="chartLabels"
          :intrRate="chartBasicRates"
          :intrRate2="chartMaxRates"
        />

        <v-row justify="end" class="mt-4">
          <v-col cols="auto">
            <v-btn
              :style="{ backgroundColor: '#6c757d', color: 'white', marginRight: '8px' }"
              @click="openEditModal"
            >
              정보 수정하기
            </v-btn>
            <v-btn
              :style="{ backgroundColor: '#dc3545', color: 'white' }"
              @click="confirmDelete"
            >
              회원 탈퇴
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- 정보 수정 모달 -->
    <v-dialog v-model="isEditDialogOpen" max-width="600">
      <v-card>
        <v-card-title class="headline">정보 수정</v-card-title>
        <v-card-text>
          <v-form>
            <v-text-field v-model="editedUser.username" label="아이디" disabled variant="outlined" clearable color="teal-lighten-1"></v-text-field>
            <v-text-field v-model="editedUser.name" label="닉네임" variant="outlined" clearable color="teal-lighten-1"></v-text-field>
            <v-text-field v-model="editedUser.email" label="이메일" variant="outlined" clearable color="teal-lighten-1"></v-text-field>
            <v-text-field v-model="editedUser.age" label="나이" type="number" variant="outlined" clearable color="teal-lighten-1"></v-text-field>
            <v-text-field v-model="editedUser.address" label="주소" variant="outlined" clearable color="teal-lighten-1"></v-text-field>
            <v-file-input label="프로필 이미지" @change="handleImageChange" variant="outlined" clearable color="teal-lighten-1"></v-file-input>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="updateProfile">저장</v-btn>
          <v-btn color="grey" @click="cancelEdit">취소</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

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
            <v-row class="align-center">
              <v-col cols="4">
                <v-list-item-title>상품명</v-list-item-title>
              </v-col>
              <v-col cols="8">
                <v-list-item-subtitle class="multiline">{{ selectedProduct.product.fin_prdt_nm }}</v-list-item-subtitle>
              </v-col>
            </v-row>
          </v-list-item>
          <v-list-item>
            <v-row class="align-center">
              <v-col cols="4">
                <v-list-item-title>은행명</v-list-item-title>
              </v-col>
              <v-col cols="8">
                <v-list-item-subtitle class="multiline">{{ selectedProduct.product.kor_co_nm }}</v-list-item-subtitle>
              </v-col>
            </v-row>
          </v-list-item>
          <v-list-item>
            <v-row class="align-center">
              <v-col cols="4">
                <v-list-item-title>가입 대상</v-list-item-title>
              </v-col>
              <v-col cols="8">
                <v-list-item-subtitle class="multiline">{{ selectedProduct.product.join_member || '제한 없음' }}</v-list-item-subtitle>
              </v-col>
            </v-row>
          </v-list-item>
          <v-list-item>
            <v-row class="align-center">
              <v-col cols="4">
                <v-list-item-title>가입 방법</v-list-item-title>
              </v-col>
              <v-col cols="8">
                <v-list-item-subtitle class="multiline">{{ selectedProduct.product.join_way || '제한 없음' }}</v-list-item-subtitle>
              </v-col>
            </v-row>
          </v-list-item>
          <v-list-item>
            <v-row class="align-center">
              <v-col cols="4">
                <v-list-item-title>우대 조건</v-list-item-title>
              </v-col>
              <v-col cols="8">
                <v-list-item-subtitle class="multiline">{{ selectedProduct.product.spcl_cnd || '해당 없음' }}</v-list-item-subtitle>
              </v-col>
            </v-row>
          </v-list-item>
          <v-list-item>
            <v-row class="align-center">
              <v-col cols="4">
                <v-list-item-title>상품 설명</v-list-item-title>
              </v-col>
              <v-col cols="8">
                <v-list-item-subtitle class="multiline">{{ selectedProduct.product.etc_note || '추가 정보 없음' }}</v-list-item-subtitle>
              </v-col>
            </v-row>
          </v-list-item>
          <v-list-item>
            <v-row class="align-center">
              <v-col cols="4">
                <v-list-item-title>가입 제한</v-list-item-title>
              </v-col>
              <v-col cols="8">
                <v-list-item-subtitle class="multiline">{{ getJoinDenyText(selectedProduct.product.join_deny) }}</v-list-item-subtitle>
              </v-col>
            </v-row>
          </v-list-item>
        </v-list>
      </v-card-text>
      <v-card-actions class="justify-end">
        <v-btn color="red" @click="terminateSelectedProduct">
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
import BarChart from '@/components/BarChart.vue'

const route = useRoute()
const store = useCounterStore()
const isEditDialogOpen = ref(false)
const editedUser = ref({})
const selectedImage = ref(null)
const selectedProduct = ref(null)
const isDialogOpen = ref(false)
const selectedMonth = ref(6) // 기본 선택 개월

const profileImageUrl = computed(() => {
  return store.user?.profile_img || `${import.meta.env.VITE_BACKEND_URL}/media/image/profile.png`
})

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

const userInfo = computed(() => ({
  아이디: store.user.username,
  닉네임: store.user.name || '미설정',
  이메일: store.user.email || '미설정',
  나이: store.user.age || '미설정',
  주소: store.user.address || '미설정'
}))

const filteredProducts = computed(() => {
  return userFinancialProducts.value.map(product => {
    const option = product.options.find(opt => opt.save_trm === selectedMonth.value);
    if (option) {
      return {
        product: product.product,
        type: product.type,
        basicRate: option.intr_rate,
        maxRate: option.intr_rate2
      };
    }
    return null;
  }).filter(product => product !== null);
});

const averageRates = computed(() => {
  const totalProducts = filteredProducts.value.length;
  if (totalProducts === 0) return { basicRate: 0, maxRate: 0 };

  const totalBasicRate = filteredProducts.value.reduce((sum, product) => sum + product.basicRate, 0);
  const totalMaxRate = filteredProducts.value.reduce((sum, product) => sum + product.maxRate, 0);

  return {
    basicRate: totalBasicRate / totalProducts,
    maxRate: totalMaxRate / totalProducts
  };
});

const chartLabels = computed(() => {
  return ['평균', ...filteredProducts.value.map(product => product.product.fin_prdt_nm)];
});

const chartBasicRates = computed(() => {
  return [averageRates.value.basicRate, ...filteredProducts.value.map(product => product.basicRate)];
});

const chartMaxRates = computed(() => {
  return [averageRates.value.maxRate, ...filteredProducts.value.map(product => product.maxRate)];
});

const selectProduct = (product) => {
  if (product && product.product) {
    selectedProduct.value = product
    isDialogOpen.value = true
  } else {
    console.error('상품 선택 오류: 유효하지 않은 상품입니다.')
  }
}

const closeModal = () => {
  selectedProduct.value = null
  isDialogOpen.value = false
}

const terminateSelectedProduct = () => {
  if (selectedProduct.value && selectedProduct.value.product) {
    if (confirm(`정말 ${selectedProduct.value.product.fin_prdt_nm} 상품을 해지하시겠습니까?`)) {
      store.terminateProduct(selectedProduct.value.type, selectedProduct.value.product.id)
        .then(() => {
          alert('상품이 성공적으로 해지되었습니다.')
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

const openEditModal = () => {
  editedUser.value = { ...store.user }
  isEditDialogOpen.value = true
}

const handleImageChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    selectedImage.value = file
  }
}

const updateProfile = () => {
  console.log('updateProfile 함수 호출됨');
  const formData = new FormData();
  
  Object.keys(editedUser.value).forEach(key => {
    if (editedUser.value[key] !== store.user[key] && editedUser.value[key] !== null) {
      formData.append(key, editedUser.value[key]);
    }
  });

  if (selectedImage.value) {
    formData.append('profile_img', selectedImage.value);
  }

  store.updateProfile(store.user.username, formData)
    .then(() => {
      return store.getProfile(route.params.username);
    })
    .then(() => {
      isEditDialogOpen.value = false;
    })
    .catch((error) => {
      console.error('프로필 업데이트 실패:', error);
    });
}

const cancelEdit = () => {
  isEditDialogOpen.value = false
}

const confirmDelete = () => {
  if (confirm('정말 탈퇴하시겠습니까?')) {
    store.deleteAccount(store.user.username)
  }
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

.list-item-content {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 8px;
}

.product-card {
  cursor: pointer;
  transition: transform 0.2s;
}

.product-card:hover {
  transform: scale(1.05);
}

.multiline {
  white-space: pre-wrap;
  overflow-wrap: break-word;
  word-wrap: break-word;
}

.user-name {
  color: #42b983;
}

.elevation-2 {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: white;
  border-radius: 8px;
}

.elevation-1 {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background-color: white;
  border-radius: 8px;
}

.small-select .v-input__control {
  min-height: 32px; /* 높이 조정 */
}

.mb-4 {
  margin-bottom: 16px; /* 간격 조정 */
}

.d-flex {
  display: flex;
}

.align-center {
  align-items: center;
}

.mr-2 {
  margin-right: 8px;
}
</style>