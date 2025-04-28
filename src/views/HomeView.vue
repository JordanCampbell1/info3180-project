<script setup>
import { ref } from "vue";

let message = ref("Welcome to Jam-Date  Find your perfect match today!")

</script>

<template>
  <div class="home-container">
    <div class="sidebar">
      <router-link to="/profiles/favourites">
        <button class="btn btn-report">View Reports</button>
      </router-link>
    </div>

    <div class="overlay">
      <h1>{{ message }}</h1>
      <router-link to="/register">
        <button class="btn btn-primary m-2">Register</button>
      </router-link>
      <router-link to="/login">
        <button class="btn btn-secondary m-2">Login</button>
      </router-link>
    </div>
  </div>
</template>


<style scoped>
.home-container {
  background-image: url('@/assets/Black_love.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  height: 100vh;
  width: 100vw;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.sidebar {
  position: absolute;
  top: 50%;
  left: 20px; /* Push it a little from the left */
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
}

.overlay {
  background-color: rgba(0, 0, 0, 0.6);
  padding: 50px;
  border-radius: 16px;
  text-align: center;
  color: white;
  display: flex;
  flex-direction: column;
  gap: 15px;
  width: 90%;
  max-width: 500px;
}

h1 {
  font-family: 'Georgia', serif; 
  font-size: 32px; 
  font-weight: bold;
  margin-bottom: 20px;
}


button {
  padding: 12px;
  font-size: 16px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  width: 100%;
  transition: all 0.2s ease-in-out;
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
  margin-bottom: 15px;
}

button:hover {
  transform: scale(1.03);
}
</style>
