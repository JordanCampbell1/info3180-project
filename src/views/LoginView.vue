<template>
  <div class="login-container">
    <div class="form-box">
      <h2>Login</h2>
      <form @submit.prevent="login">
        <input v-model="username" placeholder="Username" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <button type="submit">Login</button>
      </form>

      <!-- Registration Link -->
      <p class="register-link">
        Don't have an account? 
        <router-link to="/register" class="register-link-btn">Register Here</router-link>
      </p>

    </div>
  </div>
</template>

<script>
import api from '../api';  // Adjust the path as necessary
import { API_BASE_URL } from '../config';

// Ensure cookies (for CSRF) are always sent
api.defaults.withCredentials = true;

export default {
  data() {
    return {
      username: '',
      password: '',
      csrfToken: ''
    };
  },

  async mounted() {
    try {

      console.log("VITE_API_URL =", API_BASE_URL);

      console.log("mounted hook running...");
      const { data } = await api.get('/api/csrf-token');
      console.log("CSRF token fetched:", data.csrf_token);
      this.csrfToken = data.csrf_token;
    } catch (e) {
      console.error('Could not fetch CSRF token:', e);
    }
  },

  methods: {
    async login() {
      try {
        console.log("Login button clicked");

        // Format request correctly for Flask-WTF
        const formData = new URLSearchParams();
        formData.append("username", this.username);
        formData.append("password", this.password);

        console.log("Attempting login with URL encoded format:", formData.toString());

        const response = await api.post("/api/auth/login", formData, {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",  // Flask-WTF expects this format
            "X-CSRFToken": this.csrfToken  // Include CSRF token
          }
        });

        const token = response.data.token;
        console.log("Token received:", token);
        localStorage.setItem("token", token);
        localStorage.setItem("user", JSON.stringify(response.data.user));
        api.defaults.headers.common["Authorization"] = `Bearer ${token}`;

        console.log("Login successful, redirecting...");
        this.$router.push("/");
      }
       catch (error) {
        console.error("Login error:", error.response?.data || error);
        alert(error.response?.data?.message || "Login failed");
      }
    }


  }
};
</script>


<style scoped>
.login-container {
  background-image: url('@/assets/login-picture.jpg');
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.form-box {
  background-color: white;
  padding: 40px 20px;
  border-radius: 12px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 320px;
  text-align: center;
}

input {
  display: block;
  width: 100%;
  margin: 12px 0;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 14px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #9c27b0;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #8e14a3;
}

.register-link {
  margin-top: 1rem;
  text-align: center;
  font-size: 0.9rem;
  color: #333;
}

.register-link-btn {
  color: #9c27b0; /* Primary button color */
  font-weight: bold;
  text-decoration: none;
  padding: 0.3rem 0.6rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.register-link-btn:hover {
  background-color: #9c27b0;
  color: white;
  text-decoration: none;
}

.register-link-btn:active {
  background-color: #9c27b0;
}


</style>