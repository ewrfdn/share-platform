import request from '@/utils/http/axios'
import { categoryApi } from './category'


/**
 * User API - 用户相关接口
 * 对应 backend/app/routes/user.py
 */
export const userApi = {
  /**
   * 获取所有用户
   * GET /api/user/users
   */
  getAllUsers() {
    return request.get('/api/user/users');
  },

  /**
   * 创建用户
   * POST /api/user/users
   * @param {Object} userData - 用户数据
   * @param {string} userData.username - 用户名
   * @param {string} userData.password - 密码
   * @param {number} userData.role_id - 角色ID
   * @param {string} [userData.avatar] - 头像URL (可选)
   */
  createUser(userData) {
    return request.post('/api/user/users', userData);
  },

  /**
   * 更新用户
   * PUT /api/user/users/:id
   * @param {number} userId - 用户ID
   * @param {Object} userData - 用户数据
   * @param {string} [userData.password] - 密码 (可选，留空表示不修改)
   * @param {number} [userData.role_id] - 角色ID
   * @param {string} [userData.avatar] - 头像URL (可选)
   */
  updateUser(userId, userData) {
    return request.put(`/api/user/users/${userId}`, userData);
  },

  /**
   * 删除用户
   * DELETE /api/user/users/:id
   * @param {number} userId - 用户ID
   */
  deleteUser(userId) {
    return request.delete(`/api/user/users/${userId}`);
  }
};

/**
 * Role API - 角色相关接口
 * 对应 backend/app/routes/role.py
 */
export const roleApi = {
  /**
   * 获取所有角色
   * GET /api/roles
   */
  getAllRoles() {
    return request.get('/api/role/roles');
  }
};

/**
 * Auth API - 认证相关接口
 * 对应 backend/app/routes/auth.py
 */
export const authApi = {
  /**
   * 用户登录
   * POST /api/auth/login
   * @param {Object} credentials - 登录凭证
   * @param {string} credentials.username - 用户名
   * @param {string} credentials.password - 密码
   */
  login(credentials) {
    return request.post('/api/auth/login', credentials);
  },

  /**
   * 获取当前用户信息
   * GET /api/auth/me
   */
  getCurrentUser() {
    return request.get('/api/auth/me');
  },

  /**
   * 用户登出
   * POST /api/auth/logout
   */
  logout() {
    return request.post('/api/auth/logout');
  }
};

/**
 * Blob API - 文件相关接口
 * 对应 backend/app/routes/blob.py
 */
export const blobApi = {
  /**
   * 上传文件
   * POST /api/blob/upload
   * @param {FormData} formData - 包含文件的FormData
   */
  uploadFile(formData) {
    return request.post('/api/blob/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },

  /**
   * 获取文件信息
   * GET /api/blob/:id
   * @param {number} blobId - 文件ID
   */
  getFileInfo(blobId) {
    return request.get(`/api/blob/${blobId}`);
  },

  /**
   * 下载文件
   * GET /api/blob/:id/download
   * @param {number} blobId - 文件ID
   */
  downloadFile(blobId) {
    return request.get(`/api/blob/preview/${blobId}`, {
      responseType: 'blob'
    });
  },

  getBlobUrl(blobId) {
    return request.baseUrl + `api/blob/preview/${blobId}`;
  }
};

export default {
  user: userApi,
  role: roleApi,
  auth: authApi,
  blob: blobApi,
  category: categoryApi
};
