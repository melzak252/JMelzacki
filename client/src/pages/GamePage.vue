<template>
  <v-container class="game-page">
    <v-row>
      <!-- Chat Area -->
      <v-col cols="8">
        <v-card class="chat-box">
          <v-card-title>Ask Your Questions</v-card-title>
          <div class="sent-box">
            <v-text-field v-model="questionInput" label="Ask a True/False Question"
              placeholder="Is it located in Europe?" hide-details="auto" @keyup.enter="sendQuestion"
              :disabled="remainingQuestions <= 0 || loading || isGameOver"></v-text-field>
            <v-btn class="sent-btn" style="height: 56px;" @click="sendQuestion" color="primary"
              :disabled="remainingQuestions <= 0 || loading || isGameOver">
              Ask
              <v-icon dark right style="padding-left: 10px;">
                mdi-send
              </v-icon>
            </v-btn>
          </div>
          <v-row>
            <v-col v-for="(entry, index) in reversedQuestionsHistory" :key="index" cols="12">
              <v-card outlined :class="getRowClass(entry.answer)" class="pa-4">
                <v-card-title>{{ entry.question }}</v-card-title>
                <v-card-subtitle>{{ entry.answer }}</v-card-subtitle>
              </v-card>
            </v-col>
          </v-row>
        </v-card>
      </v-col>

      <!-- Guess Area -->
      <v-col cols="4">
        <v-card class="pa-4 guess-box">
          <v-card-title>Make a Guess</v-card-title>
          <v-card-text>
            <p>You have {{ remainingGuesses }} guesses remaining.</p>
            <v-text-field v-model="guessInput" label="Guess the Country" placeholder="Enter your guess..."
              @keyup.enter="sendGuess" :disabled="remainingGuesses <= 0 || loading || isGameOver"></v-text-field>
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
                <v-card-title>{{ entry.guess }}</v-card-title>
                <v-card-subtitle>{{ entry.response }}</v-card-subtitle>
              </v-card>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
      <v-dialog v-model="showPopup" max-width="500">
        <v-card>
          <v-card-title class="text-h5">{{ won ? 'Congratulations!' : 'Game Over' }}</v-card-title>
          <v-card-text>
            <p v-if="won">
              Great job! You've guessed the correct country. Keep it up!
            </p>
            <p v-else>
              Don't worry! The solution will be revealed tomorrow with the new country.
            </p>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="closePopup">Close</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { computed, defineComponent, ref, watch } from 'vue';
import { useAuth } from '../consumable/useAuth'
import { useGame } from '../consumable/useGame'
import { useRouter } from 'vue-router';
export default defineComponent({
  name: 'GamePage',
  setup() {
    const { isAuthenticated } = useAuth();
    const {
      remainingQuestions,
      remainingGuesses,
      isGameOver,
      questionsHistory,
      guessHistory,
      loading,
      error,
      won,
      askQuestion,
      makeGuess,
      getUserTodayHistory } = useGame()
    let router = useRouter();

    if (!isAuthenticated.value) {
      router.push({ name: 'Home' });
    }

    getUserTodayHistory()

    const questionInput = ref('');
    const guessInput = ref('');
    const showPopup = ref(false);

    // Computed property to reverse the order of the questionsHistory
    const reversedQuestionsHistory = computed(() => {
      return [...questionsHistory.value].reverse();
    });

    // Function to return the appropriate class based on the answer
    const getRowClass = (answer: string) => {
      if (answer === 'True') return 'green-outline';
      if (answer === 'False') return 'red-outline';
      return 'orange-outline';
    };

    const sendQuestion = () => {
      const question = questionInput.value;
      askQuestion(question);
      questionInput.value = "";
    }

    const sendGuess = () => {
      const guess = guessInput.value
      makeGuess(guess);
      guessInput.value = ""
    }

    const closePopup = () => {
      showPopup.value = false
    }

    watch(isGameOver, (newVal) => {
      if (!newVal) return;

      showPopup.value = true;
    });
    return {
      questionInput,
      guessInput,
      remainingGuesses,
      remainingQuestions,
      questionsHistory,
      reversedQuestionsHistory,
      guessHistory,
      isGameOver,
      error,
      loading,
      showPopup,
      won,
      getRowClass,
      sendQuestion,
      sendGuess,
      closePopup
    };
  },
});
</script>

<style scoped>
.game-page {
  height: 100vh;
}

.chat-box {
  height: 100%;
}

.guess-box {
  height: 100%;
}

.chat-log {
  height: 400px;
  /* overflow-y: auto; */
  background-color: #f9f9f9;
  padding: 10px;
  border-radius: 8px;
}

.chat-message {
  margin-bottom: 10px;
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

.orange-outline {
  border: 2px solid #ff9800;
  color: #ff9800;
  background-color: #ff980010;
}

.sent-box {
  height: 100px;
  display: grid;
  grid-template-columns: auto 100px;
  align-items: center;
  padding: 15px;
}
</style>
