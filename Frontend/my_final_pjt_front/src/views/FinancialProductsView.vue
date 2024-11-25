<template>
  <v-container class="financial-products">
    <v-card class="mx-auto pa-4" elevation="8" max-width="1200">
      <h2 class="text-center" style="color: #26A69A;">금융상품 목록</h2>

      <!-- 검색 필터 -->
      <v-row class="mb-4">
        <v-col cols="12" md="6">
          <v-text-field
            v-model="searchQuery"
            label="은행명 또는 상품명으로 검색"
            variant="outlined"
            color="#26A69A"
            dense
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="6">
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
      <v-data-table
        :headers="headers"
        :items="paginatedProducts"
        :items-per-page="itemsPerPage"
        class="elevation-1"
        dense
      >
        <template v-slot:item="{ item }">
          <tr @click="selectProduct(item)">
            <td>{{ item.type === 'deposit' ? '예금' : '적금' }}</td>
            <td>{{ item.kor_co_nm }}</td>
            <td>{{ item.fin_prdt_nm }}</td>
            <td>{{ formatRate(item.interest_rates['6']) }}</td>
            <td>{{ formatRate(item.interest_rates['12']) }}</td>
            <td>{{ formatRate(item.interest_rates['24']) }}</td>
            <td>{{ formatRate(item.interest_rates['36']) }}</td>
          </tr>
        </template>
      </v-data-table>

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
      <v-card>
        <v-card-title>
          <span class="headline">상품 상세 정보</span>
          <v-spacer></v-spacer>
          <v-btn icon @click="isDialogOpen = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text v-if="selectedProductData">
          <div class="product-header">
            <h4>{{ selectedProductData.product.fin_prdt_nm }}</h4>
            <span class="bank-badge">{{ selectedProductData.product.kor_co_nm }}</span>
          </div>

          <v-row class="info-grid">
            <v-col cols="12" md="6" v-for="info in productInfo" :key="info.title">
              <v-card class="info-card">
                <v-card-title>{{ info.title }}</v-card-title>
                <v-card-text>{{ info.content }}</v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <v-divider></v-divider>

          <h4>금리 정보</h4>
          <v-row v-for="(options, group) in groupedOptions" :key="group" class="rate-group">
            <v-col cols="12">
              <h5>{{ group }}</h5>
              <v-data-table
                :headers="rateHeaders"
                :items="options"
                class="elevation-1"
                dense
              ></v-data-table>
            </v-col>
          </v-row>

          <v-divider></v-divider>

          <div class="product-notes">
            <p>상품 설명</p>
            <p>{{ selectedProductData.product.etc_note || '추가 정보 없음' }}</p>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            v-if="store.isLogin"
            color="success"
            @click="joinProduct"
          >
            가입하기
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const router = useRouter()

// 상태 관리
const searchQuery = ref('')
const productTypeFilter = ref('')
const sortColumn = ref(null)
const sortOrder = ref(null)
const isDialogOpen = ref(false)
const selectedProductData = ref(null)
const loading = ref(true)
const currentPage = ref(1)
const itemsPerPage = ref(30)

// 초기 데이터 로드
onMounted(() => {
  store.fetchProducts()
    .then(() => {
      loading.value = false
    })
    .catch((err) => {
      console.error('상품 목록 로드 실패:', err)
      loading.value = false
    })
})

