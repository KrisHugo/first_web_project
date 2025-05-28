import '@/assets/reset.css';
import './assets/main.css'
import { createApp } from 'vue'
// import router from 'vue-router' // 确保路径正确
import router from './router' // 确保路径正确
import { createPinia } from 'pinia'
import App from './App.vue'
// Create Pinia instance
const pinia = createPinia()
// Create Vue app
const app = createApp(App)
app.use(pinia)
app.use(router) // 必须在mount前调用
app.mount('#app')