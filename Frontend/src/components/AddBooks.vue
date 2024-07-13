<template>
  <div class="container">
    <h1 class="mt-5 mb-4">Add Books to Library</h1>
    <form @submit.prevent="addBook" class="mb-4" enctype="multipart/form-data">
      <div class="mb-3">
        <label for="name" class="form-label">Book Name:</label>
        <input v-model="book.name" type="text" id="name" class="form-control" required>
        <div v-if="errors.name" class="text-danger">{{ errors.name }}</div>
      </div>
      <div class="mb-3">
        <label for="author" class="form-label">Author:</label>
        <input v-model="book.author" type="text" id="author" class="form-control" required>
        <div v-if="errors.author" class="text-danger">{{ errors.author }}</div>
      </div>
      <div class="mb-3">
        <label for="sectionId" class="form-label">Section:</label>
        <select v-model="book.sectionId" id="sectionId" class="form-select" required>
          <option v-for="section in sections" :key="section.id" :value="section.id">{{ section.name }}</option>
        </select>
        <div v-if="errors.sectionId" class="text-danger">{{ errors.sectionId }}</div>
      </div>
      <div class="mb-3">
        <label for="content" class="form-label">Content:</label>
        <textarea v-model="book.content" id="content" class="form-control" rows="4" required></textarea>
        <div v-if="errors.content" class="text-danger">{{ errors.content }}</div>
      </div>
      <div class="mb-3">
        <label for="image" class="form-label">Book Image:</label>
        <input type="file" id="image" ref="fileInput" @change="handleFileChange" class="form-control">
        <div v-if="errors.image" class="text-danger">{{ errors.image }}</div>
      </div>
      <button type="submit" class="btn btn-primary">Add Book</button>
      <div v-if="isAddingBook" class="text-info mt-2">Adding book...</div>
      <div v-if="addBookError" class="text-danger mt-2">{{ addBookError }}</div>
    </form>
  </div>
</template>


<script>
export default {
  name: 'AddBooks',
  data() {
    return {
      book: {
        name: '',
        author: '',
        sectionId: '', // Initialize sectionId to an empty string
        content: '',
        image: null
      },
      sections: [], // Initialize sections as an empty array
      errors: {},
      isAddingBook: false,
      addBookError: null
    };
  },
  mounted() {
    this.fetchSections(); // Fetch sections when the component is mounted
  },
  methods: {
    async fetchSections() {
      try {
        const response = await fetch('http://localhost:5000/sections');
        if (response.ok) {
          const data = await response.json();
          this.sections = data; // Assign fetched sections to the sections array
        } else {
          throw new Error('Failed to fetch sections');
        }
      } catch (error) {
        console.error('Error fetching sections:', error.message);
        // Handle fetch error, show message to user, etc.
      }
    },
    async addBook() {
      this.errors = {}; // Clear any previous errors
      this.isAddingBook = true;
      this.addBookError = null;

      try {
        const formData = new FormData();
        formData.append('name', this.book.name);
        formData.append('author', this.book.author);
        formData.append('sectionId', this.book.sectionId);
        formData.append('content', this.book.content);
        formData.append('image', this.book.image); // Append the image file to the form data

        const response = await fetch('http://localhost:5000/add-book', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          },
          body: formData // Use formData instead of JSON.stringify
        });

        if (response.ok) {
          alert('Book added successfully');
          // Reset book data and optional actions (same as before)
        } else {
          const errorData = await response.json();
          this.errors = errorData.errors || {}; // Handle backend validation errors
          throw new Error(errorData.message || 'Error adding book');
        }
      } catch (error) {
        console.error('Error adding book:', error.message); // Log the specific error message
        this.addBookError = error.message || 'An error occurred while adding book.'; // User-friendly error message
      } finally {
        this.isAddingBook = false; // Stop the loading spinner
      }
    },
    handleFileChange(event) {
      this.book.image = event.target.files[0]; // Update the image field when a file is selected
    }
  }
};
</script>

<style scoped>
/* Add any scoped styles here */
</style>
