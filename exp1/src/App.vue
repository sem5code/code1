<template>
  <div id="app">
    <ImageGallery />
  </div>
</template>

<script>
import ImageGallery from "./components/ImageGallery.vue";

export default {
  name: "App",
  components: { ImageGallery },
};
</script>

<style>
/* Global reset */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* Smooth font and background */
body {
  font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    sans-serif;
  background: #f4f5f7;
  color: #374151;
  min-height: 100vh;
}

/* App container - full width */
#app {
  /* Removed max-width and padding to allow full width */
  animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
