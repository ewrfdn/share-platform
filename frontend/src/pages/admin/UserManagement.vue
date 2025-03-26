<template>
  <div class="user-management-container">
    <a-card title="用户管理" :bordered="false">
      <template #extra>
        <a-button type="primary" @click="showAddUserModal" class="button-spacing">
          <plus-outlined /> 添加用户
        </a-button>
        <a-button type="default" @click="downloadTemplate" class="button-spacing">
          下载模板
        </a-button>
        <a-upload 
          accept=".xls,.xlsx" 
          @change="handleUpload" 
          show-upload-list="false"
          class="button-spacing"
        >
          <a-button type="default">
            导入用户
          </a-button>
        </a-upload>
      </template>
      
      <!-- 用户列表表格 -->
      <a-table 
        :columns="columns" 
        :data-source="users" 
        :loading="loading"
        :pagination="pagination"
        @change="handleTableChange"
        rowKey="id">
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'role'">
            <a-tag :color="getRoleColor(record.role_id)">
              {{ getRoleName(record.role_id) }}
            </a-tag>
          </template>
          <template v-if="column.key === 'avatar'">
            <a-avatar :src="record.avatar || 'https://joeschmoe.io/api/v1/random'" />
          </template>
          <template v-if="column.key === 'action'">
            <a-space>
              <a-button type="link" size="small" @click="showEditUserModal(record)">
                编辑
              </a-button>
              <a-popconfirm
                title="确定要删除该用户吗？"
                ok-text="确定"
                cancel-text="取消"
                @confirm="deleteUser(record.id)"
              >
                <a-button type="link" danger size="small">删除</a-button>
              </a-popconfirm>
            </a-space>
          </template>
        </template>
      </a-table>
      
      <!-- 添加/编辑用户的模态框 -->
      <a-modal
        v-model:visible="userModalVisible"
        :title="modalTitle"
        @ok="handleUserModalOk"
        :confirmLoading="confirmLoading"
        @cancel="userModalVisible = false"
      >
        <a-form
          :model="userForm"
          :rules="rules"
          ref="userFormRef"
          :label-col="{ span: 5 }"
          :wrapper-col="{ span: 18 }"
        >
          <a-form-item label="用户名" name="username">
            <a-input v-model:value="userForm.username" :disabled="isEdit" />
          </a-form-item>
          <a-form-item 
            label="密码" 
            name="password"
            :rules="[{ required: !isEdit, message: '请输入密码!' }]"
          >
            <a-input-password v-model:value="userForm.password" :placeholder="isEdit ? '留空表示不修改密码' : '请输入密码'" />
          </a-form-item>
          <a-form-item label="角色" name="role_id">
            <a-select v-model:value="userForm.role_id" placeholder="请选择角色">
              <a-select-option 
                v-for="role in roles" 
                :key="role.id" 
                :value="role.id"
                :disabled="currentUserRole > 1 && role.id === 1"
              >
                {{ role.display_name }}
              </a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item label="头像" name="avatar">
            <a-input v-model:value="userForm.avatar" placeholder="头像URL（可选）" />
          </a-form-item>
        </a-form>
      </a-modal>
    </a-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { message, Upload } from 'ant-design-vue';
import { PlusOutlined } from '@ant-design/icons-vue';
import { admin } from '@/api';

// 表格列定义
const columns = [
  {
    title: '用户名',
    dataIndex: 'username',
    key: 'username',
    sorter: true,
  },
  {
    title: '角色',
    dataIndex: 'role_id',
    key: 'role',
  },
  {
    title: '头像',
    dataIndex: 'avatar',
    key: 'avatar',
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
const users = ref([]);
const roles = ref([]);
const loading = ref(false);
const userModalVisible = ref(false);
const confirmLoading = ref(false);
const isEdit = ref(false);
const currentUserId = ref(null);
const currentUserRole = ref(1); // 默认为管理员

// 用户表单
const userFormRef = ref(null);
const userForm = reactive({
  username: '',
  password: '',
  role_id: undefined,
  avatar: ''
});

// 表单验证规则
const rules = {
  username: [
    { required: true, message: '请输入用户名!', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度必须在3-20之间', trigger: 'blur' }
  ],
  role_id: [
    { required: true, message: '请选择角色!', trigger: 'change' }
  ]
};

// 分页配置
const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
  showSizeChanger: true,
  showQuickJumper: true,
  showTotal: total => `共 ${total} 条记录`
});

// 计算属性 - 模态框标题
const modalTitle = computed(() => isEdit.value ? '编辑用户' : '添加用户');

// 获取当前用户角色
const getCurrentUserRole = () => {
  const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}');
  currentUserRole.value = userInfo.role_id || 1;
};

