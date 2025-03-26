import request from '@/utils/http/axios'

/**
 * Category API - 分类相关接口
 * 对应 backend/app/routes/category.py
 */
export const categoryApi = {
    /**
     * 获取所有分类
     * GET /api/category/categories
     * @returns {Promise<{data: Array, message: string}>}
     */
    getAllCategories() {
        return request.get('/api/category/categories');
    },

    /**
     * 获取分类树结构
     * GET /api/category/categories/tree
     * @returns {Promise<{data: Array, message: string}>}
     */
    getCategoryTree() {
        return request.get('/api/category/categories/tree');
    },

    /**
     * 获取指定分类信息
     * GET /api/category/categories/:id
     * @param {number} categoryId - 分类ID
     * @returns {Promise<{data: Object, message: string}>}
     */
    getCategoryById(categoryId) {
        return request.get(`/api/category/categories/${categoryId}`);
    },

    /**
     * 获取指定分类的直接子分类
     * GET /api/category/categories/:id/children
     * @param {number} categoryId - 分类ID
     * @returns {Promise<{data: Array, message: string}>}
     */
    getCategoryChildren(categoryId) {
        return request.get(`/api/category/categories/${categoryId}/children`);
    },

    /**
     * 获取指定分类的所有后代分类
     * GET /api/category/categories/:id/descendants
     * @param {number} categoryId - 分类ID
     * @returns {Promise<{data: Array, message: string}>}
     */
    getCategoryDescendants(categoryId) {
        return request.get(`/api/category/categories/${categoryId}/descendants`);
    },

    /**
     * 创建分类
     * POST /api/category/categories
     * @param {Object} data - 分类数据
     * @param {string} data.display_name - 分类名称（必填）
     * @param {number} [data.parent_id] - 父分类ID（可选）
     * @returns {Promise<{data: Object, message: string}>}
     */
    createCategory(data) {
        return request.post('/api/category/categories', data);
    },

    /**
     * 更新分类
     * PUT /api/category/categories/:id
     * @param {number} categoryId - 分类ID
     * @param {Object} data - 更新数据
     * @param {string} [data.display_name] - 分类名称
     * @param {number} [data.parent_id] - 父分类ID
     * @returns {Promise<{data: Object, message: string}>}
     */
    updateCategory(categoryId, data) {
        return request.put(`/api/category/categories/${categoryId}`, data);
    },

    /**
     * 删除分类
     * DELETE /api/category/categories/:id
     * @param {number} categoryId - 分类ID
     * @param {boolean} [recursive=false] - 是否递归删除子分类
     * @returns {Promise<{message: string}>}
     */
    deleteCategory(categoryId, recursive = false) {
        return request.delete(`/api/category/categories/${categoryId}?recursive=${recursive}`);
    }
};

export default categoryApi; 