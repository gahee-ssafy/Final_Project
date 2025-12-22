<template>
  <div class="chart-container">
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
// 1. 필요한 모듈 가져오기
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'
import { Bar } from 'vue-chartjs'

// 2. Chart.js에 필요한 기능 등록 (필수)
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

// 3. 부모 컴포넌트에서 데이터 받기 (Props)
// 차트 컴포넌트는 데이터를 직접 Store에서 꺼내기보다, 
// 부모가 준 데이터를 그리기만 하는 '멍청한 컴포넌트(Dumb Component)'로 만드는 게 재사용성에 좋습니다.
const props = defineProps({
  chartData: {
    type: Object,
    required: true
  },
  chartOptions: {
    type: Object,
    default: () => ({
      responsive: true,
      maintainAspectRatio: false
    })
  }
})
</script>

<style scoped>
.chart-container {
  position: relative;
  height: 400px; /* 높이를 지정해야 차트가 보입니다 */
  width: 100%;
}
</style>