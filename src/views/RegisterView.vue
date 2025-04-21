<template>
  <div class="register">
    <h2>Register</h2>
    <form @submit.prevent="register">
      <input v-model="username" placeholder="Username" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <input v-model="name" placeholder="Name" required />
      <input v-model="email" placeholder="Email" required />
      <button type="submit">Register</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      name: '',
      email: ''
    };
  },
  methods: {
    async register() {
      try {
        await axios.post('/api/register', {
          username: this.username,
          password: this.password,
          name: this.name,
          email: this.email
        });
        this.$router.push('/login');
      } catch (error) {
        alert('Registration failed');
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
