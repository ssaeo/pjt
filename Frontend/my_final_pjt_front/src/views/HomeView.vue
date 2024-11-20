<template>
  <div>
    <h1>환율 계산기 서비스</h1>
    <p>간단하게 환율을 계산하고 외화를 변환해보세요.</p>
    <button @click="navigateToCalculator">환율 계산기로 이동</button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const navigateToCalculator = () => {
  router.push('/calculator')
}
</script>