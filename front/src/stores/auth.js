import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore(
  'auth',
  () => {
    const router = useRouter()

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
      if (!token.value) return

      try {
        const res = await axios({
          method: 'get',
          url: `${API_URL}/accounts/me/`,
          headers: authHeader.value,
        })
        user.value = res.data
      } catch (err) {
        console.log('fetchMe 실패:', err?.response?.status, err?.response?.data)
        // 토큰이 만료/무효면 로그아웃 처리(선택)
        // token.value = null
        // user.value = null
      }
    }

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

        token.value = res.data.key || null
        await fetchMe()

        await router.push({ name: 'home' }).catch(() => router.push('/'))
      } catch (err) {
        console.error('[F08] 로그인 실패:', err)
        window.alert('로그인 실패! 아이디와 비밀번호를 확인하세요.')
      }
    }

    const logOut = async () => {
      // 서버 로그아웃까지 하려면 아래 주석 해제 가능
      // try { await axios.post(`${API_URL}/accounts/logout/`, null, { headers: authHeader.value }) } catch {}

      token.value = null
      user.value = null
      router.push({ name: 'home' }).catch(() => router.push('/'))
    }

    return {
      API_URL,
      token,
      user,
      isLogin,
      authHeader,
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
