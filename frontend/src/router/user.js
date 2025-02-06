// 学生用户可访问的路由
export default {
  path: '/user',
  component: () => import('@/layouts/UserLayout.vue'),
  meta: { 
    requiresAuth: true,
    roles: [3] // 学生角色ID
  },
  children: [
    {
      path: '',
      name: 'UserHome',
      component: () => import('@/pages/user/HomePage.vue'),
      meta: {
        title: '学生首页'
      }
    }
  ]
}
