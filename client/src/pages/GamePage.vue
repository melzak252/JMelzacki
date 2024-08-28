<template>
  <v-container class="game-page">
    <div class="game-container">
      <QuestionBox />
      <GuessBox />
    </div>
    <v-dialog v-model="showPopup" max-width="500">
      <v-card>
        <v-card-title class="text-h5">{{ won ? 'Congratulations!' : 'Game Over' }}</v-card-title>
        <v-card-text>
          <p v-if="won">
            Great job! You've guessed the correct country. Keep it up!
          </p>
          <p v-else>
            The country was {{ country?.name }}. <br>
            Don't worry! You can get it tomorrow!
          </p>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="closePopup">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script lang="ts">
import { computed, defineComponent, onMounted, ref, watch } from 'vue';
import { useGameStore } from '../stores/game';
import QuestionBox from '../components/QuestionBox.vue';
import GuessBox from '../components/GuessBox.vue';

export default defineComponent({
  name: 'GamePage',
  components: {
    QuestionBox,
    GuessBox,
  },
  setup() {
    // Access the store
    const gameStore = useGameStore();

    const won = computed(() => gameStore.won);
    const loading = computed(() => gameStore.loading);
    const country = computed(() => gameStore.correctCountry);
    const showPopup = ref(gameStore.isGameOver);
    const shouldShow = ref(false);
    onMounted(async () => {
      await gameStore.loadGameState();
    });

    const closePopup = () => {
      showPopup.value = false;
    };

    watch(() => gameStore.isGameOver, (newVal) => {
      if (gameStore.loading) {
        shouldShow.value = true;
        return
      }
      showPopup.value = newVal;
    });

    watch(() => gameStore.loading, (newVal) => {
      if (newVal) return;
      if (shouldShow) shouldShow.value = true
    })

    return {
      showPopup,
      won,
      loading,
      country,
      closePopup,
    };
  }
});
</script>

<style scoped>
.game-page {
  height: 100%;
  display: flex;
  justify-content: center;
}

.game-container {
  display: grid;
  grid-template-columns: auto 400px;
  max-width: 1440px;
  column-gap: 20px;
  width: 100%;
}

@media (max-width: 768px) {
  .game-container {
    display: grid;
    grid-template-columns: auto;
    grid-template-rows: auto auto;
    row-gap: 15px;
  }
}
</style>
