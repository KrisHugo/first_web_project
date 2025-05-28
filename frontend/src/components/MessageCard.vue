<template>
    <div class="message-card">
        <div class="user-info">
            <img :src="message.user.avatar" class="avatar" />
            <span class="username">{{ message.user.username }}</span>
        </div>
        <div class="message-content">{{ message.content }}</div>
        <div class="message-footer">
            <span class="time">{{ formatTime(message.created_at) }}</span>
            <button v-if="isOwner(message.user.username)" @click="$emit('delete')" class="delete-btn">
                删除
            </button>
        </div>
    </div>
</template>

<script>
export default {
    props: ['message', 'currentUser'],
    methods: {
        formatTime(timestamp) {
            return new Date(timestamp).toLocaleString()
        },
        isOwner(username) {
            // console.log('Current User:', this.currentUser);
            // console.log('Checking ownership for:', username);
            return this.currentUser && this.currentUser.username === username
        }
    }
}
</script>

<style scoped>
.message-card {
    border: 1px solid #eee;
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 15px;
}

.user-info {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}

.avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    margin-right: 10px;
}

.username {
    font-weight: bold;
    color: #2c3e50;
}

.message-footer {
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
    color: #7f8c8d;
    font-size: 0.8rem;
}

.delete-btn {
    color: #e74c3c;
    background: none;
    border: none;
    cursor: pointer;
}
</style>