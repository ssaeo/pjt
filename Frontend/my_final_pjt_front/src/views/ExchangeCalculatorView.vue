<template>
  <v-container class="exchange-calculator">
    <v-card
      class="mx-auto pa-12 pb-8 mt-15"
      elevation="8"
      max-width="800"
      rounded="lg"
    >
      <v-row>
        <v-col cols="12">
          <h1 class="exchange-title">환율 계산기</h1> <!-- 클래스 추가 -->
        </v-col>
      </v-row>

      <!-- 입력 모드 선택 -->
      <v-row justify="end">
        <v-col cols="auto">
          <v-radio-group v-model="inputMode" row>
            <v-radio label="원화 입력" value="krw" color="#26A69A"></v-radio>
            <v-radio label="외화 입력" value="foreign" color="#26A69A"></v-radio>
          </v-radio-group>
        </v-col>
      </v-row>

      <!-- 국가 선택 및 입력 필드 -->
      <v-row>
        <v-col cols="6">
          <v-select
            v-model="selectedCountry"
            :items="store.exchangeRates"
            item-title="cur_nm"
            item-value="cur_unit"
            label="국가 선택"
            variant="outlined"
            color="#26A69A"
            dense
          ></v-select>
        </v-col>
        <v-col cols="6">
          <v-text-field
            v-if="inputMode === 'krw'"
            v-model.number="krwAmount"
            label="원화 입력 (KRW)"
            type="number"
            variant="outlined"
            color="#26A69A"
            dense
            @input="convertToForeign"
          ></v-text-field>
          <v-text-field
            v-else
            v-model.number="foreignAmount"
            :label="`외화 입력 (${selectedCountry})`"
            type="number"
            variant="outlined"
            color="#26A69A"
            dense
            @input="convertToKRW"
          ></v-text-field>
        </v-col>
      </v-row>

      <!-- 변환된 값 출력 -->
      <v-row>
        <v-col cols="12">
          <v-text-field
            v-model="outputValue"
            :label="outputLabel"
            variant="outlined"
            color="#26A69A"
            dense
          ></v-text-field>
        </v-col>
      </v-row>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const selectedCountry = ref('')
const krwAmount = ref(0)
const foreignAmount = ref(0)
const convertedForeignAmount = ref(0)
const convertedKRWAmount = ref(0)
const inputMode = ref('krw') // 입력 모드: 'krw' 또는 'foreign'

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

const outputValue = computed(() => {
  return inputMode.value === 'krw'
    ? `${formatNumber(convertedForeignAmount.value)} ${selectedCountry.value}`
    : `${formatNumber(convertedKRWAmount.value)} 원`
})

const outputLabel = computed(() => {
  return inputMode.value === 'krw'
    ? `변환된 외화 (${selectedCountry.value})`
    : '변환된 원화 (KRW)'
})

onMounted(() => {
  store.loadExchangeRates()
  if (store.exchangeRates.length > 0) {
    selectedCountry.value = store.exchangeRates[0].cur_unit
  }
})
</script>

<style scoped>
.exchange-calculator {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.exchange-title {
  color: #26A69A; /* 원하는 색상으로 변경 */
}

p {
  color: #2c3e50;
  font-size: 1.1em;
  margin-top: 10px;
}
</style>