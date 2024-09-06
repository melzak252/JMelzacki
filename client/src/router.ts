// src/router.ts
import { createRouter, createWebHistory } from "vue-router";
import HomePage from "./pages/HomePage.vue";
import PortfolioPage from "./pages/PortfolioPage.vue";
import AboutMePage from "./pages/AboutMePage.vue";
import GamePage from "./pages/GamePage.vue";
import SignPage from "./pages/SignPage.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: HomePage,
  },
  {
    path: "/portfolio",
    name: "Portfolio",
    component: PortfolioPage,
  },
  {
    path: "/aboutme",
    name: "AboutMe",
    component: AboutMePage,
  },
  {
    path: "/game",
    name: "Game",
    component: GamePage,
  },
  { path: "/sign", name: "Sign", component: SignPage },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});
