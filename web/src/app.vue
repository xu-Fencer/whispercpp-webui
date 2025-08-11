<template>
  <div class="app">
    <header class="app-bar">
      <div class="app-bar-title">Whisper Web UI</div>
      <nav class="app-bar-nav">
        <router-link to="/">任务</router-link>
        <router-link to="/preview">预览</router-link>
        <router-link to="/settings">设置</router-link>
      </nav>
    </header>

    <main class="app-main">
      <router-view />
    </main>
  </div>
</template>

<script setup>
</script>

<style scoped>
.app-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
}
.app-bar-title {
  font-weight: 600;
  font-size: 18px;
}
.app-bar-nav a {
  color: var(--md-sys-color-on-primary);
  text-decoration: none;
  margin-left: 16px;
}
.app-main {
  padding: 16px;
}
</style>
