<template>
  <div class="container d-flex justify-content-center align-items-center min-vh-100">
    <div class="card w-75">
      <div class="card-body">
        <h2 class="card-title text-center mb-4">Admin Login</h2>
        <form @submit.prevent="login" class="needs-validation" novalidate>
          <div class="mb-3">
            <label for="username" class="form-label">Username:</label>
            <input v-model="username" type="text" id="username" class="form-control" required>
            <div class="invalid-feedback">Please enter your username.</div>
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password:</label>
            <input v-model="password" type="password" id="password" class="form-control" required>
            <div class="invalid-feedback">Please enter your password.</div>
          </div>
          <div class="d-grid gap-2">
            <button type="submit" class="btn btn-primary btn-block rounded-pill">Login</button>
          </div>
        </form>
        <div class="text-center mt-3">
          <p>
            Don't have an account?
            <router-link to="/AdminRegistration" class="link-primary">Register</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

  
  <script>
  import { jwtDecode } from 'jwt-decode'; // Named import for jwtDecode
  
  export default {
    name: 'AdminLogin',
    data() {
      return {
        username: '',
        password: ''
      };
    },
    methods: {
      async login() {
        try {
          const response = await fetch('http://localhost:5000/admin/login', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              username: this.username,
              password: this.password
            })
          });
  
          if (response.ok) { // Login successful
            const data = await response.json();
            console.log('Admin login successful!');
            this.$router.push('/AdminDashboard');
  
            const decodedToken = jwtDecode(data.access_token); // Use jwtDecode directly
            localStorage.setItem('admin_access_token', data.access_token);
            console.log(decodedToken);
  
            // Optionally, perform actions on successful login (e.g., store admin info in Vuex)
          } else {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Admin login failed'); // Handle failed login with error message
          }
        } catch (error) {
          console.error('An error occurred during admin login:', error.message);
          // Display an error message to the user
        }
      }
    }
  };
  </script>
  