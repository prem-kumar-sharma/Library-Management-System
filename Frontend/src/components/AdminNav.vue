<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <router-link class="navbar-brand" to="/">Your Library Name</router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/AdminLogin">Login</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/AdminRegistration">Register</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/AddBooks">Add Books</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/AddSection">Add Section</router-link>
          </li>
          <li class="nav-item">
            <button @click="logout" class="btn btn-outline-danger my-2 my-sm-0">Logout</button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

  
  <script>
  export default {
    name: 'AdminNav',
    methods: {
    async logout() {
      try {
        // You may want to send a request to the server to invalidate the token,
        // but for simplicity, let's just remove the token from localStorage.
        localStorage.removeItem("access_token");

        // Redirect to the login page (adjust the route as needed)
        this.$router.push('/AdminDashboard');

        console.log('Logout successful!');
      } catch (error) {
        console.error('An error occurred during admin logout:', error.message);
        // Handle other errors if necessary
      }
    }
  },
  };
  </script>
  
  <style>
  nav {
    background-color: #333;
    padding: 10px 0;
  }
  
  ul {
    list-style-type: none;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
  }
  
  li {
    margin: 0 10px;
  }
  
  a {
    color: white;
    text-decoration: none;
  }
  
  a:hover {
    text-decoration: underline;
  }
  </style>
  