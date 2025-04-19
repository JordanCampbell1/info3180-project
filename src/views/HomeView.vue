<script setup>
import { ref } from "vue";

let message = ref("Hello World! This is a VueJS and Flask Starter Template.")

</script>

<template>
    <div class="container">
      <div class="text-center">
        <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />
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

<style>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  flex-direction: column;
  text-align: center;
}

.logo {
  margin-bottom: 20px;
}

button {
  padding: 10px 20px;
  margin: 10px;
  font-size: 16px;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.btn-primary {
  background-color: #42b983;
  color: white;
}

.btn-secondary {
  background-color: #35495e;
  color: white;
}

button:hover {
  transform: scale(1.05);
}
/* Add any component specific styles here */
</style>
