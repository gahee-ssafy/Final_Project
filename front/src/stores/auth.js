import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

// [핵심] export const useAuthStore <- 이 이름이 중요합니다!
// HomeView에서 import { useAuthStore } 로 찾고 있기 때문입니다.
export const useAuthStore = defineStore('auth', () => {
  
  // 1. 상태 (State)
  // Django 서버 주소 (나중에 배포하면 바뀔 수 있으니 변수로 관리)
  const API_URL = 'http://127.0.0.1:8000'
  
  const token = ref(null) // 로그인 토큰 (나중에 로그인 구현할 때 사용)

  // 2. 기능 (Actions)
  // 로그인 기능 등이 여기에 들어갑니다. 지금은 비워둡니다.

  return { API_URL, token }
}, { persist: true }) // persist는 새로고침해도 로그인 유지되게 하는 플러그인 (없으면 에러날 수 있으니 일단 넣어둠)
