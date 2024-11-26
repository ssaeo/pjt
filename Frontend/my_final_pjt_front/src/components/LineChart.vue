<template>
  <div>
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)

const props = defineProps({
  labels: Array,
  intrRate: Array,
  intrRate2: Array
})

const chartData = {
  labels: props.labels,
  datasets: [
    {
      label: '기본 금리',
      data: props.intrRate,
      borderColor: '#42A5F5',
      fill: false
    },
    {
      label: '최고 우대 금리',
      data: props.intrRate2,
      borderColor: '#66BB6A',
      fill: false
    }
  ]
}

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    title: {
      display: true,
      text: '금리 정보'
    }
  }
}
</script>