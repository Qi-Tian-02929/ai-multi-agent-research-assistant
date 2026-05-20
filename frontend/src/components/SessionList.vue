<script setup lang="ts">
import type { KnowledgeSession } from '../types'

defineProps<{
  sessions: KnowledgeSession[]
  activeSessionId: string
}>()

defineEmits<{
  create: []
  select: [sessionId: string]
}>()
</script>

<template>
  <aside class="session-panel">
    <div class="panel-head">
      <div>
        <p class="eyebrow">Sessions</p>
        <h2>会话列表</h2>
      </div>
      <el-button circle type="primary" aria-label="新建会话" @click="$emit('create')">
        +
      </el-button>
    </div>

    <div class="session-list">
      <button
        v-for="session in sessions"
        :key="session.id"
        class="session-item"
        :class="{ active: session.id === activeSessionId }"
        type="button"
        @click="$emit('select', session.id)"
      >
        <span class="session-title">{{ session.title }}</span>
        <span class="session-meta">
          {{ session.messageCount }} 条消息
          <template v-if="session.lastUploadedFile"> · 已上传 PDF</template>
        </span>
      </button>
    </div>
  </aside>
</template>

<style scoped>
.session-panel {
  display: flex;
  flex-direction: column;
  min-height: 0;
  padding: 24px 18px;
  background: #111827;
  color: #f8fafc;
}

.panel-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 22px;
}

.eyebrow {
  margin: 0 0 4px;
  color: #93c5fd;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0;
  text-transform: uppercase;
}

h2 {
  margin: 0;
  color: #f8fafc;
  font-size: 22px;
  line-height: 1.2;
}

.session-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-height: 0;
  overflow: auto;
}

.session-item {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 7px;
  width: 100%;
  min-height: 72px;
  padding: 14px;
  border: 1px solid rgba(148, 163, 184, 0.22);
  border-radius: 8px;
  background: rgba(15, 23, 42, 0.72);
  color: inherit;
  cursor: pointer;
  text-align: left;
  transition:
    background 0.2s,
    border-color 0.2s;
}

.session-item:hover,
.session-item.active {
  border-color: #60a5fa;
  background: rgba(30, 64, 175, 0.46);
}

.session-title {
  width: 100%;
  overflow: hidden;
  color: #f8fafc;
  font-size: 15px;
  font-weight: 700;
  line-height: 1.3;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.session-meta {
  color: #cbd5e1;
  font-size: 13px;
}
</style>
