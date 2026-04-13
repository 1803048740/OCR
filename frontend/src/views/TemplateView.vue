<template>
  <div class="tmpl-view">
    <div class="page-header">
      <h2>模板管理</h2>
      <p class="sub">管理票据字段映射模板，用于批量导出</p>
    </div>

    <div v-loading="loading" class="tmpl-grid">
      <div v-if="!store.templates.length" class="empty-card card">
        <el-icon size="48" color="#C0C4CC"><Files /></el-icon>
        <p>暂无模板</p>
        <p class="sub">在「识别工作台」完成字段绑定后保存为模板</p>
        <el-button type="primary" @click="$router.push('/recognition')">前往工作台</el-button>
      </div>

      <div v-for="t in store.templates" :key="t.id" class="tmpl-card card">
        <div class="tmpl-card-header">
          <div class="tmpl-title">{{ t.name }}</div>
          <el-dropdown trigger="click">
            <el-icon class="more-btn"><MoreFilled /></el-icon>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="del(t.id)">
                  <el-icon><Delete /></el-icon> 删除
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
        <div class="tmpl-meta">
          <el-tag size="small">{{ t.field_count }} 个字段</el-tag>
          <span class="date">更新于 {{ new Date(t.updated_at).toLocaleDateString() }}</span>
        </div>
        <p v-if="t.description" class="tmpl-desc">{{ t.description }}</p>
        <div class="tmpl-actions">
          <el-button size="small" @click="viewDetail(t.id)">查看详情</el-button>
          <el-button size="small" type="primary" @click="useInBatch(t.id)">用于批量导出</el-button>
        </div>
      </div>
    </div>

    <!-- Detail dialog -->
    <el-dialog v-model="showDetail" title="模板详情" width="560px">
      <div v-if="detailTemplate">
        <el-descriptions :column="1" border size="small">
          <el-descriptions-item label="模板名称">{{ detailTemplate.name }}</el-descriptions-item>
          <el-descriptions-item label="说明">{{ detailTemplate.description || '-' }}</el-descriptions-item>
          <el-descriptions-item label="Excel列">{{ detailTemplate.excel_columns.join('、') }}</el-descriptions-item>
        </el-descriptions>
        <div style="margin-top:16px">
          <div style="font-weight:600;margin-bottom:8px;font-size:13px;">字段映射</div>
          <el-table :data="detailTemplate.field_mappings" size="small" border>
            <el-table-column prop="field_label" label="字段标签" />
            <el-table-column prop="excel_column" label="Excel列" />
          </el-table>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useTemplateStore } from '../stores/template'
import type { Template } from '../api/client'
import { getTemplate } from '../api/client'

const store = useTemplateStore()
const router = useRouter()
const loading = ref(false)
const showDetail = ref(false)
const detailTemplate = ref<Template | null>(null)

onMounted(async () => {
  loading.value = true
  await store.fetchTemplates()
  loading.value = false
})

async function del(id: string) {
  await ElMessageBox.confirm('确定删除此模板？', '删除', { type: 'warning' })
  await store.deleteTemplate(id)
  ElMessage.success('已删除')
}

async function viewDetail(id: string) {
  const res = await getTemplate(id)
  detailTemplate.value = res.data
  showDetail.value = true
}

function useInBatch(id: string) {
  router.push({ path: '/batch', query: { template: id } })
}
</script>

<style scoped>
.tmpl-view {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  font-size: 22px;
  font-weight: 700;
}

.page-header .sub {
  font-size: 14px;
  color: var(--text-secondary);
  margin-top: 4px;
}

.tmpl-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.empty-card {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 60px;
  color: var(--text-secondary);
  font-size: 14px;
}

.tmpl-card {
  padding: 18px;
}

.tmpl-card-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.tmpl-title {
  flex: 1;
  font-size: 15px;
  font-weight: 600;
}

.more-btn {
  cursor: pointer;
  color: var(--text-secondary);
  font-size: 18px;
}

.tmpl-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.date { font-size: 12px; color: var(--text-secondary); }
.tmpl-desc { font-size: 12px; color: var(--text-secondary); margin-bottom: 12px; }

.tmpl-actions { display: flex; gap: 8px; margin-top: 12px; }
</style>
