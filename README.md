# OCR 票据识别系统

基于 PaddleOCR 和 Qwen3-VL 的票据识别系统，支持字段拖拽绑定模板、批量导出 Excel，并提供完整的 REST API。

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green)
![Vue](https://img.shields.io/badge/Vue-3.4+-brightgreen)

---

## 功能特性

- **双OCR引擎**：PaddleOCR（本地高精度）和 Qwen3-VL:4b（多模态大模型，via Ollama）
- **可视化识别**：识别结果以 bbox 叠加在图片上，悬停字段双向高亮
- **拖拽模板绑定**：将识别到的字段拖拽到 Excel 列名完成绑定，保存为模板
- **批量导出**：加载模板对多张同类票据批量识别，一键导出 Excel
- **REST API**：所有功能均通过 API 暴露，可与其他系统集成
- **现代 UI**：Vue 3 + Element Plus，三栏式工作台，操作高效

---

## 截图

```
+------------------------------------------------------------------+
| 🧾 OCR 票据识别系统    [PaddleOCR] [Qwen3-VL]      [模板管理]    |
+------------------------------------------------------------------+
|  图片预览（bbox叠加）  |  识别结果（可拖拽）  |  字段映射（拖入）  |
|                        |                       |                  |
|  [ticket image]        |  "沃尔玛"  98%  🔲   |  商户名称 [绑定] |
|  ┌──────────┐         |  "¥128.50" 97%  🔲   |  金额     [绑定] |
|  │ bbox overlay│       |  "2024-03-15" 94% 🔲 |  日期     [绑定] |
|  └──────────┘         |                       |  [保存模板]      |
+------------------------------------------------------------------+
```

---

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+（仅开发时需要）
- [Ollama](https://ollama.com)（使用 Qwen3-VL 时需要）

### 1. 安装依赖

```bash
# 安装 Python 依赖
pip install fastapi "uvicorn[standard]" httpx openpyxl Pillow python-multipart pydantic aiofiles

# 安装 PaddleOCR
pip install paddleocr
```

或直接运行：

```bash
install.bat       # Windows
# 或
pip install -r requirements.txt
```

### 2. 启动 Qwen3-VL（可选）

```bash
# 安装 Ollama：https://ollama.com
ollama pull qwen3-vl:4b
ollama serve
```

### 3. 启动应用

```bash
python main.py
# 或
start.bat
```

浏览器自动打开 `http://localhost:8000`

---

## 项目结构

```
OCR/
├── main.py                    # 启动入口
├── requirements.txt
├── backend/
│   ├── app.py                 # FastAPI 应用
│   ├── config.py              # 配置（Ollama地址、存储路径等）
│   ├── engines/
│   │   ├── paddle_engine.py   # PaddleOCR 引擎
│   │   └── qwen_engine.py     # Qwen3-VL 引擎（Ollama）
│   ├── models/                # Pydantic 数据模型
│   ├── services/
│   │   ├── template_service.py  # 模板管理 + 空间匹配算法
│   │   └── export_service.py    # Excel 生成
│   └── api/                   # REST 接口路由
├── frontend/
│   └── src/
│       ├── views/             # 识别工作台 / 模板管理 / 批量处理
│       └── components/        # ImageViewer / TemplateBinder 等
└── data/
    ├── templates/             # 模板 JSON 文件
    └── uploads/               # 上传图片
```

---

## API 文档

启动后访问 `http://localhost:8000/api/docs` 查看完整 Swagger 文档。

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/ocr/engines` | 查询引擎可用状态 |
| POST | `/api/ocr/recognize` | 识别图片（返回字段+bbox） |
| POST | `/api/images/upload` | 上传图片 |
| GET | `/api/images/{id}` | 获取图片 |
| GET | `/api/templates` | 列出所有模板 |
| POST | `/api/templates` | 创建模板 |
| PUT | `/api/templates/{id}` | 更新模板 |
| DELETE | `/api/templates/{id}` | 删除模板 |
| POST | `/api/export/excel` | 单张图片导出 Excel |
| POST | `/api/export/batch` | 批量导出 Excel |
| POST | `/api/export/preview` | 预览导出结果（JSON） |

### 示例：调用识别接口

```bash
# 上传图片
curl -X POST http://localhost:8000/api/images/upload \
  -F "file=@receipt.jpg"
# 返回: {"image_id": "abc123", "filename": "receipt.jpg"}

# 识别
curl -X POST http://localhost:8000/api/ocr/recognize \
  -H "Content-Type: application/json" \
  -d '{"image_id": "abc123", "engine": "paddleocr"}'
```

---

## 使用流程

### 单张识别

1. 在**识别工作台**上传图片
2. 选择引擎（PaddleOCR / Qwen3-VL），点击**开始识别**
3. 图片上显示 bbox 框，右侧显示识别字段列表

### 模板绑定与导出

1. 识别完成后，在右侧**字段映射**面板添加 Excel 列名
2. 从识别结果列表拖拽字段到对应列名的拖放区域
3. 点击**保存为模板**

### 批量处理

1. 进入**批量处理**页面，选择已保存的模板
2. 上传多张同类票据
3. 点击**开始识别并导出 Excel**

---

## 技术架构

- **后端**：FastAPI + Pydantic v2 + uvicorn
- **OCR**：PaddleOCR (`paddleocr` ≥ 2.7) / Qwen3-VL via Ollama HTTP API
- **Excel**：openpyxl，置信度低于 80% 自动标黄
- **前端**：Vue 3 + TypeScript + Vite + Element Plus + Pinia
- **拖拽**：HTML5 原生 Drag and Drop API
- **模板存储**：本地 JSON 文件（`data/templates/`）
- **坐标系**：所有引擎输出统一归一化到 0.0–1.0，与图片尺寸无关

---

## 开发

```bash
# 后端开发模式（热重载）
uvicorn backend.app:app --reload --port 8000

# 前端开发模式
cd frontend && npm run dev
```

前端开发服务器运行在 `http://localhost:5173`，API 请求自动代理到后端 8000 端口。

---

## License

MIT
