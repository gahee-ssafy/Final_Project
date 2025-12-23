<template>
  <header class="topbar">
    <RouterLink to="/" class="brand-link">
      첫월급 적금메이트
    </RouterLink>

    <!-- 비로그인 -->
    <nav class="nav" v-if="!auth.isLogin">
      <RouterLink class="nav-link" :to="{ name: 'LogInView' }">로그인</RouterLink>
      <RouterLink class="nav-link" :to="{ name: 'SignUpView' }">회원가입</RouterLink>
      <RouterLink class="nav-link" :to="{ name: 'CommunityListView' }">커뮤니티</RouterLink>
    </nav>

    <!-- 로그인 -->
    <nav class="nav" v-else>
      <!-- ✅ F08 마이페이지 링크 추가 -->
      <RouterLink class="nav-link" :to="{ name: 'ProfileView' }">마이페이지</RouterLink>

      <a class="nav-link" href="#" @click.prevent="auth.logOut()">로그아웃</a>
    </nav>
  </header>

  <main class="container">
    <RouterView />
  </main>
</template>

<script setup>
import { RouterView, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { onMounted } from 'vue'

const auth = useAuthStore()

// 로그인 상태인데 user 정보(닉네임 등)가 비어있으면 서버에서 받아오기
onMounted(() => {
  if (auth.isLogin && !auth.user?.nickname) {
    auth.fetchMe?.()
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
}

.brand-link {
  font-weight: 800;
  cursor: pointer;
}

/* 오른쪽 메뉴 */
.nav {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* 링크 */
.nav-link,
.nav-link:visited,
.nav-link:hover,
.nav-link:active {
  color: inherit;
  text-decoration: none;
}

.nav-link {
  padding: 8px 10px;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
}

.nav-link:hover {
  background: rgba(0, 0, 0, 0.05);
}

/* 본문 컨테이너 */
.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 24px 18px;
}

/* 모바일에서 간격 조정 */
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
