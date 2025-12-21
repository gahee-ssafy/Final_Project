<template>
  <section class="hero">
    <h1 class="title">사회초년생의 첫 적금 메이트</h1>
    <p class="subtitle">
      목표/기간/월 납입액/선호 조건을 바탕으로 적금 상품을 비교·점수화해 추천하는 서비스
    </p>
  </section>

  <section class="banner-grid">
    <RouterLink class="banner" to="/savings">
      <div class="banner-title">예·적금</div>
      <div class="banner-desc">상품 조회/검색/필터/정렬</div>
    </RouterLink>

    <RouterLink class="banner" to="/gold">
      <div class="banner-title">현물</div>
      <div class="banner-desc">금/은 데이터 보기</div>
    </RouterLink>

    <RouterLink class="banner" to="/map">
      <div class="banner-title">지도</div>
      <div class="banner-desc">은행/지점 찾기</div>
    </RouterLink>
  </section>

  <section class="preview">
    <h2 class="section-title">오늘의 예·적금 미리보기</h2>

    <div v-if="loading" class="empty">불러오는 중...</div>

    <div v-else-if="items.length" class="card-grid">
      <div v-for="p in items" :key="p.id ?? p.product_code ?? p.fin_prdt_cd ?? p.name" class="card">
        <div class="card-title">{{ p.name ?? p.fin_prdt_nm ?? '상품명' }}</div>
        <div class="card-meta">{{ p.bank ?? p.kor_co_nm ?? '은행 정보' }}</div>
      </div>
    </div>

    <div v-else class="empty">
      아직 저장된 상품 데이터가 없어요. (F03 파싱 완료 후 표시됩니다)
    </div>
  </section>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { onMounted, ref } from 'vue'

const loading = ref(false)
const items = ref([])

onMounted(async () => {
  loading.value = true
  try {
    // ✅ Django API 경로
    const res = await fetch('/api/v1/products/deposit/')
    if (!res.ok) throw new Error('API error')
    const data = await res.json()
    items.value = Array.isArray(data) ? data.slice(0, 6) : []
  } catch (e) {
    items.value = []
  } finally {
    loading.value = false
  }
})


const spot = ref(null)

onMounted(async () => {
  loading.value = true
  try {
    const [depRes, spotRes] = await Promise.all([
      fetch('/api/v1/products/deposit/'),
      fetch('/api/v1/products/spot/'),
    ])

    if (depRes.ok) {
      const depData = await depRes.json()
      items.value = Array.isArray(depData) ? depData.slice(0, 6) : []
    } else {
      items.value = []
    }

    if (spotRes.ok) {
      spot.value = await spotRes.json()
    } else {
      spot.value = null
    }
  } catch (e) {
    items.value = []
    spot.value = null
  } finally {
    loading.value = false
  }
})

</script>

<style scoped>
.hero { padding: 16px 0 24px; }
.title { margin:0 0 10px; font-size:28px; }
.subtitle { margin:0; color:#555; line-height:1.5; }

.banner-grid { display:grid; grid-template-columns:repeat(3, 1fr); gap:12px; margin:18px 0 30px; }
.banner { text-decoration:none; color:#111; border:1px solid #eee; border-radius:14px; padding:16px; transition: transform .1s ease; }
.banner:hover { transform: translateY(-2px); }
.banner-title { font-weight:800; margin-bottom:6px; }
.banner-desc { color:#666; font-size:14px; }

.section-title { margin:0 0 12px; font-size:18px; }
.card-grid { display:grid; grid-template-columns:repeat(3, 1fr); gap:12px; }
.card { border:1px solid #eee; border-radius:14px; padding:14px; }
.card-title { font-weight:700; margin-bottom:6px; }
.card-meta { color:#666; font-size:13px; }
.empty { padding:12px; background:#fafafa; border:1px dashed #ddd; border-radius:12px; color:#666; }

@media (max-width: 800px) {
  .banner-grid, .card-grid { grid-template-columns: 1fr; }
}
</style>
