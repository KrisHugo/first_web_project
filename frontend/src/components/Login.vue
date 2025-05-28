<template>
  <div class="login-container">
    <h2 class="login-title">用户登录</h2>

    <!-- 用户名输入框 -->
    <div class="input-group">
      <label for="username">用户名</label>
      <input id="username" v-model="username" type="text" placeholder="请输入用户名" class="login-input" @keyup.enter="login">
    </div>

    <!-- 密码输入框 -->
    <div class="input-group">
      <label for="password">密码</label>
      <input id="password" v-model="password" type="password" placeholder="请输入密码" class="login-input"
        @keyup.enter="login">
    </div>

    <!-- 错误提示 -->
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>

    <!-- 登录按钮 -->
    <button class="login-button" :disabled="isLoading" @click="login">
      <span v-if="!isLoading">登 录</span>
      <span v-else class="loading-spinner">⏳</span>
    </button>
    <p class="register-link">
      没有账号？<a @click="$emit('switch-to-register')">立即注册</a>
    </p>
  </div>
</template>


<script>
import axios from 'axios';

export default {

  data() {
    return {
      username: '',
      password: '',
      errorMessage: '',
      isLoading: false
    }
  },
  emits: ['login-success', 'switch-to-register'],
  methods: {
    async login() {
      // 验证输入
      if (!this.username.trim() || !this.password.trim()) {
        this.errorMessage = '用户名和密码不能为空'
        return
      }

      this.isLoading = true
      this.errorMessage = ''
      try {
        const response = await axios.post('/api/login', {
          username: this.username,
          password: this.password
        });
        if (response.data.token && response.data.user) {
          console.log('登录成功:', response.data.user.username);
          this.$emit('login-success', response.data);

        } else {
          throw new Error('登录失败:服务器未返回token')
        }
        // alert('登录成功！');
      } catch (error) {
        this.errorMessage = error.response?.data?.error || error.message || '登录失败，请重试'
      } finally {
        this.isLoading = false
      }
    }
  },
  mounted() {
    // 清除之前的错误信息
    this.errorMessage = '';
  }
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.login-title {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 2rem;
  font-size: 1.8rem;
}

.input-group {
  margin-bottom: 1.5rem;
}

.input-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
  font-weight: 500;
}

.login-input {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: all 0.3s;
}

.login-input:focus {
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.2);
  outline: none;
}

.error-message {
  color: #e74c3c;
  background-color: #fdecea;
  padding: 10px 15px;
  border-radius: 6px;
  margin: 1rem 0;
  font-size: 0.9rem;
  animation: fadeIn 0.3s;
}

.login-button {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  margin-top: 1rem;
}

.login-button:hover {
  background: linear-gradient(135deg, #2980b9, #3498db);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.login-button:disabled {
  background: #95a5a6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.register-link {
  margin-top: 15px;
  text-align: center;
}

.register-link a {
  color: #1890ff;
  cursor: pointer;
  text-decoration: none;
}

.loading-spinner {
  display: inline-block;
  animation: spin 1s linear infinite;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>