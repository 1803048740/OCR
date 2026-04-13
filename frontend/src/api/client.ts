import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

export interface OCRField {
  id: string
  text: string
  confidence: number
  bbox: { points: number[][] }
  label?: string
}

export interface OCRResult {
  image_id: string
  engine: string
  image_width: number
  image_height: number
  fields: OCRField[]
}

export interface FieldMapping {
  field_label: string
  excel_column: string
  bbox_anchor: { points: number[][] }
  regex_pattern?: string
}

export interface Template {
  id: string
  name: string
  description: string
  created_at: string
  updated_at: string
  reference_image_id: string
  field_mappings: FieldMapping[]
  excel_columns: string[]
}

export interface TemplateSummary {
  id: string
  name: string
  description: string
  created_at: string
  updated_at: string
  field_count: number
}

// Image
export const uploadImage = (file: File) => {
  const fd = new FormData()
  fd.append('file', file)
  return api.post<{ image_id: string; filename: string }>('/images/upload', fd)
}

export const getImageUrl = (imageId: string) => `/api/images/${imageId}`

// OCR
export const getEngines = () => api.get<{ engines: { name: string; available: boolean }[] }>('/ocr/engines')

export const recognize = (imageId: string, engine: string) =>
  api.post<OCRResult>('/ocr/recognize', { image_id: imageId, engine })

// Templates
export const listTemplates = () => api.get<{ templates: TemplateSummary[] }>('/templates')
export const getTemplate = (id: string) => api.get<Template>(`/templates/${id}`)
export const createTemplate = (data: Partial<Template>) => api.post<Template>('/templates', data)
export const updateTemplate = (id: string, data: Partial<Template>) => api.put<Template>(`/templates/${id}`, data)
export const deleteTemplate = (id: string) => api.delete(`/templates/${id}`)

// Export
export const previewExport = (imageIds: string[], templateId: string) =>
  api.post('/export/preview', { image_ids: imageIds, template_id: templateId })

export const downloadExport = async (imageIds: string[], templateId: string, filename = 'export.xlsx') => {
  const resp = await api.post('/export/batch', {
    image_ids: imageIds,
    template_id: templateId,
    output_filename: filename,
  }, { responseType: 'blob' })
  const url = URL.createObjectURL(resp.data)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
}

export default api
