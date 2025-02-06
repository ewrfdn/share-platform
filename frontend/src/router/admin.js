// 管理员和教师可访问的路由
export default {
  path: '/admin',
  component: () => import('@/layouts/AdminLayout.vue'),
  meta: { 
    requiresAuth: true,
    roles: [1, 2] // 管理员和教师角色ID
  },
  children: [
    {
      path: '',
      name: 'AdminHome',
      component: () => import('@/pages/admin/HomePage.vue'),
      meta: {
        title: '管理首页'
      }
    },
    {
      path: 'users',
      name: 'UserManagement',
      component: () => import('@/pages/admin/UserManagement.vue'),
      meta: {
        title: '用户管理',
        roles: [1, 2] // 管理员和教师都可访问
      }
    },
    {
      path: 'roles',
      name: 'RoleManagement',
      component: () => import('@/pages/admin/RoleManagement.vue'),
      meta: {
        title: '角色管理',
        roles: [1] // 只有管理员可访问
      }
    }
  ]
}
