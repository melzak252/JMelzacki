<template>

  <v-container>
    <v-form @submit.prevent="submitRegistration" class="my-5">
      <v-text-field v-model="username" label="Username" required></v-text-field>

      <v-text-field v-model="email" label="Email" type="email" required></v-text-field>
      <v-text-field v-model="password" label="Password" type="password" required></v-text-field>
      <v-btn type="submit" color="primary">Register</v-btn>
    </v-form>
    <v-dialog v-model="showPopup" max-width="500">
      <v-card>
        <v-card-title class="text-h5">{{ popUpTitle }}</v-card-title>
        <v-card-text>
          {{ popUpText }}
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="closePopup">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useRouter } from 'vue-router';
import { apiService } from '../services/api';

export default defineComponent({
  name: 'RegistrationPage',
  setup() {
    const email = ref<string>('');
    const username = ref<string>('');
    const password = ref<string>('');
    const popUpTitle = ref('');
    const popUpText = ref('');
    const router = useRouter();
    const showPopup = ref<boolean>(false);
    const registered = ref<boolean>(false);
    const submitRegistration = async () => {
      // alert("Regisration is closed!");
      // return;
      try {
        // Call the registration API
        await apiService.register({
          email: email.value,
          username: username.value,
          password: password.value
        });

        showPopup.value = true;
        popUpTitle.value = `User: ${username.value} successfully registered!`
        popUpText.value = `You can go to login page and login as ${username.value}`;
        registered.value = true;
      } catch (error: any) {
        showPopup.value = true;
        popUpTitle.value = 'Registration failed.';
        popUpText.value = error.message;
        registered.value = false;
      }
    };
    const closePopup = () => {
      showPopup.value = false;
      if (registered.value) {
        router.push({ name: 'Login' })
      }
    }
    return {
      username,
      email,
      password,
      showPopup,
      popUpText,
      popUpTitle,
      submitRegistration,
      closePopup
    };
  },
});
</script>