// 获取用户列表
const fetchUsers = async () => {
  loading.value = true;
  try {
    const response = await admin.user.getAllUsers();
    users.value = response.map(user => ({
      ...user,
      key: user.id
    }));
    pagination.total = users.value.length;
  } catch (error) {
    console.error('获取用户列表失败:', error);
    message.error('获取用户列表失败');
  } finally {
    loading.value = false;
  }
};

// 获取角色列表
const fetchRoles = async () => {
  try {
    const response = await admin.role.getAllRoles();
    roles.value = response;
  } catch (error) {
    console.error('获取角色列表失败:', error);
    message.error('获取角色列表失败');
  }
};

// 角色名称和颜色映射
const getRoleName = (roleId) => {
  const role = roles.value.find(r => r.id === roleId);
  return role ? role.display_name : '未知角色';
};

const getRoleColor = (roleId) => {
  switch (roleId) {
    case 1: return 'red';
    case 2: return 'green';
    case 3: return 'blue';
    default: return 'default';
  }
};

// 显示添加用户模态框
const showAddUserModal = () => {
  isEdit.value = false;
  resetForm();
  userModalVisible.value = true;
};

// 显示编辑用户模态框
const showEditUserModal = (user) => {
  isEdit.value = true;
  currentUserId.value = user.id;
  
  // 填充表单数据
  userForm.username = user.username;
  userForm.password = ''; // 编辑时不显示密码
  userForm.role_id = user.role_id;
  userForm.avatar = user.avatar || '';
  
  userModalVisible.value = true;
};

// 处理用户表单提交
const handleUserModalOk = () => {
  userFormRef.value.validate().then(() => {
    if (isEdit.value) {
      updateUser();
    } else {
      createUser();
    }
  }).catch(error => {
    console.log('表单验证失败', error);
  });
};

// 创建用户
const createUser = async () => {
  confirmLoading.value = true;
  try {
    await admin.user.createUser(userForm);
    message.success('用户创建成功');
    userModalVisible.value = false;
    resetForm();
    fetchUsers();
  } catch (error) {
    console.error('创建用户失败:', error);
    message.error(error.response?.data?.message || '创建用户失败');
  } finally {
    confirmLoading.value = false;
  }
};

// 更新用户
const updateUser = async () => {
  confirmLoading.value = true;
  try {
    const userData = { ...userForm };
    if (!userData.password) {
      delete userData.password;
    }
    
    await admin.user.updateUser(currentUserId.value, userData);
    message.success('用户更新成功');
    userModalVisible.value = false;
    resetForm();
    fetchUsers();
  } catch (error) {
    console.error('更新用户失败:', error);
    message.error(error.response?.data?.message || '更新用户失败');
  } finally {
    confirmLoading.value = false;
  }
};

// 删除用户
const deleteUser = async (userId) => {
  try {
    await admin.user.deleteUser(userId);
    message.success('用户删除成功');
    fetchUsers();
  } catch (error) {
    console.error('删除用户失败:', error);
    message.error(error.response?.data?.message || '删除用户失败');
  }
};

// 重置表单
const resetForm = () => {
  userForm.username = '';
  userForm.password = '';
  userForm.role_id = undefined;
  userForm.avatar = '';
  if (userFormRef.value) {
    userFormRef.value.resetFields();
  }
};

// 处理表格变化
const handleTableChange = (pag, filters, sorter) => {
  pagination.current = pag.current;
  pagination.pageSize = pag.pageSize;
  
  // 这里可以添加服务端排序/过滤的逻辑
  console.log('Table change:', pag, filters, sorter);
};

// 下载用户导入模板
const downloadTemplate = async () => {
  try {
    const response = await admin.user.downloadTemplate(); // Use admin.user to download the template
    const link = document.createElement('a');
    link.href = response.url; // Assuming the response contains the URL for the template
    link.setAttribute('download', '用户导入模板.xlsx');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (error) {
    console.error('下载模板失败:', error);
    message.error('下载模板失败');
  }
};

// 处理上传
const handleUpload = async (info) => {
  if (info.file.status === 'done') {
    try {
      const formData = new FormData();
      formData.append('file', info.file.originFileObj); // Append the uploaded file

      await admin.user.importUsers(formData); // Use admin.user to import users
      message.success(`${info.file.name} 文件上传成功`);
      fetchUsers(); // Refresh the user list after upload
    } catch (error) {
      message.error(`${info.file.name} 文件上传失败`);
      console.error('上传文件失败:', error);
    }
  } else if (info.file.status === 'error') {
    message.error(`${info.file.name} 文件上传失败`);
  }
};

// 生命周期钩子 - 组件挂载后执行
onMounted(() => {
  getCurrentUserRole();
  fetchUsers();
  fetchRoles();
});
</script>

<style scoped>
.user-management-container {
  padding: 24px;
}

.button-spacing {
  margin-right: 8px; /* Adjust the value as needed for spacing */
}
</style>
