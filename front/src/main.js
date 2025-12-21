// src/main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia' // <--- 이거 필수!
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia()) // <--- 이거 필수!
app.use(router)

app.mount('#app')