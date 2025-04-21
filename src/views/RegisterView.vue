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
.login-container {
  background-color: #e0f7fa;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.form-box {
  background-color: white;
  padding: 40px;
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
</style>
