import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { TemplateSummary, Template, FieldMapping } from '../api/client'
import * as api from '../api/client'

export const useTemplateStore = defineStore('template', () => {
  const templates = ref<TemplateSummary[]>([])
  const current = ref<Template | null>(null)
  // pending mappings being built in UI: excel_column -> OCR field info
  const pendingMappings = ref<Record<string, { text: string; fieldId: string; bbox: { points: number[][] } }>>({})
  const excelColumns = ref<string[]>([])

  async function fetchTemplates() {
    const res = await api.listTemplates()
    templates.value = res.data.templates
  }

  async function loadTemplate(id: string) {
    const res = await api.getTemplate(id)
    current.value = res.data
    excelColumns.value = [...res.data.excel_columns]
    pendingMappings.value = {}
    return res.data
  }

  function addColumn(name: string) {
    if (name && !excelColumns.value.includes(name)) {
      excelColumns.value.push(name)
    }
  }

  function removeColumn(name: string) {
    excelColumns.value = excelColumns.value.filter(c => c !== name)
    delete pendingMappings.value[name]
  }

  function bindField(column: string, fieldText: string, fieldId: string, bbox: { points: number[][] }) {
    pendingMappings.value[column] = { text: fieldText, fieldId, bbox }
  }

  function unbindField(column: string) {
    delete pendingMappings.value[column]
  }

  function buildFieldMappings(): FieldMapping[] {
    return Object.entries(pendingMappings.value).map(([col, info]) => ({
      field_label: col,
      excel_column: col,
      bbox_anchor: info.bbox,
    }))
  }

  async function saveTemplate(name: string, description: string, referenceImageId: string) {
    const fms = buildFieldMappings()
    const res = await api.createTemplate({
      name,
      description,
      reference_image_id: referenceImageId,
      field_mappings: fms,
      excel_columns: excelColumns.value,
    })
    templates.value.unshift({
      id: res.data.id,
      name: res.data.name,
      description: res.data.description,
      created_at: res.data.created_at,
      updated_at: res.data.updated_at,
      field_count: res.data.field_mappings.length,
    })
    return res.data
  }

  async function deleteTemplate(id: string) {
    await api.deleteTemplate(id)
    templates.value = templates.value.filter(t => t.id !== id)
    if (current.value?.id === id) current.value = null
  }

  return {
    templates, current, pendingMappings, excelColumns,
    fetchTemplates, loadTemplate, addColumn, removeColumn,
    bindField, unbindField, buildFieldMappings, saveTemplate, deleteTemplate,
  }
})
