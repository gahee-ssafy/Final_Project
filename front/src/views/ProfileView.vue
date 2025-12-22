
<!-- 가입 상품 금리를 가져와 막대 그래프로 보여주는 페이지 -->
<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'
import Chart from 'chart.js/auto'

const store = useAuthStore()
const profileData = ref(null)
const chartCanvas = ref(null)

onMounted(() => {
  // 1. 프로필 정보 가져오기
  axios({
    method: 'get',
    url: `${store.API_URL}/accounts/profile/`,
    headers: { Authorization: `Token ${store.token}` }
  })
  .then(res => {
    profileData.value = res.data
    createChart() // 데이터 로드 후 차트 생성
  })
})

const createChart = () => {
  if (!profileData.value.joined_deposit_products.length) return

  const ctx = chartCanvas.value.getContext('2d')
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: profileData.value.joined_deposit_products.map(p => p.fin_prdt_nm),
      datasets: [{
        label: '가입 상품 금리 비교',
        data: [3.5, 4.2, 3.8], // 실제로는 상품 데이터의 금리 필드 연결
        backgroundColor: 'rgba(66, 185, 131, 0.5)',
        borderColor: '#42b983',
        borderWidth: 1
      }]
    }
  })
}
</script>

<template>
  <div class="profile-container">
    <h1>내 프로필</h1>
    
    <section v-if="profileData" class="user-info">
      <div class="info-card">
        <p><strong>아이디:</strong> {{ profileData.username }}</p>
        <p><strong>닉네임:</strong> {{ profileData.nickname || '미설정' }}</p>
        <p><strong>자산:</strong> {{ profileData.money?.toLocaleString() }}원</p>
      </div>

      <div class="chart-section">
        <h3>📊 가입한 상품 금리 비교</h3>
        <canvas ref="chartCanvas"></canvas>
      </div>
    </section>
  </div>
</template>

<style scoped>
.profile-container { max-width: 800px; margin: 0 auto; padding: 20px; }
.info-card { background: #f9f9f9; padding: 20px; border-radius: 10px; margin-bottom: 30px; }
.chart-section { height: 400px; }
</style>