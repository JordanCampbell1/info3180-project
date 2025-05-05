<template>
  <div class="container mt-4">
    <h2 class="mb-4">Latest Profiles</h2>

    <!-- Search Box -->
    <div class="mb-4 p-3 bg-light rounded">
      <div class="row g-2 align-items-center">
        <div class="col-md-6">
          <input
            v-model="searchText"
            type="text"
            placeholder="Search..."
            class="form-control"
          />
        </div>
        <div class="col-md-6 d-flex justify-content-md-end gap-2 flex-wrap">
          <button class="btn btn-secondary" @click="setFilter('name')">Name</button>
          <button class="btn btn-secondary" @click="setFilter('birth_year')">Birth Year</button>
          <button class="btn btn-secondary" @click="setFilter('sex')">Sex</button>
          <button class="btn btn-secondary" @click="setFilter('race')">Race</button>
          <button class="btn btn-outline-danger" @click="clearSearch">Clear</button>
        </div>
      </div>
    </div>

    <!-- Profiles Grid -->
    <div class="row">
      <div v-for="profile in displayedProfiles" :key="profile.id" class="col-12 col-sm-6 col-lg-3 mb-4">
        <div class="card h-100 shadow-sm">
          <div class="img-container">
            <img
              :src="profile.photo ? `${API_BASE_URL}/uploads/${profile.photo}` : defaultAvatar"
              class="card-img-top profile-img"
              alt="Profile photo"
            />
          </div>
          <div class="card-body d-flex flex-column">
            <h5 class="card-title">{{ profile.name }}</h5>
            <p class="card-text mb-1"><strong>Sex:</strong> {{ profile.sex }}</p>
            <p class="card-text mb-1"><strong>Race:</strong> {{ profile.race }}</p>
            <p class="card-text mb-1"><strong>Parish:</strong> {{ profile.parish }}</p>

            <!-- View More Button -->
            <router-link 
              :to="`/profiles/${profile.id}`" 
              class="btn btn-outline-pink mt-auto"
            >
              View More Details
            </router-link>
          </div>

          <div class="card-footer text-muted small text-end">
            Joined: {{ formatDate(profile.date_joined) }}
          </div>
        </div>
      </div>
    </div>

    <!-- Messages -->
    <div v-if="!loading && displayedProfiles.length === 0" class="alert alert-info text-center">
      No profiles found.
    </div>
    <div v-if="loading" class="alert alert-warning text-center">
      Loading profiles...
    </div>
    <div v-if="error" class="alert alert-danger text-center">
      {{ error }}
    </div>
  </div>
</template>



<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../api'
import { API_BASE_URL } from '../config'
import defaultAvatar from '@/assets/defaultAvatar.jpg';


// State
const allProfiles = ref([])
const profiles = ref([])
const searchText = ref('')
const filterKey = ref('')
const loading = ref(false)
const error = ref('')
const searching = ref(false)


// Computed
const displayedProfiles = computed(() => profiles.value)


// Methods
const fetchProfiles = async () => {
  loading.value = true
  error.value = ''
  searching.value = false

  try {
    const token = localStorage.getItem('token')
    if (!token) {
      error.value = 'Not authenticated. Please log in.'
      return
    }

    const res = await api.get('/api/profiles', {
      headers: { Authorization: `Bearer ${token}` }
    })

    profiles.value = res.data.slice(0, 4) // Only 4 on default load
  } catch (err) {
    console.error('Error fetching profiles:', err)
    error.value = err.response?.data?.message || 'Failed to load profiles'
  } finally {
    loading.value = false
  }
}


const setFilter = (key) => {
  filterKey.value = key
  if (searchText.value) {
    searchProfiles()
  }
}



const clearSearch = () => {
  filterKey.value = ''
  searchText.value = ''
  fetchProfiles() // goes back to 4 latest
}



function formatDate(dateStr) {
  const options = { year: 'numeric', month: 'short', day: 'numeric' }
  return new Date(dateStr).toLocaleDateString(undefined, options)
}

const searchProfiles = async () => {
  loading.value = true
  error.value = ''
  searching.value = true

  try {
    const token = localStorage.getItem('token')
    if (!token) {
      error.value = 'Not authenticated. Please log in.'
      return
    }

    const params = new URLSearchParams()
    if (filterKey.value && searchText.value) {
      params.append(filterKey.value, searchText.value)
    }

    const res = await api.get(`/api/search?${params.toString()}`, {
      headers: { Authorization: `Bearer ${token}` }
    })

    profiles.value = res.data // Full search results
  } catch (err) {
    console.error('Search failed:', err)
    error.value = err.response?.data?.message || 'Search failed'
  } finally {
    loading.value = false
  }
}




// Lifecycle
onMounted(fetchProfiles)
</script>

<style>
  #container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    height: 30vh;
    background-color: rgb(204, 192, 182);
    border-radius: 2ch;
  }

  #inner-container-top {
    display: flex;
    width: 77%;
    height: 25vh;
    background-color: rgb(180, 163, 146);
    color: white;
    padding-left: 16px;
    padding-top: 16px;
  }

  #inner-container-bottom {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 10vh + 1ch;
    background-color: rgb(255, 183, 0);
    margin-bottom: 1ch;
    border-bottom-left-radius: 2ch;
    border-bottom-right-radius: 2ch;
  }

  .search-bar {
    padding: 8px;
    width: 250px;
    border-radius: 6px;
    border: none;
    margin-top: 10px;
    font-size: 16px;
  }

  .button {
    margin-left: 16px;
    margin-top: 32px;
    border-radius: 8px;
    border: none;
    color: white;
    padding: 16px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    transition-duration: 0.4s;
    cursor: pointer;
    background-color: rgb(188, 173, 163);
  }

  #profiles {
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
    gap: 20px;
  }

  .profile-card {
    width: 150px;
    height: 200px;
    background-color: rgba(255, 255, 255, 0.5);
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    padding: 10px;
  }

  .profile-card-content {
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }

  .profile-image {
    width: 100px;
    height: 100px;
    object-fit: cover;
    border-radius: 50%;
    background-color: transparent;
  }

  .profile-name {
    position: absolute;
    bottom: 10px;
    color: white;
    font-weight: bold;
    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.7);
  }

  .no-profiles, .loading-message, .error-message {
    width: 100%;
    text-align: center;
    margin-top: 1rem;
    font-size: 1.2rem;
    color: #333;
  }

  .img-container {
  width: 100%;
  aspect-ratio: 1 / 1; /* Square image container */
  overflow: hidden;
}

.profile-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.btn-outline-pink {
  color: #ff4b91;
  border-color: #ff4b91;
  background-color: transparent;
}

.btn-outline-pink:hover {
  background-color: #ff4b91;
  color: white;
}


</style>
