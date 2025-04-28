<script setup>
import { ref } from "vue";

let message = ref("Welcome to Jam-Date💕  Find your perfect match today! 💕")
let sidebarOpen = ref(false);

function toggleSidebar() {
  sidebarOpen.value = !sidebarOpen.value;
}
</script>

<template>
  <div class="home-container">
    <!-- Sidebar Menu Button -->
    <button class="menu-button" @click="toggleSidebar">
      ☰ Menu
    </button>

    <!-- Sidebar -->
    <div class="sidebar" :class="{ open: sidebarOpen }">
      <router-link to="/profiles/favourites">
        <button class="btn btn-report">View Reports</button>
      </router-link>
      <router-link to="/register">
        <button class="btn btn-register">Register</button>
      </router-link>
      <router-link to="/login">
        <button class="btn btn-login">Login</button>
      </router-link>
    </div>

    <!-- Main Content -->
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

.menu-button {
  position: absolute;
  top: 20px;
  left: 20px;
  background-color: #2196f3;
  color: white;
  border: none;
  padding: 12px 16px;
  border-radius: 8px;
  cursor: pointer;
  z-index: 1000;
}

.sidebar {
  position: absolute;
  top: 0;
  left: -200px; 
  width: 200px;
  height: 100%;
  background-color: rgba(0,0,0,0.8);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  z-index: 500;
}

.sidebar.open {
  left: 0; 
}

.btn-report {
  background-color: #e6f4f5;
  color: white;
  width: 150px;
}

.btn-register {
  background-color: #e6f4f5;
  color: white;
  width: 150px;
}

.btn-login {
  background-color: #e6f4f5;
  color: white;
  width: 150px;
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

button:hover {
  transform: scale(1.03);
}
</style>
