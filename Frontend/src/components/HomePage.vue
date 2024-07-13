<template>
  <div class="home-page">
    <NavBar></NavBar>

    <div class="container mt-4">
      <h1>Welcome to Our Library Management System!</h1>
      <p class="lead">Explore our collection of e-books and manage your reading journey.</p>

      <div class="input-group mb-3">
        <input v-model="searchQuery" type="text" class="form-control" placeholder="Search books...">
        <button @click="searchBooks" class="btn btn-primary">Search</button>
      </div>

      <div v-if="sections.length > 0" class="mt-4">
        <h2>Sections:</h2>
        <ul class="list-group">
          <li v-for="section in sections" :key="section.id" class="list-group-item">{{ section.name }} - {{ section.description }}</li>
        </ul>
      </div>

      <div v-if="books.length > 0" class="mt-4">
        <h2>Books:</h2>
        <ul class="list-group">
          <li v-for="book in books" :key="book.id" class="list-group-item">
            <div class="d-flex align-items-center">
              <div>
                <img v-if="book.image_url" :src="book.image_url" alt="Book Cover" class="book-image">
                <div v-else class="placeholder-image">No Image Available</div>
              </div>
              <div class="ml-3">
                <h3>{{ book.name }}</h3>
                <p>{{ book.author }}</p>
                <p>Section: {{ book.section }}</p>
                <button @click="requestBook(book.id)" v-if="!isBookRequested(book.id)" class="btn btn-success">
                  Request Book
                </button>
                <button @click="returnBook(book.id)" class="btn btn-warning">
                Return Book
                </button>
              </div>
            </div>
          </li>
        </ul>
      </div>
      <h2 class="mt-4">Submit Feedback:</h2>
      <button @click.prevent="submitFeedback" class="btn btn-primary">Submit Feedback</button>

    </div>
  </div>
</template>


<script>
import NavBar from "@/components/NavBar.vue";


export default {
  name: 'HomePage',
  components: {
    NavBar
  },
  data() {
    return {
      sections: [],
      books: [],
      // feedback: {
      //   bookId: null,
      //   rating: null,
      //   comment: ''
      // },
      searchQuery: ''
    };
  },

  mounted() {
    this.fetchSections();
    this.fetchBooks();
  },
  methods: {
    async fetchSections() {
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
        // Handle fetch error, show message to user, etc.
      }
    },
    async fetchBooks() {
      let apiUrl = 'http://localhost:5000/books';

      if (this.searchQuery.trim() !== '') {
        apiUrl += `?query=${this.searchQuery}`;
      }

      try {
        const response = await fetch(apiUrl, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        });

        if (response.ok) {
          const data = await response.json();
          this.books = data;
        } else if (response.status === 401) {
          // Handle unauthorized access (e.g., redirect to login page)
          alert('Unauthorized access. Please log in.');
          // Redirect to login page or handle as needed
        } else {
          throw new Error('Failed to fetch books');
        }
      } catch (error) {
        console.error('Error fetching books:', error.message);
        // Handle fetch error, show message to user, etc.
      }
    },
    async requestBook(bookId) {
    try {
      const response = await fetch(`http://localhost:5000/add-book-request/${bookId}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });

      if (response.ok) {
        alert('Book request successful');
        // You may want to refresh the book list after requesting
        this.fetchBooks();
      } else if (response.status === 401) {
        // Handle unauthorized access (e.g., redirect to login page)
        alert('Unauthorized access. Please log in.');
        // Redirect to login page or handle as needed
      } else {
        throw new Error('Error requesting book');
      }
    } catch (error) {
      console.error('Error requesting book:', error.message);
      // Handle request error, show message to user, etc.
    }
  },

  async returnBook(bookId) {
  try {
    const response = await fetch(`http://localhost:5000/return-book/${bookId}`, {
      method: 'POST',
      
    });

    if (response.ok) {
      alert('Book returned successfully');
      this.fetchBooks(); // Refresh book list after returning
    } else if (response.status === 401) {
      alert('Unauthorized access. Please log in.');
    } else {
      throw new Error('Error returning book');
    }
  } catch (error) {
    console.error('Error returning book:', error.message);
    // Handle return error, show message to user, etc.
  }
},


    
    isBookRequested(bookId) {
      // Placeholder implementation, adjust as needed
      return false;
    },
    async submitFeedback() {
      this.$router.push(`/SubmitFeedback`); // Use ${} to interpolate variables

},


    async searchBooks() {
  try {
    if (this.searchQuery.trim() !== '') {
      const response = await fetch(`http://localhost:5000/search-books?query=${encodeURIComponent(this.searchQuery)}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        this.books = data;
      } else if (response.status === 400) {
        const errorMessage = await response.json();
        alert(errorMessage.message);
      } else if (response.status === 401) {
        alert('Unauthorized access. Please log in.');
        // Redirect to login page or handle as needed
      } else {
        throw new Error('Failed to fetch books');
      }
    } else {
      // Handle empty search query if needed
    }
  } catch (error) {
    console.error('Error searching books:', error.message);
    // Handle fetch error, show message to user, etc.
  }
}

  }
};
</script>

<style scoped>
.home-page {
  padding: 20px;
  background-color: #f7f7f7;
  border-radius: 5px;
}

.btn-success {
  background-color: #28a745;
  border-color: #28a745;
}

.btn-warning {
  background-color: #ffc107;
  border-color: #ffc107;
}

.book-image {
  width: 100px; /* Adjust the width as needed */
  height: auto; /* Maintain aspect ratio */
}

.placeholder-image {
  width: 100px; /* Adjust the width as needed */
  height: 100px; /* Adjust the height as needed */
  background-color: #ccc;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #fff;
}
</style>
