<template>
  <div class="engine-selector">
    <span class="label">识别引擎：</span>
    <el-radio-group v-model="selected" size="small" @change="$emit('update:modelValue', selected)">
      <el-radio-button
        v-for="e in engines"
        :key="e.name"
        :label="e.name"
        :disabled="!e.available"
      >
        <el-tooltip v-if="!e.available" :content="`${engineLabel(e.name)} 不可用`" placement="top">
          <span>{{ engineLabel(e.name) }}</span>
        </el-tooltip>
        <span v-else>{{ engineLabel(e.name) }}</span>
      </el-radio-button>
    </el-radio-group>
    <el-button
      size="small"
      :icon="'Refresh'"
      circle
      text
      @click="fetchEngines"
      :loading="loading"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getEngines } from '../api/client'

defineProps<{ modelValue: string }>()
const emit = defineEmits<{ 'update:modelValue': [v: string] }>()

const selected = defineModel<string>({ default: 'paddleocr' })
const engines = ref<{ name: string; available: boolean }[]>([])
const loading = ref(false)

function engineLabel(name: string) {
  return name === 'paddleocr' ? 'PaddleOCR' : 'Qwen3-VL'
}

async function fetchEngines() {
  loading.value = true
  try {
    const res = await getEngines()
    engines.value = res.data.engines
  } finally {
    loading.value = false
  }
}

onMounted(fetchEngines)
</script>

<style scoped>
.engine-selector {
  display: flex;
  align-items: center;
  gap: 8px;
}

.label {
  font-size: 13px;
  color: var(--text-secondary);
  white-space: nowrap;
}
</style>
