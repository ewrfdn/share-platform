<template>
    <div class="categories-container">
        <a-row :gutter="16">
            <!-- 左侧一级分类列表 -->
            <a-col :span="8">
                <a-card title="一级分类" :bordered="false">
                    <template #extra>
                        <a-button type="primary" @click="showAddRootCategoryModal">
                            <plus-outlined /> 新增一级分类
                        </a-button>
                    </template>
                    <a-table
                        :columns="rootColumns"
                        :data-source="rootCategories"
                        :loading="loading"
                        :pagination="false"
                        rowKey="id"
                        :row-selection="{ 
                            selectedRowKeys: [selectedRootId], 
                            onChange: handleRootSelect,
                            type: 'radio'
                        }"
                        @row-click="(record) => handleRootSelect([record.id])"
                    >
                        <template #bodyCell="{ column, record }">
                            <template v-if="column.key === 'action'">
                                <a-space>
                                    <a-button type="link" size="small" @click="showEditCategoryModal(record)">
                                        编辑
                                    </a-button>
                                    <a-popconfirm
                                        title="确定要删除该分类吗？这将同时删除其所有子分类！"
                                        ok-text="确定"
                                        cancel-text="取消"
                                        @confirm="deleteCategory(record.id, true)"
                                    >
                                        <a-button type="link" danger size="small">删除</a-button>
                                    </a-popconfirm>
                                </a-space>
                            </template>
                        </template>
                    </a-table>
                </a-card>
            </a-col>

            <!-- 右侧子分类树状结构 -->
            <a-col :span="16">
                <a-card :title="selectedRootCategory ? `${selectedRootCategory.display_name}的子分类` : '子分类'" :bordered="false">
                    <template #extra>
                        <a-space>
                            <a-button 
                                type="primary" 
                                @click="showAddSubCategoryModal"
                                :disabled="!selectedTreeNode && !selectedRootId"
                            >
                                <plus-outlined /> 新增子分类
                            </a-button>
                        </a-space>
                    </template>
                    <div v-if="selectedRootId" class="tree-container">
                        <a-tree
                            v-if="categoryTree.length"
                            :tree-data="categoryTree"
                            :field-names="{ title: 'display_name', key: 'id' }"
                            :show-line="true"
                            :selectable="true"
                            :default-expanded-all="true"
                            @select="handleTreeSelect"
                            :selectedKeys="selectedTreeKeys"
                        >
                            <template #title="{ display_name, id }">
                                <span class="tree-node">
                                    {{ display_name }}
                                    <a-space class="tree-node-actions">
                                        <a-button type="link" size="small" @click.stop="showEditCategoryModal({ id, display_name })">
                                            编辑
                                        </a-button>
                                        <a-popconfirm
                                            title="确定要删除该分类吗？"
                                            ok-text="确定"
                                            cancel-text="取消"
                                            @confirm.stop="deleteCategory(id)"
                                        >
                                            <a-button type="link" danger size="small">删除</a-button>
                                        </a-popconfirm>
                                    </a-space>
                                </span>
                            </template>
                        </a-tree>
                        <a-empty v-else description="暂无子分类" />
                    </div>
                    <a-empty v-else description="请先选择一个一级分类" />
                </a-card>
            </a-col>
        </a-row>

        <!-- 分类编辑/新增模态框 -->
        <a-modal
            v-model:visible="categoryModalVisible"
            :title="modalTitle"
            @ok="handleCategoryModalOk"
            :confirm-loading="confirmLoading"
            @cancel="categoryModalVisible = false"
        >
            <a-form
                :model="categoryForm"
                :rules="rules"
                ref="categoryFormRef"
                :label-col="{ span: 5 }"
                :wrapper-col="{ span: 18 }"
            >
                <a-form-item label="分类名称" name="display_name">
                    <a-input v-model:value="categoryForm.display_name" placeholder="请输入分类名称" />
                </a-form-item>
            </a-form>
        </a-modal>
    </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import { PlusOutlined } from '@ant-design/icons-vue';
import { categoryApi } from '@/api/category';

// 表格列定义
const rootColumns = [
    {
        title: '分类名称',
        dataIndex: 'display_name',
        key: 'display_name',
    },
    {
        title: '操作',
        key: 'action',
        width: 150,
    }
];

// 状态定义
const loading = ref(false);
const rootCategories = ref([]);
const categoryTree = ref([]);
const selectedRootId = ref(null);
const selectedTreeNode = ref(null);
const selectedTreeKeys = ref([]);
const expandedKeys = ref([]);
const categoryModalVisible = ref(false);
const confirmLoading = ref(false);
const isEdit = ref(false);
const currentCategoryId = ref(null);

// 计算属性
const selectedRootCategory = computed(() => {
    return rootCategories.value.find(cat => cat.id === selectedRootId.value);
});

const modalTitle = computed(() => {
    if (isEdit.value) {
        return '编辑分类';
    }
    if (selectedTreeNode.value) {
        return `新增 ${selectedTreeNode.value.display_name} 的子分类`;
    }
    if (selectedRootId.value && !categoryForm.parent_id) {
        return '新增一级分类';
    }
    return `新增 ${selectedRootCategory.value?.display_name || ''} 的子分类`;
});

// 表单相关
const categoryFormRef = ref(null);
const categoryForm = reactive({
    display_name: '',
    parent_id: null
});

