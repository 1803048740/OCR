<template>
  <div class="viewer-wrap" ref="wrapRef">
    <div class="viewer-inner" :style="innerStyle">
      <img
        ref="imgRef"
        :src="imageUrl"
        class="viewer-img"
        @load="onImgLoad"
        draggable="false"
        alt="ticket"
      />
      <!-- SVG bbox overlay -->
      <svg
        v-if="imgLoaded"
        class="bbox-overlay"
        :viewBox="`0 0 ${dispW} ${dispH}`"
        :width="dispW"
        :height="dispH"
      >
        <g v-for="field in fields" :key="field.id">
          <polygon
            :points="toSvgPoints(field.bbox.points)"
            :class="['bbox-poly', {
              hovered: hoveredId === field.id,
              selected: selectedIds.has(field.id),
            }]"
            @mouseenter="$emit('hover', field.id)"
            @mouseleave="$emit('hover', null)"
            @click="$emit('select', field.id)"
          />
          <!-- Label on hover -->
          <text
            v-if="hoveredId === field.id || selectedIds.has(field.id)"
            :x="labelX(field.bbox.points)"
            :y="labelY(field.bbox.points) - 4"
            class="bbox-label"
          >{{ field.text }}</text>
        </g>
      </svg>
    </div>
    <div v-if="!imageUrl" class="viewer-empty">
      <el-icon size="48" color="#C0C4CC"><Picture /></el-icon>
      <p>请上传票据图片</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import type { OCRField } from '../api/client'

const props = defineProps<{
  imageUrl: string
  fields: OCRField[]
  hoveredId: string | null
  selectedIds: Set<string>
}>()
const emit = defineEmits<{
  hover: [id: string | null]
  select: [id: string]
}>()

const wrapRef = ref<HTMLElement>()
const imgRef = ref<HTMLImageElement>()
const imgLoaded = ref(false)
const dispW = ref(0)
const dispH = ref(0)

function onImgLoad() {
  imgLoaded.value = true
  dispW.value = imgRef.value!.offsetWidth
  dispH.value = imgRef.value!.offsetHeight
}

watch(() => props.imageUrl, () => { imgLoaded.value = false })

const innerStyle = computed(() => ({
  width: dispW.value ? `${dispW.value}px` : 'auto',
  height: dispH.value ? `${dispH.value}px` : 'auto',
}))

function toSvgPoints(pts: number[][]): string {
  return pts.map(([x, y]) => `${x * dispW.value},${y * dispH.value}`).join(' ')
}

function labelX(pts: number[][]): number {
  return Math.min(...pts.map(p => p[0])) * dispW.value
}

function labelY(pts: number[][]): number {
  return Math.min(...pts.map(p => p[1])) * dispH.value
}
</script>

<style scoped>
.viewer-wrap {
  width: 100%;
  height: 100%;
  overflow: auto;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  background: #f0f0f0;
  position: relative;
}

.viewer-inner {
  position: relative;
  display: inline-block;
}

.viewer-img {
  display: block;
  max-width: 100%;
  max-height: calc(100vh - 180px);
  object-fit: contain;
}

.bbox-overlay {
  position: absolute;
  top: 0;
  left: 0;
  pointer-events: none;
}

.bbox-overlay polygon { pointer-events: all; }

.bbox-poly {
  fill: rgba(43, 92, 230, 0.08);
  stroke: #2B5CE6;
  stroke-width: 1.5;
  cursor: pointer;
  transition: fill 0.1s;
}

.bbox-poly.hovered {
  fill: rgba(43, 92, 230, 0.22);
  stroke-width: 2;
}

.bbox-poly.selected {
  fill: rgba(24, 160, 88, 0.18);
  stroke: #18A058;
  stroke-width: 2;
}

.bbox-label {
  font-size: 11px;
  fill: #1a1a2e;
  background: #fff;
  paint-order: stroke;
  stroke: white;
  stroke-width: 3px;
  font-weight: 500;
  pointer-events: none;
}

.viewer-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: #C0C4CC;
  font-size: 14px;
  height: 100%;
  min-height: 300px;
}
</style>
