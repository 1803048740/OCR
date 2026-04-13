<template>
  <div class="app-layout">
    <header class="app-header">
      <div class="header-brand">
        <span class="brand-icon">🧾</span>
        <span class="brand-name">OCR 票据识别系统</span>
      </div>
      <nav class="header-nav">
        <router-link to="/recognition" class="nav-item">
          <el-icon><Document /></el-icon> 识别工作台
        </router-link>
        <router-link to="/templates" class="nav-item">
          <el-icon><Files /></el-icon> 模板管理
        </router-link>
        <router-link to="/batch" class="nav-item">
          <el-icon><Grid /></el-icon> 批量处理
        </router-link>
      </nav>
      <div class="header-right">
        <el-tag type="success" size="small">API 已启动</el-tag>
        <a href="/api/docs" target="_blank" class="api-link">
          <el-icon><Link /></el-icon> API 文档
        </a>
      </div>
    </header>
    <main class="app-main">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<style scoped>
.app-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-header {
  height: 56px;
  background: #fff;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  padding: 0 24px;
  gap: 24px;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}

.header-brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 700;
  color: var(--primary);
  white-space: nowrap;
}

.brand-icon { font-size: 22px; }

.header-nav {
  display: flex;
  gap: 4px;
  flex: 1;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border-radius: 6px;
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 14px;
  transition: all 0.15s;
}

.nav-item:hover { background: var(--bg); color: var(--primary); }
.nav-item.router-link-active {
  background: var(--primary-light);
  color: var(--primary);
  font-weight: 600;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.api-link {
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 13px;
}

.api-link:hover { color: var(--primary); }

.app-main {
  flex: 1;
  overflow: hidden;
}
</style>
