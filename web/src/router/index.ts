import { createRouter, createWebHistory } from 'vue-router';
import TasksPage from '../pages/TasksPage.vue';
import PreviewPage from '../pages/PreviewPage.vue';
import SettingsPage from '../pages/SettingsPage.vue';

const routes = [
  { path: '/', component: TasksPage },
  { path: '/preview', component: PreviewPage },
  { path: '/settings', component: SettingsPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
