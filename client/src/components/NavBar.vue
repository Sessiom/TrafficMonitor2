

<template>
    <nav> 
      <router-link class="nav-link-center" to="/">Traffic Monitor</router-link> | 
      <router-link class="nav-link-left" to="/history"> History <i class="fas fa-history"></i></router-link>
    </nav>
  </template>
  
  <style scoped>

  .nav-link-left {
    color: white;
    text-decoration: none;
  }

  .nav-link-center {
    color: white;
    font-size: 1.5rem;
    text-decoration: none;
  }
  .nav-link-center:hover, .nav-link-left:hover {
    text-decoration: underline;
  }

  nav {
    text-align: center;
    overflow: hidden;
    padding: 20px;
    background-color: #335485;
  }
  
  nav a {
    font-weight: bold;
  }
  
  nav a.router-link-exact-active {
    color: #42b983;
  }
  </style>