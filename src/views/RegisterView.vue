<template>
  <div class="register-container">
    <div class="form-box">
      <h2>Register</h2>
      <form @submit.prevent="register">
        <input v-model="username" placeholder="Username" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <input v-model="name" placeholder="Name" required />
        <input v-model="email" placeholder="Email" required />
        <button type="submit">Register</button>
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
      password: '',
      csrf_token: ''
    };
  },
  async created() {
    try {
      const response = await axios.get('/api/csrf-token');
      this.csrf_token = response.data.csrf_token;
    } catch (error) {
      console.error('Failed to get CSRF token:', error);
    }
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('/api/auth/login', {
          username: this.username,
          password: this.password,
          csrf_token: this.csrf_token
        });

        const token = response.data.token;
        // Save JWT Token
        localStorage.setItem('token', token);

        // Set default Authorization header for Axios
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
.register-container {
  background-color: #e0f7fa;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.form-box {
  background-color: white;
  padding: 40px 30px;
  border-radius: 12px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

input {
  display: block;
  width: 100%;
  margin: 10px 0;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 14px;
}

button {
  width: 100%;
  padding: 12px;
  background-color: #ff5c8a;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #e14b76;
}
</style>
