<template>
  <header class="topbar">
    <div class="brand">첫월급 적금메이트</div>
    <nav class="nav">
      <a class="nav-link" href="#">로그인</a>
      <a class="nav-link" href="#">회원가입</a>
    </nav>
  </header>

  <main class="container">
    <RouterView />
  </main>
</template>

<script setup>
import { RouterView } from 'vue-router'
</script>

<style scoped>
.topbar { display:flex; justify-content:space-between; align-items:center; padding:14px 18px; border-bottom:1px solid #eee; }
.brand { font-weight:800; }
.nav { display:flex; gap:10px; }
.nav-link { text-decoration:none; color:#333; font-size:14px; }
.container { max-width:960px; margin:0 auto; padding:24px 16px; }
</style>
