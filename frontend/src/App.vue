<template>
  <div class="app-container">
    <!-- 顶部导航栏 -->
    <header class="app-header">
      <div class="header-content">
        <h1 class="app-title">✨ Vue + Flask 留言板</h1>
        <p class="app-subtitle" v-if="isLoggedIn">欢迎回来，{{ username }}！</p>
        <button v-if="isLoggedIn" @click="logout" class="logout-btn">退出登录</button>
      </div>
    </header>

    <!-- 主内容区：根据登录状态切换显示 -->
    <main class="app-main">
      <div class="background" :class="showRegister ? 'login' : 'register'"></div>
      <div class="auth-outer" v-if="!isLoggedIn">
        <div class="auth-inner">

          <TransitionGroup name="slide-fade" mode="out-in">
            <div class="form-container" :key="showRegister ? 'login' : 'register'">
              <Register v-if="showRegister" @register-success="handleRegistrationSuccess"
                @switch-to-login="showRegister = false" />
              <Login v-else @login-success="handleLoginSuccess"
                @switch-to-register="showRegister = true" />
            </div>

          </TransitionGroup>
        </div>
      </div>
      <MessageBoard ref="messageBoard" />
    </main>

    <!-- 页脚 -->
    <footer class="app-footer">
      <p>版权所有© 2025 KrisHugo</p>
    </footer>
  </div>
</template>
<script lang="ts">
import Register from './components/Register.vue';
import Login from './components/Login.vue';
import MessageBoard from './components/MessageBoard.vue';
// import { useAuthStore } from './stores/authStore';
import { useAuthStore } from './stores/authStore'; // 确保路径正确

export default {
  name: 'App',
  components: { Login, Register, MessageBoard },
  data() {
    return {
      isLoggedIn: false,  // 初始未登录
      showRegister: false, // 控制注册表单显示
      username: ''        // 存储登录用户名
    };
  },
  methods: {
    // 处理登录成功事件（由 Login 组件触发）
    handleLoginSuccess(res: any) {

      const userStore = useAuthStore();
      userStore.updateUserInfo(res);
      this.isLoggedIn = userStore.isLoggedIn();
      this.username = userStore.user.username; // 从 store 获取用户名
      const board = this.$refs.messageBoard as InstanceType<typeof MessageBoard>;
      board.fetchMessages(); // 刷新留言列表
    },
    handleRegistrationSuccess() {
      this.showRegister = false;
      alert('注册成功！请登录');
    },
    // 退出登录
    logout() {

      const userStore = useAuthStore();
      this.isLoggedIn = false;
      this.username = '';
      // 清除本地存储的 token 和用户信息
      userStore.clearUserInfo();
    }
  },
  mounted() {

    const userStore = useAuthStore();
    if (userStore.isLoggedIn()) {
      this.isLoggedIn = true;
      this.username = userStore.user.username; // 从 store 获取用户名
      // 这里可以调用 API 验证 token 有效性
    }
  }
};
</script>

<style scoped>
/* 全局容器 */
.app-container {
  width: 100vw;
  min-height: 100vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  /* background-color: #f8f9fa; */
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  margin: 0 auto;
  width: 100%;
  /* max-width: 1400px; 控制整体宽度 */
  justify-content: center;
  position: relative;
}

/* 导航栏样式 */
.app-header {
  background: linear-gradient(135deg, #3498db, #2c3e50);
  color: white;
  padding: 2rem 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.header-content {
  /* max-width: 1400px; 更宽的最大宽度 */
  margin: 0 auto;
  padding: 0 2rem;
  text-align: center;
}

.app-title {
  font-size: 2.5rem;
  margin: 0;
  letter-spacing: 1px;
}

.app-subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin: 0.5rem 0 0;
}

/* 主内容区 */
.app-main {
  flex: 1;
  width: 90%;
  /* 内容区稍窄于外层 */
  margin: 0 auto;
  padding: 0 20px;
  /* position: relative; */
  /* 左右留白 */
  min-height: 400px;
  overflow: hidden;
  /* 根据内容高度调整 */
  max-width: 100%;
  object-fit: cover;
}

/* 页脚样式 */
.app-footer {
  text-align: center;
  padding: 1.5rem;
  background-color: #2c3e50;
  color: #ecf0f1;
  font-size: 0.9rem;
}

.logout-btn {
  position: absolute;
  right: 20px;
  top: 20px;
  padding: 8px 16px;
  background: #ff4757;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.app-header {
  position: relative;
  /* 让 logout-btn 相对此定位 */
}


/* 响应式设计 */
@media (max-width: 1200px) {

  .header-content,
  .app-main {
    max-width: 1000px;
  }
}

@media (max-width: 768px) {
  .app-title {
    font-size: 2rem;
  }

  .app-main {
    padding: 0 1rem;
  }
}


.background {
  position: absolute;
  top: 0;
  left: 0;
  width: 200%;
  height: 100%;
  background: linear-gradient(90deg, #4facfe 0%, #00f2fe 50%, #4facfe 100%);
  transition: transform 0.6s ease;
  z-index: -1;
  margin: 0;
  padding: 0;
}

.background.login {
  transform: translateX(0) skewY(0deg);
}

.background.register {
  transform: translateX(-50%) skewY(5deg);
}


/* 添加至你的全局样式文件或组件内 */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.5s cubic-bezier(0.55, 0, 0.1, 1);
  transform-style: preserve-3d;
  position: absolute;
  left: 0;
  right: 0;
  margin: 0 auto;
  /* width: 100%; */
  max-width: 400px;
  will-change: transform, opacity;
  
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(30px) rotateY(90deg);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(-30px) rotateY(-90deg);
}

.form-container{
  perspective: 1000px;
  transform-style: preserve-3d;
}

/* 修复后的样式 */
.auth-outer {
  display: flex;
  justify-content: center;
  width: 100%;
}

.auth-inner {
  position: relative;
  width: 100%;
  max-width: 400px; /* 表单设计宽度 */
}

.auth-container {
  position: relative;
  min-height: 400px;
  /* 根据内容高度调整 */
  overflow: hidden;
}
</style>