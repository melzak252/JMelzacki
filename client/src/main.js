import { createApp } from 'vue'
import './style.scss'
import App from './App.vue'
import router from './router';
import {createBootstrap} from 'bootstrap-vue-next'

const app = createApp(App);
app.use(router);
app.use(createBootstrap());
app.mount('#app');
