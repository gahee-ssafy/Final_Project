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
    const token = ref(null) // 로그인 토큰 (Token key or JWT access)
    const user = ref(null)  // 유저 정보(닉네임 등)

    // 3. 파생 상태 (Getters)
    const isLogin = computed(() => !!token.value)

    // ✅ [추가] 로그인한 사용자 정보 가져오기 (nickname/money/salary 등)
    // 백엔드: GET /accounts/me/  (Authorization: Token <key>)
    const fetchMe = async () => {
      if (!token.value) return null

      try {
        const res = await axios({
          method: 'get',
          url: `${API_URL}/accounts/me/`,
          headers: {
            Authorization: `Token ${token.value}`,
          },
        })

        user.value = res.data
        return res.data
      } catch (err) {
        console.log('me 조회 실패', err)
        console.log('서버 응답:', err?.response?.status, err?.response?.data)
        return null
      }
    }

    // 4. 회원가입 액션
    // payload: { username, password1, password2, nickname, money, salary }
    const signUp = (payload) => {
      axios({
        method: 'post',
        url: `${API_URL}/accounts/signup/`,
        data: payload,
      })
        .then((res) => {
          console.log('회원가입 성공!', res)
          window.alert('회원가입이 완료되었습니다. 로그인 해주세요.')
          router.push({ name: 'LogInView' }).catch(() => router.push({ name: 'home' }))
        })
        .catch((err) => {
          console.log('회원가입 실패', err)
          console.log('서버 응답:', err?.response?.status, err?.response?.data)
          window.alert('회원가입에 실패했습니다. 입력 정보를 확인해주세요.')
        })
    }

    // 5. 로그인 액션
    const logIn = async (payload) => {
      try {
        const res = await axios({
          method: 'post',
          url: `${API_URL}/accounts/login/`,
          data: payload,
        })

        console.log('로그인 성공!', res)

        // dj-rest-auth Token 방식: key
        // JWT 방식이면 access
        token.value = res.data.key || res.data.access || null

        // ✅ [추가] 로그인 직후 내 정보 받아와서 user에 저장
        await fetchMe()

        // 홈으로 이동
        await router.push({ name: 'home' }).catch(() => router.push('/'))
      } catch (err) {
        console.log('로그인 실패', err)
        console.log('서버 응답:', err?.response?.status, err?.response?.data)
        window.alert('로그인 실패! 아이디와 비밀번호를 확인하세요.')
      }
    }

    // 6. 로그아웃 액션
    const logOut = () => {
      token.value = null
      user.value = null
      router.push({ name: 'home' })
    }

    return {
      API_URL,
      token,
      user,
      isLogin,
      fetchMe, // ✅ export 추가 (필요하면 Home에서도 호출 가능)
      signUp,
      logIn,
      logOut,
    }
  },
  {
    persist: {
      key: 'auth',
      storage: localStorage,
      paths: ['token', 'user'],
    },
  }
)
