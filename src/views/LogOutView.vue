<template>
    <div class="logout-container">
      <div class="message-box">
        <h2>Logging Out</h2>
        <p>You are about to log out. Please wait...</p>
      </div>
    </div>
  </template>
  
  <script>
  import { useRouter } from 'vue-router';
  import api from '../api';
  
  export default {
    async mounted() {
      try {
        const token = localStorage.getItem('token');
        if (!token) throw new Error('No token found');
  
        await api.post('/api/auth/logout', {}, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
  
        // Clean up the local storage
        localStorage.removeItem('token');
        localStorage.removeItem('user');
  
        // Redirect to the login page after logging out
        this.$router.push('/login');
      } catch (error) {
        console.error('Logout failed:', error);
        alert('An error occurred while logging out');
        this.$router.push('/');
      }
    },
  };
  </script>
  
  <style scoped>
  .logout-container {
    /* background-image: url('@/assets/logout-pic.png'); */
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
  }
  
  .message-box {
    background-color: white;
    padding: 40px 30px;
    border-radius: 12px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    text-align: center;
    width: 100%;
    max-width: 400px;
  }
  
  h2 {
    color: #ff5c8a;
    font-size: 1.5rem;
  }
  
  p {
    font-size: 1rem;
    color: #333;
  }
  </style>
  