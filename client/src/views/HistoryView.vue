<template>

    <PostComponent />

</template>
  
  <script>
  import PostComponent from '../components/PostComponent.vue'
  
  export default {
    name: 'App',
    components: {
      PostComponent
    }
  }
  </script>
  
  <style>
  
html {
  overflow-y: scroll;
}
  </style>