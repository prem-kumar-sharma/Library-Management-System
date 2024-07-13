<template>
  <div class="container">
    <h2 class="mt-4">Add Section</h2>
    <form @submit.prevent="addSection" class="mb-4">
      <div class="mb-3">
        <label for="name" class="form-label">Name:</label>
        <input v-model="name" type="text" id="name" class="form-control" required>
      </div>
      <div class="mb-3">
        <label for="description" class="form-label">Description:</label>
        <textarea v-model="description" id="description" rows="4" class="form-control" required></textarea>
      </div>
      <!-- Display error message -->
      <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>
      <div class="d-grid gap-2">
        <button type="submit" class="btn btn-primary">Add Section</button>
      </div>
    </form>
  </div>
</template>

  
  <script>
  export default {
    data() {
      return {
        name: '',
        description: '',
        errorMessage: '' // Initialize error message
      };
    },
    methods: {
      async addSection() {
  try {
    const response = await fetch('http://localhost:5000/add-section', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      },
      body: JSON.stringify({
        name: this.name,
        description: this.description,
      }),
    });

    if (response.ok) {
      // Handle successful response
      console.log('Section added successfully');
      alert('Section added successfully');
      
    } else {
      const data = await response.json();
      throw new Error(data.message || 'Failed to add section');
    }
  } catch (error) {
    console.error('An error occurred during section addition:', error.message);
    // Handle error display or other actions
  }
}
    }
  };
  </script>
  
  <style scoped>
  /* Add any scoped styles here */
  </style>
  