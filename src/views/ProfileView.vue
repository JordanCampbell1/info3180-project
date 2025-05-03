<template>
  <div class="profile-detail">
    <h1>{{ profile.id ? 'Profile Detail' : 'Create Profile' }}</h1>

    <div v-if="loading">Loading profile...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else>
      <div v-if="!editing" class="profile-section">
        <!-- Dynamic Path Display -->
        <p class="path"><strong>Path:</strong> Home / Profiles / {{ profile.id }}</p>

        <p><strong>ID:</strong> {{ profile.id }}</p>
        <p><strong>Description:</strong> {{ profile.description }}</p>
        <p><strong>Parish:</strong> {{ profile.parish }}</p>
        <p><strong>Biography:</strong> {{ profile.biography }}</p>
        <p><strong>Sex:</strong> {{ profile.sex }}</p>
        <p><strong>Race:</strong> {{ profile.race }}</p>
        <p><strong>Birth Year:</strong> {{ profile.birth_year }}</p>
        <p><strong>Height:</strong> {{ profile.height }}</p>
        <p><strong>Favourite Cuisine:</strong> {{ profile.fav_cuisine }}</p>
        <p><strong>Favourite Colour:</strong> {{ profile.fav_colour }}</p>
        <p><strong>Favourite School Subject:</strong> {{ profile.fav_school_subject }}</p>
        <p><strong>Political View:</strong> {{ profile.political }}</p>
        <p><strong>Religious View:</strong> {{ profile.religious }}</p>
        <p><strong>Family Oriented:</strong> {{ profile.family_oriented ? 'Yes' : 'No' }}</p>

        <div class="buttons">
          <button class="heart-button" @click="addToFavourites" :disabled="loading">❤️ Add to Favourites</button>
          <button class="email-button" :disabled="loading">📧 Email Profile</button>
          <button 
            class="edit-button" 
            @click="startEditing" 
            :disabled="loading || !isOwnProfile"
          >
            ✏️ Edit Profile
          </button>
        </div>
      </div>

      <!-- Edit form -->
      <div v-else class="edit-form">
        <label>Description: <input v-model="editable.description" @blur="validateField('description')" /></label>
        <label>Parish: <input v-model="editable.parish" /></label>
        <label>Biography: <textarea v-model="editable.biography" /></label>
        <label>Sex: <input v-model="editable.sex" /></label>
        <label>Race: <input v-model="editable.race" /></label>
        <label>Birth Year: <input v-model="editable.birth_year" /></label>
        <label>Height: <input v-model="editable.height" /></label>
        <label>Favourite Cuisine: <input v-model="editable.fav_cuisine" /></label>
        <label>Favourite Colour: <input v-model="editable.fav_colour" /></label>
        <label>Favourite School Subject: <input v-model="editable.fav_school_subject" /></label>
        <label>Political View: <input v-model="editable.political" /></label>
        <label>Religious View: <input v-model="editable.religious" /></label>
        <label>Family Oriented:
          <select v-model="editable.family_oriented">
            <option :value="true">Yes</option>
            <option :value="false">No</option>
          </select>
        </label>

        <div class="buttons">
          <button class="save-button" @click="saveProfile" :disabled="saving">
            {{ saving ? 'Saving...' : '💾 Save' }}
          </button>
          <button class="cancel-button" @click="cancelEdit" :disabled="saving">❌ Cancel</button>
        </div>

        <div v-if="editError" style="color: red; margin-top: 1rem;">{{ editError }}</div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { onMounted, ref, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../api';

const route = useRoute();
const router = useRouter();
const profile = ref(null);
const loading = ref(false);
const saving = ref(false);
const error = ref('');
const editError = ref('');
const editing = ref(false);
const editable = ref({});
const user = JSON.parse(localStorage.getItem("user"));

const fetchProfile = async () => {
  const user = JSON.parse(localStorage.getItem("user"));
  
  if (!user?.id) {
    console.error("No user ID in localStorage");
    router.push("/login");
    return;
  }

  try {
    const res = await api.get(`/api/profiles/${user.id}`, {
      headers: { 
        Authorization: `Bearer ${localStorage.getItem("token")}`
      }
    });
    profile.value = res.data;
  } catch (err) {
    if (err.response?.status === 404) {
      // Initialize empty profile if not found
      profile.value = { user_id: user.id };
    } else {
      console.error("Fetch error:", err);
    }
  }
};

const createProfile = async () => {
  console.log("Creating profile with data:", editable.value);
  if (!validateField('description')) return;

  saving.value = true;

  try {
    const token = localStorage.getItem('token');
    // Include user_id in the request
    const profileData = {
      ...editable.value,
      user_id: user.id
    };
    
    const res = await api.post(
      `/api/profiles`,
      profileData,
      { headers: { Authorization: `Bearer ${token}` } }
    );
    console.log("Profile created:", res.data.profile);
    profile.value = res.data.profile;
    editing.value = false;
    alert('Profile created successfully!');
  } catch (err) {
    console.error("Error creating profile:", err);
    editError.value = err.response?.data?.message || 'Failed to create profile.';
  } finally {
    saving.value = false;
  }
};

const saveProfile = async () => {
  console.log("Saving profile with data:", editable.value);
  if (!validateField('description')) return;

  saving.value = true;
  try {
    const token = localStorage.getItem('token');
    const res = await api.put(
      `/api/profiles/${user.id}`,
      editable.value,
      { headers: { Authorization: `Bearer ${token}` } }
    );
    console.log("Profile updated:", res.data);
    profile.value = res.data.profile;
    editing.value = false;
    alert('Profile updated successfully!');
  } catch (err) {
    console.error("Error updating profile:", err);
    editError.value = err.response?.data?.message || 'Failed to update profile.';
  } finally {
    saving.value = false;
  }
};

const addToFavourites = async () => {
  if (!profile.value?.id) {
    alert('Please create a profile first!');
    return;
  }
  
  console.log("Adding profile to favourites:", profile.value.id);
  try {
    const token = localStorage.getItem('token');
    await api.post(
      '/api/favourites',
      { profile_id: profile.value.id },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    console.log("Added to favourites!");
    alert('Added to favourites!');
  } catch (err) {
    console.error("Error adding to favourites:", err);
    alert(err.response?.data?.message || 'Failed to add to favourites.');
  }
};

const startEditing = () => {
  console.log("Starting edit mode");
  editable.value = { ...profile.value };
  editError.value = '';
  editing.value = true;
};

const cancelEdit = () => {
  console.log("Cancelling edit mode");
  editing.value = false;
  editError.value = '';
};

const validateField = (field) => {
  if (!editable.value[field]) {
    editError.value = `${field.replace('_', ' ')} is required.`;
    console.error(editError.value);
    return false;
  }
  editError.value = '';
  return true;
};

onMounted(() => {
  console.log("Component mounted, fetching profile");
  fetchProfile();
});
</script>

<style scoped>
.profile-detail {
  padding: 2rem;
}
.profile-section p {
  margin: 0.5rem 0;
}
.path {
  font-size: 0.95rem;
  color: #777;
  margin-bottom: 1rem;
}
.edit-form label {
  display: block;
  margin-bottom: 1rem;
}
.edit-form input,
.edit-form textarea,
.edit-form select {
  width: 100%;
  padding: 0.5rem;
  margin-top: 0.25rem;
}
.buttons {
  margin-top: 1rem;
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}
.heart-button,
.email-button,
.edit-button,
.save-button,
.cancel-button {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: none;
  font-size: 16px;
  cursor: pointer;
}
.heart-button { background-color: #ffaaaa; }
.email-button { background-color: #aaddff; }
.edit-button { background-color: #ffe599; }
.save-button { background-color: #b6eeb6; }
.cancel-button { background-color: #f4cccc; }
</style>
