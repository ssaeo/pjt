<template>
  <div>
    <div v-if="loading">로딩 중...</div>
    <div v-else-if="product">
      <h1>{{ product.fin_prdt_nm }}</h1>
      <p><strong>은행명:</strong> {{ product.kor_co_nm }}</p>
      <p><strong>상품 설명:</strong> {{ product.etc_note || '설명이 없습니다.' }}</p>
      <p><strong>가입 방법:</strong> {{ product.join_way || '정보 없음' }}</p>
      <p><strong>가입 대상:</strong> {{ product.join_member || '정보 없음' }}</p>
      <p><strong>가입 제한:</strong> {{ getJoinDenyText(product.join_deny) }}</p>
      <p><strong>우대 조건:</strong> {{ product.spcl_cnd || '정보 없음' }}</p>

      <h2>기간별 금리</h2>
      <table v-if="options.length > 0" class="styled-table">
        <thead>
          <tr>
            <th>저축 기간</th>
            <th>기본 금리 (%)</th>
            <th>최대 금리 (%)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(option, index) in options" :key="option.id">
            <td>{{ formatTerm(index, option.save_trm, options) }}</td>
            <td>{{ formatRate(option.intr_rate) }}</td>
            <td>{{ formatRate(option.intr_rate2) }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else>옵션 정보가 없습니다.</p>
    </div>
    <div v-else>
      <p>상품 정보를 불러오는 데 실패했습니다.</p>
    </div>
    <button @click="goBack">뒤로 가기</button>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

export default {
  setup() {
    const product = ref(null) // 상품 데이터
    const options = ref([]) // 옵션 데이터
    const loading = ref(true) // 로딩 상태

    const route = useRoute() // Vue Router에서 현재 경로 정보 가져오기

    const getJoinDenyText = (joinDeny) => {
      switch (joinDeny) {
        case 1:
          return '제한 없음'
        case 2:
          return '서민 전용'
        case 3:
          return '일부 제한'
        default:
          return '정보 없음'
      }
    }

    const formatTerm = (index, term, optionsList) => {
      if (optionsList.length === 1) {
        return `${term}개월`
      }
      const nextOption = optionsList[index + 1]
      if (index === 0) {
        return nextOption ? `${term}개월 이상 ~ ${nextOption.save_trm}개월 미만` : `${term}개월 이상`
      }
      if (!nextOption) {
        return `${term}개월 이상`
      }
      return `${term}개월 이상 ~ ${nextOption.save_trm}개월 미만`
    }

    const formatRate = (rate) => {
      return rate === -1 || rate === null ? '-' : rate.toFixed(2)
    }

    const fetchProductDetails = async () => {
      const { productType, id } = route.params // Vue Router에서 매개변수 가져오기

      try {
        const response = await axios.get(`http://localhost:8000/finlife/products/${productType}/${id}/`)
        product.value = response.data.product
        options.value = response.data.options.sort((a, b) => a.save_trm - b.save_trm)
        loading.value = false
      } catch (error) {
        console.error('상품 정보를 불러오는 중 오류:', error)
        loading.value = false
      }
    }

    const goBack = () => {
      window.history.back()
    }

    onMounted(fetchProductDetails)

    return {
      product,
      options,
      loading,
      getJoinDenyText,
      formatTerm,
      formatRate,
      goBack,
    }
  },
}
</script>

<style scoped>
/* 테이블 스타일 */
.styled-table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
  font-size: 16px;
  text-align: center;
  border: 1px solid #ccc;
}

.styled-table th,
.styled-table td {
  padding: 12px 15px;
  border: 1px solid #ccc;
}

.styled-table thead tr {
  background-color: #f4f4f4;
  color: #333;
}

.styled-table tbody tr:nth-of-type(even) {
  background-color: #f9f9f9;
}

.styled-table tbody tr:hover {
  background-color: #e9ecef;
  cursor: pointer;
}

/* 버튼 스타일 */
button {
  margin-top: 20px;
  padding: 10px 20px;
  font-size: 14px;
  border: none;
  background-color: #6c757d;
  color: white;
  cursor: pointer;
}

button:hover {
  background-color: #5a6268;
}
</style>
