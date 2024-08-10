<template>
  <div>
    <h1>Edit Section</h1>
    <form @submit.prevent="editSection">
      <div class="mb-3">
        <label for="editSection" class="form-label">Select Section to Edit:</label>
        <select v-model="selectedSectionId" id="editSection" class="form-control" required>
          <option value="" disabled>Select a section</option>
          <option v-for="section in sections" :key="section.id" :value="section.id">{{ section.name }}</option>
        </select>
      </div>
      <div v-if="selectedSection">
        <div class="mb-3">
          <label for="editName" class="form-label">Section Name:</label>
          <input v-model="selectedSection.name" type="text" id="editName" class="form-control" required>
        </div>
        <div class="mb-3">
          <label for="editDescription" class="form-label">Description:</label>
          <textarea v-model="selectedSection.description" id="editDescription" class="form-control" rows="4" required></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Save Changes</button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'EditSection',
  data() {
    return {
      selectedSectionId: '',
      selectedSection: null,
      sections: [], // Populate sections data
    };
  },
  mounted() {
    // Fetch sections data when component is mounted
    this.fetchSections();
  },
  methods: {
    async fetchSections() {
      // Fetch sections from the server
      try {
        const response = await fetch('http://localhost:5000/sections');
        if (response.ok) {
          const data = await response.json();
          this.sections = data;
        } else {
          throw new Error('Failed to fetch sections');
        }
      } catch (error) {
        console.error('Error fetching sections:', error.message);
      }
    },
    async editSection() {
  try {
    const formData = {
      name: this.selectedSection.name,
      description: this.selectedSection.description,
    };

    const response = await fetch(`http://localhost:5000/edit-section/${this.selectedSection.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    });

    if (response.status === 200) {
      // Handle success
      alert('Section updated successfully');
      this.$router.push(`/AdminDashboard`); // Use ${} to interpolate variables
      // Optionally, redirect or update UI
    } else if (response.status === 400) {
      // Handle bad request (e.g., missing fields)
      throw new Error('Bad request: missing fields');
    } else if (response.status === 404) {
      // Handle not found (e.g., section ID not valid)
      throw new Error('Section not found');
    } else {
      // Handle other errors
      throw new Error('Failed to update section');
    }
  } catch (error) {
    console.error('Error editing section:', error.message);
    alert('Failed to update section');
  }
},

  },
  watch: {
    selectedSectionId(newValue) {
      // Update selectedSection when selectedSectionId changes
      this.selectedSection = this.sections.find(section => section.id === newValue);
    },
  },
};
</script>

<style scoped>
/* Add scoped styles here */
</style>
