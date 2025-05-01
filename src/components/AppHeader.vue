<template>
  <header>
    <nav class="navbar navbar-expand-lg">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">Jam + Date</a>

        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <div class="d-flex ms-auto align-items-center gap-3">
            <RouterLink to="/" class="nav-link">Home</RouterLink>
            <RouterLink to="/about" class="nav-link">About</RouterLink>
            <button class="btn btn-outline-light" @click="logout">
              Logout
            </button>
          </div>
        </div>

      </div>
    </nav>
    <div class="subheader container-fluid px-4 py-2">
      <RouterLink to="/profile" class="subheader-link">My Profile</RouterLink>
      <span class="divider">/</span>
      <span class="current-page">{{ currentPage }}</span>
    </div>

  </header>
</template>


<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function logout() {
  // Remove token or any auth info
  localStorage.removeItem('token')
  localStorage.removeItem('user') // optional, if stored

  // Redirect to login
  router.push('/login')
}
</script>

<style>
/* Add any component specific styles here */
.navbar {
  background-color: #2f2f2f;
}
.navbar .nav-link {
  color: azure !important;
  font-weight: 500;
  margin-left: 8px;
}

.navbar-brand {
  color: azure !important;
  font-weight: 800;
  font-size: 1.5rem;
  text-decoration: none;
  text-transform: uppercase;
}

.navbar .nav-link:hover {
  text-decoration: underline;
  color: #ffffff;
  margin-right: 24px;
  text-decoration: none;
}

.btn-outline-light {
  color: azure;
  border-color: azure;
}

.btn-outline-light:hover {
  background-color: azure;
  color: #16110c;
}

.subheader {
  background-color: #8e7b67;
  color: #f5f5f5;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
  width: 90%;
  height: 48px;
  border-bottom-left-radius: 2ch;
  border-bottom-right-radius: 2ch;
}

.subheader-link {
  color: #ffc107;
  text-decoration: none;
  font-weight: bold;
}

.subheader-link:hover {
  text-decoration: underline;
}

.divider {
  color: #ccc;
}

</style>