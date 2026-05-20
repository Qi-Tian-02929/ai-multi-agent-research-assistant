import axios from 'axios'
import type { ApiErrorInfo, ChatRequest, ChatResponse, UploadResponse } from '../types'

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000',
  timeout: 120000,
})

const getResponseMessage = (data: unknown) => {
  if (typeof data === 'object' && data !== null) {
    const record = data as Record<string, unknown>
    const detail = record.detail
    const error = record.error
    const message = record.message

    if (typeof detail === 'string') {
      return detail
    }
    if (typeof error === 'string') {
      return error
    }
    if (typeof message === 'string') {
      return message
    }
  }

  return ''
}

export const normalizeApiError = (error: unknown, fallback: string): ApiErrorInfo => {
  if (typeof error === 'object' && error !== null) {
    const record = error as Record<string, unknown>
    if (
      typeof record.kind === 'string' &&
      ['backend', 'network', 'upload', 'unknown'].includes(record.kind) &&
      typeof record.message === 'string'
    ) {
      return {
        kind: record.kind as ApiErrorInfo['kind'],
        message: record.message,
      }
    }
  }

  if (axios.isAxiosError(error)) {
    if (error.response) {
      return {
        kind: 'backend',
        message: getResponseMessage(error.response.data) || `后端错误：HTTP ${error.response.status}`,
      }
    }

    if (error.request) {
      return {
        kind: 'network',
        message: '网络错误：无法连接到后端服务，请确认 http://127.0.0.1:8000 已启动。',
      }
    }
  }

  return {
    kind: 'unknown',
    message: error instanceof Error ? error.message : fallback,
  }
}

export const sendChatMessage = async (payload: ChatRequest) => {
  const { data } = await http.post<ChatResponse>('/chat', payload)
  return data
}

export const streamChat = async (
  payload: ChatRequest,
  onChunk: (chunk: string) => void | Promise<void>,
) => {
  const response = await fetch('http://127.0.0.1:8000/chat/stream', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      query: payload.query,
      session_id: payload.session_id,
    }),
  })

  if (!response.ok) {
    let message = `HTTP ${response.status}`
    try {
      const data = await response.json()
      message = getResponseMessage(data) || message
    } catch {
      // Keep the HTTP status fallback when the backend does not return JSON.
    }

    throw {
      kind: 'backend',
      message,
    } satisfies ApiErrorInfo
  }

  if (!response.body) {
    throw {
      kind: 'network',
      message: 'Streaming response is not available.',
    } satisfies ApiErrorInfo
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder()

  while (true) {
    const { done, value } = await reader.read()
    if (done) {
      break
    }

    const chunk = decoder.decode(value, { stream: true })
    if (chunk) {
      await onChunk(chunk)
    }
  }

  const remaining = decoder.decode()
  if (remaining) {
    await onChunk(remaining)
  }
}

export const uploadPdf = async (file: File) => {
  const formData = new FormData()
  formData.append('file', file)

  const { data } = await http.post<UploadResponse>('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })

  if (data.error) {
    throw {
      kind: 'upload',
      message: data.error,
    } satisfies ApiErrorInfo
  }

  return data
}
