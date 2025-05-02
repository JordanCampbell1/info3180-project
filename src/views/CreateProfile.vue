<template>
    <div class="container mt-5">
      <div class="card shadow-lg">
        <div class="card-header bg-primary text-white">
          <h4 class="mb-0">Create New Profile</h4>
        </div>
        <div class="card-body">
          <form @submit.prevent="submitProfile">
            <div class="row mb-3">
              <div class="col-md-6">
                <label class="form-label">Biography</label>
                <textarea v-model="form.biography" class="form-control" rows="2" required></textarea>
              </div>
              <div class="col-md-6">
                <label class="form-label">Description</label>
                <textarea v-model="form.description" class="form-control" rows="2" required></textarea>
              </div>
            </div>
  
            <div class="row mb-3">
              <div class="col-md-4">
                <label class="form-label">Parish</label>
                <input v-model="form.parish" type="text" class="form-control" required />
              </div>
              <div class="col-md-4">
                <label class="form-label">Sex</label>
                <select v-model="form.sex" class="form-select" required>
                  <option value="">Select</option>
                  <option>Male</option>
                  <option>Female</option>
                </select>
              </div>
              <div class="col-md-4">
                <label class="form-label">Race</label>
                <input v-model="form.race" type="text" class="form-control" required />
              </div>
            </div>
  
            <div class="row mb-3">
              <div class="col-md-3">
                <label class="form-label">Birth Year</label>
                <input v-model.number="form.birth_year" type="number" class="form-control" required />
              </div>
              <div class="col-md-3">
                <label class="form-label">Height (m)</label>
                <input v-model.number="form.height" type="number" step="0.01" class="form-control" required />
              </div>
              <div class="col-md-3">
                <label class="form-label">Favourite Cuisine</label>
                <input v-model="form.fav_cuisine" type="text" class="form-control" required />
              </div>
              <div class="col-md-3">
                <label class="form-label">Favourite Colour</label>
                <input v-model="form.fav_colour" type="text" class="form-control" required />
              </div>
            </div>
  
            <div class="row mb-3">
              <div class="col-md-6">
                <label class="form-label">Favourite School Subject</label>
                <input v-model="form.fav_school_subject" type="text" class="form-control" required />
              </div>
              <div class="col-md-6">
                <label class="form-label">Beliefs</label>
                <div class="form-check">
                  <input v-model="form.political" class="form-check-input" type="checkbox" id="political" />
                  <label class="form-check-label" for="political">Political</label>
                </div>
                <div class="form-check">
                  <input v-model="form.religious" class="form-check-input" type="checkbox" id="religious" />
                  <label class="form-check-label" for="religious">Religious</label>
                </div>
                <div class="form-check">
                  <input v-model="form.family_oriented" class="form-check-input" type="checkbox" id="family_oriented" />
                  <label class="form-check-label" for="family_oriented">Family Oriented</label>
                </div>
              </div>
            </div>
  
            <div class="text-end">
              <button type="submit" class="btn btn-success">Create Profile</button>
            </div>
  
            <div v-if="message" class="alert mt-3" :class="messageType">
              {{ message }}
            </div>
          </form>
        </div>
      </div>
    </div>
  </template>
  
<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const userStr = localStorage.getItem('user')
const user = JSON.parse(userStr)

console.log('User ID:', user.id)



// State
const csrfToken = ref('')
const form = ref({
  description: '',
  parish: '',
  biography: '',
  sex: '',
  race: '',
  birth_year: '',
  height: '',
  fav_cuisine: '',
  fav_colour: '',
  fav_school_subject: '',
  political: false,
  religious: false,
  family_oriented: false,
  user_id: user.id,
})
const message = ref('')
const messageType = ref('')

// Fetch CSRF token on mount
const fetchCSRFToken = async () => {
  try {
    const res = await axios.get('http://localhost:8080/api/csrf-token', { withCredentials: true })
    csrfToken.value = res.data.csrf_token
  } catch (err) {
    console.error('Failed to fetch CSRF token:', err)
    message.value = 'Unable to get CSRF token.'
    messageType.value = 'alert-danger'
  }
}

// Submit profile
const submitProfile = async () => {
  message.value = ''
  try {
    await axios.post('http://localhost:8080/api/profiles', form.value, {
      headers: {
        'X-CSRFToken': csrfToken.value,
      },
      withCredentials: true
    })
    message.value = 'Profile created successfully!'
    messageType.value = 'alert-success'
    Object.keys(form.value).forEach(key => form.value[key] = typeof form.value[key] === 'boolean' ? false : '')
  } catch (err) {
    console.error(err)
    message.value = err.response?.data?.message || 'Failed to create profile.'
    messageType.value = 'alert-danger'
  }
}

// Fetch CSRF token once
onMounted(fetchCSRFToken)
</script>