<template>
  <div class="exchange-calculator">
    <h1>환율 계산기</h1>

    <!-- rates를 store.exchangeRates로 변경 -->
    <div class="input-group">
      <label for="country-select">환율을 계산할 국가를 선택하세요:</label>
      <select id="country-select" v-model="selectedCountry">
        <option v-for="rate in store.exchangeRates" :key="rate.cur_unit" :value="rate.cur_unit">
          {{ rate.cur_nm }} ({{ rate.cur_unit }})
        </option>
      </select>
    </div>

    <!-- 원화 입력 -->
    <div class="input-group">
      <label for="krw-input">원화를 입력하세요 (KRW):</label>
      <input
        id="krw-input"
        v-model.number="krwAmount"
        type="number"
        placeholder="원화 금액을 입력하세요"
        @input="convertToForeign"
      />
      <p v-if="krwAmount > 0">
        {{ formatNumber(krwAmount) }} 원 → 
        {{ formatNumber(convertedForeignAmount) }} {{ selectedCountry }}
      </p>
    </div>

    <!-- 외화 입력 -->
    <div class="input-group">
      <label for="foreign-input">외화를 입력하세요 ({{ selectedCountry }}):</label>
      <input
        id="foreign-input"
        v-model.number="foreignAmount"
        type="number"
        placeholder="외화 금액을 입력하세요"
        @input="convertToKRW"
      />
      <p v-if="foreignAmount > 0">
        {{ formatNumber(foreignAmount) }} {{ selectedCountry }} → 
        {{ formatNumber(convertedKRWAmount) }} 원
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const selectedCountry = ref('')
const krwAmount = ref(0)
const foreignAmount = ref(0)
const convertedForeignAmount = ref(0)
const convertedKRWAmount = ref(0)

const convertToForeign = () => {
  const selectedRate = store.exchangeRates.find(rate => rate.cur_unit === selectedCountry.value)
  if (selectedRate) {
    convertedForeignAmount.value = krwAmount.value / parseFloat(selectedRate.deal_bas_r)
  }
}

const convertToKRW = () => {
  const selectedRate = store.exchangeRates.find(rate => rate.cur_unit === selectedCountry.value)
  if (selectedRate) {
    convertedKRWAmount.value = foreignAmount.value * parseFloat(selectedRate.deal_bas_r)
  }
}

const formatNumber = (number) => {
  return new Intl.NumberFormat().format(Number(number).toFixed(2))
}

onMounted(() => {
  store.loadExchangeRates()
  if (store.exchangeRates.length > 0) {
    selectedCountry.value = store.exchangeRates[0].cur_unit
  }
})
</script>

<style scoped>
.exchange-calculator {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.input-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
}

select, input {
  width: 100%;
  padding: 8px;
  margin-bottom: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

p {
  color: #2c3e50;
  font-size: 1.1em;
}
</style>