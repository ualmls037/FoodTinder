<template>

   
    <main class="app-fondo">
      <NavBar/>
      <RouterView /> 
    </main>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import NavBar from './components/NavBar.vue'
</script>


<style>
.app-fondo {
  min-height: 100vh;
  background-image: url('/fondo1.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed;
}
.main-layout {
  text-align: center;
  font-family: sans-serif;
}
</style>


