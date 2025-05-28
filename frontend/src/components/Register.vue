<template>
  <div class="register-container">
    <h2 class="register-title">用户注册</h2>
    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <label for="username">用户名</label>
        <input v-model="form.username" type="text" id="username" placeholder="请输入用户名"
          :class="{ 'is-invalid': errors.username }" />
        <div class="error-message" v-if="errors.username">
          {{ errors.username }}
        </div>
      </div>

      <div class="form-group">
        <label for="email">邮箱</label>
        <input v-model="form.email" type="email" id="email" placeholder="请输入邮箱"
          :class="{ 'is-invalid': errors.email }" />
        <div class="error-message" v-if="errors.email">
          {{ errors.email }}
        </div>
      </div>

      <div class="form-group">
        <label for="password">密码</label>
        <input v-model="form.password" type="password" id="password" placeholder="请输入密码"
          :class="{ 'is-invalid': errors.password }" />
        <div class="error-message" v-if="errors.password">
          {{ errors.password }}
        </div>
      </div>

      <div class="form-group">
        <label for="confirmPassword">确认密码</label>
        <input v-model="form.confirmPassword" type="password" id="confirmPassword" placeholder="请再次输入密码"
          :class="{ 'is-invalid': errors.confirmPassword }" />
        <div class="error-message" v-if="errors.confirmPassword">
          {{ errors.confirmPassword }}
        </div>
      </div>

      <button type="submit" :disabled="isSubmitting">
        {{ isSubmitting ? '注册中...' : '立即注册' }}
      </button>

      <div class="server-error" v-if="serverError">
        {{ serverError }}
      </div>

      <div class="login-link">
        已有账号？<a @click="$emit('switch-to-login')">去登录</a>
      </div>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios'

export default {
  name: 'RegisterPage',
  emits: ['switch-to-login', 'register-success'],
  setup(props, { emit }) {
    const form = ref({
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    })

    const errors = ref({
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    })

    const serverError = ref('')
    const isSubmitting = ref(false)

    const validateForm = () => {
      let isValid = true
      errors.value = {
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
      }

      // 用户名验证
      if (!form.value.username.trim()) {
        errors.value.username = '用户名不能为空'
        isValid = false
      } else if (form.value.username.length < 4) {
        errors.value.username = '用户名至少4个字符'
        isValid = false
      }

      // 邮箱验证
      if (!form.value.email.trim()) {
        errors.value.email = '邮箱不能为空'
        isValid = false
      } else if (!/^\S+@\S+\.\S+$/.test(form.value.email)) {
        errors.value.email = '请输入有效的邮箱地址'
        isValid = false
      }

      // 密码验证
      if (!form.value.password) {
        errors.value.password = '密码不能为空'
        isValid = false
      } else if (form.value.password.length < 6) {
        errors.value.password = '密码至少6个字符'
        isValid = false
      }

      // 确认密码验证
      if (form.value.password !== form.value.confirmPassword) {
        errors.value.confirmPassword = '两次输入的密码不一致'
        isValid = false
      }

      return isValid
    }

    const handleRegister = async () => {
      if (!validateForm()) return

      isSubmitting.value = true
      serverError.value = ''

      try {
        const response = await axios.post('/api/register', {
          username: form.value.username,
          email: form.value.email,
          password: form.value.password
        })

        if (response.status === 201) {
          // 注册成功后的处理
          emit('register-success', {
            username: form.value.username,
            email: form.value.email
          })
        }
      } catch (error) {
        if (error.response) {
          // 服务器返回的错误
          const { status, data } = error.response
          if (status === 400 && data.error === '用户名已存在') {
            errors.value.username = data.error
          } else {
            // console.log('error check!')
            // console.log(data.error)
            serverError.value = data.error || '注册失败，请稍后重试'
            if (data.error === "验证失败") {

              // console.log(errors)
              // 如果有详细错误信息，显示第一个
              if (data.details.username) {
                errors.value.username = data.details.username
              }
              else if (data.details.email) {
                errors.value.email = data.details.email
              }
              else if (data.details.password) {
                errors.value.password = data.details.password
              }
              else if (data.details.confirmPassword) {
                errors.value.confirmPassword = data.details.confirmPassword
              }
            }
          }
        } else {
          serverError.value = '网络错误，请检查网络连接'
        }
      } finally {
        isSubmitting.value = false
      }
    }

    return {
      form,
      errors,
      serverError,
      isSubmitting,
      handleRegister
    }
  }
}
</script>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  border-radius: 10px;
  background: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.register-title {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 2rem;
  font-size: 1.8rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: all 0.3s;
}

input:focus {
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.2);
  outline: none;
}

input.is-invalid {
  border-color: #ff4d4f;
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


button {
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

button:hover {
  background: linear-gradient(135deg, #2980b9, #3498db);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
button:disabled {
  background: #95a5a6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.server-error {
  color: #ff4d4f;
  margin-top: 10px;
  text-align: center;
}

.login-link {
  margin-top: 15px;
  text-align: center;
}

.login-link a {
  color: #1890ff;
  cursor: pointer;
  text-decoration: none;
}
.loading-spinner {
  display: inline-block;
  animation: spin 1s linear infinite;
}
/* 
.login-link a:hover {
  text-decoration: underline;
} */

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