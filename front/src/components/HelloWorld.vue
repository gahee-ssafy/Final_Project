<script setup>
// [F08] 1. Pinia Store 및 유틸리티 가져오기
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia' // 반응성을 유지하며 state를 꺼내기 위해 사용

defineProps({
  msg: {
    type: String,
    required: true,
  },
})

// [F08] 2. Store 초기화 및 데이터 가져오기
const authStore = useAuthStore()
// storeToRefs를 사용해야 user나 isLogin 값이 바뀌었을 때 화면도 같이 바뀝니다.
const { user, isLogin } = storeToRefs(authStore)
</script>

<template>
  <div class="greetings">
    <h1 class="green">{{ msg }}</h1>

    <div v-if="isLogin && user">
      <h3>
        안녕하세요, <strong>{{ user.nickname || user.username }}</strong>님! 👋<br>
        현재 보유 자산은 <strong>{{ user.money?.toLocaleString() }}원</strong> 입니다.
      </h3>
    </div>

    <div v-else>
      <h3>
        You’ve successfully created a project with
        <a href="https://vite.dev/" target="_blank" rel="noopener">Vite</a> +
        <a href="https://vuejs.org/" target="_blank" rel="noopener">Vue 3</a>.
        <br>
        <span class="highlight">로그인하여 자산을 확인해보세요!</span>
      </h3>
    </div>
  </div>
</template>

<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}

.greetings h1,
.greetings h3 {
  text-align: center;
}

/* [F08] 4. 강조 스타일 추가 */
.highlight {
  color: hsla(160, 100%, 37%, 1);
  font-weight: bold;
  font-size: 0.9em;
}

strong {
  color: hsla(160, 100%, 37%, 1); 
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}
</style>
