<template>
  <div class="container">
    <AdminNav></AdminNav>
    <h2 class="mt-4">Welcome, {{ username }}!</h2>
    <div v-if="requests && requests.length > 0" class="mt-4">
      <h3>Book Requests:</h3>
      <ul class="list-unstyled">
        <li v-for="request in requests" :key="request.id" class="mb-3">
          <p>User Name: {{ request.user_name }}, Book Name: {{ request.book_name }}, Request Date: {{ request.request_date }}</p>
          <span v-if="request.status === 'pending'">
            <button @click="approveRequest(request.id)" class="btn btn-success me-2">Approve</button>
            <button @click="rejectRequest(request.id)" class="btn btn-danger">Reject</button>
          </span>
          <span v-else class="badge bg-secondary">{{ request.status }}</span>
        </li>
      </ul>
    </div>
    <div v-else class="mt-4">
      <p>No book requests at the moment.</p>
    </div>
    <div v-if="sections.length > 0" class="mt-4">
  <h2>Sections:</h2>
  <ul class="list-group">
    <li v-for="section in sections" :key="section.id" class="list-group-item">
      {{ section.name }} - {{ section.description }}
      <button @click="deleteSection(section)" class="btn btn-danger ms-2">Delete</button>
      <button @click="editSection(section.id)" class="btn btn-primary me-2">Edit</button>

    </li>
  </ul>
</div>

    <div v-if="books.length > 0" class="mt-4">
      <h2>Books:</h2>
      <ul class="list-group">
        <li v-for="book in books" :key="book.id" class="list-group-item">
          <div class="d-flex align-items-center">
            <div>
              <img v-if="book.image_url" :src="book.image_url" alt="Book Cover" class="book-image" width="50" height="50">
              <div v-else class="placeholder-image">No Image Available</div>
            </div>
            <div class="ml-3">
              <h3>{{ book.name }}</h3>
              <p>{{ book.author }}</p>
              <p>Section: {{ book.section }}</p>
              <button @click="editBook(book.id)" class="btn btn-primary me-2">Edit</button>
              <button @click="deleteBook(book.id)" class="btn btn-danger">Delete</button>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>


<script>
import AdminNav from "@/components/AdminNav.vue";
export default {
  name: 'AdminDashboard',
  components: {
    AdminNav
  },
  data() {
    return {
      username: '',
      requests: [], // Make sure requests contain objects with a 'status' property
      sections: [],
      books: [],
    };
  },
  mounted() {
    // Fetch data when component is mounted
    this.fetchSections();
    this.fetchBooks();
    this.fetchBookRequests();
  },
  methods: {
    async fetchBookRequests() {
      // Fetch book requests from the server
      try {
        const response = await fetch('http://127.0.0.1:5000/admin/book-requests', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('admin_access_token')}`,
          },
        });
        if (response.ok) {
          const data = await response.json();
          this.requests = data.requests;
        } else {
          throw new Error('Failed to fetch book requests');
        }
      } catch (error) {
        console.error('Error fetching book requests:', error.message);
      }
    },
    async approveRequest(requestId) {
  try {
    const response = await fetch(`http://localhost:5000/admin/approve-request/${requestId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json', // Add content type header if needed
        Authorization: `Bearer ${localStorage.getItem('admin_access_token')}`,
      },
    });
    if (response.ok) {
      alert('Request approved successfully');
      this.fetchBookRequests(); // Refresh book requests after approval
    } else {
      throw new Error('Failed to approve request');
    }
  } catch (error) {
    console.error('Error approving request:', error.message);
  }
},
async rejectRequest(requestId) {
  try {
    const response = await fetch(`http://localhost:5000/admin/reject-request/${requestId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json', // Add content type header if needed
        Authorization: `Bearer ${localStorage.getItem('admin_access_token')}`,
      },
    });
    if (response.ok) {
      alert('Request rejected successfully');
      this.fetchBookRequests(); // Refresh book requests after rejection
    } else {
      throw new Error('Failed to reject request');
    }
  } catch (error) {
    console.error('Error rejecting request:', error.message);
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
    async fetchBooks() {
      // Fetch books from the server
      try {
        const response = await fetch('http://localhost:5000/get_books', {
          method : 'GET'
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
    async deleteBook(bookId) {
  try {
    const response = await fetch(`http://localhost:5000/delete_book/${bookId}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${localStorage.getItem('admin_access_token')}`,
      },
    });
    if (response.ok) {
      this.books = this.books.filter(book => book.id !== bookId);
      alert('Book deleted successfully');
    } else {
      throw new Error('Failed to delete book');
    }
  } catch (error) {
    console.error('Error deleting book:', error.message);
  }
},
async editBook(bookId) {
  this.$router.push(`/EditBook/${bookId}`); // Use ${} to interpolate variables

},
async deleteSection(section) {
  try {
    const response = await fetch(`http://localhost:5000/delete-section/${section.id}`, {
      method: 'DELETE',
    });
    if (response.ok) {
      this.sections = this.sections.filter(s => s.id !== section.id);
      alert('Section deleted successfully');
    } else {
      throw new Error('Failed to delete section');
    }
  } catch (error) {
    console.error('Error deleting section:', error.message);
  }
},
async editSection(sectionId) {
  this.$router.push(`/EditSection/${sectionId}`); // Use ${} to interpolate variables

},
  },
};
</script>

<style>
/* Add your component-specific styles here */
</style>
