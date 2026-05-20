# AI Multi-Agent Research Assistant

AI Multi-Agent Research Assistant 是一个基于 FastAPI、Vue3、LangGraph、LangChain Tool Calling、RAG、Redis 和 Docker Compose 构建的多 Agent 研究助手项目。

项目面向文档问答、联网检索、计算分析和多轮研究对话场景。用户可以上传 PDF 文档，系统会自动完成解析、切分、Embedding 和 Chroma 向量库入库，并在对话中通过 RAG 检索文档内容。同时，系统支持普通问答、流式输出、多工具调用和基于 `session_id` 的多轮上下文记忆。

---

## 1. 项目介绍

本项目实现了一个完整的 AI 多 Agent 研究助手。后端通过 FastAPI 提供 API 服务，使用 LangGraph 编排 Planner、Router、Summary 等 Agent 节点，使用 LangChain Tool Calling 接入 `calculator`、`web_search`、`rag_search` 等工具。

前端使用 Vue3 + Vite + TypeScript 构建，提供 PDF 上传、会话管理、聊天问答和流式 AI 回复展示。后端和 Redis 通过 Docker Compose 启动，前端通过 npm 在本地启动。

---

## 2. 技术栈

| 模块 | 技术 |
| --- | --- |
| 后端框架 | FastAPI |
| 前端框架 | Vue3 + Vite + TypeScript |
| UI 与交互 | Element Plus、Markdown 渲染、ReadableStream |
| Agent 工作流 | LangGraph |
| LLM 工具调用 | LangChain Tool Calling |
| 大模型 | DeepSeek Chat |
| Embedding | DashScope Embeddings |
| 联网搜索 | Tavily |
| 向量数据库 | Chroma |
| PDF 解析 | PyPDF |
| 文本切分 | LangChain Text Splitters |
| 多轮记忆 | Redis |
| 后端部署 | Docker Compose |

---

## 3. 系统架构

```text
用户
 |
 | 访问 http://localhost:5173
 v
Vue3 + Vite + TypeScript 前端
 |        |        |
 |        |        +-- PDF 上传
 |        +----------- 普通问答
 +-------------------- 流式问答
 |
 v
FastAPI 后端 API
 |
 +-- /upload
 |     |
 |     +-- PDF 解析
 |     +-- 文本切分
 |     +-- Embedding
 |     +-- Chroma 向量库入库
 |
 +-- /chat
 +-- /chat/stream
       |
       +-- Redis 读取 session_id 对应的历史上下文
       |
       v
   LangGraph Workflow
       |
       +-- Planner Agent
       +-- Router Agent
       |     |
       |     +-- calculator
       |     +-- web_search
       |     +-- rag_search -> Chroma Vector DB
       |
       +-- Summary Agent
       |
       v
   最终回复 / 流式回复
```

---

## 4. 核心功能

- 多 Agent 工作流：使用 LangGraph 编排 Planner、Router、Summary 三类 Agent 节点。
- 多工具调用：基于 LangChain Tool Calling 自动调用 `calculator`、`web_search`、`rag_search`。
- PDF 知识库：支持 PDF 上传、解析、切分、Embedding 和 Chroma 向量库入库。
- RAG 问答：支持基于已上传 PDF 文档的语义检索和问答。
- 多轮对话记忆：使用 Redis 保存会话历史，通过 `session_id` 管理上下文。
- 普通问答接口：提供 `/chat` 接口返回完整 AI 回复。
- 流式问答接口：提供 `/chat/stream` 接口逐段返回 AI 回复。
- 前端流式展示：前端通过 `ReadableStream` 读取后端流式响应，实现 AI 回复逐段显示。
- 前后端分离：后端提供 REST API，前端独立通过 Vite 本地启动。
- Docker Compose 部署：后端 API 和 Redis 使用 Docker Compose 一键启动。

---

## 5. 项目结构

```text
AI Multi-Agent Research Assistant
|-- app
|   |-- agents
|   |   |-- planner.py
|   |   |-- router.py
|   |   `-- summary_agent.py
|   |-- api
|   |   `-- routes.py
|   |-- data
|   |   `-- docs
|   |-- graph
|   |   |-- state.py
|   |   `-- workflow.py
|   |-- rag
|   |   |-- loader.py
|   |   |-- retriever.py
|   |   |-- splitter.py
|   |   `-- vectorstore.py
|   |-- scripts
|   |   `-- ingest.py
|   |-- services
|   |   |-- embedding.py
|   |   |-- llm.py
|   |   |-- memory.py
|   |   `-- redis_client.py
|   |-- tools
|   |   |-- calculator.py
|   |   |-- rag_search.py
|   |   `-- web_search.py
|   `-- main_api.py
|-- chroma_db
|-- frontend
|   |-- src
|   |   |-- api
|   |   |-- components
|   |   |-- types
|   |   |-- App.vue
|   |   `-- main.ts
|   |-- package.json
|   `-- vite.config.ts
|-- docker-compose.yml
|-- Dockerfile
|-- requirements.txt
`-- README.md
```

---

## 6. 环境变量配置

在项目根目录创建 `.env` 文件，配置后端运行所需变量：

