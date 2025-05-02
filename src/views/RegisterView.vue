<template>
  <div class="register-container">
    <div class="form-box">
      <h2>Register</h2>
      <form @submit.prevent="register">
        <input v-model="username" placeholder="Username" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <input v-model="name" placeholder="Name" required />
        <input v-model="email" type="email" placeholder="Email" required />
        <button type="submit">Register</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

// Send cookies (for CSRF token)
axios.defaults.withCredentials = true;

export default {
  data() {
    return {
      username: '',
      password: '',
      name: '',
      email: '',
      csrfToken: ''
    };
  },
  async mounted() {
    try {
      const { data } = await axios.get('http://localhost:8080/api/csrf-token');
      this.csrfToken = data.csrf_token;
    } catch (e) {
      console.error('Could not fetch CSRF token:', e);
    }
  },
  methods: {
    async register() {
      try {
        const formData = new FormData();
        formData.append('username', this.username);
        formData.append('password', this.password);
        formData.append('name', this.name);
        formData.append('email', this.email);

        // Always include default avatar
        const resp = await fetch('/defaultAvatar.jpg');
        const blob = await resp.blob();
        const file = new File([blob], 'defaultAvatar.jpg', { type: blob.type });
        formData.append('photo', file);

        await axios.post('http://localhost:8080/api/register', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'X-CSRFToken': this.csrfToken
          }
        });

        this.$router.push('/login');
      } catch (error) {
        const data = error.response?.data;
        if (data?.errors) {
          alert(Object.values(data.errors).flat().join('\n'));
        } else {
          alert(data?.message || 'Registration failed');
        }
        console.error(error);
      }
    }
  }
};
</script>

<style scoped>
.register-container {
  background-image: url('@/assets/register-pic.png');
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