// 검색 및 필터링된 상품 목록
const filteredProducts = computed(() => {
  let allProducts = []

  // deposits 데이터 처리
  if (store.products.deposits) {
    allProducts = allProducts.concat(
      store.products.deposits.map(item => ({
        ...item,
        type: 'deposit'
      }))
    )
  }

  // savings 데이터 처리
  if (store.products.savings) {
    allProducts = allProducts.concat(
      store.products.savings.map(item => ({
        ...item,
        type: 'saving'
      }))
    )
  }

  // 상품 유형 필터
  if (productTypeFilter.value) {
    allProducts = allProducts.filter(product => product.type === productTypeFilter.value)
  }

  // 검색어 필터
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim()
    allProducts = allProducts.filter(product =>
      product.kor_co_nm.toLowerCase().includes(query) ||
      product.fin_prdt_nm.toLowerCase().includes(query)
    )
  }

  // 금리 정렬
  if (sortColumn.value) {
    allProducts.sort((a, b) => {
      const rateA = parseFloat(a?.interest_rates?.[sortColumn.value]) || 0
      const rateB = parseFloat(b?.interest_rates?.[sortColumn.value]) || 0

      // NaN 처리 및 정렬
      const valueA = isNaN(rateA) || rateA === -1 ? -Infinity : rateA
      const valueB = isNaN(rateB) || rateB === -1 ? -Infinity : rateB

      return sortOrder.value === 'asc' ? valueA - valueB : valueB - valueA
    })
  }

  // 최종 필터링된 상품 배열 반환
  return allProducts
})

// 페이지네이션
const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredProducts.value.slice(start, end)
})

const totalPages = computed(() => Math.ceil(filteredProducts.value.length / itemsPerPage.value))

const goToPage = page => {
  if (page >= 1 && page <= totalPages.value) currentPage.value = page
}

const goToFirstPage = () => (currentPage.value = 1)
const goToLastPage = () => (currentPage.value = totalPages.value)
const goToPrevPage = () => {
  if (currentPage.value > 1) currentPage.value--
}
const goToNextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++
}

const groupedOptions = computed(() => {
  if (!selectedProductData.value?.options) return {}

  // 그룹화
  return selectedProductData.value.options.reduce((acc, option) => {
    const groupKey = option.rsrv_type_nm || '정보 없음'
    if (!acc[groupKey]) {
      acc[groupKey] = []
    }
    acc[groupKey].push(option)
    return acc
  }, {})
})

// 상품 선택 및 상세 정보 조회
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
      isDialogOpen.value = true
    })
    .catch((err) => {
      console.error('상품 상세 정보 조회 실패:', err)
      alert('상품 정보를 불러오는데 실패했습니다.')
    })
}

// 금리 정렬
const sortByRate = (term, order) => {
  sortColumn.value = term
  sortOrder.value = order
}

// 금리 표시 형식화
const formatRate = (rate) => {
  if (rate === undefined || rate === null || rate === -1) return '-'
  const parsedRate = parseFloat(rate)
  return isNaN(parsedRate) ? '-' : `${parsedRate}%`
}

// 상품 가입
const joinProduct = () => {
  if (!store.isLogin) {
    alert('로그인이 필요한 서비스입니다.')
    router.push('/login')
    return
  }

  const productType = selectedProductData.value.product.type
  const productId = selectedProductData.value.product.id

  if (!productType || !productId) {
    alert('상품 정보가 올바르지 않습니다.')
    return
  }

  store.joinFinancialProduct(productType, productId)
    .then(() => {
      alert('상품 가입이 완료되었습니다.')
      isDialogOpen.value = false
    })
    .catch((err) => {
      const errorMessage = err.response?.data?.message || '상품 가입에 실패했습니다.'
      alert(errorMessage)
    })
}

const getJoinDenyText = (joinDeny) => {
  const denyTexts = {
    1: '제한 없음',
    2: '서민전용',
    3: '일부 제한',
  }
  return denyTexts[joinDeny] || '정보 없음'
}

const productTypes = [
  { text: '전체 상품', value: '' },
  { text: '예금', value: 'deposit' },
  { text: '적금', value: 'saving' }
]

const headers = [
  { text: '상품 유형', value: 'type' },
  { text: '은행명', value: 'kor_co_nm' },
  { text: '상품명', value: 'fin_prdt_nm' },
  { text: '6개월 금리', value: '6' },
  { text: '12개월 금리', value: '12' },
  { text: '24개월 금리', value: '24' },
  { text: '36개월 금리', value: '36' }
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
</script>

<style scoped>
.financial-products {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.v-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.v-data-table {
  margin-top: 20px;
}

.v-pagination {
  justify-content: center;
}

.headline {
  color: #26A69A;
}

.v-btn {
  color: #26A69A;
}
</style>