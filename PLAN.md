# OCR票据识别应用 - 实现计划

## 架构
FastAPI后端 + Vue 3 Web前端，`python main.py` 一键启动。

## 分阶段实施

### 阶段1：后端骨架 + OCR引擎 ✅
- main.py, backend/app.py, backend/config.py
- backend/models/ (ocr_result, template, export)
- backend/engines/ (base, paddle_engine, qwen_engine)
- backend/api/ (ocr, images)

### 阶段2：前端核心 ✅
- Vue 3 + Vite + Element Plus + Pinia
- ImageUploader.vue — 图片拖放上传
- ImageViewer.vue — 图片 + SVG bbox叠加
- OcrResultPanel.vue + FieldChip.vue — 结果展示

### 阶段3：模板系统 ✅
- backend/services/template_service.py — 模板管理 + 空间匹配
- backend/api/templates.py
- TemplateBinder.vue — 拖拽绑定
- TemplateManager.vue

### 阶段4：导出与批量处理 ✅
- backend/services/export_service.py — Excel生成
- backend/api/export.py
- BatchProcessor.vue

### 阶段5：体验优化 ✅
- 加载状态、错误提示
- 置信度颜色编码
- 响应式布局

## 核心数据流
```
用户上传图片
  → POST /api/images/upload → 返回 image_id
  → POST /api/ocr/recognize (image_id + engine)
  → 返回 OCRResult { fields: [{id, text, confidence, bbox}] }
  → 前端SVG叠加显示bbox
  → 用户拖拽字段到Excel列 → 保存模板
  → 批量导出 POST /api/export/batch
```

## 关键技术点
- 所有引擎输出统一归一化坐标 0.0-1.0
- PaddleOCR: asyncio.to_thread (CPU密集)
- Qwen3-VL: httpx.AsyncClient (I/O密集，Ollama localhost:11434)
- 空间匹配：欧氏距离最近邻

## API清单
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/ocr/engines | 引擎状态 |
| POST | /api/ocr/recognize | 识别图片 |
| POST | /api/images/upload | 上传图片 |
| GET | /api/images/{id} | 获取图片 |
| GET | /api/templates | 列出模板 |
| POST | /api/templates | 创建模板 |
| PUT | /api/templates/{id} | 更新模板 |
| DELETE | /api/templates/{id} | 删除模板 |
| POST | /api/export/excel | 单张导出 |
| POST | /api/export/batch | 批量导出 |
