<template>
    <v-app-bar app>
      <v-btn icon @click="drawer = !drawer">
        <v-icon>mdi-menu</v-icon>
      </v-btn>
      <v-toolbar-title style="width: max-content;">
        <router-link to="/" style="text-decoration: none; color: inherit; width: max-content;" class="home-link">
          <template v-if="!authStore.isAuth">
            JMelzacki
          </template>
          <template v-else>
            <div style="border: 1px solid white; border-radius: 3px; max-width: max-content; padding: 5px 10px;">{{ authStore.user?.username }}</div>
          </template>
        </router-link>
      </v-toolbar-title>
      <v-spacer>
      </v-spacer>
      <template v-if="!authStore.isAuth">
        <v-btn to='/sign' style="height: 100%; font-size: 20px; padding: 10px 20px; width: max-content; align-items: center;">
          Sign in
        </v-btn>
      </template>
      <template v-else>
        <v-btn style="height: 100%; font-size: 20px; padding: 10px 20px; width: max-content; align-items: center; background-color: #660000;" @click="handleLogout">
          Logout
        </v-btn>
      </template>
  </v-app-bar>

  <!-- Mobile Navigation Drawer -->
  <v-navigation-drawer v-model="drawer" app temporary @click="handleDrawerClick">
    <v-list>
      <v-list-item to='/'>
        <v-list-item-title>Home</v-list-item-title>
      </v-list-item>
      <!-- If the user is logged in -->
      <template v-if="authStore.isAuth">
        <v-list-item to='/game'>
          <v-list-item-title>Play</v-list-item-title>
        </v-list-item>
        <v-list-item to='/account'>
          <v-list-item-title>Account</v-list-item-title>
        </v-list-item>
      </template>
    </v-list>
  </v-navigation-drawer>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'Header',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    const drawer = ref(false);

    const handleLogout = () => {
      authStore.logout();
      router.push({ name: 'Home' })
    };

    onMounted(() => {
      authStore.checkAuth();
    });

    const handleDrawerClick = () => {
      drawer.value = !drawer.value
    }

    return {
      authStore,
      drawer,
      handleLogout,
      handleDrawerClick
    };
  },
});
</script>

<style>
.home-link:hover {
  color: #ddaa00 !important;
  border-color: #ddaa00 !important;;
}
</style>