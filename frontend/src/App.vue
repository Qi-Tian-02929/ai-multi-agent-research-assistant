<script setup lang="ts">
import { computed, nextTick, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { normalizeApiError, streamChat } from './api'
import ChatWindow from './components/ChatWindow.vue'
import PdfUpload from './components/PdfUpload.vue'
import SessionList from './components/SessionList.vue'
import type { ChatMessage, KnowledgeSession, UploadResponse } from './types'

const createSessionId = () => `session-${Date.now().toString(36)}`

const initialSessionId = createSessionId()
const activeSessionId = ref(initialSessionId)
const loading = ref(false)

const sessions = ref<KnowledgeSession[]>([
  {
    id: initialSessionId,
    title: '默认知识库问答',
    updatedAt: new Date().toISOString(),
    messageCount: 0,
  },
])

const messagesBySession = reactive<Record<string, ChatMessage[]>>({
  [initialSessionId]: [],
})

const activeMessages = computed(() => messagesBySession[activeSessionId.value] ?? [])

const activeSession = computed(() =>
  sessions.value.find((session) => session.id === activeSessionId.value),
)

const createMessage = (role: ChatMessage['role'], content: string): ChatMessage => ({
  id: `${role}-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`,
  role,
  content,
  createdAt: new Date().toISOString(),
})

const allowBrowserPaint = async () => {
  await nextTick()
  await new Promise((resolve) => setTimeout(resolve, 10))
}

const updateSessionMeta = (sessionId: string, query?: string) => {
  const session = sessions.value.find((item) => item.id === sessionId)
  if (!session) {
    return
  }

  session.updatedAt = new Date().toISOString()
  session.messageCount = messagesBySession[sessionId]?.length ?? 0
  if (query && session.messageCount <= 1) {
    session.title = query.length > 18 ? `${query.slice(0, 18)}...` : query
  }
}

const handleCreateSession = () => {
  const id = createSessionId()
  sessions.value.unshift({
    id,
    title: '新的问答会话',
    updatedAt: new Date().toISOString(),
    messageCount: 0,
  })
  messagesBySession[id] = []
  activeSessionId.value = id
}

const handleSelectSession = (sessionId: string) => {
  activeSessionId.value = sessionId
  if (!messagesBySession[sessionId]) {
    messagesBySession[sessionId] = []
  }
}

const shouldRewritePdfQuestion = (query: string) => {
  const normalized = query.replace(/\s+/g, '')
  return normalized === '这份PDF讲了什么' || normalized === '这份pdf讲了什么'
}

const getBackendQuery = (query: string) => {
  const fileName = activeSession.value?.lastUploadedFile
  if (!fileName || !shouldRewritePdfQuestion(query)) {
    return query
  }

  return `根据刚上传的 PDF 文件 ${fileName}，总结核心内容`
}

const handleSend = async (query: string) => {
  const sessionId = activeSessionId.value
  const backendQuery = getBackendQuery(query)
  messagesBySession[sessionId].push(createMessage('user', query))
  updateSessionMeta(sessionId, query)
  const assistantMessage = createMessage('assistant', '')
  messagesBySession[sessionId].push(assistantMessage)
  const aiIndex = messagesBySession[sessionId].length - 1
  loading.value = true
  await allowBrowserPaint()

  try {
    await streamChat(
      {
        query: backendQuery,
        session_id: sessionId,
      },
      async (chunk) => {
        messagesBySession[sessionId][aiIndex].content += chunk
        messagesBySession[sessionId] = [...messagesBySession[sessionId]]
        await allowBrowserPaint()
      },
    )

    updateSessionMeta(sessionId)
  } catch (error) {
    const normalized = normalizeApiError(error, '聊天请求失败')
    messagesBySession[sessionId][aiIndex].content = `请求失败：${normalized.message}`
    messagesBySession[sessionId] = [...messagesBySession[sessionId]]
    await allowBrowserPaint()
    ElMessage.error(
      normalized.kind === 'backend' ? `后端错误：${normalized.message}` : normalized.message,
    )
    updateSessionMeta(sessionId)
  } finally {
    loading.value = false
  }
}

const handleUploaded = (response: UploadResponse) => {
  if (!response.file) {
    return
  }

  const sessionId = activeSessionId.value
  const session = activeSession.value
  if (session) {
    session.lastUploadedFile = response.file
    session.lastUploadedChunks = response.chunks ?? 0
  }

  messagesBySession[sessionId].push(
    createMessage('system', `PDF 上传成功：${response.file}，共 ${response.chunks ?? 0} 个 chunks。`),
  )
  updateSessionMeta(sessionId)
}

const handleClearSession = () => {
  const sessionId = activeSessionId.value
  messagesBySession[sessionId] = []

  const session = activeSession.value
  if (session) {
    session.messageCount = 0
    session.title = '新的问答会话'
    session.updatedAt = new Date().toISOString()
    session.lastUploadedFile = undefined
    session.lastUploadedChunks = undefined
  }

  ElMessage.success('当前会话已清空')
}
</script>

<template>
  <main class="app-shell">
    <div class="sidebar">
      <SessionList
        :sessions="sessions"
        :active-session-id="activeSessionId"
        @create="handleCreateSession"
        @select="handleSelectSession"
      />
      <PdfUpload @uploaded="handleUploaded" />
    </div>

    <ChatWindow
      :messages="activeMessages"
      :loading="loading"
      :session-id="activeSessionId"
      @clear="handleClearSession"
      @send="handleSend"
    />
  </main>
</template>
