import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { OCRResult, OCRField } from '../api/client'

export const useOcrStore = defineStore('ocr', () => {
  const imageId = ref<string>('')
  const imageFile = ref<File | null>(null)
  const imageUrl = ref<string>('')
  const imageW = ref(0)
  const imageH = ref(0)
  const engine = ref<string>('paddleocr')
  const result = ref<OCRResult | null>(null)
  const loading = ref(false)
  const hoveredFieldId = ref<string | null>(null)
  const selectedFieldIds = ref<Set<string>>(new Set())

  function setImage(id: string, file: File, url: string) {
    imageId.value = id
    imageFile.value = file
    imageUrl.value = url
    result.value = null
    selectedFieldIds.value = new Set()
  }

  function setResult(r: OCRResult) {
    result.value = r
    imageW.value = r.image_width
    imageH.value = r.image_height
  }

  function hoverField(id: string | null) {
    hoveredFieldId.value = id
  }

  function toggleSelect(id: string) {
    if (selectedFieldIds.value.has(id)) {
      selectedFieldIds.value.delete(id)
    } else {
      selectedFieldIds.value.add(id)
    }
  }

  return {
    imageId, imageFile, imageUrl, imageW, imageH,
    engine, result, loading, hoveredFieldId, selectedFieldIds,
    setImage, setResult, hoverField, toggleSelect,
  }
})
