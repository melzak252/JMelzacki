<!-- src/pages/AboutMePage.vue -->
<template>
  <v-container class="text-center my-10">
    <v-row class="justify-center">
      <v-col cols="12" md="8">
        <v-card elevation="10" class="pa-5">
          <v-card-title class="headline font-weight-bold">
            Jakub Melzacki
          </v-card-title>
          <v-card-text class="py-5">
            <v-row class="my-5">
              <v-col cols="12">
                <v-avatar
                  size="150"
                  class="mx-auto mb-4"
                >
                  <v-img
                    src="@/assets/Jakub_Melzacki.png"
                    alt="Jakub Melzacki"
                  ></v-img>
                </v-avatar>
                <h2 class="text-h5 font-weight-bold mb-4">About Me</h2>
                <p>
                  I am a passionate knowledge-seeker. If you have interesting information, I’m always eager to hear it! 😋 My main fields of interest include Physics, Mathematics, Computer Science, and Philosophy (I strongly believe Hegel is a charlatan!). Currently, I am focusing on developing my skills in <strong>Data Science</strong>, aiming to apply this knowledge to my hobby of creating intelligent systems for games like <strong>League of Legends, TFT, Chess</strong>, and many others.
                </p>
                <p>
                  Currently, I work as a <strong>Python Developer</strong>, which is the programming language I am most comfortable with. However, that doesn’t mean other technologies are foreign to me! I also have experience with <strong>C++20, TypeScript, Bash</strong>, and many other tools and languages.
                </p>
                <p>
                  Do you have an exciting project and need versatile support? <strong>I’m your man!</strong>
                </p>
              </v-col>
            </v-row>
            <v-divider></v-divider>
            <v-row class="my-5 justify-center">
              <v-col cols="12">
                <h3 class="text-h6 font-weight-bold mb-4">Get in Touch:</h3>
                <v-row justify="center" class="mb-4">
                  <v-col cols="12" md="4">
                    <v-btn
                      block
                      color="indigo"
                      href="https://github.com/melzak252"
                      target="_blank"
                      large
                    >
                      <v-icon left>mdi-github</v-icon>
                      GitHub
                    </v-btn>
                  </v-col>
                  <v-col cols="12" md="4">
                    <v-btn
                      block
                      color="blue darken-3"
                      href="https://linkedin.com/in/jmelzacki/"
                      target="_blank"
                      large
                    >
                      <v-icon left>mdi-linkedin</v-icon>
                      LinkedIn
                    </v-btn>
                  </v-col>
                  <v-col cols="12" md="4">
                    <v-btn
                      block
                      color="purple"
                      large
                    >
                      <v-icon left>mdi-discord</v-icon>
                      Discord: .melzak
                    </v-btn>
                  </v-col>
                </v-row>
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
  name: 'AboutMePage',
};
</script>

<style scoped>
.headline {
  color: #1e88e5;
}

.text-h5 {
  color: #424242;
}

.text-h6 {
  color: #616161;
}

.v-avatar img {
  border-radius: 50%;
}
</style>
