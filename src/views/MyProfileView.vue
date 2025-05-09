<template>
  <div class="container mt-5">
    <!-- User Info Section -->
    <div v-if="loading" class="alert alert-info text-center">Loading user profile...</div>
    <div v-else-if="error" class="alert alert-danger text-center">{{ error }}</div>
    <div v-else>
      <div class="card mb-4 shadow">
        <div class="row g-0">
          <div class="col-md-4 d-flex justify-content-center align-items-center p-3">
            <img
              :src="user.photo ? `${API_BASE_URL}/uploads/${user.photo}` : defaultAvatar"
              class="img-fluid rounded-circle user-img"
              alt="User Photo"
            />
          </div>
          <div class="col-md-8">
            <div class="card-body">
              <h4 class="card-title">{{ user.name }}</h4>
              <p class="card-text"><strong>Email:</strong> {{ user.email }}</p>
              <p class="card-text"><strong>Joined:</strong> {{ formatDate(user.date_joined) }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- All Profiles Created by This User -->
      <h5 class="mb-3">My Profiles</h5>
      <div v-if="profiles.length === 0" class="alert alert-warning text-center">
        You haven't created any profiles yet.
      </div>
      <div class="row">
        <div v-for="profile in profiles" :key="profile.id" class="col-md-4 mb-4">
          <div class="card h-100 shadow-sm">
            <div class="card-body">
              <h5 class="card-title">{{ profile.sex }} - {{ profile.race }}</h5>
              <p class="card-text"><strong>Parish:</strong> {{ profile.parish }}</p>
              <p class="card-text"><strong>Birth Year:</strong> {{ profile.birth_year }}</p>
              <p class="card-text"><strong>Favourite Colour:</strong> {{ profile.fav_colour }}</p>
              <p class="card-text"><strong>Favourite Cuisine:</strong> {{ profile.fav_cuisine }}</p>
              <router-link 
                :to="`/profiles/${profile.id}`" 
                class="btn btn-outline-primary me-2 mt-2"
              >
                View Profile
              </router-link>
              <router-link 
                :to="`/match-report/${profile.id}`" 
                class="btn btn-outline-success mt-2"
              >
                Match Me
              </router-link>
            </div>
            <div class="card-footer text-muted small text-end">
              Created: {{ formatDate(profile.created_at) }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import defaultAvatar from '@/assets/defaultAvatar.jpg'; // ✅ import the image from assets

import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import { API_BASE_URL } from '../config'

const router = useRouter()
const userStr = localStorage.getItem('user')
const userParse = JSON.parse(userStr)
const userId = userParse.id 

//console.log('User ID:', userId)

const user = ref({})
const profiles = ref([])
const loading = ref(true)
const error = ref('')

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

const fetchUserAndProfiles = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) throw new Error('Not authenticated')

    const userRes = await api.get(`/api/users/${userId}`, {
      headers: { Authorization: `Bearer ${token}` }
    })

    const profileRes = await api.get(`/api/users/${userId}/profiles`, {
      headers: { Authorization: `Bearer ${token}` }
    })

    user.value = userRes.data
    profiles.value = profileRes.data
    //console.log('Profiles:', profiles.value)
  }  catch (err) {
    const msg = err.response?.data?.message
    if (msg === 'No profiles found for this user.') {
      router.push('/profiles/new')  // 🔁 Redirect to profile creation page
    } else {
      error.value = msg || 'Could not load profile data.'
    }
  } finally {
    loading.value = false
  }
}

onMounted(fetchUserAndProfiles)
</script>

<style scoped>
.user-img {
  width: 120px;
  height: 120px;
  object-fit: cover;
}
</style>
