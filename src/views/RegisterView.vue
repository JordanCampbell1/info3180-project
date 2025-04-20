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
