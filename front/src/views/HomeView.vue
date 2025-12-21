<script setup>
import { RouterLink } from 'vue-router'
import { onMounted, ref } from 'vue'
import { useAuthStore } from '@/stores/auth' 
import axios from 'axios'

const store = useAuthStore()
const loading = ref(false)
const items = ref([])

// 메인 페이지에 들어오면 '예금' 데이터 6개를 미리보기로 가져옵니다.
onMounted(() => {
  loading.value = true
  
  // 백엔드 서버가 꺼져있거나 주소가 틀리면 여기서 에러가 나서 화면이 멈출 수 있음
  // try-catch 대신 .catch로 방어 코드를 넣어둠
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/products/deposit/`
  })
  .then((res) => {
    items.value = Array.isArray(res.data) ? res.data.slice(0, 6) : []
  })
  .catch((err) => {
    console.log('데이터 로드 실패 (백엔드 서버 확인 필요)', err)
    items.value = [] // 에러 나도 빈 배열로 두어서 화면은 뜨게 함
  })
  .finally(() => {
    loading.value = false
  })
})
</script>

<template>
  <main class="main-container">
    <section class="hero">
      <h1 class="title">사회초년생의 첫 적금 메이트</h1>
      <p class="subtitle">금융 상품 비교부터 금/은 시세까지 한눈에!</p>
    </section>

    <section class="banner-grid">
      <RouterLink class="banner" :to="{ name: 'DepositView' }"> 
        <div class="banner-icon">🏦</div>
        <div class="banner-text">
          <div class="banner-title">예적금 조회</div>
          <div class="banner-desc">예금·적금 상품 한눈에</div>
        </div>
      </RouterLink>

      <RouterLink class="banner" :to="{ name: 'GoldView' }">
        <div class="banner-icon">🥇</div>
        <div class="banner-text">
          <div class="banner-title">금/은 시세</div>
          <div class="banner-desc">실시간 현물 시세 확인</div>
        </div>
      </RouterLink>

      <RouterLink class="banner" to="/map">
        <div class="banner-icon">🗺️</div>
        <div class="banner-text">
          <div class="banner-title">지도 조회</div>
          <div class="banner-desc">내 근처 은행 찾기</div>
        </div>
      </RouterLink>
    </section>

    </main>
</template>

<style scoped>
/* 전체 레이아웃 */
.main-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
  font-family: 'Noto Sans KR', sans-serif;
}

/* 1. 히어로 섹션 */
.hero {
  text-align: center;
  margin-bottom: 50px;
}
.title {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 10px;
  color: #2c3e50;
}
.subtitle {
  font-size: 1.1rem;
  color: #666;
  line-height: 1.6;
}

/* 2. 배너 그리드 (버튼 3개) */
.banner-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* 3열 */
  gap: 20px;
  margin-bottom: 60px;
}

.banner {
  display: flex;
  align-items: center;
  background: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 16px;
  padding: 25px;
  text-decoration: none;
  color: #333;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

.banner:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
  border-color: #42b983;
}

.banner-icon {
  font-size: 2.5rem;
  margin-right: 15px;
}

.banner-title {
  font-size: 1.2rem;
  font-weight: 800;
  margin-bottom: 4px;
}

.banner-desc {
  font-size: 0.9rem;
  color: #888;
}

/* 3. 미리보기 섹션 */
.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 20px;
  color: #2c3e50;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.card {
  background: white;
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 20px;
  transition: transform 0.2s;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.card:hover {
  transform: translateY(-3px);
  border-color: #42b983;
}

.bank-badge {
  background-color: #f1f3f5;
  color: #495057;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600; }

  </style>