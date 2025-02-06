import { createRouter, createWebHistory } from 'vue-router'
import userRoutes from './user'
import adminRoutes from './admin'

// 公共路由
const publicRoutes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/pages/Login.vue'),
    meta: { 
      requiresAuth: false,
      title: '登录'
    }
  },
  {
    path: '/',
    redirect: '/login'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes: [...publicRoutes, userRoutes, adminRoutes]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 获取存储的用户信息
  const accessToken = localStorage.getItem('accessToken')
  const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}')
  
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - 教材制作分享系统`
  }

  // 不需要认证的路由直接通过
  if (!to.meta.requiresAuth) {
    next()
    return
  }

  // 需要认证但没有token，跳转到登录页
  if (!accessToken) {
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
    return
  }

  // 检查角色权限
  if (to.meta.roles && !to.meta.roles.includes(userInfo.role_id)) {
    next({
      path: userInfo.role_id === 3 ? '/user' : '/admin',
      query: { redirect: to.fullPath }
    })
    return
  }

  // 根据角色重定向首页
  if (to.path === '/') {
    next(userInfo.role_id === 3 ? '/user' : '/admin')
    return
  }

  next()
})

// 路由错误处理
router.onError((error) => {
  console.error('路由错误:', error)
})

export default router
