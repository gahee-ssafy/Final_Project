// src/stores/auth.js
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()
  // 1. Django 서버 주소 (보통 8000번 포트)
  const API_URL = 'http://127.0.0.1:8000'

  // 2. 상태(State) 정의
  const token = ref(null) // JWT 토큰
  const user = ref(null)  // 로그인한 유저 정보

  // 3. 회원가입 액션 (F02 핵심)
  // payload에는 username, password 외에 nickname, money, salary가 포함됨
  const signUp = function (payload) {
    axios({
      method: 'post',
      // dj-rest-auth의 회원가입 기본 URL
      url: `${API_URL}/accounts/registration/`,
      data: payload,
    })
      .then((res) => {
        console.log('회원가입 성공!', res)
        window.alert('회원가입이 완료되었습니다. 로그인 해주세요.')
        router.push({ name: 'LogInView' })
      })
      .catch((err) => {
        console.log('회원가입 실패', err)
        window.alert('회원가입에 실패했습니다. 입력 정보를 확인해주세요.')
      })
  }

  // 4. 로그인 액션
  const logIn = function (payload) {
    axios({
      method: 'post',
      // dj-rest-auth의 로그인 기본 URL
      url: `${API_URL}/accounts/login/`,
      data: payload,
    })
      .then((res) => {
        console.log('로그인 성공!', res)
        
        // 백엔드에서 받은 토큰 저장 (key 혹은 access 등 설정에 따라 다름)
        // dj-rest-auth 기본 설정은 'key'로 옵니다. (JWT 설정시 access일 수 있음)
        token.value = res.data.key || res.data.access 
        
        // 로그인 후 메인 페이지로 이동
        router.push({ name: 'HomeView' }) // 혹은 MainView
      })
      .catch((err) => {
        console.log('로그인 실패', err)
        window.alert('로그인 실패! 아이디와 비밀번호를 확인하세요.')
      })
  }

  return { API_URL, token, user, signUp, logIn }
})