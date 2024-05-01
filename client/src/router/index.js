import { createRouter, createWebHistory } from 'vue-router';

// Define your routes here, for example:
const routes = [
  { path: '/', component: () => import('../views/Home.vue') },
  { path: '/countrydle', component: () => import('../views/Countrydle.vue') }
  { path: '/guess-country', component: () => import('../views/GuessCountry.vue') }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;