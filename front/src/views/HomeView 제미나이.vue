<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const router = useRouter()
const store = useAuthStore()

/* ---------------------------
   ✅ 오늘의 팁(2번 기능)
--------------------------- */
const tips = [
  '💰 첫 월급의 50%는 무조건 저축하는 습관을 들여보세요!',
  '📌 소비 전 “필요 vs 욕구”를 10초만 구분해보면 지출이 줄어요.',
  '🧾 고정지출(통신/구독)을 먼저 줄이면 절약이 쉬워요.',
  '🏦 우대금리 조건(급여이체/자동이체)을 체크하면 체감수익이 커져요.',
  '📈 적금은 “목표 금액/기간”부터 정하면 선택이 쉬워요.',
]
const todayTip = ref('')
const showTip = ref(false)

/* ---------------------------
   ✅ 데이터 로딩 상태 및 변수
--------------------------- */
const loading = ref(false)
const items = ref([]) // 예적금

const loadingPosts = ref(false)
const posts = ref([]) // 커뮤니티

const loadingSpot = ref(false)
const spotList = ref([]) // 금/은 시세

// 데이터 가공 computed
const topDeposits = computed(() => (Array.isArray(items.value) ? items.value.slice(0, 3) : []))
const latestPosts = computed(() => (Array.isArray(posts.value) ? posts.value.slice(0, 3) : []))

const formatDate = (iso) => (iso ? String(iso).slice(0, 10) : '')

// 금리 추출 헬퍼
const pickRate = (p) => {
  const candidates = [p?.intr_rate2, p?.max_intr_rate, p?.intr_rate, p?.highest_rate, p?.best_rate]
  const n = candidates.find((v) => typeof v === 'number')
  return typeof n === 'number' ? n : null
}

const goDepositDetail = (p) => {
  if (p?.fin_prdt_cd) {
    router.push({ name: 'DepositDetailView', params: { fin_prdt_cd: p.fin_prdt_cd } })
  } else {
    router.push({ name: 'DepositView' })
  }
}

/* ---------------------------
   ✅ API 요청 함수들
--------------------------- */
const fetchDeposits = async () => {
  loading.value = true
  try {
    const res = await axios.get(`${store.API_URL}/api/v1/products/deposit/`)
    items.value = Array.isArray(res.data) ? res.data : []
  } catch (err) {
    console.log('예적금 로드 실패', err)
  } finally {
    loading.value = false
  }
}

const fetchCommunity = async () => {
  loadingPosts.value = true
  try {
    const res = await axios.get(`${store.API_URL}/api/v1/community/posts/`)
    posts.value = Array.isArray(res.data) ? res.data : []
  } catch (err) {
    console.log('커뮤니티 로드 실패', err)
  } finally {
    loadingPosts.value = false
  }
}

const fetchSpot = async () => {
  loadingSpot.value = true
  try {
    const res = await axios.get(`${store.API_URL}/api/v1/products/spot/`)
    spotList.value = Array.isArray(res.data) ? res.data : []
  } catch (err) {
    console.log('시세 로드 실패', err)
  } finally {
    loadingSpot.value = false
  }
}

const latestSpotOf = (name) => {
  const arr = (spotList.value || []).filter((x) => x.item_name === name)
  return arr.length === 0 ? null : arr.reduce((a, b) => (a.base_date > b.base_date ? a : b))
}

const goldSpot = computed(() => latestSpotOf('Gold'))
const silverSpot = computed(() => latestSpotOf('Silver'))
const spotBaseDate = computed(() => goldSpot.value?.base_date || silverSpot.value?.base_date || '')

/* ---------------------------
   ✅ 목표 달성 계산기(3번 기능)
--------------------------- */
const calcAmount = ref(500000)
const calcMonths = ref(12)
const calcRate = ref(4.0)

const expectedResult = computed(() => {
  const p = calcAmount.value
  const n = calcMonths.value
  const r = calcRate.value / 100 / 12
  const principal = p * n
  const interest = p * (n * (n + 1) / 2) * r
  return Math.floor(principal + interest).toLocaleString()
})

/* ---------------------------
   ✅ Lifecycle Hooks
--------------------------- */
onMounted(async () => {
  todayTip.value = tips[Math.floor(Math.random() * tips.length)]
  setTimeout(() => { showTip.value = true }, 350)

  if (store.isLogin && !store.user?.nickname && typeof store.fetchMe === 'function') {
    await store.fetchMe()
  }
  await Promise.all([fetchDeposits(), fetchCommunity(), fetchSpot()])
})
</script>

