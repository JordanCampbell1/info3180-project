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
          <button class="btn btn-secondary" @click="setFilter('username')">Name</button>
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
              :src="profile.photo ? `http://localhost:8080/uploads/${profile.photo}` : `http://localhost:8080/uploads/defaultAvatar.png`"
              class="card-img-top profile-img"
              alt="Profile photo"
            />
          </div>
          <div class="card-body">
            <h5 class="card-title">{{ profile.username }}</h5>
            <p class="card-text mb-1"><strong>Sex:</strong> {{ profile.sex }}</p>
            <p class="card-text mb-1"><strong>Race:</strong> {{ profile.race }}</p>
            <p class="card-text mb-1"><strong>Parish:</strong> {{ profile.parish }}</p>
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
import axios from 'axios'

// State
const allProfiles = ref([])
const profiles = ref([])
const searchText = ref('')
const filterKey = ref('')
const loading = ref(false)
const error = ref('')

// Computed
const displayedProfiles = computed(() => {
  if (searchText.value && filterKey.value) {
    return allProfiles.value.filter(profile => {
      const value = String(profile[filterKey.value] || '').toLowerCase()
      return value.includes(searchText.value.toLowerCase())
    })
  }
  return profiles.value
})

// Methods
const fetchProfiles = async () => {
  loading.value = true
  error.value = ''
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      error.value = 'Not authenticated. Please log in.'
      return
    }

    const res = await axios.get('http://localhost:8080/api/profiles', {
      headers: { Authorization: `Bearer ${token}` }
    })

    allProfiles.value = res.data
    profiles.value = [...allProfiles.value].slice(-4).reverse()
  } catch (err) {
    console.error('Error fetching profiles:', err)
    error.value = err.response?.data?.message || 'Failed to load profiles'
  } finally {
    loading.value = false
  }
}

const setFilter = key => {
  filterKey.value = key
  searchText.value = ''
}

const clearSearch = () => {
  filterKey.value = ''
  searchText.value = ''
}

function formatDate(dateStr) {
  const options = { year: 'numeric', month: 'short', day: 'numeric' }
  return new Date(dateStr).toLocaleDateString(undefined, options)
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

</style>
