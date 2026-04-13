import { createRouter, createWebHistory } from 'vue-router'
import RecognitionView from './views/RecognitionView.vue'
import TemplateView from './views/TemplateView.vue'
import BatchView from './views/BatchView.vue'

const routes = [
  { path: '/', redirect: '/recognition' },
  { path: '/recognition', component: RecognitionView, meta: { title: '识别工作台' } },
  { path: '/templates', component: TemplateView, meta: { title: '模板管理' } },
  { path: '/batch', component: BatchView, meta: { title: '批量处理' } },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
