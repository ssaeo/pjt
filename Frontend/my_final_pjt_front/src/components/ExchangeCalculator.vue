<template>
  <div>
    <h1>환율 계산기</h1>

    <!-- 국가 선택 -->
    <div>
      <label for="country-select">환율을 계산할 국가를 선택하세요:</label>
      <select id="country-select" v-model="selectedCountry">
        <option v-for="rate in rates" :key="rate.cur_unit" :value="rate.cur_unit">
          {{ rate.cur_nm }} ({{ rate.cur_unit }})
        </option>
      </select>
    </div>

    <!-- 원화 입력 -->
    <div>
      <label for="krw-input">원화를 입력하세요 (KRW):</label>
      <input
        id="krw-input"
        v-model.number="krwAmount"
        type="number"
        placeholder="원화 금액을 입력하세요"
        @input="convertToForeign"
      />
      <p v-if="krwAmount > 0">{{ krwAmount }} 원 → {{ convertedForeignAmount }} {{ selectedCountry }}</p>
    </div>

    <!-- 외화 입력 -->
    <div>
      <label for="foreign-input">외화를 입력하세요 ({{ selectedCountry }}):</label>
      <input
        id="foreign-input"
        v-model.number="foreignAmount"
        type="number"
        placeholder="외화 금액을 입력하세요"
        @input="convertToKRW"
      />
      <p v-if="foreignAmount > 0">{{ foreignAmount }} {{ selectedCountry }} → {{ convertedKRWAmount }} 원</p>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import exchangeData from '@/assets/exchangeJSON.json'

export default {
  setup() {
    const rates = ref([]) // 환율 데이터
    const selectedCountry = ref('') // 선택된 국가
    const krwAmount = ref(0) // 입력한 원화 금액
    const foreignAmount = ref(0) // 입력한 외국 통화 금액
    const convertedForeignAmount = ref(0) // 변환된 외국 통화 금액
    const convertedKRWAmount = ref(0) // 변환된 원화 금액

    const convertToForeign = () => {
      const selectedRate = rates.value.find(rate => rate.cur_unit === selectedCountry.value)
      if (selectedRate) {
        convertedForeignAmount.value = (krwAmount.value / parseFloat(selectedRate.deal_bas_r)).toFixed(2)
      }
    }

    const convertToKRW = () => {
      const selectedRate = rates.value.find(rate => rate.cur_unit === selectedCountry.value)
      if (selectedRate) {
        convertedKRWAmount.value = (foreignAmount.value * parseFloat(selectedRate.deal_bas_r)).toFixed(2)
      }
    }

    onMounted(() => {
      // 환율 데이터 로드
      rates.value = exchangeData
      if (rates.value.length > 0) {
        selectedCountry.value = rates.value[0].cur_unit // 기본값 설정
      }
    })

    return {
      rates,
      selectedCountry,
      krwAmount,
      foreignAmount,
      convertedForeignAmount,
      convertedKRWAmount,
      convertToForeign,
      convertToKRW,
    }
  },
}
</script>
