<template>
  <div class="financial-products">
    <h2>금융상품 목록</h2>
    
    <!-- 검색 필터 -->
    <div class="search-filters">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="은행명 또는 상품명으로 검색"
        class="search-input"
      />
      <select v-model="productTypeFilter" class="filter-select">
        <option value="">전체 상품</option>
        <option value="deposit">예금</option>
        <option value="saving">적금</option>
      </select>
    </div>

    <!-- 상품 목록 테이블 -->
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>상품 유형</th>
            <th>은행명</th>
            <th>상품명</th>
            <th>
              6개월 금리
              <div class="sort-buttons">
                <button @click="sortByRate('6', 'desc')">▲</button>
                <button @click="sortByRate('6', 'asc')">▼</button>
              </div>
            </th>
            <th>
              12개월 금리
              <div class="sort-buttons">
                <button @click="sortByRate('12', 'desc')">▲</button>
                <button @click="sortByRate('12', 'asc')">▼</button>
              </div>
            </th>
            <th>
              24개월 금리
              <div class="sort-buttons">
                <button @click="sortByRate('24', 'desc')">▲</button>
                <button @click="sortByRate('24', 'asc')">▼</button>
              </div>
            </th>
            <th>
              36개월 금리
              <div class="sort-buttons">
                <button @click="sortByRate('36', 'desc')">▲</button>
                <button @click="sortByRate('36', 'asc')">▼</button>
              </div>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="product in paginatedProducts"
            :key="`${product.type}-${product.id}`"
            @click="selectProduct(product)"
            class="product-row"
          >
            <td>{{ product.type === 'deposit' ? '예금' : '적금' }}</td>
            <td>{{ product.kor_co_nm }}</td>
            <td>{{ product.fin_prdt_nm }}</td>
            <td>{{ formatRate(product?.interest_rates?.['6']) }}</td>
            <td>{{ formatRate(product?.interest_rates?.['12']) }}</td>
            <td>{{ formatRate(product?.interest_rates?.['24']) }}</td>
            <td>{{ formatRate(product?.interest_rates?.['36']) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 페이지네이션 -->
    <div class="pagination">
  <!-- 첫 페이지와 이전 페이지 -->
  <button class="page-button" @click="goToFirstPage" :disabled="currentPage === 1">«</button>
  <button class="page-button" @click="goToPrevPage" :disabled="currentPage === 1">‹</button>
  
  <!-- 숫자 버튼 -->
  <button
    v-for="page in totalPages"
    :key="page"
    @click="goToPage(page)"
    :class="['page-button', { active: page === currentPage }]"
  >
    {{ page }}
  </button>
  
  <!-- 다음 페이지와 마지막 페이지 -->
  <button class="page-button" @click="goToNextPage" :disabled="currentPage === totalPages">›</button>
  <button class="page-button" @click="goToLastPage" :disabled="currentPage === totalPages">»</button>
</div>
    
    <!-- 상품 상세 모달 -->
    <div v-if="selectedProduct" class="modal-overlay" @click.self="selectedProduct = null">
      <div class="modal-content">
        <div class="modal-header">
          <h3>상품 상세 정보</h3>
          <button @click="selectedProduct = null" class="close-button">×</button>
        </div>

        <div class="modal-body">
          <div class="product-header">
            <h4>{{ selectedProduct.product.fin_prdt_nm }}</h4>
            <span class="bank-badge">{{ selectedProduct.product.kor_co_nm }}</span>
          </div>

          <div class="info-grid">
            <div class="info-card">
              <h5>가입 대상</h5>
              <p>{{ selectedProduct.product.join_member || '제한 없음' }}</p>
            </div>
            <div class="info-card">
              <h5>가입 방법</h5>
              <p>{{ selectedProduct.product.join_way || '제한 없음' }}</p>
            </div>
            <div class="info-card">
              <h5>가입 제한</h5>
              <p>{{ getJoinDenyText(selectedProduct.product.join_deny) }}</p>
            </div>
            <div class="info-card">
              <h5>우대 조건</h5>
              <p>{{ selectedProduct.product.spcl_cnd || '해당 없음' }}</p>
            </div>
          </div>

          <div class="rates-table">
            <h4>금리 정보</h4>
            <div v-for="(options, group) in groupedOptions" :key="group" class="rate-group">
              <h5>{{ group }}</h5> <!-- 그룹명 출력 -->
              <table>
                <thead>
                  <tr>
                    <th>가입 기간</th>
                    <th>금리 유형</th>
                    <th>기본 금리</th>
                    <th>최고 우대 금리</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="option in options" :key="option.id">
                    <td>{{ option.save_trm }}개월</td>
                    <td>{{ option.intr_rate_type_nm }}</td>
                    <td>{{ formatRate(option.intr_rate) }}</td>
                    <td>{{ formatRate(option.intr_rate2) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>


          <div class="product-notes">
            <p>상품 설명</p>
            <!-- h태그 오류나서 p태그로 수정 -->
            <p>{{ selectedProduct.product.etc_note || '추가 정보 없음' }}</p>
          </div>

          <div class="modal-actions">
            <button 
              v-if="store.isLogin" 
              @click="joinProduct" 
              class="join-button"
            >
              가입하기
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
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
const selectedProduct = ref(null)
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
  if (!selectedProduct.value?.options) return {}

  // 그룹화
  return selectedProduct.value.options.reduce((acc, option) => {
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
  console.log('선택된 상품 원본:', product)  // 디버깅용 로그
  
  store.fetchProductDetail(product.type, product.id)
    .then((detail) => {
      // 상품 타입 정보 추가
      detail.product.type = product.type  // 이 부분이 중요
      console.log('가공된 상세 정보:', detail)
      selectedProduct.value = detail
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

  console.log('selectedProduct:', selectedProduct.value)

  // product 객체에서 직접 type과 id를 가져옴
  const productType = selectedProduct.value.product.type  // type 필드가 있는지 확인 필요
  const productId = selectedProduct.value.product.id

  console.log('전송할 데이터:', { productType, productId })

  // 값이 없는 경우 처리
  if (!productType || !productId) {
    alert('상품 정보가 올바르지 않습니다.')
    return
  }

  store.joinFinancialProduct(productType, productId)
    .then(() => {
      alert('상품 가입이 완료되었습니다.')
      selectedProduct.value = null
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
} // 가입제한 유형 추가

</script>

<style scoped>
/* 전체 레이아웃 */
.financial-products {
  padding: 20px;
  font-family: Arial, sans-serif;
}

/* 검색 필터 스타일 */
.search-filters {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.search-input {
  flex: 1;
  max-width: 400px;
  padding: 10px 15px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 16px;
  outline: none;
  transition: border-color 0.3s ease;
}

.search-input:focus {
  border-color: #42b983;
}

.filter-select {
  padding: 10px 15px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 16px;
  outline: none;
  transition: border-color 0.3s ease;
}

.filter-select:focus {
  border-color: #42b983;
}

/* 페이지네이션 컨테이너 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px; /* 버튼 간 간격 */
  margin-top: 20px;
}

/* 공통 버튼 스타일 */
.page-button {
  width: 50px; /* 버튼 너비 */
  height: 50px; /* 버튼 높이 */
  border: 1px solid #ddd;
  border-radius: 6px; /* 약간 둥근 모서리 */
  background-color: #f9f9f9;
  color: #333;
  font-size: 16px;
  font-weight: bold;
  text-align: center;
  line-height: 50px; /* 버튼 높이와 동일하게 설정 */
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 호버 효과 */
.page-button:hover:not(:disabled) {
  background-color: #42b983;
  color: #fff;
  border-color: #42b983;
}

/* 현재 페이지 버튼 강조 */
.page-button.active {
  background-color: #42b983;
  color: #fff;
  border-color: #42b983;
  pointer-events: none; /* 클릭 불가능 */
}

/* 비활성화 버튼 스타일 */
.page-button:disabled {
  background-color: #f1f1f1;
  color: #aaa;
  cursor: not-allowed;
}

/* 테이블 스타일 */
.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
  font-size: 14px;
}

th, td {
  padding: 15px;
  border: 1px solid #ddd;
  text-align: center;
}

th {
  background-color: #f1f1f1;
  position: relative;
  font-weight: bold;
}

.sort-buttons {
  display: inline-flex;
  flex-direction: column;
  margin-left: 5px;
}

.sort-buttons button {
  padding: 2px 5px;
  font-size: 10px;
  border: none;
  background: none;
  cursor: pointer;
  transition: color 0.3s ease;
}

.sort-buttons button:hover {
  color: #007bff;
}

.product-row {
  cursor: pointer;
  transition: background-color 0.2s;
}

.product-row:hover {
  background-color: #f9f9f9;
}

/* 페이지네이션 컨테이너 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin-top: 20px;
}

/* 공통 버튼 스타일 */
.page-button {
  width: 50px; /* 숫자 버튼 너비 */
  height: 50px; /* 숫자 버튼 높이 */
  border: 1px solid #ddd;
  border-radius: 6px; /* 약간 둥근 모서리 */
  background-color: #f9f9f9;
  color: #333;
  font-size: 16px; /* 텍스트 크기 */
  font-weight: bold; /* 텍스트 굵기 */
  display: flex; /* 중앙 정렬 */
  justify-content: center; /* 가로 중앙 정렬 */
  align-items: center; /* 세로 중앙 정렬 */
  cursor: pointer; /* 클릭 가능한 상태 */
  transition: all 0.3s ease; /* 부드러운 전환 효과 */
}

/* 좌우 버튼 크기 조정 */
.page-button.small {
  width: 40px; /* 좌우 버튼 너비 */
  height: 40px; /* 좌우 버튼 높이 */
  font-size: 14px; /* 좌우 버튼 글자 크기 */
}

/* 호버 효과 (하단 강조 색상 적용) */
.page-button:hover:not(.active):not(:disabled) {
  background-color: #42b983; /* 초록 계열 강조 */
  color: #fff;
  border-color: #42b983;
}

/* 현재 페이지 버튼 강조 */
.page-button.active {
  background-color: #42b983; /* 현재 페이지 강조 색상 */
  color: #fff;
  border-color: #42b983;
  pointer-events: none; /* 클릭 불가능 */
}

/* 비활성화 버튼 스타일 */
.page-button:disabled {
  background-color: #f1f1f1;
  color: #aaa;
  cursor: not-allowed;
}

/* 모달 스타일 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 12px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.modal-header {
  padding: 20px;
  border-bottom: 1px solid #dee2e6;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  background-color: white;
  z-index: 1;
}

.modal-header h3 {
  margin: 0;
}

.modal-body {
  padding: 20px;
}

.modal-actions {
  padding: 20px;
  border-top: 1px solid #dee2e6;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  position: sticky;
  bottom: 0;
  background-color: white;
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #6c757d;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.3s ease;
}

.close-button:hover {
  color: #343a40;
}

/* 상세 정보 카드 스타일 */
.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.info-card {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.info-card h5 {
  margin: 0 0 10px;
  font-size: 16px;
  /* color: #42b983; */
}

.info-card p {
  margin: 0;
  font-size: 14px;
  color: #333;
}

/* 기타 스타일 */
.product-notes {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 6px;
  margin: 20px 0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.join-button {
  padding: 12px 20px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.join-button:hover {
  background-color: #218838;
}

@media (max-width: 768px) {
  .search-filters {
    flex-direction: column;
  }

  .search-input {
    max-width: none;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .modal-content {
    width: 95%;
    margin: 10px;
  }
}
</style>