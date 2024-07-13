<!-- SearchBar.vue -->
<template>
    <div>
      <input type="text" v-model="searchQuery" @input="handleInput" placeholder="Search...">
      <button @click="search">Search</button>
  
      <div v-if="searchResults.books.length > 0">
        <h2>Books:</h2>
        <ul>
          <li v-for="book in searchResults.books" :key="book.id">{{ book.name }} by {{ book.author }}</li>
        </ul>
      </div>
  
      <div v-if="searchResults.sections.length > 0">
        <h2>Sections:</h2>
        <ul>
          <li v-for="section in searchResults.sections" :key="section.id">{{ section.name }} - {{ section.description }}</li>
        </ul>
      </div>
  
      <div v-if="errorMessage">{{ errorMessage }}</div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        searchQuery: '',
        searchResults: { books: [], sections: [] },
        errorMessage: ''
      };
    },
    methods: {
      handleInput() {
        this.errorMessage = '';
      },
      search() {
        if (!this.searchQuery.trim()) {
          this.errorMessage = 'Please enter a search query';
          return;
        }
  
        // Make a GET request to the backend search API
        axios.get(`http://localhost:5000/search?query=${encodeURIComponent(this.searchQuery)}`)
          .then(response => {
            this.searchResults = response.data;
            this.errorMessage = '';
          })
          .catch(error => {
            this.errorMessage = 'An error occurred while fetching search results';
            console.error(error);
          });
      }
    }
  };
  </script>
  
  <style scoped>
  /* Add custom styles for SearchBar component if needed */
  </style>
  