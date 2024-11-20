<template>
  <div>
    <h1>상품 목록</h1>
    <table>
      <thead>
        <tr>
          <th>은행명</th>
          <th>상품명</th>
          <th>6개월</th>
          <th>12개월</th>
          <th>24개월</th>
          <th>36개월</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in products" :key="product.id">
          <td>{{ product.kor_co_nm }}</td>
          <td>
            <router-link :to="`/products/${product.type}/${product.id}`">
              {{ product.fin_prdt_nm }}
            </router-link>
          </td>
          <td>{{ product.interest_rates['6'] }}%</td>
          <td>{{ product.interest_rates['12'] }}%</td>
          <td>{{ product.interest_rates['24'] }}%</td>
          <td>{{ product.interest_rates['36'] }}%</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const products = ref([])

onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:8000/finlife/products/')
    const { deposits, savings } = response.data
    products.value = [...deposits, ...savings]
  } catch (error) {
    console.error('상품 목록을 불러오는 중 오류:', error)
  }
})
</script>