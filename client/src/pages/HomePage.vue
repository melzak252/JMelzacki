<template>
  <v-alert type="error" dense prominent color="red" dark>
    Registration is currently closed.
  </v-alert>
  <v-container class="my-10">
    <v-row class="justify-center">
      <v-col cols="12" md="8">
        <v-card elevation="10" class="pa-5">
          <v-card-title class="headline font-weight-bold text-left">
            Welcome to the Guess Country Game!
          </v-card-title>
          <v-card-text class="py-5">
            <div class="timeline">
              <h2 class="text-h8 font-weight-medium mb-4 timeline-title">
                How I Built This Website
              </h2>
              <v-timeline align-top dense>
                <v-timeline-item v-for="(item, index) in completedItems" :key="index" :color="item.color" small
                  fill-dot>
                  <v-card flat>
                    <v-card-title>{{ item.title }}</v-card-title>
                    <v-card-subtitle>{{ item.subtitle }}</v-card-subtitle>
                  </v-card>
                </v-timeline-item>
              </v-timeline>
            </div>
            <div class="timeline">
              <h2 class="text-h8 font-weight-medium mb-4 timeline-title">
                Future improvements
              </h2>
              <v-timeline align-top dense>
                <v-timeline-item v-for="(item, index) in plannedItems" :key="index" :color="item.color" small fill-dot>
                  <v-card flat>
                    <v-card-title>{{ item.title }}</v-card-title>
                    <v-card-subtitle>{{ item.subtitle }}</v-card-subtitle>
                  </v-card>
                </v-timeline-item>
              </v-timeline>
            </div>
            <v-divider></v-divider>
            <v-row class="my-5">
              <v-col cols="12">
                <h2 class="text-h5 font-weight-medium mb-4">
                  How to Play:
                </h2>
                <v-card class="pa-3" outlined>
                  <v-card-title class="text-h6 font-weight-bold">
                    Objective
                  </v-card-title>
                  <v-card-text>
                    Guess the country by asking up to 10 true/false questions and making up to 3 guesses.
                  </v-card-text>
                </v-card>
                <v-card class="pa-3 mt-3" outlined>
                  <v-card-title class="text-h6 font-weight-bold">
                    Step 1: Log In
                  </v-card-title>
                  <v-card-text>
                    To start, you need to register an account (Actualy registration is closed! If you re lucky today You
                    can be first today to use test acc (login: TestUser pass: test) and pass quiz before everyone). <br>
                    Once registered, log in to access the game.
                  </v-card-text>
                </v-card>
                <v-card class="pa-3 mt-3" outlined>
                  <v-card-title class="text-h6 font-weight-bold">
                    Step 2: Ask Questions
                  </v-card-title>
                  <v-card-text>
                    You can ask up to 10 true/false questions to narrow down the possibilities.
                  </v-card-text>
                </v-card>
                <v-card class="pa-3 mt-3" outlined>
                  <v-card-title class="text-h6 font-weight-bold">
                    Step 3: Make Guesses
                  </v-card-title>
                  <v-card-text>
                    You have 3 attempts to guess the correct country. Use your questions wisely!
                  </v-card-text>
                </v-card>
                <v-card class="pa-3 mt-3" outlined>
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
  data() {
    return {
      completedItems: [
        { title: "Idea for the Game", subtitle: "Conceptualized the game", color: "teal" },
        { title: "Creating API in FastAPI", subtitle: "Developed backend API using FastAPI", color: "green" },
        { title: "Adding PostgreSQL Database", subtitle: "Integrated PostgreSQL for data storage", color: "blue" },
        { title: "OpenAI Integration", subtitle: "Incorporated OpenAI for main game functionality", color: "red" },
        { title: "Creating Frontend in Vue3 TS", subtitle: "Developed the frontend using Vue 3 and TypeScript", color: "orange" },
        { title: "Containerization with Docker", subtitle: "Containerized all services using Docker Compose, managed by an Nginx container", color: "purple" },
        { title: "Hosting on Linode", subtitle: "Deployed on a Debian 11 server at Linode", color: "brown" }
      ],
      plannedItems: [
        { title: "Add Qdrant Database", subtitle: "Integrate Qdrant to enhance data retrieval for creating context for quiz country", color: "cyan" },
        { title: "Open Registration", subtitle: "After secure all endpoints I will open registration page!", color: "white" },
        { title: "Add Email Verification", subtitle: "Implement email verification for new users", color: "light-green" },
        { title: "More Visual Updates", subtitle: "Plan for ongoing improvements in UI/UX", color: "pink" }
      ]
    };
  }
};
</script>

<style>
.v-timeline--vertical.v-timeline .v-timeline-item:nth-child(2n) .v-timeline-item__body {
  grid-column: 3 !important;
}

.v-timeline-item__opposite {
  display: none;
}

.v-timeline-item__body {
  padding-left: 1.5rem;
  text-align: left;
  /* Align text to the left */
}

.timeline-title {
  text-align: center;
  padding-right: 2rem;
}

.v-timeline-item .v-card-title,
.v-timeline-item .v-card-subtitle,
.v-timeline-item .v-card-text {
  text-align: left;
  /* Ensure all text in cards is left-aligned */
}

.timeline {
  display: flex;
  flex-direction: column;
  align-items: start;
}
</style>