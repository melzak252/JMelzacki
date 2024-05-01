<script setup>

</script>

<template>
  <div>
    <Header />
    <router-view></router-view>
  </div>
</template>

<script>
import Header from './components/Header.vue';

export default {
  name: 'App',
  components: {
    Header
  }
}
</script>

<style scoped>

</style>
