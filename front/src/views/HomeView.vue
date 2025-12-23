<script setup>
import { RouterLink } from 'vue-router'
import { onMounted, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const store = useAuthStore()
const loading = ref(false)
const items = ref([])

// 메인 페이지에 들어오면 '예금' 데이터 6개를 미리보기로 가져옵니다.
onMounted(async () => {
  // ✅ [추가] 로그인 상태인데 user 정보가 없으면(새로고침 등) 내 정보 다시 불러오기
  if (store.isLogin && !store.user?.nickname && typeof store.fetchMe === 'function') {
    await store.fetchMe()
  }

  loading.value = true

  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/products/deposit/`,
  })
    .then((res) => {
      items.value = Array.isArray(res.data) ? res.data.slice(0, 6) : []
    })
    .catch((err) => {
      console.log('데이터 로드 실패 (백엔드 서버 확인 필요)', err)
      items.value = []
    })
    .finally(() => {
      loading.value = false
    })
})
</script>

<template>
  <main class="main-container">
    <section class="hero">
      <!-- ✅ [추가] 로그인 시 닉네임 환영 문구 -->
      <p v-if="store.isLogin && store.user?.nickname" class="welcome">
        안녕하세요, <b>{{ store.user.nickname }}</b>님!
      </p>

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

      <RouterLink class="banner" :to="{ name: 'YoutubeSearchView' }">
        <div class="banner-icon">📺</div>
        <div class="banner-text">
          <div class="banner-title">유튜브</div>
          <div class="banner-desc">관심 종목 영상 보기</div>
        </div>
      </RouterLink>

      <RouterLink class="banner" :to="{ name: 'CommunityListView' }">
        <div class="banner-icon">💬</div>
        <div class="banner-text">
          <div class="banner-title">커뮤니티</div>
          <div class="banner-desc">정보 공유 · 후기 · 질문</div>
        </div>
      </RouterLink>
      <RouterLink class="banner" :to="{ name: 'AIRecommendView' }">
        <div class="banner-icon">🤖</div>
        <div class="banner-text">
          <div class="banner-title">AI</div>
          <div class="banner-desc">사회초년생 맞춤 AI 추천</div>
        </div>
      </RouterLink>
      

    </section>
  </main>
</template>

<style scoped>
/* ✅ [추가] 환영 문구 스타일 */
.welcome {
  margin: 0 0 14px;
  font-size: 1.05rem;
  color: #2c3e50;
}

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


.banner-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
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

/* 3. 미리보기 섹션(미사용 중이어도 유지) */
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
  font-weight: 600;
}
</style>
