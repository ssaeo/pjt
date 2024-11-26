<template>
  <div class="chart-container">
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { defineProps, computed } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import ChartDataLabels from 'chartjs-plugin-datalabels'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ChartDataLabels)

const props = defineProps({
  labels: Array,
  intrRate: Array,
  intrRate2: Array
})

const chartData = computed(() => ({
  labels: props.labels,
  datasets: [
    {
      label: '기본 금리',
      data: props.intrRate,
      backgroundColor: 'rgba(66, 165, 245, 0.6)',
      borderColor: '#42A5F5',
      borderWidth: 1
    },
    {
      label: '최고 우대 금리',
      data: props.intrRate2,
      backgroundColor: 'rgba(102, 187, 106, 0.6)',
      borderColor: '#66BB6A',
      borderWidth: 1
    }
  ]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    title: {
      display: true,
      text: '금리 정보',
      font: {
        size: 18
      }
    },
    legend: {
      position: 'top',
      labels: {
        font: {
          size: 14
        }
      }
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          return `${context.dataset.label}: ${context.raw}%`;
        }
      }
    },
    datalabels: {
      anchor: 'end', // 막대의 끝에 레이블을 표시
      align: 'top',  // 막대의 위쪽에 레이블을 정렬
      formatter: (value) => `${value.toFixed(2)}%`, // 소수점 둘째 자리까지 표시
      color: 'black', // 레이블의 색상을 검은색으로 설정
      font: {
        size: 12
      }
    }
  },
  scales: {
    x: {
      grid: {
        display: false
      }
    },
    y: {
      beginAtZero: true,
      ticks: {
        callback: function(value) {
          return value + '%';
        }
      }
    }
  }
}
</script>

<style scoped>
.chart-container {
  height: 400px; /* 차트 높이를 설정 */
}
</style>