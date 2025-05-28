import axios from 'axios'
import { useUserStore } from '@/stores/userStore.js'
import router from '@/router/index.js'

// 创建实例
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api', // 从环境变量读取
//   baseURL: '/api', // 从环境变量读取
  timeout: 10000, // 请求超时
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    const userStore = useUserStore()
    // 添加JWT Token
    if (userStore.token) {
      config.headers.Authorization = `Bearer ${userStore.token}`
    }
    
    // 处理特殊Content-Type
    if (config.data instanceof FormData) {
      config.headers['Content-Type'] = 'multipart/form-data'
    }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    // 统一处理成功响应
    return response.data
  },
  (error) => {
    // 统一错误处理
    if (error.response) {
      switch (error.response.status) {
        case 401:
          router.push('/login?expired=1')
          break
        case 403:
          router.push('/403')
          break
        case 500:
          // 触发全局错误提示
          break
      }
    }
    return Promise.reject(error)
  }
)

export default api