<template>
  <v-container class="home-container">
    <v-card class="rules">
      <v-card-title class="headline font-weight-bold">
        Welcome to JMelzacki!
      </v-card-title>
      <v-card-text class="py-5">
        <h2 class="text-h5 font-weight-medium mb-4">
          How to play Countrydle:
        </h2>
        <v-row class="d-flex flex-column">
          <!-- Objective Card -->
          <v-col cols="12" class="d-flex">
            <v-card class="pa-3 flex-grow-1 d-flex flex-column" variant="tonal">
              <v-card-title class="text-h6 font-weight-bold">
                Objective
              </v-card-title>
              <v-card-text class="flex-grow-1">
                Guess the country by asking up to 10 true/false questions and making up to 3 guesses.
              </v-card-text>
            </v-card>
          </v-col>
          <!-- Step 1 Card -->
          <v-col cols="12" class="d-flex">
            <v-card class="pa-3 flex-grow-1 d-flex flex-column" variant="tonal">
              <v-card-title class="text-h6 font-weight-bold">
                Step 1: Log In
              </v-card-title>
              <v-card-text class="flex-grow-1">
                To start, you need to register an account.<br>
                Once registered, log in to access the game.
              </v-card-text>
            </v-card>
          </v-col>
          <!-- Step 2 Card -->
          <v-col cols="12" class="d-flex">
            <v-card class="pa-3 flex-grow-1 d-flex flex-column" variant="tonal">
              <v-card-title class="text-h6 font-weight-bold">
                Step 2: Ask Questions
              </v-card-title>
              <v-card-text class="flex-grow-1">
                You can ask up to 10 true/false questions to narrow down the possibilities.
              </v-card-text>
            </v-card>
          </v-col>
          <!-- Step 3 Card -->
          <v-col cols="12" class="d-flex">
            <v-card class="pa-3 flex-grow-1 d-flex flex-column" variant="tonal">
              <v-card-title class="text-h6 font-weight-bold">
                Step 3: Make Guesses
              </v-card-title>
              <v-card-text class="flex-grow-1">
                You have 3 attempts to guess the correct country. Use your questions wisely!
              </v-card-text>
            </v-card>
          </v-col>
          <!-- Step 4 Card -->
          <v-col cols="12" class="d-flex">
            <v-card class="pa-3 flex-grow-1 d-flex flex-column" variant="tonal">
              <v-card-title class="text-h6 font-weight-bold">
                Step 4: Win!
              </v-card-title>
              <v-card-text class="flex-grow-1">
                Celebrate your victory!
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
    <!-- Second Column: Buttons and Leaderboard -->
    <!-- Buttons Section -->
    <v-card class="home-buttons">
      <v-btn large variant="tonal" to="/game" class="home-btn mb-3">
        Play
      </v-btn>
      <v-btn large variant="tonal" to="/aboutme" class="home-btn mb-3">
        About Me
      </v-btn>
      <v-btn large variant="tonal" to="/portfolio" class="home-btn">
        Portfolio
      </v-btn>
    </v-card>
    <v-card class="home-leader-board">
      <v-data-table class="pa-5" style="height: 100%;">
        <thead>
          <tr>
            <td colspan="3">
              <h1>Leaderboard</h1>
            </td>
          </tr>
          <tr>
            <td>
              Nr
            </td>
            <td>
              Username
            </td>
            <td>
              Points
            </td>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td colspan="3" style="text-align: center;">
            </td>
          </tr>
          <tr>
            <td colspan="3" style="text-align: center;">
            </td>
          </tr>
          <tr>
            <td colspan="3" style="text-align: center;">
            </td>
          </tr>
          <tr>
            <td colspan="3" style="text-align: center;">
            </td>
          </tr>
          <tr>
            <td colspan="3" style="text-align: center;">
              <h2 style="opacity: 0.4;">Comming soon!</h2>
            </td>
          </tr>
          <tr>
            <td colspan="3" style="text-align: center;">
            </td>
          </tr>
          <tr>
            <td colspan="3" style="text-align: center;">
            </td>
          </tr>
          <tr>
            <td colspan="3" style="text-align: center;">
            </td>
          </tr>
        </tbody>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script lang="ts">
export default {
  name: 'HomePage',
  setup() { },
};
</script>

<style>
.home-container {
  display: grid;
  grid-template-columns: 4fr 3fr;
  grid-template-rows: auto auto;
  column-gap: 15px;
  row-gap: 15px;
}

.rules {
  grid-column: 1;
  grid-row: 1 / 2 span;
}

.home-buttons {
  grid-column: 2;
  grid-row: 1;
  display: flex;
  flex-direction: column;
  padding: 10px 20px !important;
}

.headline {
  text-align: center;
}

.home-leader-board {
  grid-column: 2;
  grid-row: 2;
  height: 100%;
}

.home-btn {
  width: 100%;
  height: max-content !important;
  padding: 10px 20px !important;
  font-size: 36px !important;
}
</style>
