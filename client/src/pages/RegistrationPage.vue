<template>
    <v-container>
      <v-form @submit.prevent="submitRegistration">
        <v-text-field
          v-model="username"
          label="Username"
          required
        ></v-text-field>
    
        <v-text-field
          v-model="email"
          label="Email"
          type="email"
          required
        ></v-text-field>
        <v-text-field
          v-model="password"
          label="Password"
          type="password"
          required
        ></v-text-field>
        <v-btn type="submit" color="primary">Register</v-btn>
        <v-alert v-if="errorMessage" type="error">{{ errorMessage }}</v-alert>
      </v-form>
    </v-container>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref } from 'vue';
  import { register } from '../services/api';  // Import the registration API call
  import { setTokenCookie } from '../services/cookies';  // Set token as cookie
  import { useAuth } from '../services/useAuth';  // Import auth composable
  
  export default defineComponent({
    name: 'RegistrationPage',
    setup() {
      const email = ref('');
      const username = ref('');
      const password = ref('');
      const errorMessage = ref('');
      const { login } = useAuth();  // Get login function from auth composable
  
      const submitRegistration = async () => {
        try {
          // Call the registration API
          const response = await register({ username: username.value, email: email.value, password: password.value });
        
          errorMessage.value = '';
          window.location.href = '/';
        } catch (error) {
          errorMessage.value = 'Registration failed. Please try again.';
        }
      };
  
      return {
        username,
        email,
        password,
        submitRegistration,
        errorMessage,
      };
    },
  });
  </script>
  2. Explanation o