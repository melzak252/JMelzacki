<!-- src/App.vue -->
<template>
  <v-app>
    <template v-if="!isMobile">
      <v-app-bar app>
        <v-toolbar-title>Countrydle</v-toolbar-title>
        <v-spacer class="menu-spacer">
        </v-spacer>
        <v-btn elevation="8" tonal to="/">Home</v-btn>
        <v-btn elevation="8" tonal to="/portfolio">Portfolio</v-btn>
        <v-btn elevation="8" tonal to="/aboutme">About Me</v-btn>
        <template v-if="!authStore.isAuth">
          <v-btn elevation="8" tonal to="/sign">Sign in</v-btn>
        </template>
        <template v-else>
          <v-btn elevation="8" tonal to="/game">Play</v-btn>
          <v-btn elevation="8" tonal style="background-color: #660000;" @click="handleLogout">Logout</v-btn>
          <span style="padding: 20px; margin-left: 20px; border-left: 1px solid grey;"> {{ authStore.user?.username }}</span>
        </template>
      </v-app-bar>
    </template>
    <template v-else>
      <v-app-bar app>
        <v-slide-group style="display: flex; justify-content: center; width: 100%;" show-arrows>
          <v-btn elevation="4" size="small" tonal to="/">Home</v-btn>
          <v-btn elevation="4" size="small" to="/portfolio">Portfolio</v-btn>
          <v-btn elevation="4" size="small" to="/aboutme">About Me</v-btn>
          <template v-if="!authStore.isAuth">
            <v-btn elevation="4" size="small" to="/sign">Sign in</v-btn>
          </template>
          <template v-else>
            <v-btn elevation="4" size="small" to="/game">Play</v-btn>
            <v-btn elevation="4" size="small" style="background-color: #660000;" @click="handleLogout">Logout</v-btn>
          </template>
        </v-slide-group>
      </v-app-bar>
    </template>


    <v-main>
      <v-container>
        <router-view /> <!-- This will display the current route component -->
      </v-container>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue';
import { useAuthStore } from './stores/auth';
import { useMediaQuery } from './consumable/useMediaQuery';

export default defineComponent({
  name: 'App',
  setup() {
    const authStore = useAuthStore()
    const isMobile = useMediaQuery("(max-width: 800px)")
    const handleLogout = () => {
      authStore.logout();
      window.location.href = '/';
    };

    onMounted(() => {
      authStore.getUser()
    });

    return {
      authStore,
      isMobile,
      handleLogout,
    };
  },
});
</script>

<style scoped>
.menu-spacer {
  display: flex;
}

.registration-alert {
  padding: 0 !important;
  font-size: small !important;
  max-width: 500px !important;
  margin-left: 25%;
}
</style>

<style>

.v-slide-group__content {
  justify-content: center;
}

.v-btn {
  width: 120px;
}

@media (max-width: 600px) {
  .v-btn {
    width: 100px;
  }
}
</style>