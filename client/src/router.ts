// src/router.ts
import { createRouter, createWebHistory } from "vue-router";
import HomePage from "./pages/HomePage.vue";
import InfoPage from "./pages/InfoPage.vue";
import GamePage from "./pages/GamePage.vue";
import LoginPage from "./pages/LoginPage.vue";
import RegistrationPage from "./pages/RegistrationPage.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: HomePage,
  },
  {
    path: "/info",
    name: "Info",
    component: InfoPage,
  },
  {
    path: "/game",
    name: "Game",
    component: GamePage,
  },
  { path: "/login", name: "Login", component: LoginPage },
  { path: "/register", name: "Register", component: RegistrationPage },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});
