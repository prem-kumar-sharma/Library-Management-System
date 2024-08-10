<template>
  <div>
    <h1>Edit Book</h1>
    <form @submit.prevent="editBook">
      <div class="mb-3">
        <label for="editBook" class="form-label">Select Book to Edit:</label>
        <select v-model="selectedBookId" id="editBook" class="form-control" required>
          <option value="" disabled>Select a book</option>
          <option v-for="book in books" :key="book.id" :value="book.id">{{ book.name }}</option>
        </select>
      </div>
      <div v-if="selectedBook">
        <div class="mb-3">
          <label for="editName" class="form-label">Book Name:</label>
          <input v-model="selectedBook.name" type="text" id="editName" class="form-control" required>
        </div>
        <div class="mb-3">
          <label for="editAuthor" class="form-label">Author:</label>
          <input v-model="selectedBook.author" type="text" id="editAuthor" class="form-control" required>
        </div>
        <div class="mb-3">
          <label for="editSection">Section:</label>
          <select v-model="selectedBook.section_id" id="editSection" class="form-control" required>
            <option v-for="section in sections" :key="section.id" :value="section.id">{{ section.name }}</option>
          </select>
        </div>
        <div class="mb-3">
          <label for="editContent" class="form-label">Content:</label>
          <textarea v-model="selectedBook.content" id="editContent" class="form-control" rows="4" required></textarea>
        </div>
        <div class="mb-3">
          <label for="editImage" class="form-label">Upload Image:</label>
          <input type="file" @change="handleImageUpload" id="editImage" class="form-control" accept="image/*">
        </div>
        <button type="submit" class="btn btn-primary">Save Changes</button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'EditBook',
  data() {
    return {
      selectedBookId: '',
      selectedBook: null,
      books: [], // Populate books data
      sections: [], // Populate sections data
    };
  },
  mounted() {
    // Fetch books and sections data when component is mounted
    this.fetchBooks();
    this.fetchSections();
  },
  methods: {
    async fetchBooks() {
      // Fetch books from the server
      try {
        const response = await fetch('http://localhost:5000/get_books', {
          method: 'GET'
        });
        if (response.ok) {
          const data = await response.json();
          this.books = data;
        } else {
          throw new Error('Failed to fetch books');
        }
      } catch (error) {
        console.error('Error fetching books:', error.message);
      }
    },
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
    handleImageUpload(event) {
      // Handle image upload and set it to selectedBook.image (e.g., display preview)
      const file = event.target.files[0];
      if (file) {
        // Assuming you want to display the image preview
        const reader = new FileReader();
        reader.onload = () => {
          this.selectedBook.image = reader.result; // Set image data (URL or base64)
        };
        reader.readAsDataURL(file); // Read file as data URL
      }
    },
    async editBook() {
  try {
    const formData = new FormData();
    formData.append('name', this.selectedBook.name);
    formData.append('author', this.selectedBook.author);
    formData.append('section_id', this.selectedBook.section_id);
    formData.append('content', this.selectedBook.content);
    if (this.selectedBook.image) {
      formData.append('image', this.selectedBook.image);
    }

    const response = await fetch(`http://localhost:5000/edit_book/${this.selectedBook.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json', // Set Content-Type to JSON
      },
      body: JSON.stringify(Object.fromEntries(formData)), // Convert FormData to JSON
    });

    if (response.ok) {
      // Handle success
      alert('Book updated successfully');
    } else {
      // Handle error
      throw new Error('Failed to update book');
    }
  } catch (error) {
    console.error('Error editing book:', error.message);
  }
},

  },
  watch: {
    selectedBookId(newValue) {
      // Update selectedBook when selectedBookId changes
      this.selectedBook = this.books.find(book => book.id === newValue);
    },
  },
};
</script>

<style scoped>
/* Add scoped styles here */
</style>
