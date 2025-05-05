<template>
  <div class="register-container">
    <div class="form-box">
      <h2>Register</h2>
      <form @submit.prevent="register">
        <input v-model="username" placeholder="Username" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <input v-model="name" placeholder="Name" required />
        <input v-model="email" type="email" placeholder="Email" required />
        <!-- Profile Picture Label and File Input -->
        <label for="profile-pic" class="profile-pic-label">Choose a Profile Picture (jpg, jpeg, png)</label>
        <input
          type="file"
          id="profile-pic"
          @change="handleFile"
          accept=".jpg, .jpeg, .png"
          class="file-input"
        />
        <button type="submit">Register</button>
      </form>
    </div>
  </div>
</template>


<script>
import api from '../api';
import defaultAvatar from '@/assets/defaultAvatar.jpg'; // ✅ import the image from assets


api.defaults.withCredentials = true;

export default {
  data() {
    return {
      username: '',
      password: '',
      name: '',
      email: '',
      photoFile: null,
      csrfToken: ''
    };
  },
  async mounted() {
    try {
      const { data } = await api.get('/api/csrf-token');
      this.csrfToken = data.csrf_token;
    } catch (e) {
      console.error('Could not fetch CSRF token:', e);
    }
  },
  methods: {
    handleFile(event) {
      this.photoFile = event.target.files[0];
    },
    async register() {
      try {
        const formData = new FormData();
        formData.append('username', this.username);
        formData.append('password', this.password);
        formData.append('name', this.name);
        formData.append('email', this.email);

        // Use uploaded photo or fallback to default
        if (this.photoFile) {
          formData.append('photo', this.photoFile);
        } else {
          const resp = await fetch(defaultAvatar);
          const blob = await resp.blob();
          const file = new File([blob], 'defaultAvatar.jpg', { type: blob.type });
          formData.append('photo', file);
        }

        await api.post('/api/register', formData, {
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

/* Hide the file input */
.file-input {
  display: none;
}

/* Style the label to look like a button */
.profile-pic-label {
  display: block;
  width: 100%;
  padding: 12px;
  background-color: #f5f5f5;
  border: 1px solid #ccc;
  border-radius: 8px;
  text-align: center;
  font-size: 14px;
  color: #333;
  cursor: pointer;
  margin-top: 10px;
  font-weight: 600;
  margin-bottom: 2em;
}

.profile-pic-label:hover {
  background-color: #ff5c8a;
  color: white;
}

.profile-pic-label:active {
  background-color: #e14b76;
  color: white;
}

.profile-pic-label:focus {
  outline: none;
  border-color: #ff5c8a;
}
</style>
