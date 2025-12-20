import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ComingSoonView from '../views/ComingSoonView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/savings', name: 'savings', component: ComingSoonView },
    { path: '/gold', name: 'gold', component: ComingSoonView },
    { path: '/map', name: 'map', component: ComingSoonView },
  ],
})

export default router