const rules = {
    display_name: [
        { required: true, message: '请输入分类名称', trigger: 'blur' },
        { min: 2, max: 50, message: '分类名称长度必须在2-50个字符之间', trigger: 'blur' }
    ]
};

// 获取一级分类列表
const fetchRootCategories = async () => {
    loading.value = true;
    try {
        const response = await categoryApi.getAllCategories();
        rootCategories.value = response.data.filter(cat => !cat.parent_id);
    } catch (error) {
        console.error('获取一级分类失败:', error);
        message.error('获取一级分类失败');
    } finally {
        loading.value = false;
    }
};

// 获取分类树
const fetchCategoryTree = async () => {
    if (!selectedRootId.value) return;
    
    loading.value = true;
    try {
        const response = await categoryApi.getCategoryTree();
        const selectedRoot = response.data.find(item => item.id === selectedRootId.value);
        categoryTree.value = selectedRoot ? (selectedRoot.children || []) : [];
        expandedKeys.value = getTreeKeys(categoryTree.value);
    } catch (error) {
        console.error('获取分类树失败:', error);
        message.error('获取分类树失败');
    } finally {
        loading.value = false;
    }
};

// 获取树中所有节点的key
const getTreeKeys = (tree) => {
    const keys = [];
    const traverse = (nodes) => {
        nodes.forEach(node => {
            keys.push(node.id);
            if (node.children && node.children.length) {
                traverse(node.children);
            }
        });
    };
    traverse(tree);
    return keys;
};

// 选择一级分类
const handleRootSelect = (selectedRowKeys) => {
    if (selectedRowKeys && selectedRowKeys.length > 0) {
        selectedRootId.value = selectedRowKeys[0];
        selectedTreeNode.value = null;
        selectedTreeKeys.value = [];
        fetchCategoryTree();
    }
};

// 选择树节点
const handleTreeSelect = (selectedKeys, info) => {
    if (selectedKeys && selectedKeys.length > 0) {
        selectedTreeKeys.value = selectedKeys;
        selectedTreeNode.value = info.selectedNodes[0];
    } else {
        selectedTreeKeys.value = [];
        selectedTreeNode.value = null;
    }
};

// 显示新增一级分类模态框
const showAddRootCategoryModal = () => {
    isEdit.value = false;
    resetForm();
    categoryForm.parent_id = null;
    categoryModalVisible.value = true;
};

// 显示新增子分类模态框
const showAddSubCategoryModal = () => {
    if (!selectedTreeNode.value && !selectedRootId.value) {
        message.warning('请先选择一个分类');
        return;
    }
    isEdit.value = false;
    resetForm();
    // 如果选中了树节点，使用树节点的ID作为父ID，否则使用根分类ID
    categoryForm.parent_id = selectedTreeNode.value ? selectedTreeNode.value.id : selectedRootId.value;
    categoryModalVisible.value = true;
};

// 显示编辑分类模态框
const showEditCategoryModal = (category) => {
    isEdit.value = true;
    currentCategoryId.value = category.id;
    categoryForm.display_name = category.display_name;
    categoryForm.parent_id = category.parent_id;
    categoryModalVisible.value = true;
};

// 处理模态框确认
const handleCategoryModalOk = () => {
    categoryFormRef.value.validate().then(() => {
        if (isEdit.value) {
            updateCategory();
        } else {
            createCategory();
        }
    });
};

// 创建分类
const createCategory = async () => {
    confirmLoading.value = true;
    try {
        await categoryApi.createCategory(categoryForm);
        message.success('分类创建成功');
        categoryModalVisible.value = false;
        resetForm();
        refreshData();
    } catch (error) {
        console.error('创建分类失败:', error);
        message.error('创建分类失败');
    } finally {
        confirmLoading.value = false;
    }
};

// 更新分类
const updateCategory = async () => {
    confirmLoading.value = true;
    try {
        await categoryApi.updateCategory(currentCategoryId.value, categoryForm);
        message.success('分类更新成功');
        categoryModalVisible.value = false;
        resetForm();
        refreshData();
    } catch (error) {
        console.error('更新分类失败:', error);
        message.error('更新分类失败');
    } finally {
        confirmLoading.value = false;
    }
};

// 删除分类
const deleteCategory = async (categoryId, recursive = false) => {
    try {
        await categoryApi.deleteCategory(categoryId, recursive);
        message.success('分类删除成功');
        refreshData();
    } catch (error) {
        console.error('删除分类失败:', error);
        message.error('删除分类失败');
    }
};

// 重置表单
const resetForm = () => {
    categoryForm.display_name = '';
    if (categoryFormRef.value) {
        categoryFormRef.value.resetFields();
    }
};

// 刷新数据
const refreshData = () => {
    fetchRootCategories();
    if (selectedRootId.value) {
        fetchCategoryTree();
    }
};

// 生命周期钩子
onMounted(() => {
    fetchRootCategories();
});
</script>

<style scoped>
.categories-container {
    padding: 24px;
}

.tree-container {
    min-height: 400px;
}

.tree-node {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
}

.tree-node-actions {
    opacity: 0;
    transition: opacity 0.3s;
}

.tree-node:hover .tree-node-actions {
    opacity: 1;
}

:deep(.ant-tree-node-content-wrapper) {
    width: 100%;
}

:deep(.ant-tree-title) {
    width: 100%;
}
</style> 