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
      <Login v-if="!isLoggedIn" @login-success="handleLoginSuccess" />
      <MessageBoard v-else ref="messageBoard" :key="isLoggedIn" />
    </main>

    <!-- 页脚 -->
    <footer class="app-footer">
      <p>© 2023 留言板</p>
    </footer>
  </div>
</template>
<script>
import Login from './components/Login.vue';
import MessageBoard from './components/MessageBoard.vue';

export default {
  components: { Login, MessageBoard },
  data() {
    return {
      isLoggedIn: false,  // 初始未登录
      username: ''        // 存储登录用户名
    };
  },
  methods: {
    // 处理登录成功事件（由 Login 组件触发）
    async handleLoginSuccess(token, username) {
      this.isLoggedIn = true;
      this.username = username;
      localStorage.setItem('token', token);
      console.log("登录成功，尝试刷新！");
      
      await this.$nextTick(); // 确保子组件已挂载
      this.$refs.messageBoard.fetchMessages(); // 手动触发刷新
    },
    // 退出登录
    logout() {
      this.isLoggedIn = false;
      this.username = '';
      localStorage.removeItem('token');  // 清除 token
    }
  },
  mounted() {
    // 检查本地是否有 token（自动登录）
    const token = localStorage.getItem('token');
    if (token) {
      this.isLoggedIn = true;
      // 这里可以调用 API 验证 token 有效性
    }
  }
};
</script>

<style scoped>
/* 全局容器 */
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f8f9fa;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  margin: 0 auto;
  width: 100%;
  /* max-width: 1400px; 控制整体宽度 */
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
  width: 90%; /* 内容区稍窄于外层 */
  margin: 0 auto;
  padding: 0 20px; /* 左右留白 */
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
  position: relative;  /* 让 logout-btn 相对此定位 */
}


/* 响应式设计 */
@media (max-width: 1200px) {
  .header-content, .app-main {
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
</style>