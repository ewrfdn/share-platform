<template>
    <a-layout class="layout-container">
        <a-layout-sider v-model:collapsed="collapsed" collapsible>
            <div class="logo">
                <img src="@/assets/logo.png" alt="Logo" />
                <span v-show="!collapsed">教材管理系统</span>
            </div>
            <a-menu v-model:selectedKeys="selectedKeys" theme="dark" mode="inline">
                <a-menu-item key="home">
                    <template #icon>
                        <home-outlined />
                    </template>
                    <router-link to="/admin">首页</router-link>
                </a-menu-item>

                <!-- 管理员和教师可见 -->
                <a-menu-item v-if="userInfo.role_id <= 2" key="users">
                    <template #icon>
                        <user-outlined />
                    </template>
                    <router-link to="/admin/users">用户管理</router-link>
                </a-menu-item>

                <!-- 仅管理员可见 -->
                <a-menu-item v-if="userInfo.role_id === 1" key="roles">
                    <template #icon>
                        <team-outlined />
                    </template>
                    <router-link to="/admin/roles">角色管理</router-link>
                </a-menu-item>
            </a-menu>
        </a-layout-sider>

        <a-layout>
            <a-layout-header class="header">
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
    </a-layout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
    HomeOutlined,
    UserOutlined,
    TeamOutlined,
    LogoutOutlined
} from '@ant-design/icons-vue'

const router = useRouter()
const route = useRoute()

// 侧边栏折叠状态
const collapsed = ref(false)
// 选中的菜单项
const selectedKeys = ref([])
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

.logo {
    height: 64px;
    padding: 16px;
    color: white;
    display: flex;
    align-items: center;
    gap: 8px;
}

.logo img {
    height: 32px;
}

.header {
    background: #fff;
    padding: 0 24px;
    display: flex;
    justify-content: flex-end;
    align-items: center;
    box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
}

.header-right {
    display: flex;
    align-items: center;
}

.user-dropdown {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
}

.username {
    color: rgba(0, 0, 0, 0.85);
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
</style>