<template>
  <div class="wrap">
    <div class="top">
      <h2>커뮤니티</h2>
      <button v-if="auth.isLogin" class="btn" @click="goCreate">글쓰기</button>
    </div>

    <p v-if="loading">불러오는 중...</p>
    <p v-else-if="posts.length === 0">게시글이 없습니다.</p>

    <ul class="list">
      <li v-for="p in posts" :key="p.id" class="item" @click="goDetail(p.id)">
        <div class="title">{{ p.title }}</div>
        <div class="meta">
          <span>{{ p.author_nickname || p.author_username }}</span>
          <span>·</span>
          <span>{{ formatDate(p.created_at) }}</span>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const loading = ref(false)
const posts = ref([])

const fetchPosts = async () => {
  loading.value = true
  try {
    const res = await axios.get(`${auth.API_URL}/api/v1/community/posts/`)
    posts.value = Array.isArray(res.data) ? res.data : []
  } catch (e) {
    console.log('posts 로드 실패', e)
    posts.value = []
  } finally {
    loading.value = false
  }
}

const goDetail = (id) => router.push({ name: 'CommunityDetailView', params: { id } })
const goCreate = () => router.push({ name: 'CommunityCreateView' })

const formatDate = (iso) => (iso ? iso.slice(0, 10) : '')

onMounted(fetchPosts)
</script>

<style scoped>
.wrap { max-width: 900px; margin: 0 auto; padding: 24px; }
.top { display:flex; align-items:center; justify-content:space-between; }
.btn { padding: 8px 12px; border: none; border-radius: 8px; cursor:pointer; }
.list { list-style:none; padding:0; margin-top: 16px; }
.item { padding: 14px 12px; border: 1px solid #eee; border-radius: 10px; margin-bottom: 10px; cursor:pointer; }
.title { font-weight: 800; margin-bottom: 6px; }
.meta { color:#777; font-size: 12px; display:flex; gap:6px; }
</style>
