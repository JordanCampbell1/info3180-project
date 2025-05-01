<template>
  <div class="about container">
    <div>

    </div>
    <br>
    <br>
    <div id="container">
      <div id="inner-container-top">
        <div id="content">
          <h2>Search</h2>
          <input 
            v-model="searchText" 
            type="text" 
            placeholder="Enter search text..." 
            class="search-bar"
          />
        </div>
      </div>
      <div id="inner-container-bottom">
        <button class="button" @click="setFilter('username')">Name</button>
        <button class="button" @click="setFilter('birth_year')">Birth</button>
        <button class="button" @click="setFilter('sex')">Sex</button>
        <button class="button" @click="setFilter('race')">Race</button>
        <button class="button" @click="clearSearch">Clear</button>
      </div>
    </div>

    <br>
    <div id="profiles">
      <div 
        v-for="profile in displayedProfiles" 
        :key="profile.id" 
        class="profile-card">
        <div class="profile-card-content">
          <img :src="profile.photo || 'default-avatar.png'" alt="profile picture" class="profile-image"/>
          <div class="profile-name">{{ profile.user_id }}</div>
        </div>
      </div>

      <!-- Show message if no profiles -->
      <div v-if="!loading && displayedProfiles.length === 0" class="no-profiles">
        No profiles found.
      </div>
      <div v-if="loading" class="loading-message">
        Loading profiles...
      </div>
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      allProfiles: [],
      profiles: [],
      searchText: '',
      filterKey: '',
      loading: false,
      error: ''
    };
  },
  computed: {
    displayedProfiles() {
      if (this.searchText && this.filterKey) {
        return this.allProfiles.filter(profile => {
          const value = String(profile[this.filterKey] || '').toLowerCase();
          return value.includes(this.searchText.toLowerCase());
        });
      }
      return this.profiles;
    }
  },
  methods: {
    async fetchProfiles() {
      this.loading = true;
      this.error = '';
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          this.error = 'Not authenticated. Please log in.';
          return;
        }
        const res = await axios.get(
          'http://localhost:8080/api/profiles',
          { headers: { Authorization: `Bearer ${token}` } }
        );
        this.allProfiles = res.data;
        this.profiles = [...this.allProfiles].slice(-4).reverse();
      } catch (error) {
        console.error('Error fetching profiles:', error);
        this.error = error.response?.data?.message || 'Failed to load profiles';
      } finally {
        this.loading = false;
      }
    },
    setFilter(key) {
      this.filterKey = key;
      this.searchText = '';
    },
    clearSearch() {
      this.filterKey = '';
      this.searchText = '';
    }
  },
  mounted() {
    this.fetchProfiles();
  }
};
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
</style>
