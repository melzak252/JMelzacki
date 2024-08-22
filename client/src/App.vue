<!-- src/App.vue -->
<template>
  <v-app>
    <v-app-bar app>
      <v-toolbar-title>Country Guessing Game</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn to="/">Home</v-btn>
      <v-btn to="/info">About</v-btn>
      <template v-if="!isAuthenticated">
        <v-btn to="/login">Login</v-btn>
        <v-btn to="/register">Register</v-btn>
      </template>
      <template v-else>
        <v-btn to="/game">Play</v-btn>
        <v-btn style="background-color: #660000;" @click="handleLogout">Logout</v-btn>
        <span style="padding: 20px;"> {{ user?.username }}</span>
      </template>
    </v-app-bar>
    
    <v-main>
      <v-container>
        <router-view /> <!-- This will display the current route component -->
      </v-container>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue';
import { useAuth } from './services/useAuth';
import { getTokenCookie } from './services/cookies';

export default defineComponent({
  name: 'App',
  setup() {
    const { isAuthenticated, user, login, logout, fetchUserData } = useAuth();

    const handleLogout = () => {
      logout();
      window.location.href = '/';
    };

    // Fetch user data on app initialization if the user is authenticated
    onMounted(() => {
      
      if (isAuthenticated.value) {
        fetchUserData()
      } else if(getTokenCookie()) {
        let token = getTokenCookie();
        if(!token) return;
        login()
      }
    });

    return {
      isAuthenticated,
      user,
      handleLogout,
    };
  },
});
</script>