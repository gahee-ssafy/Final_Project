import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

// [핵심] export const useAuthStore <- 이 이름이 중요합니다!
// HomeView에서 import { useAuthStore } 로 찾고 있기 때문입니다.
export const useAuthStore = defineStore(
  'auth',
  () => {
    const router = useRouter()

    // 1. Django 서버 주소
    const API_URL = 'http://127.0.0.1:8000'

    // 2. 상태 (State)
    const token = ref(null) // 로그인 토큰 (JWT or key)
    const user = ref(null)  // (선택) 유저 정보 - 현재는 로그인 응답에서 안 받아오면 null 유지

    // 3. 파생 상태 (Getters)
    const isLogin = computed(() => !!token.value)

    // 4. 회원가입 액션
    // payload: { username, password1, password2, ... } 혹은 백엔드 스펙에 맞게
    // (팀 F02 코드 기준: nickname, money, salary 포함 가능)
    const signUp = (payload) => {
      axios({
        method: 'post',
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

    // 5. 로그인 액션
    // payload: { username, password }
    const logIn = (payload) => {
      axios({
        method: 'post',
        url: `${API_URL}/accounts/login/`,
        data: payload,
      })
        .then((res) => {
          console.log('로그인 성공!', res)

          // dj-rest-auth 기본: key
          // JWT 설정일 경우: access
          token.value = res.data.key || res.data.access || null

          // (선택) 유저 정보가 응답으로 오면 저장
          // user.value = res.data.user ?? null

          router.push({ name: 'HomeView' })
        })
        .catch((err) => {
          console.log('로그인 실패', err)
          window.alert('로그인 실패! 아이디와 비밀번호를 확인하세요.')
        })
    }

    // 6. 로그아웃 액션(추가하면 편함)
    const logOut = () => {
      token.value = null
      user.value = null
      router.push({ name: 'HomeView' })
    }

    return {
      API_URL,
      token,
      user,
      isLogin,
      signUp,
      logIn,
      logOut,
    }
  },
  { persist: true }
)
