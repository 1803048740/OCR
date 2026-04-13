<template>
  <div class="batch-view">
    <div class="page-header">
      <h2>批量处理</h2>
      <p class="sub">上传多张同类票据，使用模板批量识别并导出 Excel</p>
    </div>

    <div class="batch-layout">
      <!-- Step 1: Select template -->
      <div class="step-card card">
        <div class="step-title"><span class="step-num">1</span> 选择模板</div>
        <div v-if="!selectedTemplate" class="no-template">
          <el-button type="primary" @click="showTmplMgr = true">
            <el-icon><Files /></el-icon> 选择模板
          </el-button>
        </div>
        <div v-else class="tmpl-selected">
          <div class="tmpl-name">{{ selectedTemplate.name }}</div>
          <div class="tmpl-meta">{{ selectedTemplate.field_count }} 个字段</div>
          <el-button size="small" text @click="showTmplMgr = true">更换</el-button>
        </div>
      </div>

      <!-- Step 2: Upload images -->
      <div class="step-card card">
        <div class="step-title"><span class="step-num">2</span> 上传票据</div>
        <div
          class="batch-drop"
          :class="{ dragging: dropDragging }"
          @dragover.prevent="dropDragging = true"
          @dragleave="dropDragging = false"
          @drop.prevent="onBatchDrop"
          @click="batchInputRef?.click()"
        >
          <input ref="batchInputRef" type="file" accept="image/*" multiple style="display:none" @change="onBatchPick" />
          <el-icon size="28" :color="dropDragging ? 'var(--primary)' : '#C0C4CC'"><UploadFilled /></el-icon>
          <p>拖拽多张图片或点击上传</p>
        </div>
        <!-- File list -->
        <div v-if="imageItems.length" class="file-list scrollable">
          <div v-for="item in imageItems" :key="item.file.name" class="file-item">
            <el-icon class="file-icon"><Picture /></el-icon>
            <span class="file-name">{{ item.file.name }}</span>
            <el-icon v-if="item.status === 'done'" color="var(--success)"><CircleCheck /></el-icon>
            <el-icon v-else-if="item.status === 'error'" color="var(--danger)"><CircleClose /></el-icon>
            <el-icon v-else-if="item.status === 'uploading'" class="spinning"><Loading /></el-icon>
            <el-icon v-else color="#C0C4CC"><Clock /></el-icon>
            <el-icon class="remove-btn" @click="removeItem(item)"><Close /></el-icon>
          </div>
        </div>
      </div>

      <!-- Step 3: Process & Export -->
      <div class="step-card card">
        <div class="step-title"><span class="step-num">3</span> 识别与导出</div>
        <div class="engine-row">
          <span style="font-size:13px;color:var(--text-secondary)">引擎：</span>
          <el-select v-model="batchEngine" size="small" style="width:140px">
            <el-option label="PaddleOCR" value="paddleocr" />
            <el-option label="Qwen3-VL" value="qwen3vl" />
          </el-select>
        </div>
        <el-button
          type="primary"
          :loading="processing"
          :disabled="!selectedTemplate || !imageItems.length"
          @click="startBatch"
          style="width:100%"
        >
          <el-icon><Download /></el-icon>
          开始识别并导出 Excel
        </el-button>
        <div v-if="progress" class="progress-wrap">
          <el-progress :percentage="progress.pct" :status="progress.status" />
          <p class="progress-text">{{ progress.text }}</p>
        </div>

        <!-- Preview table -->
        <div v-if="previewData" class="preview-wrap">
          <div style="font-weight:600;margin-bottom:8px;font-size:13px">预览</div>
          <el-table :data="previewRows" size="small" border max-height="260">
            <el-table-column label="图片" width="90">
              <template #default="{ row }">
                <span class="img-id">{{ row.image_id.slice(0, 8) }}</span>
              </template>
            </el-table-column>
            <el-table-column
              v-for="col in previewData.columns"
              :key="col"
              :label="col"
              :prop="`columns.${col}`"
            >
              <template #default="{ row }">
                {{ row.columns[col] || '-' }}
              </template>
            </el-table-column>
          </el-table>
          <el-button
            type="success"
            size="small"
            style="margin-top:10px"
            @click="exportNow"
          >
            <el-icon><Download /></el-icon> 下载 Excel
          </el-button>
        </div>
      </div>
    </div>

    <TemplateManager v-model:visible="showTmplMgr" @apply="onApplyTemplate" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { uploadImage, previewExport, downloadExport, getTemplate } from '../api/client'
import type { TemplateSummary } from '../api/client'
import { useTemplateStore } from '../stores/template'
import TemplateManager from '../components/TemplateManager.vue'

const route = useRoute()
const templateStore = useTemplateStore()

interface ImageItem {
  file: File
  imageId?: string
  status: 'pending' | 'uploading' | 'done' | 'error'
}

const imageItems = ref<ImageItem[]>([])
const dropDragging = ref(false)
const batchInputRef = ref<HTMLInputElement>()
const showTmplMgr = ref(false)
const selectedTemplate = ref<TemplateSummary | null>(null)
const batchEngine = ref('paddleocr')
const processing = ref(false)
const progress = ref<{ pct: number; text: string; status?: 'success' | 'exception' } | null>(null)
const previewData = ref<{ columns: string[]; rows: any[] } | null>(null)

