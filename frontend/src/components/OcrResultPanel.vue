<template>
  <div class="result-panel">
    <div class="panel-header">
      <el-icon><List /></el-icon>
      识别结果
      <el-tag v-if="fields.length" size="small" type="info" style="margin-left:auto">
        {{ fields.length }} 项
      </el-tag>
    </div>
    <div v-if="!fields.length" class="empty-hint">
      <el-icon><InfoFilled /></el-icon> 运行识别后显示结果
    </div>
    <div v-else class="field-list scrollable">
      <div
        v-for="field in fields"
        :key="field.id"
        class="field-item"
        :class="{ hovered: hoveredId === field.id, selected: selectedIds.has(field.id) }"
        @mouseenter="$emit('hover', field.id)"
        @mouseleave="$emit('hover', null)"
        @click="$emit('select', field.id)"
        draggable="true"
        @dragstart="onDragStart($event, field)"
      >
        <div class="field-text" :title="field.text">{{ field.text }}</div>
        <span :class="['badge-conf', confClass(field.confidence)]">
          {{ (field.confidence * 100).toFixed(0) }}%
        </span>
        <el-icon class="drag-handle"><Rank /></el-icon>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { OCRField } from '../api/client'

const props = defineProps<{
  fields: OCRField[]
  hoveredId: string | null
  selectedIds: Set<string>
}>()
const emit = defineEmits<{
  hover: [id: string | null]
  select: [id: string]
}>()

function confClass(conf: number) {
  if (conf >= 0.9) return 'badge-high'
  if (conf >= 0.7) return 'badge-mid'
  return 'badge-low'
}

function onDragStart(e: DragEvent, field: OCRField) {
  e.dataTransfer!.effectAllowed = 'copy'
  // Use text/plain for maximum browser compatibility
  e.dataTransfer!.setData('text/plain', JSON.stringify({
    id: field.id,
    text: field.text,
    confidence: field.confidence,
    bbox: field.bbox,
  }))
}
</script>

<style scoped>
.result-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.empty-hint {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 20px 16px;
  font-size: 13px;
  color: var(--text-secondary);
}

.field-list {
  flex: 1;
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.field-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 7px 10px;
  border-radius: 6px;
  border: 1px solid transparent;
  cursor: grab;
  transition: all 0.15s;
  background: var(--bg);
}

.field-item:hover,
.field-item.hovered {
  background: var(--primary-light);
  border-color: var(--primary);
}

.field-item.selected {
  background: #F0FFF4;
  border-color: var(--success);
}

.field-text {
  flex: 1;
  font-size: 13px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.drag-handle {
  color: var(--text-secondary);
  opacity: 0.4;
}

.field-item:hover .drag-handle { opacity: 1; }
</style>
