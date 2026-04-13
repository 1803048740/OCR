<template>
  <el-dialog v-model="visible" title="选择模板" width="500px" @open="load">
    <div v-loading="loading" class="tmpl-list">
      <div v-if="!templates.length" class="empty">暂无模板</div>
      <div
        v-for="t in templates"
        :key="t.id"
        class="tmpl-item"
        :class="{ active: selected === t.id }"
        @click="selected = t.id"
      >
        <div class="tmpl-main">
          <div class="tmpl-name">{{ t.name }}</div>
          <div class="tmpl-meta">
            {{ t.field_count }} 个字段 &nbsp;·&nbsp;
            {{ new Date(t.updated_at).toLocaleDateString() }}
          </div>
          <div v-if="t.description" class="tmpl-desc">{{ t.description }}</div>
        </div>
        <el-button
          size="small"
          type="danger"
          text
          :icon="'Delete'"
          @click.stop="del(t.id)"
        />
      </div>
    </div>
    <template #footer>
      <el-button @click="visible = false">取消</el-button>
      <el-button type="primary" :disabled="!selected" @click="confirm">应用模板</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useTemplateStore } from '../stores/template'
import { ElMessage, ElMessageBox } from 'element-plus'

const visible = defineModel<boolean>('visible', { default: false })
const emit = defineEmits<{ apply: [id: string] }>()

const store = useTemplateStore()
const { templates } = store
const loading = ref(false)
const selected = ref('')

async function load() {
  loading.value = true
  await store.fetchTemplates()
  loading.value = false
}

async function del(id: string) {
  await ElMessageBox.confirm('确定删除此模板？', '删除', { type: 'warning' })
  await store.deleteTemplate(id)
  ElMessage.success('已删除')
}

function confirm() {
  if (selected.value) {
    emit('apply', selected.value)
    visible.value = false
  }
}
</script>

<style scoped>
.tmpl-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 360px;
  overflow-y: auto;
}

.empty {
  text-align: center;
  color: var(--text-secondary);
  padding: 30px;
  font-size: 14px;
}

.tmpl-item {
  border: 2px solid var(--border);
  border-radius: 8px;
  padding: 12px 14px;
  cursor: pointer;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  transition: all 0.15s;
}

.tmpl-item:hover { border-color: var(--primary); background: var(--primary-light); }
.tmpl-item.active { border-color: var(--primary); background: var(--primary-light); }

.tmpl-main { flex: 1; }
.tmpl-name { font-weight: 600; font-size: 14px; }
.tmpl-meta { font-size: 12px; color: var(--text-secondary); margin-top: 2px; }
.tmpl-desc { font-size: 12px; color: var(--text-secondary); margin-top: 4px; }
</style>
