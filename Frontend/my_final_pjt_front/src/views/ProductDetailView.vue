<template>
  <div class="product-detail">
    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      상품 정보를 불러오는 중...
    </div>

    <div v-else-if="product" class="product-container">
      <div class="product-header">
        <h2>{{ product.product.fin_prdt_nm }}</h2>
        <span class="bank-badge">{{ product.product.kor_co_nm }}</span>
      </div>

      <!-- 주요 정보 그리드 -->
      <div class="info-grid">
        <div class="info-card">
          <h3>가입 대상</h3>
          <p>{{ product.product.join_member || '제한 없음' }}</p>
        </div>
        <div class="info-card">
          <h3>가입 방법</h3>
          <p>{{ product.product.join_way || '제한 없음' }}</p>
        </div>
        <div class="info-card">
          <h3>가입 제한</h3>
          <p>{{ getJoinDenyText(product.product.join_deny) }}</p>
        </div>
        <div class="info-card">
          <h3>우대 조건</h3>
          <p>{{ product.product.spcl_cnd || '해당 없음' }}</p>
        </div>
      </div>

      <!-- 금리 정보 -->
      <div class="rates-section">
        <h3>금리 정보</h3>
        <div class="table-container">
          <table v-if="product.options?.length > 0" class="rates-table">
            <thead>
              <tr>
                <th>저축 기간</th>
                <th>금리 유형</th>
                <th>기본 금리</th>
                <th>최고 우대금리</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="option in sortedOptions" :key="option.id">
                <td>{{ formatTerm(option.save_trm) }}</td>
                <td>{{ option.intr_rate_type_nm }}</td>
                <td>{{ formatRate(option.intr_rate) }}</td>
                <td>{{ formatRate(option.intr_rate2) }}</td>
              </tr>
            </tbody>
          </table>
          <p v-else class="no-data">금리 정보가 없습니다.</p>
        </div>
      </div>

      <!-- 상품 설명 -->
      <div class="description-section">
        <h3>상품 설명</h3>
        <div class="description-content">
          {{ product.product.etc_note || '상품 설명이 없습니다.' }}
        </div>
      </div>

      <!-- 가입하기 버튼 -->
      <div class="action-buttons">
        <button 
          v-if="store.isLogin" 
          @click="joinProduct" 
          class="join-button"
        >
          가입하기
        </button>
        <button @click="goBack" class="back-button">
          목록으로
        </button>
      </div>
    </div>

    <div v-else class="error-message">
      <p>상품 정보를 불러오는데 실패했습니다.</p>
      <button @click="goBack" class="back-button">목록으로</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'

const route = useRoute()
const router = useRouter()
const store = useCounterStore()

const loading = ref(true)
const product = ref(null)

// 가입 제한 텍스트 변환
const getJoinDenyText = (joinDeny) => {
  const denyTexts = {
    1: '제한 없음',
    2: '서민전용',
    3: '일부제한',
  }
  return denyTexts[joinDeny] || '정보 없음'
}

// 기간 포맷
const formatTerm = (term) => {
  return `${term}개월`
}

// 금리 포맷
const formatRate = (rate) => {
  if (rate === null || rate === undefined || rate === -1) return '-'
  return `${rate.toFixed(2)}%`
}

// 옵션 정렬
const sortedOptions = computed(() => {
  if (!product.value?.options) return []
  return [...product.value.options].sort((a, b) => a.save_trm - b.save_trm)
})

// 상품 정보 조회
onMounted(async () => {
  const { type, id } = route.params
  try {
    const data = await store.fetchProductDetail(type, id)
    product.value = data
  } catch (error) {
    console.error('상품 정보 조회 실패:', error)
  } finally {
    loading.value = false
  }
})

// 상품 가입
const joinProduct = async () => {
  if (!product.value) return
  
  try {
    await store.joinFinancialProduct(
      route.params.type,
      product.value.product.id
    )
    alert('상품 가입이 완료되었습니다.')
    router.push('/financial-products')
  } catch (error) {
    alert('상품 가입에 실패했습니다.')
  }
}

// 뒤로 가기
const goBack = () => {
  router.push('/financial-products')
}
</script>

<style scoped>
.product-detail {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.loading {
  text-align: center;
  padding: 40px;
}

.loading-spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.product-header {
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  gap: 15px;
}

.bank-badge {
  background-color: #e9ecef;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 0.9em;
}

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
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.info-card h3 {
  color: #495057;
  margin-bottom: 10px;
  font-size: 1.1em;
}

.rates-section {
  margin: 30px 0;
}

.table-container {
  overflow-x: auto;
}

.rates-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
}

.rates-table th,
.rates-table td {
  padding: 12px;
  border: 1px solid #dee2e6;
  text-align: center;
}

.rates-table th {
  background-color: #f8f9fa;
  font-weight: 600;
}

.rates-table tr:hover {
  background-color: #f8f9fa;
}

.description-section {
  margin: 30px 0;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.description-content {
  white-space: pre-line;
  line-height: 1.6;
}

.action-buttons {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-top: 30px;
}

.join-button,
.back-button {
  padding: 12px 24px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.2s;
}

.join-button {
  background-color: #4CAF50;
  color: white;
}

.back-button {
  background-color: #6c757d;
  color: white;
}

.join-button:hover {
  background-color: #45a049;
}

.back-button:hover {
  background-color: #5a6268;
}

.error-message {
  text-align: center;
  padding: 40px;
  background-color: #fff3f3;
  border-radius: 8px;
  margin-top: 20px;
}

.no-data {
  text-align: center;
  padding: 20px;
  color: #6c757d;
}

@media (max-width: 768px) {
  .product-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    flex-direction: column;
  }

  .join-button,
  .back-button {
    width: 100%;
  }
}
</style>