<template>
  <main class="home">
    <section class="hero">
      <p v-if="store.isLogin && store.user?.nickname" class="welcome">
        안녕하세요, <b>{{ store.user.nickname }}</b>님!
      </p>
      <h1 class="title">
        <span class="title-weak">사회초년생의</span>
        <span class="title-strong">첫 적금 메이트</span>
      </h1>
      <p class="subtitle">금융 상품 비교부터 <b>금/은 시세</b>까지 한눈에!</p>

      <transition name="fade-up">
        <div class="tip-bar" v-if="showTip && todayTip">
          <div class="tip-content">
            <span class="tip-badge">💡 오늘의 팁</span>
            <p class="tip-text">{{ todayTip }}</p>
          </div>
        </div>
      </transition>
    </section>

    <section class="banner-grid">
      <RouterLink class="banner b-orange" :to="{ name: 'DepositView' }">
        <div class="icon-box">🏦</div>
        <div class="banner-text">
          <div class="banner-title">예적금 조회</div>
          <div class="banner-desc">예금·적금 상품 한눈에</div>
        </div>
      </RouterLink>
      <RouterLink class="banner b-yellow" :to="{ name: 'GoldView' }">
        <div class="icon-box">🥇</div>
        <div class="banner-text">
          <div class="banner-title">금/은 시세</div>
          <div class="banner-desc">실시간 현물 시세 확인</div>
        </div>
      </RouterLink>
      <RouterLink class="banner b-blue" :to="{ name: 'MapView' }">
        <div class="icon-box">🗺️</div>
        <div class="banner-text">
          <div class="banner-title">지도 조회</div>
          <div class="banner-desc">내 근처 은행 찾기</div>
        </div>
      </RouterLink>
      <RouterLink class="banner b-peach" :to="{ name: 'YoutubeSearchView' }">
        <div class="icon-box">📺</div>
        <div class="banner-text">
          <div class="banner-title">유튜브</div>
          <div class="banner-desc">관심 종목 영상 보기</div>
        </div>
      </RouterLink>
      <RouterLink class="banner b-sky" :to="{ name: 'CommunityListView' }">
        <div class="icon-box">💬</div>
        <div class="banner-text">
          <div class="banner-title">커뮤니티</div>
          <div class="banner-desc">정보 공유 · 후기 · 질문</div>
        </div>
      </RouterLink>
      <RouterLink class="banner b-purple" :to="{ name: 'AIRecommendView' }">
        <div class="icon-box">🤖</div>
        <div class="banner-text">
          <div class="banner-title">AI</div>
          <div class="banner-desc">사회초년생 맞춤 AI 추천</div>
        </div>
      </RouterLink>
    </section>

    <section class="bottom">
      <div class="summary-grid">
        <div class="summary-card">
          <div class="summary-head">
            <div class="summary-title">오늘의 예적금 미리보기</div>
            <RouterLink class="summary-link" :to="{ name: 'DepositView' }">전체 보기 →</RouterLink>
          </div>
          <div v-if="loading" class="mini-loading">불러오는 중...</div>
          <div v-else class="deposit-mini">
            <div v-for="p in topDeposits" :key="p.fin_prdt_cd" class="deposit-row" @click="goDepositDetail(p)">
              <div class="deposit-left">
                <div class="deposit-name">{{ p.fin_prdt_nm }}</div>
                <div class="deposit-bank">{{ p.kor_co_nm }}</div>
              </div>
              <div class="deposit-right">
                <span class="rate-badge">{{ pickRate(p) }}%</span>
              </div>
            </div>
          </div>
        </div>

        <div class="summary-card">
          <div class="summary-head"><div class="summary-title">AI 맞춤 추천</div></div>
          <p class="summary-desc">내 조건으로 바로 추천 받아보세요.</p>
          <RouterLink class="cta" :to="{ name: 'AIRecommendView' }">추천 받으러 가기 →</RouterLink>
        </div>

        <div class="summary-card">
          <div class="summary-head">
            <div class="summary-title">금/은 시세</div>
            <RouterLink class="summary-link" :to="{ name: 'GoldView' }">자세히 →</RouterLink>
          </div>
          <div class="spot-mini">
             <div class="spot-row"><span>🟡 금 (g당)</span><strong>{{ goldSpot ? Number(goldSpot.price).toLocaleString() : '—' }}원</strong></div>
             <div class="spot-row"><span>⚪ 은 (g당)</span><strong>{{ silverSpot ? Number(silverSpot.price).toLocaleString() : '—' }}원</strong></div>
          </div>
        </div>
      </div>

      <div class="dash-grid">
        <div class="panel">
          <div class="panel-head">
            <div class="panel-title">커뮤니티 최신글</div>
            <RouterLink class="panel-link" :to="{ name: 'CommunityListView' }">더보기 →</RouterLink>
          </div>
          <div class="post-list">
            <div v-for="post in latestPosts" :key="post.id" class="post-row" @click="router.push({ name: 'CommunityDetailView', params: { id: post.id } })">
              <div class="post-title">{{ post.title }}</div>
              <div class="post-meta">{{ post.author_nickname }} · {{ formatDate(post.created_at) }}</div>
            </div>
          </div>
        </div>

        <div class="panel calc-panel">
          <div class="panel-head"><div class="panel-title">💰 목표 달성 계산기</div></div>
          <div class="calc-body">
            <div class="calc-input-row">
              <label>매달 <b>{{ (calcAmount/10000).toLocaleString() }}만</b>원씩</label>
              <input type="range" v-model.number="calcAmount" min="100000" max="2000000" step="100000">
            </div>
            <div class="calc-input-row">
              <label><b>{{ calcMonths }}개월</b> 동안 모으면?</label>
              <input type="range" v-model.number="calcMonths" min="6" max="36" step="6">
            </div>
            <div class="calc-result-box">
              <span class="result-label">만기 예상 수령액(세전)</span>
              <div class="result-value">약 <span>{{ expectedResult }}</span>원</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
