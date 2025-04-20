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
</style>
📁 Make sure you put an image like dating-bg.jpg in src/assets/.

✅ 2. Add "View Reports" Button
You're already doing that in the update above:

vue
Copy
Edit
<router-link to="/profiles/favourites">
  <button class="btn btn-report m-2">View Reports</button>
</router-link>
✅ Route /profiles/favourites will lead to your report view.

✅ 3. Add Solid Background Colors to Login + Register Pages
Update both LoginView.vue and RegisterView.vue like this:

🔁 Example for LoginView.vue:
vue
Copy
Edit
<template>
  <div class="login-container">
    <div class="form-box">
      <h2>Login</h2>
      <form @submit.prevent="login">
        <input v-model="username" placeholder="Username" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <button type="submit">Login</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('/api/auth/login', {
          username: this.username,
          password: this.password
        });
        const token = response.data.token;
        localStorage.setItem('token', token);
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        this.$router.push('/');
      } catch (error) {
        alert('Login failed');
        console.error(error);
      }
    }
  }
};
</script>

<style scoped>
.login-container {
  background-color: #ffe3ec;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.form-box {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

input {
  display: block;
  width: 100%;
  margin: 10px 0;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

button {
  background-color: #ff5c8a;
  color: white;
  border: none;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  width: 100%;
}
/* Add any component specific styles here */
</style>
