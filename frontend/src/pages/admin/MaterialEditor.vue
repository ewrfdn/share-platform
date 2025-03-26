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

        <!-- Vditor 编辑器 -->
        <div class="editor-content">
            <div ref="editorRef"></div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import Vditor from 'vditor'
import 'vditor/dist/index.css'
import { materialApi } from '@/api/material'

const route = useRoute()
const router = useRouter()
const materialId = route.params.id

const editorRef = ref(null)
const material = ref(null)
const vditor = ref(null)

// 初始化编辑器
const initEditor = () => {
    vditor.value = new Vditor(editorRef.value, {
        height: 'calc(100vh - 380px)',
        mode: 'wysiwyg',
        cache: {
            enable: true,
            id: `vditor-${materialId}` // 使用教材ID作为缓存标识
        },
        toolbar: [
            'emoji', 'headings', 'bold', 'italic', 'strike', 'link', '|',
            'list', 'ordered-list', 'check', 'outdent', 'indent', '|',
            'quote', 'line', 'code', 'inline-code', '|',
            'upload', 'table', '|',
            'undo', 'redo', '|',
            'fullscreen'
        ],
        upload: {
            accept: 'image/*',
            handler: async (files) => {
                // 处理文件上传
                // 根据实际需求实现
            }
        },
        after: () => {
            fetchMaterialContent()
        }
    })
}

// 获取教材内容
const fetchMaterialContent = async () => {
    try {
        const response = await materialApi.getMaterialContent(materialId)
        if (vditor.value) {
            vditor.value.setValue(response.data || '')
        }
    } catch (error) {
        message.error('获取教材内容失败')
    }
}

// 保存教材
const saveMaterial = async () => {
    try {
        if (vditor.value) {
            const content = vditor.value.getValue()
            await materialApi.saveMaterialContent(materialId, content)
            message.success('保存成功')
        }
    } catch (error) {
        message.error('保存失败')
    }
}

// 返回列表页
const goBack = () => {
    router.push('/admin/materials')
}

onMounted(() => {
    initEditor()
})

onBeforeUnmount(() => {
    if (vditor.value) {
        vditor.value.destroy()
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
    background: #fff;
}
</style>