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
import exchangeData from '@/assets/exchangeJSON.json';

export default {
  name: 'ExchangeCalculator',
  data() {
    return {
      rates: [], // 환율 데이터
      selectedCountry: '', // 선택된 국가
      krwAmount: 0, // 입력한 원화 금액
      foreignAmount: 0, // 입력한 외국 통화 금액
      convertedForeignAmount: 0, // 변환된 외국 통화 금액
      convertedKRWAmount: 0, // 변환된 원화 금액
    };
  },
  methods: {
    convertToForeign() {
      const selectedRate = this.rates.find(rate => rate.cur_unit === this.selectedCountry);
      if (selectedRate) {
        this.convertedForeignAmount = (this.krwAmount / parseFloat(selectedRate.deal_bas_r)).toFixed(2);
      }
    },
    convertToKRW() {
      const selectedRate = this.rates.find(rate => rate.cur_unit === this.selectedCountry);
      if (selectedRate) {
        this.convertedKRWAmount = (this.foreignAmount * parseFloat(selectedRate.deal_bas_r)).toFixed(2);
      }
    },
  },
  mounted() {
    // 환율 데이터 로드
    this.rates = exchangeData;
    if (this.rates.length > 0) {
      this.selectedCountry = this.rates[0].cur_unit; // 기본값 설정
    }
  },
};
</script>
