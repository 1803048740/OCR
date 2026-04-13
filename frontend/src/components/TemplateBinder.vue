<template>
  <div class="binder-panel">
    <div class="panel-header">
      <el-icon><Connection /></el-icon>
      字段映射
      <el-tooltip content="从左侧拖拽识别结果到此处的列名进行绑定" placement="top">
        <el-icon style="margin-left:auto;color:var(--text-secondary)"><QuestionFilled /></el-icon>
      </el-tooltip>
    </div>
    <div class="binder-body scrollable">
      <!-- Column list -->
      <div v-if="!columns.length" class="empty-hint">
        <el-icon><InfoFilled /></el-icon> 请先添加 Excel 列名
      </div>
      <div v-for="col in columns" :key="col" class="col-row">
        <div class="col-name">
          <el-icon><Grid /></el-icon>
          {{ col }}
        </div>
        <div
          class="drop-target"
          :class="{
            'drag-over': dragOverCol === col,
            'has-value': !!mappings[col],
          }"
          @dragover.prevent="dragOverCol = col"
          @dragleave="dragOverCol = null"
          @drop.prevent="onDrop($event, col)"
        >
          <template v-if="mappings[col]">
            <span class="mapped-text">{{ mappings[col].text }}</span>
            <el-icon class="clear-btn" @click.stop="$emit('unbind', col)"><Close /></el-icon>
          </template>
          <template v-else>
            <el-icon><Plus /></el-icon>
            <span>拖入字段</span>
          </template>
        </div>
        <el-icon class="del-col" @click="$emit('removeColumn', col)"><Delete /></el-icon>
      </div>

      <!-- Add column input -->
      <div class="add-col-row">
        <el-input
          v-model="newColName"
          placeholder="新列名，如：发票金额"
          size="small"
          @keyup.enter="addCol"
          clearable
        />
        <el-button size="small" type="primary" @click="addCol">添加</el-button>
      </div>
    </div>

    <!-- Save template -->
    <div class="binder-footer">
      <el-button type="primary" size="small" :icon="'FolderChecked'" @click="showSave = true">
        保存为模板
      </el-button>
      <el-button size="small" @click="$emit('loadTemplate')">
        <el-icon><FolderOpened /></el-icon> 加载模板
      </el-button>
    </div>

    <!-- Save dialog -->
    <el-dialog v-model="showSave" title="保存模板" width="400px">
      <el-form label-width="70px">
        <el-form-item label="模板名称">
          <el-input v-model="saveName" placeholder="如：增值税发票" />
        </el-form-item>
        <el-form-item label="说明">
          <el-input v-model="saveDesc" type="textarea" :rows="2" placeholder="可选" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showSave = false">取消</el-button>
        <el-button type="primary" @click="doSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  columns: string[]
  mappings: Record<string, { text: string; fieldId: string; bbox: { points: number[][] } }>
}>()

const emit = defineEmits<{
  bind: [column: string, data: { id: string; text: string; confidence: number; bbox: { points: number[][] } }]
  unbind: [column: string]
  addColumn: [name: string]
  removeColumn: [name: string]
  save: [name: string, desc: string]
  loadTemplate: []
}>()

const dragOverCol = ref<string | null>(null)
const newColName = ref('')
const showSave = ref(false)
const saveName = ref('')
const saveDesc = ref('')

function onDrop(e: DragEvent, col: string) {
  dragOverCol.value = null
  const raw = e.dataTransfer?.getData('application/json')
  if (!raw) return
  try {
    const data = JSON.parse(raw)
    emit('bind', col, data)
  } catch {}
}

function addCol() {
  if (newColName.value.trim()) {
    emit('addColumn', newColName.value.trim())
    newColName.value = ''
  }
}

function doSave() {
  if (!saveName.value.trim()) return
  emit('save', saveName.value.trim(), saveDesc.value.trim())
  showSave.value = false
  saveName.value = ''
  saveDesc.value = ''
}
</script>

<style scoped>
.binder-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.binder-body {
  flex: 1;
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.col-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.col-name {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--text-secondary);
  width: 80px;
  flex-shrink: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.drop-target {
  flex: 1;
  min-height: 34px;
  border: 2px dashed var(--border);
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 8px;
  font-size: 12px;
  color: var(--text-secondary);
  transition: all 0.15s;
}

.drop-target.drag-over {
  border-color: var(--primary);
  background: var(--primary-light);
  color: var(--primary);
}

.drop-target.has-value {
  border-style: solid;
  border-color: var(--success);
  background: #F0FFF4;
  color: var(--success);
  font-weight: 600;
  font-size: 13px;
}

.mapped-text {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.clear-btn {
  cursor: pointer;
  color: var(--danger);
  flex-shrink: 0;
}

.del-col {
  color: var(--text-secondary);
  cursor: pointer;
  flex-shrink: 0;
  font-size: 14px;
}
.del-col:hover { color: var(--danger); }

.add-col-row {
  display: flex;
  gap: 6px;
  margin-top: 4px;
}

.binder-footer {
  padding: 10px 12px;
  border-top: 1px solid var(--border);
  display: flex;
  gap: 8px;
}

.empty-hint {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 12px 4px;
  font-size: 12px;
  color: var(--text-secondary);
}
</style>
