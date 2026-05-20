export type ChatRole = 'user' | 'assistant' | 'system'

export interface ChatMessage {
  id: string
  role: ChatRole
  content: string
  createdAt: string
}

export interface ChatRequest {
  query: string
  session_id: string
}

export interface ChatResponse {
  answer: string
  session_id: string
}

export interface UploadResponse {
  message?: string
  file?: string
  chunks?: number
  error?: string
}

export interface KnowledgeSession {
  id: string
  title: string
  updatedAt: string
  messageCount: number
  lastUploadedFile?: string
  lastUploadedChunks?: number
}

export type ApiErrorKind = 'backend' | 'network' | 'upload' | 'unknown'

export interface ApiErrorInfo {
  kind: ApiErrorKind
  message: string
}
