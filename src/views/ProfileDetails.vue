<template>
    <div class="container mt-5">
      <div v-if="loading" class="alert alert-info text-center">Loading profile...</div>
      <div v-else-if="error" class="alert alert-danger text-center">{{ error }}</div>
      <div v-else class="card shadow-lg mx-auto" style="max-width: 600px;">
        <div class="row g-0">
          <div class="col-md-5">
            <img
              :src="profile.photo ? `http://localhost:8080/uploads/${profile.photo}` : `http://localhost:8080/uploads/defaultAvatar.png`"
              class="img-fluid rounded-start h-100"
              alt="Profile Picture"
              style="object-fit: cover;"
            />
          </div>
          <div class="col-md-7">
            <div class="card-body">
              <h4 class="card-title mb-2">{{ profile.username }}</h4>
              <p class="card-text"><strong>Bio:</strong> {{ profile.biography || 'N/A' }}</p>
              <p class="card-text mb-1"><strong>Parish:</strong> {{ profile.parish }}</p>
              <p class="card-text mb-1"><strong>Sex:</strong> {{ profile.sex }}</p>
              <p class="card-text mb-1"><strong>Race:</strong> {{ profile.race }}</p>
              <p class="card-text mb-1"><strong>Birth Year:</strong> {{ profile.birth_year }}</p>
              <p class="card-text mb-1"><strong>Height:</strong> {{ profile.height }} in</p>
              <p class="card-text mb-1"><strong>Fav Cuisine:</strong> {{ profile.fav_cuisine }}</p>
              <p class="card-text mb-1"><strong>Fav Colour:</strong> {{ profile.fav_colour }}</p>
              <p class="card-text mb-1"><strong>School Subject:</strong> {{ profile.fav_school_sibject }}</p>
              <p class="card-text mb-1"><strong>Political:</strong> {{ profile.political ? 'Yes' : 'No' }}</p>
              <p class="card-text mb-1"><strong>Religious:</strong> {{ profile.religious ? 'Yes' : 'No' }}</p>
              <p class="card-text mb-1"><strong>Family Oriented:</strong> {{ profile.family_oriented ? 'Yes' : 'No' }}</p>
              <p class="card-text text-muted mt-3 small">Joined: {{ formatDate(profile.date_joined) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import axios from 'axios'
  
  const route = useRoute()
  const profile = ref({})
  const loading = ref(true)
  const error = ref('')
  
  const formatDate = (dateStr) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric' }
    return new Date(dateStr).toLocaleDateString(undefined, options)
  }
  
  const fetchProfile = async () => {
    loading.value = true
    try {
      const token = localStorage.getItem('token')
      const id = route.params.id
  
      const res = await axios.get(`http://localhost:8080/api/profiles/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
  
      profile.value = res.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Profile not found.'
    } finally {
      loading.value = false
    }
  }
  
  onMounted(fetchProfile)
  </script>
  