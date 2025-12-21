import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

// [중요] 우리가 만든 파일들을 import(수입) 해옵니다.
import DepositView from '@/views/DepositView.vue'
import GoldView from '@/views/GoldView.vue'

// ✅ 로그인/회원가입 뷰 추가
import LogInView from '@/views/LogInView.vue'
import SignUpView from '@/views/SignUpView.vue'

// (지도는 아직 안 만들었으니 임시로 HomeView나 ComingSoonView를 씁니다)
// import MapView from '@/views/MapView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // 1. 메인 페이지
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },

    // ✅ 로그인 / 회원가입 페이지
    {
      path: '/login',
      name: 'LogInView',
      component: LogInView,
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView,
    },

    // 2. 예적금 조회 페이지 (버튼: DepositView)
    {
      path: '/deposit',
      name: 'DepositView', // HomeView의 :to="{ name: 'DepositView' }" 와 일치해야 함
      component: DepositView,
    },

    // 3. 금/은 시세 페이지 (버튼: GoldView)
    {
      path: '/gold',
      name: 'GoldView', // HomeView의 :to="{ name: 'GoldView' }" 와 일치해야 함
      component: GoldView,
    },

    // 4. 지도 페이지 (아직 안 만들었으므로 임시로 HomeView 연결)
    {
      path: '/map',
      name: 'MapView',
      component: HomeView, // 나중에 MapView 만들면 교체하세요!
    },
  ],
})

export default router
