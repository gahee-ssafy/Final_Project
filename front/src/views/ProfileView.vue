<template>
  <div class="profile-container">
    <h1>내 프로필</h1>
    <hr />

    <div v-if="!profileData" class="loading-state">
      <p>사용자 정보를 불러오는 중입니다...</p>
    </div>

    <div v-else>
      <div v-if="!isEditing" class="info-card">
        <div class="user-details">
          <p><strong>아이디:</strong> {{ profileData.username }}</p>
          <p><strong>닉네임:</strong> {{ profileData.nickname || '미설정' }}</p>
          <p><strong>나이:</strong> {{ profileData.age }}세</p>
          <p><strong>이메일:</strong> {{ profileData.email }}</p>
          <p><strong>현재 자산:</strong> {{ profileData.money?.toLocaleString() }}원</p>
          <p><strong>연봉:</strong> {{ profileData.salary?.toLocaleString() }}원</p>
        </div>
        
        <div v-if="profileData.joined_deposit_products?.length" class="joined-products">
          <h4>가입한 예금 상품</h4>
          <ul>
            <li v-for="product in profileData.joined_deposit_products" :key="product.id">
              {{ product.fin_prdt_nm }} (ID: {{ product.id }})
            </li>
          </ul>
        </div>

        <button @click="toggleEdit" class="btn-edit">정보 수정하기</button>
      </div>

      <div v-else class="edit-form">
        <h3>회원정보 수정</h3>
        <form @submit.prevent="updateProfile">
          <div class="input-group">
            <label>닉네임</label>
            <input v-model="userInfo.nickname" type="text" />
          </div>
          <div class="input-group">
            <label>나이</label>
            <input v-model.number="userInfo.age" type="number" />
          </div>
          <div class="input-group">
            <label>자산 (원)</label>
            <input v-model.number="userInfo.money" type="number" />
          </div>
          <div class="input-group">
            <label>연봉 (원)</label>
            <input v-model.number="userInfo.salary" type="number" />
          </div>
          
          <div class="button-group">
            <button type="submit" class="btn-save">저장</button>
            <button type="button" @click="toggleEdit" class="btn-cancel">취소</button>
          </div>
        </form>
      </div>

      <div class="chart-section">
        <h3>📊 가입 상품 금리 비교</h3>
        <div class="canvas-container">
          <canvas ref="chartCanvas"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Chart from 'chart.js/auto'

const store = useAuthStore()
const router = useRouter()
const profileData = ref(null)
const chartCanvas = ref(null)
const isEditing = ref(false)
let chartInstance = null

// 수정용 임시 데이터
const userInfo = ref({
  username: '',
  nickname: '',
  email: '',
  age: null,
  money: 0,
  salary: 0
})

// 수정 모드 토글
const toggleEdit = () => {
  isEditing.value = !isEditing.value
  if (isEditing.value && profileData.value) {
    userInfo.value = { ...profileData.value }
  }
}

// 1. 프로필 정보 가져오기
const fetchProfile = () => {
  axios({
    method: 'get',
    url: `${store.API_URL}/accounts/profile/`,
    headers: { Authorization: `Bearer ${store.token}` } // JWT Bearer 방식 
  })
  .then(res => {
    profileData.value = res.data
    userInfo.value = { ...res.data }
    
    // 차트 생성 (데이터 로드 후 실행)
    if (res.data.joined_deposit_products?.length) {
      setTimeout(() => createChart(), 100)
    }
  })
  .catch(async (err) => {
    if (err.response?.status === 401) { // 토큰 만료 [cite: 507, 522]
      const ok = await store.refreshAccessToken() // [cite: 508, 525]
      if (ok) {
        fetchProfile() // 재시도 [cite: 535]
      } else {
        alert('다시 로그인이 필요합니다.') // [cite: 530]
        store.logOut()
        router.push({ name: 'LogInView' }) // [cite: 531]
      }
    }
  })
}

// 2. 프로필 정보 수정
const updateProfile = async () => {
  try {
    const res = await axios({
      method: 'put',
      url: `${store.API_URL}/accounts/profile/update/`,
      data: userInfo.value,
      headers: { Authorization: `Bearer ${store.token}` }
    })
    profileData.value = res.data
    isEditing.value = false
    alert('회원정보가 수정되었습니다.')
    createChart()
  } catch (err) {
    if (err.response?.status === 401) {
      const ok = await store.refreshAccessToken()
      if (ok) updateProfile()
    }
  }
}

// 3. 차트 생성 로직
const createChart = () => {
  if (!chartCanvas.value || !profileData.value?.joined_deposit_products?.length) return
  if (chartInstance) chartInstance.destroy()

  const ctx = chartCanvas.value.getContext('2d')
  chartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: profileData.value.joined_deposit_products.map(p => p.fin_prdt_nm),
      datasets: [{
        label: '가입 상품 금리 (%)',
        data: profileData.value.joined_deposit_products.map(p => p.intr_rate || 3.5), // 실제 필드명 확인 필요
        backgroundColor: 'rgba(66, 185, 131, 0.5)',
        borderColor: '#42b983',
        borderWidth: 1
      }]
    },
    options: { responsive: true, maintainAspectRatio: false }
  })
}

onMounted(() => {
  fetchProfile()
})
</script>

<style scoped>
.profile-container { max-width: 800px; margin: 0 auto; padding: 20px; }
.info-card, .edit-form { background: #f9f9f9; padding: 20px; border-radius: 10px; margin-bottom: 30px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.user-details p { margin: 10px 0; font-size: 1.1rem; }
.input-group { margin-bottom: 15px; display: flex; flex-direction: column; }
.input-group label { margin-bottom: 5px; font-weight: bold; }
.input-group input { padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
.button-group { display: flex; gap: 10px; margin-top: 20px; }
.btn-edit, .btn-save { background-color: #42b983; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
.btn-cancel { background-color: #e74c3c; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
.chart-section { height: 400px; margin-top: 30px; }
.canvas-container { height: 300px; }
</style>