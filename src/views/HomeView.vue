<script setup>
import { ref } from "vue";

let message = ref("Welcome to Jam-Date — Find your perfect match today!")

</script>

<template>
  <div class="home-container">
    <div class="overlay">
      <h1>{{ message }}</h1>
      <router-link to="/register">
        <button class="btn btn-primary m-2">Register</button>
      </router-link>
      <router-link to="/login">
        <button class="btn btn-secondary m-2">Login</button>
      </router-link>
      <router-link to="/profiles/favourites">
        <button class="btn btn-report m-2">View Reports</button>
      </router-link>
    </div>
  </div>
</template>

<style scoped>
.home-container {
  background-image: url('@/assets/dating-bg.jpg'); /* make sure this file exists */
  background-size: cover;
  background-position: center;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.overlay {
  background-color: rgba(0, 0, 0, 0.6);
  padding: 40px;
  border-radius: 16px;
  text-align: center;
  color: white;
}

button {
  padding: 10px 20px;
  font-size: 16px;
  margin: 10px;
  border-radius: 10px;
  border: none;
  cursor: pointer;
}

.btn-primary {
  background-color: #ff5c8a;
  color: white;
}

.btn-secondary {
  background-color: #9c27b0;
  color: white;
}

.btn-report {
  background-color: #2196f3;
  color: white;
}
/* Add any component specific styles here */
</style>
