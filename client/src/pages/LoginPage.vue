<!-- src/pages/LoginPage.vue -->
<template>
    <v-container>
      <v-form @submit.prevent="submitLogin">
        <v-text-field
          v-model="username"
          label="Username"
          type="username"
          required
        ></v-text-field>
        <v-text-field
          v-model="password"
          label="Password"
          type="password"
          required
        ></v-text-field>
        <v-btn type="submit" color="primary">Login</v-btn>
        <v-alert v-if="errorMessage" type="error">{{ errorMessage }}</v-alert>
      </v-form>
    </v-container>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref } from 'vue';
  import { login as loginApi } from '../services/auth';
  import { setTokenCookie } from '../services/cookies';
  import { useAuth } from '../services/useAuth';
import { useRouter } from 'vue-router';
  
  export default defineComponent({
    name: 'LoginPage',
    setup() {
      const username = ref('');
      const password = ref('');
      const errorMessage = ref('');
      const { login } = useAuth();
      const router = useRouter();

      const submitLogin = async () => {
        try {
          const response = await loginApi({ username: username.value, password: password.value });
          const token = response.data.access_token;
          
          // Save the token and update the auth state
          setTokenCookie(token);
          login();
  
          errorMessage.value = '';
          router.push({ name: 'Home' });
        } catch (error) {
          errorMessage.value = 'Login failed. Please check your credentials.';
        }
      };
  
      return {
        username,
        password,
        submitLogin,
        errorMessage,
      };
    },
  });
  </script>