<template>

  <v-container>

    <v-row class="justify-center">
      <v-col cols="12" md="8">
        <v-card elevation="10" class="pa-5">
          <!-- <v-alert border="top" type="warning" variant="outlined" prominent class="registration-alert">
            Registration is currently closed.
          </v-alert> -->
          <br>
          <v-card-title class="headline font-weight-bold">
            Welcome to Countrydle!
          </v-card-title>
          <v-card-text class="py-5">
            <v-row class="my-5">
              <v-col cols="12">
                <h2 class="text-h5 font-weight-medium mb-4">
                  How to Play:
                </h2>
                <v-card class="pa-3" variant="tonal">
                  <v-card-title class="text-h6 font-weight-bold">
                    Objective
                  </v-card-title>
                  <v-card-text>
                    Guess the country by asking up to 10 true/false questions and making up to 3 guesses.
                  </v-card-text>
                </v-card>
                <v-card class="pa-3 mt-3" variant="tonal">
                  <v-card-title class="text-h6 font-weight-bold">
                    Step 1: Log In
                  </v-card-title>
                  <v-card-text>
                    To start, you need to register an account. <br>
                    Once registered, log in to access the game.
                  </v-card-text>
                </v-card>
                <v-card class="pa-3 mt-3" variant="tonal">
                  <v-card-title class="text-h6 font-weight-bold">
                    Step 2: Ask Questions
                  </v-card-title>
                  <v-card-text>
                    You can ask up to 10 true/false questions to narrow down the possibilities.
                  </v-card-text>
                </v-card>
                <v-card class="pa-3 mt-3" variant="tonal">
                  <v-card-title class="text-h6 font-weight-bold">
                    Step 3: Make Guesses
                  </v-card-title>
                  <v-card-text>
                    You have 3 attempts to guess the correct country. Use your questions wisely!
                  </v-card-text>
                </v-card>
                <v-card class="pa-3 mt-3" variant="tonal">
                  <v-card-title class="text-h6 font-weight-bold">
                    Step 4: Win!
                  </v-card-title>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">

export default {
  name: 'HomePage',
  setup() {

  },
};
</script>

<style scoped>

</style>

<style>
.headline {
  text-align: center;
}
</style>