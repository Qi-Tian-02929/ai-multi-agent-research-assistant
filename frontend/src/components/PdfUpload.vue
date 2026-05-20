<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { normalizeApiError, uploadPdf } from '../api'
import type { ApiErrorInfo, UploadResponse } from '../types'

const emit = defineEmits<{
  uploaded: [response: UploadResponse]
}>()

const uploading = ref(false)

const showUploadError = (error: ApiErrorInfo) => {
  const prefix = error.kind === 'backend' ? '后端错误' : error.kind === 'network' ? '网络错误' : '上传失败'
  ElMessage.error(`${prefix}：${error.message}`)
}

const beforeUpload = (file: File) => {
  if (file.type !== 'application/pdf' && !file.name.toLowerCase().endsWith('.pdf')) {
    ElMessage.error('上传失败：请上传 PDF 文件')
    return false
  }

  return true
}

const handleUpload = async (options: { file: File }) => {
  uploading.value = true

  try {
    const response = await uploadPdf(options.file)
    ElMessage.success(`上传成功：${response.file ?? options.file.name}，${response.chunks ?? 0} 个 chunks`)
    emit('uploaded', response)
  } catch (error) {
    const normalized =
      typeof error === 'object' && error !== null && 'kind' in error && 'message' in error
        ? (error as ApiErrorInfo)
        : normalizeApiError(error, 'PDF 上传失败')
    showUploadError(normalized)
  } finally {
    uploading.value = false
  }
}
</script>

<template>
  <section class="upload-panel">
    <div>
      <p class="eyebrow">PDF Ingestion</p>
      <h2>知识库文档</h2>
      <p class="hint">上传 PDF 后写入后端向量库，后续问题会基于文档检索回答。</p>
    </div>

    <el-upload
      drag
      accept="application/pdf,.pdf"
      :show-file-list="false"
      :disabled="uploading"
      :before-upload="beforeUpload"
      :http-request="handleUpload"
    >
      <div class="upload-content">
        <span class="upload-icon">PDF</span>
        <span>{{ uploading ? '正在入库...' : '拖拽或点击上传 PDF' }}</span>
      </div>
    </el-upload>
  </section>
</template>

<style scoped>
.upload-panel {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 18px;
  border-top: 1px solid rgba(148, 163, 184, 0.24);
  background: rgba(15, 23, 42, 0.46);
}

.eyebrow {
  margin: 0 0 4px;
  color: #93c5fd;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0;
  text-transform: uppercase;
}

h2 {
  margin: 0 0 8px;
  color: #f8fafc;
  font-size: 18px;
  line-height: 1.25;
}

.hint {
  margin: 0;
  color: #cbd5e1;
  font-size: 13px;
  line-height: 1.55;
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  color: #e0f2fe;
  font-size: 14px;
}

.upload-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border: 1px solid rgba(147, 197, 253, 0.45);
  border-radius: 8px;
  background: rgba(37, 99, 235, 0.22);
  font-weight: 800;
}

:deep(.el-upload-dragger) {
  padding: 22px 14px;
  border-color: rgba(147, 197, 253, 0.4);
  background: rgba(15, 23, 42, 0.56);
}

:deep(.el-upload-dragger:hover) {
  border-color: #60a5fa;
}
</style>
