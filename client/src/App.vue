<script>
import NavBar from './components/NavBar.vue'

import { RouterView } from 'vue-router'

export default {
  name: 'App',
  components: {
    NavBar,
    RouterView
  }
}
</script>

<template>

 <div id="app">
    <NavBar />
    <div class="container">
      <RouterView />
    </div>
  </div>

</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

body {
    margin: 0;
  }
  
</style>
