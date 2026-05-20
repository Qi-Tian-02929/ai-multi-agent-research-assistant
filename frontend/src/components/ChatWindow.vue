<script setup lang="ts">
import MarkdownIt from 'markdown-it'
import { computed, nextTick, ref, watch } from 'vue'
import type { ChatMessage } from '../types'

const props = defineProps<{
  messages: ChatMessage[]
  loading: boolean
  sessionId: string
}>()

const emit = defineEmits<{
  clear: []
  send: [query: string]
}>()

const markdown = new MarkdownIt({
  breaks: true,
  html: false,
  linkify: true,
})

const draft = ref('')
const messageBodyRef = ref<HTMLElement | null>(null)

const canSend = computed(() => draft.value.trim().length > 0 && !props.loading)

const submit = () => {
  const query = draft.value.trim()
  if (!query || props.loading) {
    return
  }

  emit('send', query)
  draft.value = ''
}

const renderMarkdown = (content: string) => markdown.render(content)

const scrollToBottom = async () => {
  await nextTick()
  if (messageBodyRef.value) {
    messageBodyRef.value.scrollTop = messageBodyRef.value.scrollHeight
  }
}

watch(
  () => [props.messages.length, props.loading, props.sessionId, props.messages.at(-1)?.content],
  scrollToBottom,
)
</script>

<template>
  <section class="chat-window">
    <header class="chat-header">
      <div>
        <p class="eyebrow">Knowledge Assistant</p>
        <h1>AI 多工具研究助手</h1>
        <p class="subtitle">支持 PDF 知识库、联网搜索、多轮对话与工具调用的 AI 研究助手</p>
      </div>
      <div class="header-actions">
        <el-tag type="success" effect="light">Session: {{ sessionId }}</el-tag>
        <el-button :disabled="messages.length === 0 || loading" @click="$emit('clear')">
          清空会话
        </el-button>
      </div>
    </header>

    <div ref="messageBodyRef" class="message-body">
      <div v-if="messages.length === 0" class="empty-state">
        <h2>开始提问</h2>
        <p>上传 PDF 后，可以围绕文档内容、摘要、关键数据和结论进行追问。</p>
      </div>

      <article
        v-for="message in messages"
        :key="message.id"
        class="message-row"
        :class="message.role"
      >
        <div class="message-bubble">
          <div class="message-role">
            {{ message.role === 'user' ? '你' : message.role === 'system' ? '系统' : 'AI' }}
          </div>
          <div
            v-if="message.role === 'assistant'"
            class="markdown-body"
            v-html="renderMarkdown(message.content)"
          />
          <p v-else>{{ message.content }}</p>
        </div>
      </article>

      <article v-if="loading && messages.at(-1)?.role !== 'assistant'" class="message-row assistant">
        <div class="message-bubble loading-bubble">
          <div class="message-role">AI</div>
          <el-skeleton :rows="2" animated />
        </div>
      </article>
    </div>

    <footer class="composer">
      <el-input
        v-model="draft"
        :disabled="loading"
        :autosize="{ minRows: 2, maxRows: 5 }"
        type="textarea"
        resize="none"
        placeholder="输入你的问题，例如：这份 PDF 讲了什么"
        @keydown.enter.exact.prevent="submit"
      />
      <el-button type="primary" :loading="loading" :disabled="!canSend" @click="submit">
        发送
      </el-button>
    </footer>
  </section>
</template>

<style scoped>
.chat-window {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
  background: #f8fafc;
}

.chat-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  padding: 24px 30px 18px;
  border-bottom: 1px solid #e2e8f0;
  background: #ffffff;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.eyebrow {
  margin: 0 0 6px;
  color: #2563eb;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0;
  text-transform: uppercase;
}

h1 {
  margin: 0;
  color: #0f172a;
  font-size: 28px;
  line-height: 1.2;
}

.subtitle {
  margin: 8px 0 0;
  color: #64748b;
  line-height: 1.6;
}

.message-body {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 16px;
  min-height: 0;
  padding: 24px 30px;
  overflow: auto;
}

.empty-state {
  margin: auto;
  max-width: 440px;
  padding: 34px;
  border: 1px dashed #cbd5e1;
  border-radius: 8px;
  background: #ffffff;
  text-align: center;
}

.empty-state h2 {
  margin: 0 0 10px;
  color: #0f172a;
  font-size: 24px;
}

.empty-state p {
  margin: 0;
  color: #64748b;
  line-height: 1.7;
}

.message-row {
  display: flex;
}

.message-row.user {
  justify-content: flex-end;
}

.message-row.assistant,
.message-row.system {
  justify-content: flex-start;
}

.message-bubble {
  max-width: min(720px, 78%);
  padding: 14px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 0 8px 22px rgba(15, 23, 42, 0.06);
}

.message-row.user .message-bubble {
  border-color: #bfdbfe;
  background: #2563eb;
  color: #ffffff;
}

.message-row.system .message-bubble {
  border-color: #bbf7d0;
  background: #f0fdf4;
  color: #166534;
}

.message-role {
  margin-bottom: 7px;
  font-size: 12px;
  font-weight: 800;
  opacity: 0.72;
}

.message-bubble p {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.7;
}

.markdown-body {
  color: #1e293b;
  line-height: 1.7;
  word-break: break-word;
}

.markdown-body :deep(p),
.markdown-body :deep(ul),
.markdown-body :deep(ol),
.markdown-body :deep(pre),
.markdown-body :deep(blockquote) {
  margin: 0 0 10px;
}

.markdown-body :deep(p:last-child),
.markdown-body :deep(ul:last-child),
.markdown-body :deep(ol:last-child),
.markdown-body :deep(pre:last-child),
.markdown-body :deep(blockquote:last-child) {
  margin-bottom: 0;
}

.markdown-body :deep(code) {
  padding: 2px 5px;
  border-radius: 4px;
  background: #e2e8f0;
  font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
  font-size: 0.92em;
}

.markdown-body :deep(pre) {
  overflow: auto;
  padding: 12px;
  border-radius: 8px;
  background: #0f172a;
  color: #e2e8f0;
}

.markdown-body :deep(pre code) {
  padding: 0;
  background: transparent;
  color: inherit;
}

.markdown-body :deep(a) {
  color: #2563eb;
}

.loading-bubble {
  width: min(520px, 72%);
}

.composer {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 92px;
  gap: 12px;
  padding: 18px 30px 24px;
  border-top: 1px solid #e2e8f0;
  background: #ffffff;
}

.composer .el-button {
  min-height: 54px;
}

@media (max-width: 760px) {
  .chat-header {
    flex-direction: column;
    padding: 20px;
  }

  .header-actions {
    justify-content: flex-start;
  }

  .message-body {
    padding: 20px;
  }

  .message-bubble {
    max-width: 92%;
  }

  .composer {
    grid-template-columns: 1fr;
    padding: 16px 20px 20px;
  }
}
</style>
