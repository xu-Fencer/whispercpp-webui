import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './app.vue';
import { createRouter, createWebHistory } from 'vue-router';

// 路由设置
import TasksPage from './pages/TasksPage.vue';
import PreviewPage from './pages/PreviewPage.vue';
import SettingsPage from './pages/SettingsPage.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: TasksPage },
    { path: '/preview', component: PreviewPage },
    { path: '/settings', component: SettingsPage },
  ],
});

const app = createApp(App);
app.use(createPinia());
app.use(router);
app.mount('#app');
