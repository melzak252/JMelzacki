<template>
  <v-card class="pa-4 guess-box">
    <v-card-title>Make a Guess</v-card-title>
    <p style="padding-left: 1rem; padding-bottom: 2px;">You have {{ remainingGuesses }} guesses remaining.</p>
    <div class="guess-container">
      <v-text-field maxlength="30" v-model="guessInput" label="Guess the Country" placeholder="Enter your guess..."
        @keyup.enter="sendGuess" :disabled="remainingGuesses <= 0 || loading || isGameOver" :rules="guessRules"
        class="ma-0 mb-4 guess-input"></v-text-field>
      <v-btn @click="sendGuess" color="primary" class="guess-button"
        :disabled="remainingGuesses <= 0 || loading || isGameOver || !guessInput">
        <template v-if="loading">
          <v-progress-circular indeterminate color="white" size="24" class="mr-2"></v-progress-circular>
        </template>
        <template v-else>
          Guess
          <v-icon dark right style="padding-left: 10px;">
            mdi-magnify
          </v-icon>
        </template>
      </v-btn>
    </div>
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
      if (!guessInput.value) return;
      const guess = guessInput.value;
      gameStore.makeGuess(guess);
      guessInput.value = "";
    };

    const guessRules = [
      // (v: string): string | boolean => !!v || 'Guess is required!',
      (v: string): string | boolean => v.length <= 30 || 'Guess cannot be longer than 30 characters!'
    ];
    return {
      guessInput,
      remainingGuesses,
      isGameOver,
      guessHistory,
      loading,
      guessRules,
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

.guess-button {
  width: 100%;
  margin-bottom: 10px;
}

.guess-container {
  padding: 0.5rem 1rem;
}
</style>
