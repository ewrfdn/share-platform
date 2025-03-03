<template>
  <div class="role-management-container">
    <a-card title="角色管理" :bordered="false">
      <!-- 角色列表表格 -->
      <a-table 
        :columns="columns" 
        :data-source="roles" 
        :loading="loading"
        :pagination="pagination"
        @change="handleTableChange"
        rowKey="id">
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'action'">
            <a-space>
              <a-button type="link" size="small" @click="showRoleDetails(record)">
                查看详情
              </a-button>
            </a-space>
          </template>
        </template>
      </a-table>
      
      <!-- 查看角色详情的模态框 -->
      <a-modal
        v-model:visible="roleModalVisible"
        title="角色详情"
        @cancel="roleModalVisible = false"
        :footer="null"
      >
        <a-descriptions bordered>
          <a-descriptions-item label="角色ID" span={3}>
            {{ currentRole.id }}
          </a-descriptions-item>
          <a-descriptions-item label="显示名称" span={3}>
            {{ currentRole.display_name }}
          </a-descriptions-item>
          <a-descriptions-item label="角色描述" span={3}>
            {{ currentRole.description || '无描述' }}
          </a-descriptions-item>
          <a-descriptions-item label="创建时间" span={3}>
            {{ currentRole.created_at }}
          </a-descriptions-item>
          <a-descriptions-item label="更新时间" span={3}>
            {{ currentRole.updated_at }}
          </a-descriptions-item>
        </a-descriptions>
      </a-modal>
    </a-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import { admin } from '@/api';

// 表格列定义
const columns = [
  {
    title: 'ID',
    dataIndex: 'id',
    key: 'id',
    sorter: true,
  },
  {
    title: '显示名称',
    dataIndex: 'display_name',
    key: 'display_name',
  },
  {
    title: '描述',
    dataIndex: 'description',
    key: 'description',
    ellipsis: true,
  },
  {
    title: '创建时间',
    dataIndex: 'created_at',
    key: 'created_at',
    sorter: true,
  },
  {
    title: '操作',
    key: 'action',
  }
];

// 状态定义
const roles = ref([]);
const loading = ref(false);
const roleModalVisible = ref(false);
const currentRole = ref({});

// 分页配置
const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
  showSizeChanger: true,
  showQuickJumper: true,
  showTotal: total => `共 ${total} 条记录`
});

// 获取角色列表
const fetchRoles = async () => {
  loading.value = true;
  try {
    const response = await admin.role.getAllRoles();
    roles.value = response.map(role => ({
      ...role,
      key: role.id
    }));
    pagination.total = roles.value.length;
  } catch (error) {
    console.error('获取角色列表失败:', error);
    message.error('获取角色列表失败');
  } finally {
    loading.value = false;
  }
};

// 显示角色详情
const showRoleDetails = (role) => {
  currentRole.value = { ...role };
  roleModalVisible.value = true;
};

// 处理表格变化
const handleTableChange = (pag, filters, sorter) => {
  pagination.current = pag.current;
  pagination.pageSize = pag.pageSize;
  
  // 这里可以添加服务端排序/过滤的逻辑
  console.log('Table change:', pag, filters, sorter);
};

// 生命周期钩子 - 组件挂载后执行
onMounted(() => {
  fetchRoles();
});
</script>

<style scoped>
.role-management-container {
  padding: 24px;
}
</style>
