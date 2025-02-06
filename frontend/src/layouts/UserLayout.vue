<template>
    <a-layout class="layout-container">
        <a-layout-header class="header">
            <div class="logo">
                <img src="@/assets/logo.png" alt="Logo" />
                <span>教材学习系统</span>
            </div>
            <a-menu v-model:selectedKeys="selectedKeys" theme="dark" mode="horizontal">
                <a-menu-item key="home">
                    <router-link to="/user">首页</router-link>
                </a-menu-item>
            </a-menu>
            <div class="header-right">
                <a-dropdown>
                    <a class="user-dropdown" @click.prevent>
                        <a-avatar :src="userInfo.avatar || '@/assets/default-avatar.png'" />
                        <span class="username">{{ userInfo.username }}</span>
                    </a>
                    <template #overlay>
                        <a-menu>
                            <a-menu-item key="profile">
                                <user-outlined />
                                个人信息
                            </a-menu-item>
                            <a-menu-item key="logout" @click="handleLogout">
                                <logout-outlined />
                                退出登录
                            </a-menu-item>
                        </a-menu>
                    </template>
                </a-dropdown>
            </div>
        </a-layout-header>

        <a-layout-content class="content">
            <router-view></router-view>
        </a-layout-content>

        <a-layout-footer class="footer">
            教材制作分享系统 ©{{ new Date().getFullYear() }}
        </a-layout-footer>
    </a-layout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
    UserOutlined,
    LogoutOutlined
} from '@ant-design/icons-vue'

const router = useRouter()
const route = useRoute()

// 选中的菜单项
const selectedKeys = ref(['home'])
// 用户信息
const userInfo = ref(JSON.parse(localStorage.getItem('userInfo') || '{}'))

// 监听路由变化，更新选中的菜单项
onMounted(() => {
    const path = route.path.split('/')[2] || 'home'
    selectedKeys.value = [path]
})

// 退出登录
const handleLogout = () => {
    localStorage.removeItem('accessToken')
    localStorage.removeItem('userInfo')
    router.push('/login')
}
</script>

<style scoped>
.layout-container {
    min-height: 100vh;
}

.header {
    display: flex;
    align-items: center;
    padding: 0 24px;
}

.logo {
    display: flex;
    align-items: center;
    gap: 8px;
    color: white;
    margin-right: 48px;
}

.logo img {
    height: 32px;
}

.header-right {
    margin-left: auto;
}

.user-dropdown {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    color: white;
}

.content {
    margin: 24px;
    padding: 24px;
    background: #fff;
    min-height: 280px;
}

.footer {
    text-align: center;
}

:deep(.ant-menu-dark) {
    background: transparent;
}
</style>