.home { max-width: 1000px; margin: 0 auto; padding: 40px 18px; }

/* 히어로 */
.hero { text-align: center; margin-bottom: 30px; min-height: 40vh; display: flex; flex-direction: column; justify-content: center; }
.welcome { color: #ff9f43; font-weight: 700; margin-bottom: 10px; }
.title { display: flex; flex-direction: column; gap: 8px; line-height: 1.1; }
.title-weak { font-size: 1.25rem; color: #7f8c8d; font-weight: 850; }
.title-strong { font-size: 3rem; color: #223a5e; font-weight: 950; }
.subtitle { margin-top: 15px; color: #95a5a6; font-size: 1.05rem; }

/* 오늘의 팁 */
.tip-bar { margin: 20px auto 0; max-width: 800px; }
.tip-content { display: flex; align-items: center; gap: 15px; padding: 12px 24px; background: rgba(255, 255, 255, 0.7); border-radius: 99px; border: 1px solid rgba(255, 197, 120, 0.4); box-shadow: 0 6px 20px rgba(0,0,0,0.05); }
.tip-badge { background: #ff9f43; color: white; padding: 4px 12px; border-radius: 12px; font-weight: 900; font-size: 0.8rem; }
.tip-text { margin: 0; font-weight: 700; color: #5a4b3c; font-size: 0.95rem; }

/* 배너 그리드 */
.banner-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; margin-bottom: 40px; }
.banner { display: flex; align-items: center; gap: 15px; padding: 22px; border-radius: 20px; background: rgba(255,255,255,0.7); border: 1px solid rgba(0,0,0,0.05); transition: transform 0.2s; box-shadow: 0 8px 20px rgba(0,0,0,0.05); text-decoration: none !important; }
.banner:hover { transform: translateY(-5px); }
.icon-box { font-size: 1.8rem; width: 50px; height: 50px; display: grid; place-items: center; border-radius: 14px; }
.banner-title { font-weight: 900; color: #333; font-size: 1.1rem; }
.banner-desc { font-size: 0.85rem; color: #999; }

/* 배너 개별 색상 */
.b-orange { background-color: #ffcc95; } .b-yellow { background-color: #ffecb3; } .b-blue { background-color: #d1e9ff; }
.b-peach { background-color: #ffd8c4; } .b-sky { background-color: #d6ebff; } .b-purple { background-color: #f3e5f5; }

/* 대시보드 */
.summary-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 20px; }
.summary-card, .panel { background: rgba(255,255,255,0.8); padding: 20px; border-radius: 22px; border: 1px solid rgba(0,0,0,0.05); box-shadow: 0 10px 30px rgba(0,0,0,0.04); }
.summary-head, .panel-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.summary-title, .panel-title { font-weight: 950; color: #223a5e; }
.summary-link, .panel-link { font-size: 0.85rem; color: #ff9f43; font-weight: 800; text-decoration: none; }

.deposit-row, .post-row { display: flex; justify-content: space-between; align-items: center; padding: 12px; background: white; border-radius: 14px; margin-bottom: 8px; border: 1px solid rgba(0,0,0,0.03); cursor: pointer; transition: transform 0.2s; }
.deposit-row:hover, .post-row:hover { transform: scale(1.02); }
.deposit-name, .post-title { font-weight: 800; font-size: 0.9rem; color: #333; }
.rate-badge { background: #ffcc95; color: #5a4b3c; padding: 4px 10px; border-radius: 10px; font-weight: 900; font-size: 0.8rem; }

.dash-grid { display: grid; grid-template-columns: 1.5fr 1fr; gap: 16px; }

/* 계산기 */
.calc-panel { background: linear-gradient(135deg, #ffffff, #fff9f0) !important; }
.calc-body { display: flex; flex-direction: column; gap: 15px; }
.calc-input-row label { font-size: 0.9rem; font-weight: 700; color: #5a4b3c; }
.calc-input-row b { color: #ff9f43; }
.calc-input-row input { accent-color: #ff9f43; width: 100%; cursor: pointer; }
.calc-result-box { padding: 18px; background: white; border-radius: 16px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.02); }
.result-label { font-size: 0.8rem; color: #999; font-weight: 700; }
.result-value span { color: #ff9f43; font-size: 1.5rem; font-weight: 900; }

/* 애니메이션 */
.fade-up-enter-active { transition: all 0.5s ease; }
.fade-up-enter-from { opacity: 0; transform: translateY(20px); }

@media (max-width: 850px) { .banner-grid, .summary-grid, .dash-grid { grid-template-columns: 1fr; } }
</style>