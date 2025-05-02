<template>
    <div class="container mt-5">
      <h2 class="mb-4 text-center">Match Results</h2>
  
      <!-- Status messages -->
      <div v-if="loading" class="alert alert-info text-center">Finding your matches...</div>
      <div v-else-if="error" class="alert alert-danger text-center">{{ error }}</div>
      <div v-else-if="matches.length === 0" class="alert alert-warning text-center">No matches found.</div>
  
      <!-- Match Cards -->
      <div class="row">
        <div
          v-for="match in matches"
          :key="match.id"
          class="col-12 col-sm-6 col-lg-4 mb-4"
        >
          <div class="card h-100 shadow-sm">
            <div class="card-body">
              <h5 class="card-title">{{ match.sex }} - {{ match.race }}</h5>
              <p class="card-text mb-1"><strong>Name:</strong> {{ match.name }}</p>
              <p class="card-text mb-1"><strong>Parish:</strong> {{ match.parish }}</p>
              <p class="card-text mb-1"><strong>Birth Year:</strong> {{ match.birth_year }}</p>
              <p class="card-text mb-1"><strong>Cuisine:</strong> {{ match.fav_cuisine }}</p>
              <p class="card-text mb-1"><strong>Colour:</strong> {{ match.fav_colour }}</p>
              <p class="card-text mb-1"><strong>Subject:</strong> {{ match.fav_school_subject }}</p>
              <p class="card-text mb-1"><strong>Political:</strong> {{ match.political ? 'Yes' : 'No' }}</p>
              <p class="card-text mb-1"><strong>Religious:</strong> {{ match.religious ? 'Yes' : 'No' }}</p>
              <p class="card-text mb-1"><strong>Family Oriented:</strong> {{ match.family_oriented ? 'Yes' : 'No' }}</p>

              <div class="mt-3">
                <strong>Matched Fields:</strong>
                <ul class="list-unstyled ms-3 mt-2">
                  <li v-for="field in match.matched_fields" :key="field">
                    ✅ {{ formatField(field) }}
                  </li>
                </ul>
              </div>
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
  const matches = ref([])
  const loading = ref(false)
  const error = ref('')
  
  const profileId = route.params.profileId // passed in URL like /match-report/3
  
  const formatField = (field) => {
    const fieldMap = {
      fav_cuisine: 'Favourite Cuisine',
      fav_colour: 'Favourite Colour',
      fav_school_subject: 'Favourite Subject',
      political: 'Political',
      religious: 'Religious',
      family_oriented: 'Family Oriented',
    }
    return fieldMap[field] || field
  }
  
  const fetchMatches = async () => {
    loading.value = true
    try {
      const token = localStorage.getItem('token')
      const res = await axios.get(`http://localhost:8080/api/profiles/matches/${profileId}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      matches.value = res.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch matches.'
    } finally {
      loading.value = false
    }
  }
  
  onMounted(fetchMatches)
  </script>
  