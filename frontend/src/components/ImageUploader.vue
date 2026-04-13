<template>
  <div
    class="uploader"
    :class="{ dragging }"
    @dragover.prevent="dragging = true"
    @dragleave="dragging = false"
    @drop.prevent="onDrop"
    @click="inputRef?.click()"
  >
    <input ref="inputRef" type="file" accept="image/*" style="display:none" @change="onPick" />
    <el-icon size="32" :color="dragging ? 'var(--primary)' : '#C0C4CC'"><UploadFilled /></el-icon>
    <p class="hint">拖拽图片到此处，或 <span class="link">点击上传</span></p>
    <p class="sub">支持 JPG、PNG、BMP、WebP 等格式</p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{ file: [f: File] }>()
const dragging = ref(false)
const inputRef = ref<HTMLInputElement>()

function onDrop(e: DragEvent) {
  dragging.value = false
  const f = e.dataTransfer?.files[0]
  if (f && f.type.startsWith('image/')) emit('file', f)
}

function onPick(e: Event) {
  const f = (e.target as HTMLInputElement).files?.[0]
  if (f) emit('file', f)
}
</script>

<style scoped>
.uploader {
  border: 2px dashed var(--border);
  border-radius: 10px;
  padding: 32px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  background: var(--surface);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.uploader:hover, .uploader.dragging {
  border-color: var(--primary);
  background: var(--primary-light);
}

.hint { font-size: 14px; color: var(--text); }
.link { color: var(--primary); font-weight: 600; }
.sub  { font-size: 12px; color: var(--text-secondary); }
</style>
