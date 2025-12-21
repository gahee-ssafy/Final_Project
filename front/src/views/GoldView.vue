<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const store = useAuthStore()
const goldList = ref([])

onMounted(() => {
  // 백엔드에 금/은 데이터 요청
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/products/spot/`
  })
    .then((res) => {
      goldList.value = res.data
    })
    .catch((err) => {
      console.log('데이터 로드 실패', err)
    })
})
</script>

<template>
  <div class="container">
    <h1 class="title">🥇 오늘의 금/은 시세</h1>
    
    <div v-if="goldList.length > 0">
      <table class="gold-table">
        <thead>
          <tr>
            <th>품목</th>
            <th>기준일</th>
            <th>시세 (원)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in goldList" :key="item.id">
            <td>
              <span v-if="item.item_name === 'Gold'">🟡 금 (Gold)</span>
              <span v-else>⚪ 은 (Silver)</span>
            </td>
            <td>{{ item.base_date }}</td>
            <td class="price">{{ item.price.toLocaleString() }}원</td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div v-else class="empty-box">
      <p>데이터가 없습니다.</p>
    </div>
  </div>
</template>

<style scoped>
.container { max-width: 800px; margin: 0 auto; padding: 40px 20px; }
.title { text-align: center; margin-bottom: 30px; font-weight: 800; color: #333; }
.gold-table { width: 100%; border-collapse: collapse; background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-radius: 8px; overflow: hidden; }
.gold-table th { background: #f8f9fa; padding: 15px; text-align: left; font-weight: bold; border-bottom: 2px solid #eee; }
.gold-table td { padding: 15px; border-bottom: 1px solid #eee; }
.price { font-weight: bold; color: #d63031; }
.empty-box { text-align: center; padding: 50px; background: #f1f1f1; border-radius: 10px; color: #666; }
</style>