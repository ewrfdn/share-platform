<template>
    <div class="login-container">
        <a-card class="login-card" title="教材制作分享系统">
            <a-form :model="formState" name="login" @finish="handleSubmit" autocomplete="off">
                <a-form-item name="username" :rules="[{ required: true, message: '请输入用户名!' }]">
                    <a-input v-model:value="formState.username" placeholder="用户名">
                        <template #prefix>
                            <UserOutlined />
                        </template>
                    </a-input>
                </a-form-item>

                <a-form-item name="password" :rules="[{ required: true, message: '请输入密码!' }]">
                    <a-input-password v-model:value="formState.password" placeholder="密码">
                        <template #prefix>
                            <LockOutlined />
                        </template>
                    </a-input-password>
                </a-form-item>

                <a-form-item>
                    <a-button type="primary" html-type="submit" :loading="loading" block>
                        登录
                    </a-button>
                </a-form-item>
            </a-form>
        </a-card>
    </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { message } from 'ant-design-vue'
import { UserOutlined, LockOutlined } from '@ant-design/icons-vue'
import { login } from '@/api/auth'

const router = useRouter()
const route = useRoute()

const loading = ref(false)
const formState = reactive({
    username: '',
    password: ''
})

const handleSubmit = async () => {
    try {
        loading.value = true
        const res = await login(formState)
        if (res) {
            // 保存token和用户信息
            localStorage.setItem('accessToken', res.access_token)
            localStorage.setItem('userInfo', JSON.stringify(res.user))

            message.success('登录成功')

            // 获取重定向地址或根据角色跳转
            const redirect = route.query.redirect ||
                (res.user.role_id === 3 ? '/user' : '/admin')
            router.push(redirect)
        }
    } catch (error) {
        console.error('登录错误:', error)
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
.login-container {
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #f0f2f5;
    background-image: linear-gradient(to right, #1677ff 0%, #1890ff 100%);
}

.login-card {
    width: 100%;
    max-width: 400px;
    margin: 0 24px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

:deep(.ant-card-head) {
    border-bottom: none;
}

:deep(.ant-card-head-title) {
    text-align: center;
    font-size: 24px;
    padding: 24px 0 0;
    color: #1677ff;
}

:deep(.ant-card-body) {
    padding: 24px 32px 32px;
}

:deep(.ant-input-affix-wrapper) {
    height: 40px;
}

:deep(.ant-btn) {
    height: 40px;
}

:deep(.ant-form-item:last-child) {
    margin-bottom: 0;
}
</style>