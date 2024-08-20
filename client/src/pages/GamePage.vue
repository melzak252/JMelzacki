<!-- src/pages/GamePage.vue -->
<template>
  <div>
    <h1>Country Guessing Game</h1>
    <p>{{ responseMessage }}</p>
    <v-btn @click="startGame">Start Game</v-btn>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'GamePage',
  setup() {
    const responseMessage = ref('');

    const startGame = async () => {
    };

    return {
      responseMessage,
      startGame,
    };
  },
});
</script>
