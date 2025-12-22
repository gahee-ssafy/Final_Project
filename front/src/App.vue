<template>
  <header class="topbar">
    <RouterLink :to="{ name: 'ArticleView' }" class="brand-link">
      첫월급 적금메이트
    </RouterLink>

    <nav class="nav" v-if="!store.isLogin">
      <RouterLink class="nav-link" :to="{ name: 'LogInView' }">로그인</RouterLink>
      <RouterLink class="nav-link" :to="{ name: 'SignUpView' }">회원가입</RouterLink>
    </nav>

    <nav class="nav" v-else>
      <RouterLink class="nav-link" :to="{ name: 'ProfileView' }">마이페이지</RouterLink>
      
      <a class="nav-link" href="#" @click.prevent="store.logOut()">로그아웃</a>
    </nav>
  </header>

  <main class="container">
    <RouterView />
  </main>
</template>

<script setup>
import { onMounted } from 'vue'
import { RouterView, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Store 가져오기 (한 번만 선언)
const store = useAuthStore()

// 새로고침 시, 로그인 상태라면 최신 유저 정보를 다시 가져옴
onMounted(() => {
  if (store.isLogin && !store.user?.nickname) {
    store.fetchMe()
  }
})
</script>

<style scoped>
/* 상단바 */
.topbar {
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 22px;
  background: #fff;
  border-bottom: 1px solid #eee;
}

/* 로고/브랜드 */
.brand-link,
.brand-link:visited,
.brand-link:hover,
.brand-link:active {
  color: inherit;
  text-decoration: none;
  font-weight: 800;
  cursor: pointer;
}

/* 오른쪽 메뉴 */
.nav {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* 링크 스타일 */
.nav-link {
  font-size: 14px;
  color: #111;
  text-decoration: none;
  padding: 6px 8px;
  border-radius: 10px;
  transition: background 0.15s ease;
  cursor: pointer;
}

.nav-link:hover {
  background: #f5f5f5;
}

/* 본문 컨테이너 */
.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 24px 18px;
}

/* 모바일 반응형 */
@media (max-width: 480px) {
  .topbar {
    padding: 0 14px;
  }
  .nav {
    gap: 8px;
  }
  .nav-link {
    padding: 6px 6px;
  }
}
</style>