<template>
    <div class="message-board">
        <!-- 输入框 -->
        <form @submit.prevent="submitMessage" class="message-form">
            <input v-model="newMessage" placeholder="写下你的想法..." class="input-field" required />
            <button type="submit" class="submit-btn">发布</button>
        </form>

        <!-- 留言列表（PC 多列布局） -->
        <div v-if="isLoading" class="loading">加载中...</div>
        <div v-else class="message-grid">
            <div v-for="message in messages" :key="message.id" class="message-card">
                <p class="message-content">{{ message.content }}</p>
                <span class="message-time">{{ formatTime(message.created_at) }}</span>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            isLoading: false,
            newMessage: '',
            messages: [],  // 存储从后端获取的留言
            error: null
        }
    },
    mounted() {
        this.fetchMessages()  // 组件加载时获取留言
    },
    methods: {
        async fetchMessages() {
            this.isLoading = true;
            try {
                const response = await axios.get('http://localhost:5000/api/messages')
                this.messages = response.data
            } catch (error) {
                console.error('获取留言失败:', error)
            } finally {
                this.isLoading = false;
            }
        },
        async submitMessage() {
            try {
                await axios.post('http://localhost:5000/api/messages', {
                    content: this.newMessage
                })
                this.newMessage = ''  // 清空输入框
                this.fetchMessages()  // 重新加载留言
            } catch (error) {
                console.error('提交留言失败:', error)
            }
        },
        formatTime(timestamp) {
            return new Date(timestamp).toLocaleString()  // 格式化时间
        }
    }
}
</script>

<style scoped>
.message-board {
    width: 100%;
    max-width: 100%;
    /* 继承父容器宽度 */
    margin: 0 auto;
    padding: 1rem;
    /* 微调内边距 */
}

/* 输入框和按钮 */
.message-form {
    display: flex;
    gap: 10px;
    margin-bottom: 2rem;
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
}

.input-field {
    flex: 1;
    padding: 12px 15px;
    border: 2px solid #ddd;
    border-radius: 8px;
    font-size: 1rem;
    transition: border-color 0.3s;
}

.input-field:focus {
    border-color: #3498db;
    outline: none;
}

.submit-btn {
    padding: 12px 25px;
    background: #3498db;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: bold;
    transition: background 0.3s;
}

.submit-btn:hover {
    background: #2980b9;
}

/* 留言网格布局（PC 多列） */
.message-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 20px;
    margin: 0 auto;
    /* 网格居中 */
}

/* 留言卡片 */
.message-card {
    background: white;
    border-radius: 10px;
    padding: 1.5rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s, box-shadow 0.3s;
}

.message-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
}

.message-content {
    font-size: 1.1rem;
    color: #333;
    margin: 0 0 10px 0;
    line-height: 1.5;
}

.message-time {
    font-size: 0.85rem;
    color: #7f8c8d;
}

/* 加载动画 */
.loading {
    text-align: center;
    padding: 2rem;
    color: #7f8c8d;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .message-grid {
        grid-template-columns: 1fr;
        /* 手机端单列 */
    }

    .message-form {
        flex-direction: column;
    }

    .submit-btn {
        width: 100%;
    }
}
</style>