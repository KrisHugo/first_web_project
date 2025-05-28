import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from "@/api/index.js"

interface UserInfo {
  id: number
  username: string
  email: string
  avatar: string
}

export const useUserStore = defineStore('user', () => {
  const userInfo = ref<UserInfo | null>(null)
  const token = ref<string | null>(null)
  // 从本地存储初始化
  const initFromStorage = () => {
    const saved = localStorage.getItem('userInfo')
    if (saved) userInfo.value = JSON.parse(saved)
    const savedToken = localStorage.getItem('token')
    if (savedToken) token.value = savedToken
  }

  // 更新用户信息
  const updateUser = (data: Partial<UserInfo>) => {
    if (userInfo.value) {
      userInfo.value = { ...userInfo.value, ...data }
      localStorage.setItem('userInfo', JSON.stringify(userInfo.value)) 
    }
  }

  // 上传头像
  const uploadAvatar = async (file: File) => {
    const formData = new FormData()
    formData.append('avatar', file)
    
    const { data } = await api.patch('/user/avatar', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    
    updateUser({ avatar: data.url })
    return data.url
  }

  const isLoggedIn = () => {
    return !!token && !!token.value && !!userInfo.value
  }

  return { userInfo, token, initFromStorage, updateUser, uploadAvatar, isLoggedIn }
})