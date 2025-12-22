<template>
  <div class="home-container">
    <h1>🏠 첫월급 적금메이트</h1>
    <p>환영합니다! 금융 꿀팁 게시판은 준비 중입니다.</p>
    
    <p v-if="authStore.isLogin">
      Currently logged in as: <strong>{{ authStore.user?.username }}</strong>
    </p>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>

<style scoped>
.home-container {
  text-align: center;
  margin-top: 50px;
}
</style>
