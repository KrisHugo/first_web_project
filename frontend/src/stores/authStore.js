// 使用 Pinia（推荐）
import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    token: localStorage.getItem('token') || null
  }),
  actions: {
    updateUserInfo(payload) {
      this.user = payload.user;
      this.token = payload.token;
      localStorage.setItem('user', JSON.stringify(payload.user));
      localStorage.setItem('token', payload.token);
    },
    clearUserInfo() {
      this.user = null;
      this.token = null;
      localStorage.removeItem('user');
      localStorage.removeItem('token');
    },
    isLoggedIn() {
      return this != null && this.user !== null && this.token !== null;
    }
    
  }
});