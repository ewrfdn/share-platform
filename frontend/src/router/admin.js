import AdminLayout from '../layouts/AdminLayout.vue'

const adminRoutes = {
  path: '/admin',
  component: AdminLayout,
  meta: {
    requiresAuth: true,
    roles: [1, 2] // 管理员和教师可访问
  },
  children: [
    {
      path: '',
      name: 'AdminHome',
      component: () => import('@/pages/admin/HomePage.vue'),
      meta: {
        title: '管理首页',
        roles: [1, 2]
      }
    },
    {
      path: 'materials',
      name: 'MaterialsManagement',
      component: () => import('../pages/admin/Materials.vue'),
      meta: {
        title: '教材管理',
        roles: [1, 2]
      }
    },
    {
      path: 'categories',
      name: 'CategoriesManagement',
      component: () => import('../pages/admin/Categories.vue'),
      meta: {
        title: '分类管理',
        roles: [1, 2]
      }
    },
    {
      path: 'comments',
      name: 'CommentsManagement',
      component: () => import('../pages/admin/Comments.vue'),
      meta: {
        title: '评论管理',
        roles: [1, 2]
      }
    },
    {
      path: 'users',
      name: 'UserManagement',
      component: () => import('../pages/admin/UserManagement.vue'),
      meta: {
        title: '用户管理',
        roles: [1, 2]
      }
    },
    {
      path: 'roles',
      name: 'RoleManagement',
      component: () => import('../pages/admin/RoleManagement.vue'),
      meta: {
        title: '角色管理',
        roles: [1] // 仅管理员可访问
      }
    }
  ]
}

export default adminRoutes
