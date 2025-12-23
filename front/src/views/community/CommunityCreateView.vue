<template>
  <div class="wrap">
    <h2>글쓰기</h2>

    <div class="form">
      <input v-model.trim="title" placeholder="제목" class="input" />
      <textarea v-model.trim="content" placeholder="내용" class="textarea"></textarea>

      <div class="actions">
        <button class="btn" @click="submit" :disabled="saving">등록</button>
        <button class="btn ghost" @click="goBack">취소</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const title = ref('')
const content = ref('')
const saving = ref(false)

const submit = async () => {
  if (!auth.isLogin) return window.alert('로그인이 필요합니다.')
  if (!title.value || !content.value) return window.alert('제목/내용을 입력해주세요.')

  saving.value = true
  try {
    const res = await axios({
      method: 'post',
      url: `${auth.API_URL}/api/v1/community/posts/`,
      data: { title: title.value, content: content.value },
      headers: auth.authHeader,
      // ✅ 에러나면
    // headers: auth.authHeader.value
    })
    router.push({ name: 'CommunityDetailView', params: { id: res.data.id } })
  } catch (e) {
    console.log('작성 실패', e?.response?.status, e?.response?.data)
    window.alert('작성에 실패했습니다.')
  } finally {
    saving.value = false
  }
}

const goBack = () => router.push({ name: 'CommunityListView' })
</script>

<style scoped>
.wrap { max-width: 900px; margin: 0 auto; padding: 24px; }
.form { display:flex; flex-direction:column; gap: 12px; margin-top: 14px; }
.input { padding: 10px 12px; border:1px solid #ddd; border-radius: 10px; }
.textarea { min-height: 240px; padding: 10px 12px; border:1px solid #ddd; border-radius: 10px; resize: vertical; }
.actions { display:flex; gap: 10px; }
.btn { padding: 10px 14px; border:none; border-radius: 10px; cursor:pointer; }
.ghost { background: transparent; border: 1px solid #ddd; }
</style>
