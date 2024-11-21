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
            v-for="product in filteredProducts" 
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
              <h5>우대 조건</h5>
              <p>{{ selectedProduct.product.spcl_cnd || '해당 없음' }}</p>
            </div>
          </div>

          <div class="rates-table">
            <h5>금리 정보</h5>
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
                <tr v-for="option in selectedProduct.options" :key="option.id">
                  <td>{{ option.save_trm }}개월</td>
                  <td>{{ option.intr_rate_type_nm }}</td>
                  <td>{{ formatRate(option.intr_rate) }}</td>
                  <td>{{ formatRate(option.intr_rate2) }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="product-notes">
            <h5>상품 설명</h5>
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
  if (!store.products?.deposits && !store.products?.savings) return []
  
  // deposits와 savings 배열을 각각 가공하고 합치기
  let allProducts = []
  
  if (store.products.deposits) {
    const deposits = store.products.deposits.map(item => ({
      ...item,
      type: 'deposit'
    }))
    allProducts = [...allProducts, ...deposits]
  }
  
  if (store.products.savings) {
    const savings = store.products.savings.map(item => ({
      ...item,
      type: 'saving'
    }))
    allProducts = [...allProducts, ...savings]
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

      const valueA = isNaN(rateA) || rateA === -1 ? -Infinity : rateA
      const valueB = isNaN(rateB) || rateB === -1 ? -Infinity : rateB

      return sortOrder.value === 'asc' ? valueA - valueB : valueB - valueA
    })
  }

  return allProducts
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
</script>

<style scoped>
.financial-products {
  padding: 20px;
}

.search-filters {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.search-input {
  flex: 1;
  max-width: 400px;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
}

th, td {
  padding: 12px;
  border: 1px solid #ddd;
  text-align: center;
}

th {
  background-color: #f8f9fa;
  position: relative;
}

.sort-buttons {
  display: inline-flex;
  flex-direction: column;
  margin-left: 5px;
}

.sort-buttons button {
  padding: 0 4px;
  font-size: 10px;
  border: none;
  background: none;
  cursor: pointer;
}

.product-row {
  cursor: pointer;
  transition: background-color 0.2s;
}

.product-row:hover {
  background-color: #f8f9fa;
}

/* 모달 스타일 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
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
}

.close-button:hover {
  color: #343a40;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.info-card {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.product-notes {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 6px;
  margin: 20px 0;
}

.join-button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.join-button:hover {
  background-color: #45a049;
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