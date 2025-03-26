import request from '@/utils/http/axios'

/**
 * Material API - 教材相关接口
 */
export const materialApi = {
    /**
     * 获取所有教材
     * GET /api/material/materials
     * @param {Object} params - 查询参数
     * @param {number} params.page - 页码
     * @param {number} params.page_size - 每页数量
     * @param {string} [params.display_name] - 教材名称（模糊查询）
     * @param {string} [params.description] - 描述关键词（模糊查询）
     * @param {string} [params.category_ids] - 分类ID列表（逗号分隔）
     * @param {string} [params.type] - 教材类型 (upload/create)
     * @returns {Promise<{data: {items: Array, total: number}, message: string}>}
     */
    getAllMaterials(params = {}) {
        return request.get('/api/material/materials', {
            params: {
                page: params.page || 1,
                page_size: params.page_size || 10,
                display_name: params.display_name,
                description: params.description,
                category_ids: params.category_ids,
                type: params.type
            }
        });
    },

    /**
     * 创建教材
     * POST /api/material/materials
     * @param {Object} data - 教材数据
     * @param {string} data.display_name - 教材名称
     * @param {string} data.category_ids - 分类ID列表
     * @param {string} data.description - 教材描述
     * @param {string} data.cover - 封面图片(base64)
     * @param {number} data.blob_id - 文件ID
     * @param {string} data.type - 教材类型 (upload/create)
     */
    createMaterial(data) {
        return request.post('/api/material/materials', data);
    },

    /**
     * 更新教材
     * PUT /api/material/materials/:id
     * @param {number} id - 教材ID
     * @param {Object} data - 更新数据
     */
    updateMaterial(id, data) {
        return request.put(`/api/material/materials/${id}`, data);
    },

    /**
     * 删除教材
     * DELETE /api/material/materials/:id
     * @param {number} id - 教材ID
     */
    deleteMaterial(id) {
        return request.delete(`/api/material/materials/${id}`);
    },

    /**
     * 发布/取消发布教材
     * PUT /api/material/materials/:id/publish
     * @param {number} id - 教材ID
     * @param {boolean} isPublish - 是否发布
     */
    togglePublish(id, isPublish) {
        return request.put(`/api/material/materials/${id}/publish`, {
            publish_status: isPublish ? 'public' : 'private'
        });
    },

    /**
     * 获取教材内容
     * GET /api/material/materials/:id/content
     * @param {number} id - 教材ID
     */
    getMaterialContent(id) {
        return request.get(`/api/material/materials/${id}/content`);
    },

    /**
     * 保存教材内容
     * PUT /api/material/materials/:id/content
     * @param {number} id - 教材ID
     * @param {string} content - 教材内容
     */
    saveMaterialContent(id, content) {
        return request.put(`/api/material/materials/${id}/content`, { content });
    }
};

export default materialApi; 