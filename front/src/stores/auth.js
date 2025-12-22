import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore(
  'auth',
  () => {
    const router = useRouter()

    // 1. Django 서버 주소
    const API_URL = 'http://127.0.0.1:8000'

    // 2. 상태 (State)
    const token = ref(null) // 로그인 토큰
    const user = ref(null)  // 유저 정보

    // 3. 파생 상태 (Getters)
    // 토큰이 존재하면 로그인 상태로 간주
    const isLogin = computed(() => {
      return token.value !== null && token.value !== ''
    })

    // [F08] 4. 내 정보 가져오기
    const fetchMe = async () => {
      if (!token.value) return null

      try {
        const res = await axios({
          method: 'get',
          url: `${API_URL}/accounts/user/`, // URL 수정 (API_URL 포함)
          headers: {
            // [중요] JWT 표준은 'Bearer'입니다. (vue2_교육자료 참조)
            // 또한 ref 변수는 .value로 접근해야 실제 값 들어갑니다.
            Authorization: `Bearer ${token.value}`, 
          },
        })

        user.value = res.data
        return res.data
      } catch (err) {
        console.error('[F08] 사용자 정보 조회 실패:', err)
        // 토큰이 만료되었거나 유효하지 않으면 로그아웃 처리할 수도 있음
        return null
      }
    }

    // 5. 회원가입 액션
    const signUp = (payload) => {
      axios({
        method: 'post',
        url: `${API_URL}/accounts/signup/`,
        data: payload,
      })
        .then((res) => {
          console.log('[F08] 회원가입 성공:', res)
          window.alert('회원가입이 완료되었습니다. 로그인 해주세요.')
          router.push({ name: 'LogInView' })
        })
        .catch((err) => {
          console.error('[F08] 회원가입 실패:', err)
          window.alert('회원가입에 실패했습니다. 입력 정보를 확인해주세요.')
        })
    }

    // 6. 로그인 액션
    const logIn = async (payload) => {
      try {
        const res = await axios({
          method: 'post',
          url: `${API_URL}/accounts/login/`,
          data: payload,
        })

        console.log('[F08] 로그인 요청 성공:', res)

        // dj-rest-auth 설정에 따라 key 혹은 access로 옴
        const newToken = res.data.key || res.data.access || null
        token.value = newToken

        if (newToken) {
          // 토큰 저장 후 내 정보 갱신 (비동기 처리)
          await fetchMe()
          
          window.alert('로그인되었습니다.')
          router.replace({ name: 'ArticleView' }) // 메인 페이지나 게시판으로 이동
        } else {
          console.warn('[F08] 토큰이 응답에 포함되지 않았습니다.')
        }

      } catch (err) {
        console.error('[F08] 로그인 실패:', err)
        window.alert('로그인 실패! 아이디와 비밀번호를 확인하세요.')
      }
    }

    // 7. 로그아웃 액션
    const logOut = () => {
      token.value = null
      user.value = null
      window.alert('로그아웃 되었습니다.')
      router.push({ name: 'ArticleView' }) // 로그아웃 후 이동할 페이지
    }

    // [F08] 8. 회원정보 수정 액션
    // store/auth.js 또는 accounts.js에 정의된 재발급 함수 [cite: 483, 2853, 3787]
    const refreshAccessToken = function () {
      return axios({
        method: 'post',
        url: `${API_URL}/accounts/token/refresh/`, // URL 확인 필요 [cite: 487, 2857, 3791]
        data: { refresh: refresh.value }
      })
      .then(res => {
        token.value = res.data.access // 새 Access 토큰으로 갱신 [cite: 495, 2865, 3799]
        return true
      })
      .catch(() => false)
    }
    const updateUser = async (payload) => {
      try {
        const res = await axios({
          method: 'put', 
          url: `${API_URL}/accounts/user/`,
          headers: {
            // [수정] JWT 표준인 Bearer로 통일
            Authorization: `Bearer ${token.value}`,
          },
          data: payload,
        })

        console.log('[F08] 정보 수정 성공:', res.data)
        user.value = res.data // 수정된 정보를 즉시 상태에 반영
        window.alert('회원정보가 수정되었습니다.')
      } catch (err) {
        console.error('[F08] 정보 수정 실패:', err)
        window.alert('정보 수정에 실패했습니다.')
      }
      
    }

    return {
      API_URL,
      token,
      user,
      isLogin,
      fetchMe,
      signUp,
      logIn,
      logOut,
      updateUser,
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