```env
DEEPSEEK_API_KEY=your_deepseek_api_key
DASHSCOPE_API_KEY=your_dashscope_api_key
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
TAVILY_API_KEY=your_tavily_api_key

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
```

说明：

- `DEEPSEEK_API_KEY`：用于调用 DeepSeek Chat 模型。
- `DASHSCOPE_API_KEY`：用于调用 DashScope Embedding 模型。
- `DASHSCOPE_BASE_URL`：DashScope OpenAI 兼容接口地址。
- `TAVILY_API_KEY`：用于 `web_search` 联网搜索工具。
- `REDIS_HOST`：Docker Compose 内部使用 `redis` 作为 Redis 服务名。

---

## 7. 后端启动方式

后端 API 和 Redis 使用 Docker Compose 启动。

```bash
docker compose up -d --build
```

启动后访问：

- 后端 API 文档：http://127.0.0.1:8000/docs
- Redis：`localhost:6379`

常用命令：

```bash
docker compose ps
docker compose logs -f api
docker compose down
```

---

## 8. 前端启动方式

前端不使用 Docker，需要在本地通过 npm 启动。

```bash
cd frontend
npm install
npm run dev
```

启动后访问：

- 前端：http://localhost:5173
- 后端 API：http://127.0.0.1:8000/docs

---

## 9. API 接口说明

### 9.1 普通问答

```http
POST /chat
Content-Type: application/json
```

请求示例：

```json
{
  "query": "请总结一下刚才上传的 PDF 内容",
  "session_id": "demo-session"
}
```

响应示例：

```json
{
  "answer": "AI 返回的完整回答",
  "session_id": "demo-session"
}
```

说明：

- 后端会根据 `session_id` 从 Redis 读取历史上下文。
- Agent 会根据问题自动选择是否调用计算器、联网搜索或 RAG 检索工具。
- 回复完成后，用户问题和 AI 回复会写入 Redis。

### 9.2 流式问答

```http
POST /chat/stream
Content-Type: application/json
```

请求示例：

```json
{
  "query": "基于 PDF 给出三个核心结论",
  "session_id": "demo-session"
}
```

响应类型：

```text
text/plain
```

说明：

- 后端通过 `StreamingResponse` 返回文本流。
- 前端通过 `ReadableStream` 逐段读取内容，实现 AI 回复逐段显示。
- 当前实现会在后端生成最终回答后，再按字符向前端输出。

### 9.3 上传 PDF

```http
POST /upload
Content-Type: multipart/form-data
```

请求参数：

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| file | PDF 文件 | 待上传并入库的 PDF 文档 |

响应示例：

```json
{
  "message": "PDF 上传并入库完成",
  "file": "example.pdf",
  "chunks": 42
}
```

说明：

- 仅支持 PDF 文件。
- 上传后文件保存到 `app/data/docs`。
- 后端会自动解析 PDF、切分文本、生成 Embedding，并写入 Chroma 向量库。

---

## 10. 功能演示流程

1. 启动后端和 Redis：

```bash
docker compose up -d --build
```

2. 启动前端：

```bash
cd frontend
npm install
npm run dev
```

3. 打开前端页面：

```text
http://localhost:5173
```

4. 上传 PDF 文档，等待系统完成解析、切分、Embedding 和向量库入库。

5. 在聊天窗口提问：

```text
请总结这份 PDF 的主要内容
```

6. 继续追问：

```text
它的第二个结论有什么依据？
```

7. 测试工具调用：

```text
帮我计算 128 * 36，并解释结果
```

8. 测试联网搜索：

```text
搜索最新的 AI Agent 技术趋势，并总结三点
```

9. 在 Swagger 中调试接口：

```text
http://127.0.0.1:8000/docs
```

---

## 11. 项目亮点

- 使用 LangGraph 将 Agent 能力拆分为 Planner、Router、Summary，工作流结构清晰，便于扩展。
- 通过 LangChain Tool Calling 实现工具自动选择和调用，支持计算、联网检索和本地知识库检索。
- 实现完整 PDF RAG 链路，从上传、解析、切分、Embedding 到 Chroma 入库均由后端自动完成。
- 使用 Redis 按 `session_id` 管理多轮对话上下文，支持连续追问和跨轮语义理解。
- 提供普通响应和流式响应两种问答接口，前端通过 `ReadableStream` 实现 AI 回复逐段展示。
- 前后端分离，后端和 Redis 可通过 Docker Compose 一键启动，前端保持 Vite 本地开发体验。
- 项目结构按 Agent、Graph、RAG、Tools、Services、API 分层组织，工程边界清晰。

---

## 12. 后续优化方向

- 将 `/chat/stream` 改造为真正的 token 级流式输出，而不是最终答案生成后再逐段返回。
- 增加文件级 metadata 管理，支持按文档名、上传时间或用户会话隔离检索范围。
- 增加向量库 collection 管理，支持多知识库、多租户或多项目隔离。
- 增加用户认证和权限控制，保护上传文档和会话历史。
- 增加 Agent 执行过程可视化，展示计划、工具调用、检索结果和最终总结链路。
- 增加接口测试、RAG 召回测试和前端端到端测试。
- 增加异步任务队列，用于处理大文件上传、长文档解析和批量入库。
- 优化提示词和工具选择策略，降低误调用工具和漏调用 RAG 的概率。