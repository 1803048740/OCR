<template>
  <div class="recog-layout">
    <!-- Toolbar -->
    <div class="toolbar card">
      <ImageUploader style="flex:1;min-width:200px;max-width:280px;" @file="onFile" />
      <div class="toolbar-actions">
        <EngineSelector v-model="ocrStore.engine" />
        <el-button
          type="primary"
          :loading="ocrStore.loading"
          :disabled="!ocrStore.imageId"
          @click="doRecognize"
        >
          <el-icon><Aim /></el-icon>
          开始识别
        </el-button>
        <el-tag v-if="ocrStore.result" type="success" size="small">
          识别完成 · {{ ocrStore.result.fields.length }} 项
        </el-tag>
      </div>
    </div>

    <!-- 3-panel workspace -->
    <div class="workspace">
      <!-- Image panel -->
      <div class="panel panel-image card">
        <div class="panel-header">
          <el-icon><Picture /></el-icon> 图片预览
        </div>
        <div class="panel-body">
          <ImageViewer
            :imageUrl="ocrStore.imageUrl"
            :fields="ocrStore.result?.fields ?? []"
            :hovered-id="ocrStore.hoveredFieldId"
            :selected-ids="ocrStore.selectedFieldIds"
            @hover="ocrStore.hoverField"
            @select="ocrStore.toggleSelect"
          />
        </div>
      </div>

      <!-- OCR result panel -->
      <div class="panel panel-result card">
        <OcrResultPanel
          :fields="ocrStore.result?.fields ?? []"
          :hovered-id="ocrStore.hoveredFieldId"
          :selected-ids="ocrStore.selectedFieldIds"
          @hover="ocrStore.hoverField"
          @select="ocrStore.toggleSelect"
        />
      </div>

      <!-- Template binding panel -->
      <div class="panel panel-bind card">
        <TemplateBinder
          :columns="templateStore.excelColumns"
          :mappings="templateStore.pendingMappings"
          @bind="onBind"
          @unbind="templateStore.unbindField"
          @add-column="templateStore.addColumn"
          @remove-column="templateStore.removeColumn"
          @save="onSaveTemplate"
          @load-template="showTmplManager = true"
        />
      </div>
    </div>

    <TemplateManager
      v-model:visible="showTmplManager"
      @apply="onApplyTemplate"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useOcrStore } from '../stores/ocr'
import { useTemplateStore } from '../stores/template'
import { uploadImage, recognize, getImageUrl } from '../api/client'
import ImageUploader from '../components/ImageUploader.vue'
import ImageViewer from '../components/ImageViewer.vue'
import OcrResultPanel from '../components/OcrResultPanel.vue'
import TemplateBinder from '../components/TemplateBinder.vue'
import EngineSelector from '../components/EngineSelector.vue'
import TemplateManager from '../components/TemplateManager.vue'

const ocrStore = useOcrStore()
const templateStore = useTemplateStore()
const showTmplManager = ref(false)

async function onFile(file: File) {
  try {
    const res = await uploadImage(file)
    const id = res.data.image_id
    ocrStore.setImage(id, file, getImageUrl(id))
    ElMessage.success('图片上传成功')
  } catch {
    ElMessage.error('上传失败')
  }
}

async function doRecognize() {
  if (!ocrStore.imageId) return
  ocrStore.loading = true
  try {
    const res = await recognize(ocrStore.imageId, ocrStore.engine)
    ocrStore.setResult(res.data)
    ElMessage.success(`识别完成，共 ${res.data.fields.length} 项`)
  } catch (e: any) {
    ElMessage.error(`识别失败: ${e.response?.data?.detail ?? e.message}`)
  } finally {
    ocrStore.loading = false
  }
}

function onBind(column: string, data: { id: string; text: string; bbox: { points: number[][] } }) {
  templateStore.bindField(column, data.text, data.id, data.bbox)
}

async function onSaveTemplate(name: string, desc: string) {
  try {
    await templateStore.saveTemplate(name, desc, ocrStore.imageId)
    ElMessage.success(`模板「${name}」保存成功`)
  } catch {
    ElMessage.error('保存失败')
  }
}

async function onApplyTemplate(id: string) {
  try {
    const t = await templateStore.loadTemplate(id)
    ElMessage.success(`已加载模板「${t.name}」`)
  } catch {
    ElMessage.error('加载失败')
  }
}
</script>

<style scoped>
.recog-layout {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 56px);
  padding: 14px;
  gap: 12px;
  overflow: hidden;
}

.toolbar {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 16px;
  flex-shrink: 0;
}

.toolbar-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.workspace {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 220px 240px;
  gap: 12px;
  min-height: 0;
}

.panel {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.panel-body {
  flex: 1;
  overflow: hidden;
}
</style>
