<template>
    <div class="materials-container">
        <div class="header">
            <h1>教材管理</h1>
            <div class="actions">
                <a-space>
                    <a-button type="primary" @click="showUploadModal">上传教材</a-button>
                    <a-button type="primary" @click="showCreateModal">制作教材</a-button>
                </a-space>
            </div>
        </div>

        <!-- 搜索表单 -->
        <a-form layout="inline" class="search-form" :model="searchForm">
            <a-form-item label="教材名称">
                <a-input
                    v-model:value="searchForm.display_name"
                    placeholder="请输入教材名称"
                    allow-clear
                    @change="handleSearch"
                />
            </a-form-item>
            <a-form-item label="描述">
                <a-input
                    v-model:value="searchForm.description"
                    placeholder="请输入描述关键词"
                    allow-clear
                    @change="handleSearch"
                />
            </a-form-item>
            <a-form-item label="教材分类">
                <a-cascader
                    style="width: 120px;"
                    v-model:value="searchForm.category_ids"
                    :options="categories"
                    :field-names="{
                        label: 'display_name',
                        value: 'id',
                    }"
                    :multiple="true"
                    :check-strictly="true"
                    placeholder="请选择分类"
                    @change="handleSearch"
                />
            </a-form-item>
            <a-form-item label="教材类型">
                <a-select
                    v-model:value="searchForm.material_type"
                    placeholder="请选择类型"
                    style="width: 120px"
                    allow-clear
                    @change="handleSearch"
                >
                    <a-select-option value="upload">上传教材</a-select-option>
                    <a-select-option value="create">制作教材</a-select-option>
                </a-select>
            </a-form-item>
            <a-form-item>
                <a-space>
                    <a-button type="primary" @click="handleSearch">查询</a-button>
                    <a-button @click="resetSearch">重置</a-button>
                </a-space>
            </a-form-item>
        </a-form>

        <!-- 教材列表 -->
        <a-table :dataSource="materials" :columns="columns" style="margin-top: 20px" :pagination="pagination" @change="handleTableChange" :scroll="{ x: 1500 }">
            <template #bodyCell="{ column, record }">
                <template v-if="column.key === 'cover'">
                    <img 
                        :src="record.cover" 
                        class="material-cover" 
                        :alt="record.display_name"
                    />
                </template>
                <template v-else-if="column.key === 'description'">
                    <a-typography-paragraph :ellipsis="{ rows: 2 }" :title="record.description">
                        {{ record.description || '-' }}
                    </a-typography-paragraph>
                </template>
                <template v-else-if="column.key === 'type'">
                    {{ record.material_type === 'upload' ? '上传教材' : '制作教材' }}
                </template>
                <template v-else-if="column.key === 'publish_status'">
                    <a-switch
                        v-model:checked="record.publish_status"
                        :checked-value="'public'"
                        :unchecked-value="'private'"
                        @change="(checked) => handlePublishChange(record, checked)"
                    />
                </template>
                <template v-else-if="column.key === 'action'">
                    <a-space>
                        <a-button type="primary" size="small" @click="previewMaterial(record)">预览</a-button>
                        <a-button 
                            v-if="record.material_type !== 'upload'" 
                            type="default" 
                            size="small" 
                            @click="editMaterial(record)"
                        >编辑</a-button>
                        <a-button type="primary" danger size="small" @click="deleteMaterial(record)">删除</a-button>
                    </a-space>
                </template>
            </template>
        </a-table>

        <!-- 上传/创建教材模态框 -->
        <a-modal
            :title="dialogMode === 'upload' ? '上传教材' : '创建教材'"
            v-model:visible="dialogVisible"
            @ok="handleSubmit"
            @cancel="dialogVisible = false"
            width="500px"
        >
            <a-form :model="materialForm" layout="vertical">
                <a-form-item label="教材名称" required>
                    <a-input v-model:value="materialForm.display_name" />
                </a-form-item>
                <a-form-item label="分类" required>
                    <a-cascader
                        v-model:value="materialForm.category_ids"
                        :options="categories"
                        :field-names="{
                            label: 'display_name',
                            value: 'id',
                        }"
                        :multiple="true"
                        :check-strictly="true"
                    />
                </a-form-item>
                <a-form-item label="描述">
                    <a-textarea v-model:value="materialForm.description" />
                </a-form-item>
                <a-form-item label="封面图片">
                    <a-upload
                        list-type="picture-card"
                        :show-upload-list="false"
                        :before-upload="beforeCoverUpload"
                        class="cover-uploader"
                    >
                        <img v-if="materialForm.cover" :src="materialForm.cover" class="cover-preview" />
                        <div v-else>
                            <plus-outlined />
                            <div style="margin-top: 8px">上传</div>
                        </div>
                    </a-upload>
                </a-form-item>
                <a-form-item v-if="dialogMode === 'upload'" label="教材文件" required>
                    <a-upload
                        :maxCount="1"
                        :before-upload="handleFileChange"
                    >
                        <a-button type="primary">
                            <upload-outlined />
                            选择文件
                        </a-button>
                    </a-upload>
                </a-form-item>
            </a-form>
        </a-modal>

        <!-- 预览模态框 -->
        <a-modal
            title="教材预览"
            v-model:visible="previewVisible"
            :width="'80%'"
            :footer="null"
            class="preview-modal"
        >
            <div v-if="previewData" class="preview-container">
                <!-- HTML预览 -->
                <div v-if="previewData?.material_type === 'html'" v-html="previewContent" class="html-preview"></div>
                <!-- Office文档预览 -->
                 <div style="width: 100%; height: 90%;" v-if="previewData.blob_id.mime_type === 'application/pdf'">
                    <object
                        :data="previewUrl"
                        type="application/pdf"
                        class="office-preview"

                    ></object>
                 </div>
            </div>
        </a-modal>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { message, Modal } from 'ant-design-vue';