const previewRows = computed(() => previewData.value?.rows ?? [])

onMounted(async () => {
  const tid = route.query.template as string
  if (tid) {
    try {
      const res = await getTemplate(tid)
      selectedTemplate.value = {
        id: res.data.id,
        name: res.data.name,
        description: res.data.description,
        created_at: res.data.created_at,
        updated_at: res.data.updated_at,
        field_count: res.data.field_mappings.length,
      }
    } catch {}
  }
})

function addFiles(files: FileList | File[]) {
  for (const f of Array.from(files)) {
    if (!imageItems.value.find(i => i.file.name === f.name)) {
      imageItems.value.push({ file: f, status: 'pending' })
    }
  }
}

function onBatchDrop(e: DragEvent) {
  dropDragging.value = false
  if (e.dataTransfer?.files) addFiles(e.dataTransfer.files)
}

function onBatchPick(e: Event) {
  const files = (e.target as HTMLInputElement).files
  if (files) addFiles(files)
}

function removeItem(item: ImageItem) {
  imageItems.value = imageItems.value.filter(i => i !== item)
}

async function onApplyTemplate(id: string) {
  const res = await getTemplate(id)
  selectedTemplate.value = {
    id: res.data.id,
    name: res.data.name,
    description: res.data.description,
    created_at: res.data.created_at,
    updated_at: res.data.updated_at,
    field_count: res.data.field_mappings.length,
  }
}

async function startBatch() {
  if (!selectedTemplate.value) return
  processing.value = true
  previewData.value = null
  progress.value = { pct: 0, text: '上传图片中...' }

  const total = imageItems.value.length
  const imageIds: string[] = []

  // Upload all
  for (let i = 0; i < imageItems.value.length; i++) {
    const item = imageItems.value[i]
    item.status = 'uploading'
    try {
      const res = await uploadImage(item.file)
      item.imageId = res.data.image_id
      imageIds.push(res.data.image_id)
      item.status = 'done'
    } catch {
      item.status = 'error'
    }
    progress.value = { pct: Math.round(((i + 1) / total) * 50), text: `上传 ${i + 1}/${total}` }
  }

  // Preview export (OCR + matching)
  progress.value = { pct: 60, text: '正在识别...' }
  try {
    const res = await previewExport(imageIds, selectedTemplate.value.id)
    previewData.value = res.data
    progress.value = { pct: 100, text: '识别完成', status: 'success' }
    ElMessage.success('识别完成，可预览或下载 Excel')
  } catch (e: any) {
    progress.value = { pct: 100, text: '识别失败', status: 'exception' }
    ElMessage.error(`识别失败: ${e.response?.data?.detail ?? e.message}`)
  } finally {
    processing.value = false
  }
}

async function exportNow() {
  if (!selectedTemplate.value || !imageItems.value.length) return
  const imageIds = imageItems.value.filter(i => i.imageId).map(i => i.imageId!)
  await downloadExport(imageIds, selectedTemplate.value.id)
}
</script>

<style scoped>
.batch-view {
  padding: 24px;
  max-width: 1100px;
  margin: 0 auto;
}

.page-header { margin-bottom: 20px; }
.page-header h2 { font-size: 22px; font-weight: 700; }
.page-header .sub { font-size: 14px; color: var(--text-secondary); margin-top: 4px; }

.batch-layout {
  display: grid;
  grid-template-columns: 240px 1fr 1fr;
  gap: 16px;
  align-items: start;
}

.step-card {
  padding: 18px;
}

.step-title {
  font-weight: 600;
  font-size: 15px;
  margin-bottom: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.step-num {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: var(--primary);
  color: #fff;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.no-template {
  display: flex;
  justify-content: center;
  padding: 20px 0;
}

.tmpl-selected {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.tmpl-name { font-weight: 600; font-size: 14px; }
.tmpl-meta { font-size: 12px; color: var(--text-secondary); }

.batch-drop {
  border: 2px dashed var(--border);
  border-radius: 8px;
  padding: 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.15s;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 12px;
}

.batch-drop:hover, .batch-drop.dragging {
  border-color: var(--primary);
  background: var(--primary-light);
  color: var(--primary);
}

.file-list {
  max-height: 180px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.file-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  padding: 4px 6px;
  border-radius: 4px;
  background: var(--bg);
}

.file-icon { color: var(--primary); flex-shrink: 0; }
.file-name { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.remove-btn { color: var(--text-secondary); cursor: pointer; flex-shrink: 0; }
.remove-btn:hover { color: var(--danger); }
.img-id { font-family: monospace; font-size: 11px; }

.engine-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.progress-wrap { margin-top: 14px; }
.progress-text { font-size: 12px; color: var(--text-secondary); margin-top: 4px; }

.preview-wrap { margin-top: 16px; }

@keyframes spin { to { transform: rotate(360deg); } }
.spinning { animation: spin 1s linear infinite; }
</style>
