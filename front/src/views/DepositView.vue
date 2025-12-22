<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const store = useAuthStore()
const products = ref([])

onMounted(() => {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/products/deposit/`
  })
    .then((res) => {
      console.log('데이터 잘 들어왔는지 확인:', res.data) // 콘솔에서 데이터 확인 필수!
      products.value = res.data
    })
    .catch((err) => {
      console.log('에러 발생:', err)
    })
})
</script>

<template>
  <div class="container">
    <h1 class="page-title">💰 예금 상품 조회</h1>
    
    <div v-if="products.length > 0" class="product-list">
      <div v-for="product in products" :key="product.id" class="product-card">
        
        <div class="card-header">
          <span class="bank-name">{{ product.kor_co_nm }}</span>
          <h3 class="product-name">{{ product.fin_prdt_nm }}</h3>
        </div>

        <hr class="divider">

        <div class="options-container">
          <p class="option-title">기간별 금리 (최고 우대)</p>
          
          <table class="option-table">
            <thead>
              <tr>
                <th>기간</th>
                <th>금리 유형</th>
                <th>기본 금리</th>
                <th>최고 금리</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="opt in product.options" :key="opt.id">
                <td>{{ opt.save_trm }}개월</td>
                <td>{{ opt.intr_rate_type_nm }}</td>
                <td>{{ opt.intr_rate }}%</td>
                <td class="highlight">{{ opt.intr_rate2 }}%</td>
              </tr>
            </tbody>
          </table>
        </div>
        
      </div>
    </div>
    
    <div v-else class="loading">
      <p>상품을 불러오는 중...</p>
    </div>
  </div>
</template>

<style scoped>
.container { max-width: 1000px; margin: 0 auto; padding: 40px 20px; }
.page-title { text-align: center; font-size: 2rem; font-weight: bold; margin-bottom: 40px; color: #333; }

.product-list { display: flex; flex-direction: column; gap: 30px; }

/* 카드 디자인 */
.product-card {
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  background: white;
  transition: transform 0.2s;
}
.product-card:hover { transform: translateY(-3px); border-color: #42b983; }

.card-header { margin-bottom: 16px; }
.bank-name { font-size: 0.9rem; color: #666; font-weight: 600; display: block; margin-bottom: 4px; }
.product-name { font-size: 1.4rem; font-weight: bold; color: #2c3e50; margin: 0; }

.divider { border: 0; height: 1px; background: #eee; margin: 20px 0; }

/* 옵션 테이블 디자인 */
.options-container { background-color: #f8f9fa; padding: 16px; border-radius: 8px; }
.option-title { font-size: 0.95rem; font-weight: bold; margin-bottom: 10px; color: #555; }

.option-table { width: 100%; text-align: left; border-collapse: collapse; font-size: 0.9rem; }
.option-table th { color: #888; font-weight: 500; padding: 8px; border-bottom: 1px solid #ddd; }
.option-table td { padding: 8px; border-bottom: 1px solid #eee; color: #333; }
.option-table tr:last-child td { border-bottom: none; }

.highlight { color: #d63031; font-weight: bold; } /* 최고 금리 빨간색 강조 */

.loading { text-align: center; margin-top: 50px; color: #888; }
</style>