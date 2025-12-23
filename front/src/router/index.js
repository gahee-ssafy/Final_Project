import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

// [중요] 우리가 만든 파일들을 import(수입) 해옵니다.
import DepositView from '@/views/DepositView.vue'
import GoldView from '@/views/GoldView.vue'

// ✅ 로그인/회원가입 뷰 추가
import LogInView from '@/views/LogInView.vue'
import SignUpView from '@/views/SignUpView.vue'

import MapView from '@/views/MapView.vue'

// F05 유튜브 
import YoutubeSearchView from '@/views/youtube/YoutubeSearchView.vue'
import YoutubeVideoDetailView from '@/views/youtube/YoutubeVideoDetailView.vue'
import YoutubeSavedView from '@/views/youtube/YoutubeSavedView.vue'

// F08
import ProfileView from '@/views/ProfileView.vue'
import ArticleView from '@/views/ArticleView.vue'
// F07 커뮤니티
import CommunityListView from '@/views/community/CommunityListView.vue'
import CommunityDetailView from '@/views/community/CommunityDetailView.vue'
import CommunityCreateView from '@/views/community/CommunityCreateView.vue'
import CommunityEditView from '@/views/community/CommunityEditView.vue'


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
    // [F08] 마이페이지 라우터
    {
      path: '/profile',
      name: 'ProfileView',
      component: ProfileView,
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

    // 4. 지도 페이지
    {
      path: '/map',
      name: 'MapView',
      component: MapView
    },
    // 5. 유튜브
    {
      path: '/youtube',
      name: 'YoutubeSearchView',
      component: YoutubeSearchView,
    },
    {
      path: '/youtube/saved',
      name: 'YoutubeSavedView',
      component: YoutubeSavedView,
    },
    {
      path: '/youtube/video/:id',
      name: 'YoutubeVideoDetailView',
      component: YoutubeVideoDetailView,
    },
    {
      path: '/articles',       // 브라우저 주소창에 표시될 경로
      name: 'ArticleView',     // 에러 메시지에서 찾고 있던 그 이름! (중요)
      component: ArticleView   // 위에서 import한 컴포넌트 변수명
    // 7. 커뮤니티
    {
      path: '/community',
      name: 'CommunityListView',
      component: CommunityListView,
    },
    {
      path: '/community/create',
      name: 'CommunityCreateView',
      component: CommunityCreateView,
    },
    {
      path: '/community/:id',
      name: 'CommunityDetailView',
      component: CommunityDetailView,
    },
    {
      path: '/community/:id/edit',
      name: 'CommunityEditView',
      component: CommunityEditView,
    },

  ],
})

export default router
