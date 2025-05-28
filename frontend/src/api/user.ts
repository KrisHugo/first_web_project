import api from './index.js'

export default {
  // 获取用户信息
  getProfile() {
    return api.get('/user/profile')
  },
  
  // 上传头像
  uploadAvatar(file: File) {
    const formData = new FormData()
    formData.append('avatar', file)
    return api.patch('/user/avatar', formData)
  },
  
  // 登录
  login(credentials: { username: string; password: string }) {
    return api.post('/auth/login', credentials)
  }
}