<template>
  <v-container class="financial-products">
    <v-card class="mx-auto pa-4 my-6" elevation="8" max-width="1200">
      <h1 class="text-center title-spacing" style="color: #26A69A;">금융상품 목록</h1>

      <!-- 검색 필터 -->
      <v-row class="mb-4">
        <v-col cols="12" md="8">
          <v-text-field
            v-model="searchQuery"
            label="은행명 또는 상품명으로 검색"
            variant="outlined"
            color="#26A69A"
            dense
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="4">
          <v-select
            v-model="productTypeFilter"
            :items="productTypes"
            item-title="text"
            item-value="value"
            label="상품 유형"
            variant="outlined"
            color="#26A69A"
            dense
          ></v-select>
        </v-col>
      </v-row>

      <!-- 상품 목록 테이블 -->
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>상품 유형</th>
              <th>은행명</th>
              <th>상품명</th>
              <th>6개월 금리</th>
              <th>12개월 금리</th>
              <th>24개월 금리</th>
              <th>36개월 금리</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in paginatedProducts" :key="item.id" @click="selectProduct(item)">
              <td>{{ item.type === 'deposit' ? '예금' : '적금' }}</td>
              <td>{{ item.kor_co_nm }}</td>
              <td>{{ item.fin_prdt_nm }}</td>
              <td>{{ formatRate(item.interest_rates['6']) }}</td>
              <td>{{ formatRate(item.interest_rates['12']) }}</td>
              <td>{{ formatRate(item.interest_rates['24']) }}</td>
              <td>{{ formatRate(item.interest_rates['36']) }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 페이지네이션 -->
      <v-pagination
        v-model="currentPage"
        :length="totalPages"
        class="mt-4"
        color="#26A69A"
      ></v-pagination>
    </v-card>

    <!-- 상품 상세 모달 -->
    <v-dialog v-model="isDialogOpen" max-width="800px">
      <v-card class="fixed-card">
        <v-card-title class="headline d-flex justify-space-between align-center">
          <span>상품 상세 정보</span>
          <v-btn icon @click="isDialogOpen = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text v-if="selectedProductData">
          <v-row>
            <v-col cols="12" md="6">
              <h4>{{ selectedProductData.product.fin_prdt_nm }}</h4>
              <span class="bank-badge">{{ selectedProductData.product.kor_co_nm }}</span>
            </v-col>
            <v-col cols="12" md="6" class="text-right">
              <!-- 로그인 상태일 때만 버튼 표시 -->
              <v-btn v-if="isLoggedIn" :color="isSubscribed ? 'error' : 'primary'" @click="toggleSubscription">
                {{ isSubscribed ? '해지하기' : '가입하기' }}
              </v-btn>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <v-row>
            <v-col cols="12" md="6" v-for="info in productInfo" :key="info.title">
              <v-card class="info-card pa-3">
                <v-card-title class="subtitle-1">{{ info.title }}</v-card-title>
                <v-card-text class="text-content">{{ info.content }}</v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <h4>금리 정보</h4>
          <div v-if="Object.keys(groupedOptions).length > 0">
            <v-row v-for="(options, group) in groupedOptions" :key="group" class="rate-group">
              <v-col cols="12">
                <!-- 적금일 경우에만 그룹 헤더 출력 -->
                <h5 v-if="selectedProductData.product.type === 'saving'">{{ group }}</h5>
                <!-- 헤더를 별도의 테이블로 추가 -->
                <table class="rate-table-header">
                  <thead>
                    <tr>
                      <th>가입기간 (단위:개월)</th>
                      <th>금리 유형</th>
                      <th>기본 금리</th>
                      <th>최고 우대 금리</th>
                    </tr>
                  </thead>
                </table>
                <v-data-table
                  :headers="rateHeaders"
                  :items="options"
                  class="elevation-1"
                  dense
                  hide-default-footer
                  hide-default-header
                ></v-data-table>
              </v-col>
            </v-row>
          </div>

          <v-divider class="my-4"></v-divider>

          <div class="product-notes">
            <p>상품 설명</p>
            <p class="text-content">{{ selectedProductData.product.etc_note || '추가 정보 없음' }}</p>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()

// 상태 관리
const searchQuery = ref('')
const productTypeFilter = ref('')
const currentPage = ref(1)
const itemsPerPage = ref(30)
const isDialogOpen = ref(false)
const selectedProductData = ref(null)
const isSubscribed = ref(false)

// 로그인 상태 확인
const isLoggedIn = computed(() => !!store.user)

// 사용자가 가입한 금융 상품 목록
const userFinancialProducts = ref([])

// 초기 데이터 로드
onMounted(() => {
  store.fetchProducts()
    .then(() => {
      if (isLoggedIn.value) {
        loadUserProducts() // 사용자 가입 상품 목록 로드
      }
    })
    .catch((err) => {
      console.error('상품 목록 로드 실패:', err)
    })
})

// 사용자 가입 상품 목록 로드
const loadUserProducts = () => {
  store.getMyFinancialProducts()
    .then((products) => {
      userFinancialProducts.value = products
    })
    .catch((err) => {
      console.error('사용자 가입 상품 로드 실패:', err)
    })
}

// 상품 목록 필터링
const filteredProducts = computed(() => {
  let allProducts = []

  if (store.products.deposits) {
    allProducts = allProducts.concat(
      store.products.deposits.map(item => ({
        ...item,
        type: 'deposit'
      }))
    )
  }

  if (store.products.savings) {
    allProducts = allProducts.concat(
      store.products.savings.map(item => ({
        ...item,
        type: 'saving'
      }))
    )
  }

  if (productTypeFilter.value) {
    allProducts = allProducts.filter(product => product.type === productTypeFilter.value)
  }

  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim()
    allProducts = allProducts.filter(product =>
      product.kor_co_nm.toLowerCase().includes(query) ||
      product.fin_prdt_nm.toLowerCase().includes(query)
    )
  }

  return allProducts
})

