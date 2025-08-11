import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './app.vue';
import router from './router/index';

// 引入 Material 3 主题与全局样式
import './material/theme.css';
import './styles/global.css';

// 引入 @material/web 组件（按需）
import '@material/web/button/filled-button.js';
import '@material/web/button/filled-tonal-button.js';
import '@material/web/textfield/outlined-text-field.js';
import '@material/web/select/outlined-select.js';
import '@material/web/select/select-option.js';
import '@material/web/checkbox/checkbox.js';
import '@material/web/switch/switch.js';
import '@material/web/progress/linear-progress.js';
import '@material/web/iconbutton/icon-button.js';

const app = createApp(App);
app.use(createPinia());
app.use(router);
app.mount('#app');
