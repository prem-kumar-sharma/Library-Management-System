<template>
    <div>
      <h1>Sections</h1>
      <div v-for="section in sections" :key="section.id">
        <h2>{{ section.name }}</h2>
        <p>{{ section.description }}</p>
        <button @click="getBooks(section.id)">View Books</button>
      </div>
      <h1 v-if="books.length > 0">Books</h1>
      <div v-for="book in books" :key="book.id">
        <h2>{{ book.name }}</h2>
        <p>{{ book.author }}</p>
        <p>{{ book.section }}</p>
        <button @click="requestBook(book.id)">Request Book</button>
      </div>
      <h1 v-if="requests.length > 0">Book Requests</h1>
      <div v-for="request in requests" :key="request.id">
        <h2>{{ request.book.name }}</h2>
        <button @click="returnBook(request.id)">Return Book</button>
      </div>
      <h1>Feedback</h1>
      <textarea v-model="feedback.comment" placeholder="Enter your feedback"></textarea>
      <input v-model="feedback.rating" type="number" min="1" max="5" placeholder="Rating (1-5)">
      <button @click="submitFeedback">Submit Feedback</button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        sections: [],
        books: [],
        requests: [],
        feedback: {
          book_id: null,
          rating: null,
          comment: ''
        }
      };
    },
    mounted() {
      this.getSections();
    },
    methods: {
      async getSections() {
        const response = await fetch('http://localhost:5000/sections');
        const data = await response.json();
        this.sections = data;
      },
      async getBooks(sectionId) {
        const response = await fetch(`http://localhost:5000/books?section_id=${sectionId}`);
        const data = await response.json();
        this.books = data;
      },
      async requestBook(bookId) {
        const response = await fetch('http://localhost:5000/request-book', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ book_id: bookId })
        });
        const result = await response.json();
        console.log(result.message);
        this.getRequests();
      },
      async returnBook(requestId) {
        const response = await fetch('http://localhost:5000/return-book', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ request_id: requestId })
        });
        const result = await response.json();
        console.log(result.message);
        this.getRequests();
      },
      async getRequests() {
        const response = await fetch('http://localhost:5000/user-requests');
        const data = await response.json();
        this.requests = data;
      },
      async submitFeedback() {
        this.feedback.book_id = this.books[0].id; // Assuming feedback is for the first book shown
        const response = await fetch('http://localhost:5000/feedback', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.feedback)
        });
        const result = await response.json();
        console.log(result.message);
      }
    }
  };
  </script>
  