<!-- src/pages/HomePage.vue -->
<template>
    <v-container class="text-center my-10">
      <v-row class="justify-center">
        <v-col cols="12" md="8">
          <v-card elevation="10">
            <v-card-title class="headline font-weight-bold">
              Welcome to the Guess Country Game!
            </v-card-title>
            <v-card-text class="py-5">
              <v-row class="my-5">
                <v-col cols="12">
                  <v-img
                    src="https://cdn.vuetifyjs.com/images/cards/road.jpg"
                    alt="Game Image"
                    height="200px"
                    class="mb-4"
                  ></v-img>
                  <p>
                    This website is hosted on <strong>Linode</strong>, running
                    <strong>Debian 11</strong>, powered by <strong>Docker Compose</strong>. It is built
                    with the latest technology stack, including:
                  </p>
                  <v-list dense>
                    <v-list-item>
                      <v-list-item-content>
                        <v-list-item-title>Vue 3</v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-content>
                        <v-list-item-title>Python (Backend)</v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-content>
                        <v-list-item-title>Nginx (Proxy)</v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-content>
                        <v-list-item-title>PostgreSQL (Database)</v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-content>
                        <v-list-item-title>
                          OpenAI API for ChatGPT (Game AI)
                        </v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list>
                </v-col>
              </v-row>
              <v-divider></v-divider>
              <v-row class="my-5">
                <v-col cols="12">
                  <h2 class="text-h5 font-weight-medium mb-4">
                    How to Play:
                  </h2>
                  <p>
                    To start playing, you need to first <strong>register</strong> an
                    account. Once registered, log in to access the game.
                  </p>
                  <p>
                    The game consists of a fun challenge where you try to guess a
                    randomly selected country by asking up to <strong>10 true/false
                    questions</strong>. You also have <strong>3 attempts</strong> to
                    guess the correct country. Can you outsmart the AI and guess
                    correctly?
                  </p>
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
  };
  </script>
  
  <style scoped>
  .headline {
    color: #1e88e5;
  }
  
  .font-weight-medium {
    font-weight: 500;
  }
  </style>
  