import { PlusOutlined, UploadOutlined } from '@ant-design/icons-vue';
import { materialApi } from '@/api/material';
import { categoryApi } from '@/api/category';
import { blobApi } from '@/api/admin';

const router = useRouter();
const materials = ref([]);
const categories = ref([]);
const dialogVisible = ref(false);
const previewVisible = ref(false);
const dialogMode = ref('upload'); // 'upload' or 'create'
const previewData = ref(null);
const previewContent = ref('');
const previewUrl = ref('');

const columns = [
    {
        title: '封面',
        dataIndex: 'cover',
        key: 'cover',
        width: 100,
    },
    {
        title: '教材名称',
        dataIndex: 'display_name',
        key: 'display_name',
    },
    {
        title: '描述',
        dataIndex: 'description',
        key: 'description',
        width: 300,
    },
    {
        title: '类型',
        dataIndex: 'type',
        key: 'type',
        width: 120,
    },
    {
        title: '发布状态',
        dataIndex: 'publish_status',
        key: 'publish_status',
        width: 120,
    },
    {
        title: '操作',
        key: 'action',
        width: 300,
        fixed: 'right',
    },
];

const materialForm = ref({
    display_name: '',
    category_ids: [],
    description: '',
    cover: '',
    file: null,
    type: 'upload'
});

// 分页配置
const pagination = ref({
    current: 1,
    pageSize: 10,
    total: 0,
    showTotal: total => `共 ${total} 条`,
    showSizeChanger: true,
    showQuickJumper: true,
});

// 搜索表单
const searchForm = ref({
    display_name: '',
    description: '',
    category_ids: [],
    type: undefined
});

// 获取所有教材
const fetchMaterials = async (params = {}) => {
    try {
        const { current, pageSize } = pagination.value;
        const response = await materialApi.getAllMaterials({
            page: params.current || current,
            page_size: params.pageSize || pageSize,
            display_name: searchForm.value.display_name,
            description: searchForm.value.description,
            category_ids: searchForm.value.category_ids?.join(','),
            type: searchForm.value.material_type
        });
        materials.value = response.items.map(item => ({
            ...item,
            cover: item.cover ? (item.cover.startsWith('data:') ? item.cover : `data:image/jpeg;base64,${item.cover}`) : null
        }));
        pagination.value.total = response.total;
    } catch (error) {
        console.error('获取教材列表失败', error);
        message.error('获取教材列表失败：' + (error.message || '未知错误'));
    }
};

// 获取分类树
const fetchCategories = async () => {
    try {
        const response = await categoryApi.getCategoryTree();
        categories.value = response.data;
    } catch (error) {
        message.error('获取分类列表失败');
    }
};

// 显示上传模态框
const showUploadModal = () => {
    dialogMode.value = 'upload';
    materialForm.value = {
        display_name: '',
        category_ids: [],
        description: '',
        cover: '',
        file: null,
        type: 'upload'
    };
    dialogVisible.value = true;
};

// 显示创建模态框
const showCreateModal = () => {
    dialogMode.value = 'create';
    materialForm.value = {
        display_name: '',
        category_ids: [],
        description: '',
        cover: '',
        type: 'create'
    };
    dialogVisible.value = true;
};

