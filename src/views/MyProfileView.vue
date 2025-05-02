<template>
    <div class="profile-detail container">
      <h1>Profile Details</h1>
  
      <div v-if="loading">Loading profile...</div>
      <div v-else>
        <div class="profile-info">
          <h2>Main Info</h2>
          <p><strong>ID:</strong> {{ profile.id }}</p>
          <p><strong>Description:</strong> {{ profile.description }}</p>
          <p><strong>Parish:</strong> {{ profile.parish }}</p>
          <p><strong>Biography:</strong> {{ profile.biography }}</p>
          <p><strong>Sex:</strong> {{ profile.sex }}</p>
          <p><strong>Race:</strong> {{ profile.race }}</p>
          <p><strong>Birth Year:</strong> {{ profile.birth_year }}</p>
          <p><strong>Height:</strong> {{ profile.height }} cm</p>
          <p><strong>Favourite Cuisine:</strong> {{ profile.fav_cuisine }}</p>
          <p><strong>Favourite Colour:</strong> {{ profile.fav_colour }}</p>
          <p><strong>Favourite School Subject:</strong> {{ profile.fav_school_subject }}</p>
          <p><strong>Political View:</strong> {{ profile.political }}</p>
          <p><strong>Religious Belief:</strong> {{ profile.religious }}</p>
          <p><strong>Family Oriented:</strong> {{ profile.family_oriented ? 'Yes' : 'No' }}</p>
          <button class="edit-btn" @click="editProfile">Edit Profile</button>
        </div>
  
        <div class="favored-users">
          <h2>Favored Users</h2>
          <div class="favored-list">
            <div 
              v-for="fav in favoredProfiles" 
              :key="fav.id" 
              class="fav-card"
            >
              <img :src="fav.photo || 'default-avatar.png'" class="fav-avatar" />
              <p>{{ fav.username }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  
  const route = useRoute();
  const router = useRouter();
  const profile = ref({});
  const favoredProfiles = ref([]);
  const loading = ref(true);
  
  const fetchProfile = async () => {
    loading.value = true;
    try {
      const res = await fetch(`http://localhost:8080/api/profile/${route.params.id}`);
      const data = await res.json();
      profile.value = data.profile;
      favoredProfiles.value = data.favored_profiles || [];
    } catch (err) {
      console.error("Error fetching profile:", err);
    } finally {
      loading.value = false;
    }
  };
  
  const editProfile = () => {
    router.push(`/edit-profile/${route.params.id}`);
  };
  
  onMounted(() => {
    fetchProfile();
  });
  </script>
  
  <style scoped>
  .profile-detail {
    padding: 2rem;
    background: #f9f6f4;
    border-radius: 1rem;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
  }
  
  .profile-info {
    margin-bottom: 2rem;
  }
  
  .profile-info p {
    margin: 4px 0;
  }
  
  .edit-btn {
    margin-top: 1rem;
    padding: 0.5rem 1.5rem;
    background-color: #fca311;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
  }
  
  .favored-users {
    margin-top: 2rem;
  }
  
  .favored-list {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
  }
  
  .fav-card {
    width: 120px;
    background: white;
    border-radius: 10px;
    padding: 10px;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  
  .fav-avatar {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    object-fit: cover;
  }
  </style>
  