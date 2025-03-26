<template>
    <div class="editor-container">
        <div class="editor-header">
            <h1>{{ material?.display_name || '教材制作' }}</h1>
            <div class="actions">
                <a-space>
                    <a-button type="primary" @click="saveMaterial">保存</a-button>
                    <a-button @click="goBack">返回</a-button>
                </a-space>
            </div>
        </div>

        <!-- 富文本编辑器 -->
        <div class="editor-content">
            <Toolbar
                style="border-bottom: 1px solid #ccc"
                :editor="editorRef"
                :defaultConfig="toolbarConfig"
                mode="default"
            />
            <Editor
                style="height: calc(100vh - 180px); overflow-y: hidden;"
                v-model="editorContent"
                :defaultConfig="editorConfig"
                mode="default"
                @onCreated="handleCreated"
            />
        </div>
    </div>
</template>

<script setup>
import { ref, shallowRef, onBeforeUnmount, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import '@wangeditor/editor/dist/css/style.css'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
import { materialApi } from '@/api/material'

const route = useRoute()
const router = useRouter()
const materialId = route.params.id

// 编辑器实例，必须用 shallowRef
const editorRef = shallowRef()
const material = ref(null)
const editorContent = ref('')

// 工具栏配置
const toolbarConfig = {
    excludeKeys: []
}

// 编辑器配置
const editorConfig = {
    placeholder: '请输入内容...',
    autoFocus: false,
    MENU_CONF: {}
}

// 组件销毁时，也及时销毁编辑器
onBeforeUnmount(() => {
    const editor = editorRef.value
    if (editor == null) return
    editor.destroy()
})

// 获取教材内容
const fetchMaterialContent = async () => {
    try {
        const response = await materialApi.getMaterialContent(materialId)
        editorContent.value = response.data || ''
    } catch (error) {
        message.error('获取教材内容失败')
    }
}

// 保存教材
const saveMaterial = async () => {
    try {
        await materialApi.saveMaterialContent(materialId, editorContent.value)
        message.success('保存成功')
    } catch (error) {
        message.error('保存失败')
    }
}

// 返回列表页
const goBack = () => {
    router.push('/admin/materials')
}

// 编辑器创建完成时的回调
const handleCreated = (editor) => {
    editorRef.value = editor
}

onMounted(() => {
    if (materialId) {
        fetchMaterialContent()
    }
})
</script>

<style scoped>
.editor-container {
    padding: 24px;
}

.editor-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.editor-content {
    border: 1px solid #ccc;
    border-radius: 4px;
}

:deep(.w-e-text-container) {
    height: calc(100vh - 180px) !important;
}
</style> 