// 处理封面图片上传
const beforeCoverUpload = (file) => {
    return new Promise((resolve, reject) => {
        // 检查文件类型
        const isImage = file.type.startsWith('image/');
        if (!isImage) {
            message.error('只能上传图片文件！');
            reject(new Error('只能上传图片文件！'));
            return;
        }

        // 检查文件大小（限制为2MB）
        const isLt2M = file.size / 1024 / 1024 < 2;
        if (!isLt2M) {
            message.error('图片大小不能超过2MB！');
            reject(new Error('图片大小不能超过2MB！'));
            return;
        }

        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = (e) => {
            materialForm.value.cover = e.target.result;
            resolve(false); // 阻止自动上传
        };
        reader.onerror = (error) => {
            message.error('图片读取失败');
            reject(error);
        };
    });
};

// 处理教材文件上传
const handleFileChange = (file) => {
    materialForm.value.file = file;
    return false; // 阻止自动上传
};

// 提交表单
const handleSubmit = async () => {
    try {
        const formData = new FormData();
        
        // 添加基本字段
        formData.append('display_name', materialForm.value.display_name);
        formData.append('category_ids', materialForm.value.category_ids.join(','));
        formData.append('description', materialForm.value.description || '');
        formData.append('cover', materialForm.value.cover || '');
        formData.append('material_type', materialForm.value.material_type);
        
        // 如果是创建类型，添加一个空的 HTML 文件
        if (dialogMode.value === 'create') {
            const emptyHtmlBlob = new Blob([''], { type: 'text/html' });
            formData.append('file', emptyHtmlBlob, 'empty.html');
        } else if (dialogMode.value === 'upload' && materialForm.value.file) {
            formData.append('file', materialForm.value.file);
        }
        
        const response = await materialApi.createMaterial(formData);
        message.success('创建成功');
        dialogVisible.value = false;
        
        if (dialogMode.value === 'create') {
            // 跳转到教材制作页面
            router.push(`/admin/materials/${response.data.id}/edit`);
        } else {
            fetchMaterials();
        }
    } catch (error) {
        message.error('创建失败');
    }
};

// 预览教材
const previewMaterial = async (material) => {
    try {
        previewData.value = material;
        if (material.material_type === 'create') {
            const response = await materialApi.getMaterialContent(material.id);
            previewContent.value = response.data;
        } else {
            const url = await blobApi.getBlobUrl(material.blob_id.id);
            previewUrl.value = url;
        }
        previewVisible.value = true;
        console.log(previewVisible.value);  
    } catch (error) {
        console.error('预览失败', error);
        message.error('预览失败',error.message);
    }
};

// 编辑教材
const editMaterial = (material) => {
    router.push(`/admin/materials/${material.id}/edit`);
};

// 删除教材
const deleteMaterial = async (material) => {
    try {
        await Modal.confirm({
            title: '确认删除',
            content: `确定要删除教材"${material.display_name}"吗？此操作不可恢复。`,
            okText: '确认删除',
            cancelText: '取消',
            okType: 'danger',
            centered: true,
            maskClosable: false,
            keyboard: false
        });
        
        await materialApi.deleteMaterial(material.id);
        message.success('删除成功');
        fetchMaterials();
    } catch (error) {
        if (error !== 'cancel') {
            message.error('删除失败：' + (error.message || '未知错误'));
        }
    }
};

// 发布状态切换
const handlePublishChange = async (material, checked) => {
    try {
        await materialApi.togglePublish(material.id, checked);
        message.success('操作成功');
    } catch (error) {
        message.error('操作失败');
        material.publish_status = material.publish_status === 'public' ? 'private' : 'public';
    }
};

// 处理表格变化（分页、排序等）
const handleTableChange = (pag, filters, sorter) => {
    fetchMaterials({
        current: pag.current,
        pageSize: pag.pageSize,
    });
};

// 处理搜索
const handleSearch = () => {
    pagination.value.current = 1; // 重置页码
    fetchMaterials();
};

// 重置搜索
const resetSearch = () => {
    searchForm.value = {
        display_name: '',
        description: '',
        category_ids: [],
        type: undefined
    };
    handleSearch();
};

onMounted(() => {
    fetchMaterials();
    fetchCategories();
});
</script>

<style scoped>
.materials-container {
    padding: 24px;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.cover-uploader {
    width: 178px;
    height: 178px;
}

.cover-preview {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.preview-container {
    height: calc(100vh - 200px);
    overflow: auto;
}

.html-preview {
    padding: 20px;
}

.office-preview {
    width: 100%;
    height: 100%;
    border: none;
}

.preview-modal {
    top: 24px;
}

:deep(.ant-upload-select) {
    width: 178px;
    height: 178px;
}

.material-cover {
    width: 60px;
    height: 60px;
    object-fit: cover;
    border-radius: 4px;
}

:deep(.ant-table-cell) {
    vertical-align: middle;
}

.search-form {
    margin: 16px 0;
    padding: 24px;
    background: #fff;
    border-radius: 2px;
}

:deep(.ant-form-item) {
    margin-bottom: 16px;
}
</style>