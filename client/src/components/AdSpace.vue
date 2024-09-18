<template>
    <div class="ad-space">
      <!-- AdSense code snippet -->
      <ins class="adsbygoogle"
           style="display:block"
           data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
           data-ad-slot="YYYYYYYYYY"
           data-ad-format="auto"
           data-full-width-responsive="true"></ins>
    </div>
  </template>


<script lang="ts">
import { defineComponent, onMounted } from 'vue';

export default defineComponent({
  name: 'AdSpace',
  setup() {
    onMounted(() => {
      // Initialize Google AdSense
      try {
        // (adsbygoogle = window.adsbygoogle || []).push({});
      } catch (e) {
        console.error(e);
      }
    });
  },
});
</script>


<style scoped>
.ad-space {
  width: 100%;
  margin: 20px 0;
  text-align: center;
}
</style>