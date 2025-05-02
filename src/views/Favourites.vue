<template>
    <div class="container my-5">
      <h2 class="mb-4">Favourites Report</h2>
  
      <!-- Section 1: Top 20 Most Favoured Users -->
      <div class="mb-5">
        <h4 class="mb-3">Top 20 Most Favoured Users</h4>
        <div class="row">
          <div
            v-for="user in topFavoured"
            :key="user.id"
            class="col-12 col-sm-6 col-md-4 col-lg-3 mb-4"
          >
            <div class="card h-100 text-center shadow-sm">
              <img
                :src="user.photo ? `http://localhost:8080/uploads/${user.photo}` : `http://localhost:8080/uploads/defaultAvatar.png`"
                class="card-img-top mx-auto d-block mt-3"
                alt="Profile photo"
                style="width: 100px; height: 100px; object-fit: cover; border-radius: 50%;"
              />
              <div class="card-body">
                <h5 class="card-title">{{ user.username }}</h5>
                <p class="text-muted small">Favoured {{ user.favourite_count }} time(s)</p>
              </div>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Section 2: Users You Have Favourited -->
      <div>
        <h4 class="mb-3">Users You Have Favourited</h4>
        <div class="row">
          <div
            v-for="user in favourites"
            :key="user.id"
            class="col-12 col-sm-6 col-md-4 col-lg-3 mb-4"
          >
            <div class="card h-100 text-center shadow-sm">
              <img
                :src="user.photo ? `http://localhost:8080/uploads/${user.photo}` : `http://localhost:8080/uploads/defaultAvatar.png`"
                class="card-img-top mx-auto d-block mt-3"
                alt="Profile photo"
                style="width: 100px; height: 100px; object-fit: cover; border-radius: 50%;"
              />
              <div class="card-body">
                <h5 class="card-title">{{ user.username }}</h5>
                <p class="text-muted small">{{ user.email }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Loading / Error -->
      <div v-if="loading" class="text-center mt-4">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <div v-if="error" class="alert alert-danger mt-4 text-center">
        {{ error }}
      </div>
    </div>
  </template>
  
  <script setup>
  import { onMounted, ref } from 'vue'
  import axios from 'axios'
  
  const userStr = localStorage.getItem('user')
  const user = JSON.parse(userStr)

  console.log('User ID:', user.id)

  const favourites = ref([])
  const topFavoured = ref([])
  const loading = ref(false)
  const error = ref('')
  
  const fetchData = async () => {
    loading.value = true
    try {
      const token = localStorage.getItem('token')
      if (!token) throw new Error('Not authenticated')
  
      const [topRes, myRes] = await Promise.all([
        axios.get('http://localhost:8080/api/users/favourites/20', {
          headers: { Authorization: `Bearer ${token}` }
        }),
        axios.get(`http://localhost:8080/api/users/${user.id}/favourites`, {
          headers: { Authorization: `Bearer ${token}` }
        })
      ])
  
      topFavoured.value = topRes.data
      favourites.value = myRes.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to load favourites'
    } finally {
      loading.value = false
    }
  }
  
  onMounted(fetchData)
  </script>
  