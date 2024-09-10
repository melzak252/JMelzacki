<template>
  <v-card class="chat-box">
    <v-card-title>Ask Your Questions</v-card-title>
    <p style="padding-left: 1rem;">You have {{ remainingQuestions }} qestions remaining.</p>
    <div class="sent-box ma-0">
      <v-text-field class="question-input" v-model="questionInput" maxlength="100" label="Ask a True/False Question"
        placeholder="Is it located in Europe?" :rules="questionRules" @keyup.enter="sendQuestion" :disabled="!canSend">
      </v-text-field>
      <v-btn class="sent-btn" style="height: 56px; align-self: baseline;" @click="sendQuestion" color="primary"
        :disabled="!canSend || !questionInput">
        <template v-if="loading">
          <v-progress-circular indeterminate color="white" size="24" class="mr-2"></v-progress-circular>
        </template>
        <template v-else>
          Ask
          <v-icon dark right style="padding-left: 10px;">
            mdi-send
          </v-icon>
        </template>
      </v-btn>
    </div>
    <v-row>
      <v-col v-for="(entry, index) in reversedQuestionsHistory" :key="index" cols="12">
        <v-card outlined :class="getRowClass(entry.answer)" class="pa-4" style="overflow: initial; z-index: initial">
          <v-card-title>{{ entry.question }} - {{ entry.answer }}</v-card-title>
          <v-card-text>{{ entry.explanation }}</v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-card>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import { useGameStore } from '../stores/game';

export default defineComponent({
  name: 'QuestionBox',
  setup() {
    const gameStore = useGameStore(); // Access the Pinia store
    // Access state from the store
    const questionInput = ref('');
    const isGameOver = computed(() => gameStore.isGameOver);
    const questionsHistory = computed(() => gameStore.questionsHistory);
    const loading = computed(() => gameStore.loading);
    const canSend = computed(() => gameStore.remainingQuestions > 0 && !gameStore.loading && !gameStore.isGameOver);
    const remainingQuestions = computed(() => gameStore.remainingQuestions)
    // Reverse the questionsHistory array
    const reversedQuestionsHistory = computed(() => {
      return [...questionsHistory.value].reverse();
    });

    // Determine the row class based on the answer
    const getRowClass = (answer: string) => {
      if (answer === 'True') return 'green-outline';
      if (answer === 'False') return 'red-outline';
      return 'orange-outline';
    };

    // Handle sending the question
    const sendQuestion = () => {
      if (!questionInput.value) return;
      const question = questionInput.value;
      gameStore.askQuestion(question); // Use the store action to send a question
      questionInput.value = ""; // Clear the input field
    };

    const questionRules = [
      // (v: string): string | boolean => !!v || 'Question is required',
      // (v: string): string | boolean => v.length >= 3 || 'Question must be at least 3 characters!',
      (v: string): string | boolean => v.length <= 100 || 'Question cannot be longer than 100 characters!'
    ];

    return {
      questionInput,
      canSend,
      isGameOver,
      questionsHistory,
      reversedQuestionsHistory,
      loading,
      remainingQuestions,
      questionRules,
      getRowClass,
      sendQuestion
    };
  }
});
</script>

<style scoped>
.chat-box {
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

.orange-outline {
  border: 2px solid #ff9800;
  color: #ff9800;
  background-color: #ff980010;
}

.sent-box {
  height: 100px;
  display: grid;
  grid-template-columns: auto 100px;
  align-items: flex-start;
  padding: 0.5rem 1rem;
}
</style>