// 페이지네이션
const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredProducts.value.slice(start, end)
})

const totalPages = computed(() => Math.ceil(filteredProducts.value.length / itemsPerPage.value))

// 상품 선택 시 가입 상태 확인
const selectProduct = (product) => {
  if (!product || !product.type || !product.id) {
    console.error('상품 정보가 올바르지 않습니다:', product)
    alert('상품 정보를 불러오는데 실패했습니다.')
    return
  }

  store.fetchProductDetail(product.type, product.id)
    .then((detail) => {
      detail.product.type = product.type
      selectedProductData.value = detail
      isSubscribed.value = userFinancialProducts.value.some(p => p.product.id === product.id) // 가입 상태 확인
      isDialogOpen.value = true
    })
    .catch((err) => {
      console.error('상품 상세 정보 조회 실패:', err)
      alert('상품 정보를 불러오는데 실패했습니다.')
    })
}

// 가입/해지 토글 함수
const toggleSubscription = () => {
  const productType = selectedProductData.value.product.type
  const productId = selectedProductData.value.product.id

  if (isSubscribed.value) {
    // 해지 로직
    store.terminateProduct(productType, productId)
      .then(() => {
        alert('상품 해지가 완료되었습니다.')
        isSubscribed.value = false
        loadUserProducts() // 사용자 가입 상품 목록 갱신
      })
      .catch((err) => {
        console.error('상품 해지 실패:', err)
        alert('상품 해지에 실패했습니다.')
      })
  } else {
    // 가입 로직
    store.joinFinancialProduct(productType, productId)
      .then(() => {
        alert('상품 가입이 완료되었습니다.')
        isSubscribed.value = true
        loadUserProducts() // 사용자 가입 상품 목록 갱신
      })
      .catch((err) => {
        console.error('상품 가입 실패:', err)
        alert('상품 가입에 실패했습니다.')
      })
  }
}

// 금리 정보를 그룹화
const groupedOptions = computed(() => {
  if (!selectedProductData.value?.options) return {}

  return selectedProductData.value.options.reduce((acc, option) => {
    const groupKey = option.rsrv_type_nm || '정보 없음'
    if (!acc[groupKey]) {
      acc[groupKey] = []
    }
    acc[groupKey].push(option)
    return acc
  }, {})
})

