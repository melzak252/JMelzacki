import { createApp } from 'vue'
import './style.scss'
import App from './App.vue'
import router from './router';
import { BootstrapVue3 } from 'bootstrap-vue-next';

// Import Bootstrap and BootstrapVue CSS
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css';

const app = createApp(App);
app.use(router);
app.use(BootstrapVue3);
app.mount('#app');
