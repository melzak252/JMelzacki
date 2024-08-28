<template>
  <v-card class="pa-4 guess-box">
    <v-card-title>Make a Guess</v-card-title>
    <v-card-text>
      <p>You have {{ remainingGuesses }} guesses remaining.</p>
      <v-text-field 
        maxlength="30" 
        v-model="guessInput" 
        label="Guess the Country" 
        placeholder="Enter your guess..."
        @keyup.enter="sendGuess" 
        :disabled="remainingGuesses <= 0 || loading || isGameOver"></v-text-field>
      <v-btn @click="sendGuess" color="primary" :disabled="remainingGuesses <= 0 || loading || isGameOver">
        Guess
        <v-icon dark right style="padding-left: 10px;">
          mdi-magnify
        </v-icon>
      </v-btn>
    </v-card-text>
    <v-row>
      <v-col v-for="(entry, index) in guessHistory" :key="index" cols="12">
        <v-card outlined :class="getRowClass(entry.response)" class="pa-4">
          <v-card-title>{{ entry.guess }} - {{ entry.response }}</v-card-title>
        </v-card>
      </v-col>
    </v-row>
  </v-card>
</template>

<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import { useGameStore } from '../stores/game'; // Import Pinia store

export default defineComponent({
  name: 'GuessBox',
  setup() {
    // Access the store
    const gameStore = useGameStore();

    // Access state and actions
    const guessHistory = computed(() => gameStore.guessHistory)
    const isGameOver = computed(() => gameStore.isGameOver)
    const remainingGuesses = computed(() => gameStore.remainingGuesses)
    const loading = computed(() => gameStore.loading)
    
    const guessInput = ref('');

    const getRowClass = (correct: string) => {
      if (correct === "True") return 'green-outline';
      return 'red-outline';
    };

    const sendGuess = () => {
      const guess = guessInput.value;
      gameStore.makeGuess(guess);
      guessInput.value = "";
    };

    return {
      guessInput,
      remainingGuesses,
      isGameOver,
      guessHistory,
      loading,
      getRowClass,
      sendGuess
    };
  }
});
</script>

<style scoped>
.guess-box {
  height: 100%;
  padding: 20px;
}

.green-outline {
  border: 2px solid #4caf50;
  color: #4caf50;
  background-color: #4caf5010;
}

.red-outline {
  border: 2px solid #f44336;
  color: #f44336;
  background-color: #f4433610;
}
</style>