const formatRate = (rate) => {
  if (rate === undefined || rate === null || rate === -1) return '-'
  const parsedRate = parseFloat(rate)
  return isNaN(parsedRate) ? '-' : `${parsedRate}%`
}

const productTypes = [
  { text: '전체 상품', value: '' },
  { text: '예금', value: 'deposit' },
  { text: '적금', value: 'saving' }
]

const rateHeaders = [
  { text: '가입 기간', value: 'save_trm' },
  { text: '금리 유형', value: 'intr_rate_type_nm' },
  { text: '기본 금리', value: 'intr_rate' },
  { text: '최고 우대 금리', value: 'intr_rate2' }
]

const productInfo = computed(() => [
  { title: '가입 대상', content: selectedProductData.value?.product.join_member || '제한 없음' },
  { title: '가입 방법', content: selectedProductData.value?.product.join_way || '제한 없음' },
  { title: '가입 제한', content: getJoinDenyText(selectedProductData.value?.product.join_deny) },
  { title: '우대 조건', content: selectedProductData.value?.product.spcl_cnd || '해당 없음' }
])

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
.financial-products {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.v-card {
  background-color: white; /* 카드 배경색을 흰색으로 설정 */
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); /* 그림자 추가 */
}

.table-container {
  overflow-x: auto;
  margin-top: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  table-layout: fixed; /* 테이블 레이아웃을 고정으로 설정 */
}

th, td {
  padding: 12px;
  text-align: center; /* 텍스트 가운데 정렬 */
  border-bottom: 1px solid #e0e0e0;
  white-space: nowrap; /* 텍스트 줄바꿈 방지 */
  overflow: hidden; /* 넘치는 텍스트 숨김 */
  text-overflow: ellipsis; /* 넘치는 텍스트에 ... 표시 */
}

th {
  background-color: #26A69A;
  color: white;
  font-weight: bold;
  text-transform: uppercase;
}

tr:hover {
  background-color: #f1f1f1;
}

.v-pagination {
  justify-content: center;
  margin-top: 20px;
}

.fixed-card {
  background-color: white; /* 모달 배경색을 흰색으로 설정 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 그림자 추가 */
  border-radius: 8px;
  min-height: 500px; /* 고정된 최소 높이 설정 */
}

.headline {
  color: #26A69A;
  font-weight: bold;
}

.bank-badge {
  background-color: #e0f7fa;
  color: #00796b;
  padding: 4px 8px;
  border-radius: 4px;
  display: inline-block;
  margin-top: 8px;
}

.info-card {
  background-color: white; /* 카드 배경색을 흰색으로 설정 */
  border-radius: 8px;
  height: 200px; /* 모든 카드의 높이를 동일하게 설정 */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center; /* 수직 및 수평 중앙 정렬 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 그림자 추가 */
}

.product-notes {
  margin-top: 16px;
  padding: 8px;
  background-color: #f9f9f9;
  border-radius: 8px;
  text-align: justify; /* 텍스트 정렬 */
}

.text-content {
  max-height: 100px; /* 텍스트의 최대 높이 설정 */
  overflow-y: auto; /* 텍스트가 넘칠 경우 스크롤바 표시 */
  text-overflow: ellipsis; /* 넘치는 텍스트에 ... 표시 */
  white-space: pre-wrap; /* 줄바꿈을 허용 */
}

.v-btn {
  margin: 8px;
}

.v-card-title {
  padding: 16px;
  background-color: white; /* 카드 제목 배경색을 흰색으로 설정 */
  border-bottom: 1px solid #e0e0e0;
}

.v-card-text {
  padding: 16px;
}

.v-divider {
  margin: 16px 0;
}

.rate-table-header th {
  text-align: center; /* 헤더 가운데 정렬 */
}

.title-spacing {
  margin-top: 40px; /* 위쪽 간격 */
  margin-bottom: 40px; /* 아래쪽 간격 */
}
</style>