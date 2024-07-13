<template>
  <div>
    <div class="container d-flex justify-content-center align-items-center min-vh-100">
      <div class="card w-75">
        <div class="card-body">
          <h2 class="card-title text-center mb-4">Register</h2>
          <form @submit.prevent="register" class="needs-validation" novalidate>
            <div class="mb-3">
              <label for="username" class="form-label">Username:</label>
              <input v-model="username" type="text" id="username" class="form-control" required>
            </div>
            <div class="mb-3">
              <label for="email" class="form-label">Email:</label>
              <input v-model="email" type="email" id="email" class="form-control" required>
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Password:</label>
              <input v-model="password" type="password" id="password" class="form-control" required>
            </div>
            <div class="d-grid">
              <button :disabled="isRegistering" type="submit" class="btn btn-primary btn-block rounded-pill">
                {{ isRegistering ? 'Registering...' : 'Register' }}
              </button>
            </div>
          </form>
          <div class="text-center mt-3">
            <p>
              Already have an account? 
              <router-link to="/LoginUser" class="link-primary">Login Now</router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: 'RegisterUser',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      isRegistering: false // Added boolean data property
    };
  },
  methods: {
    async register() {
      try {
        this.isRegistering = true; // Disable button during registration

        const response = await fetch('http://localhost:5000/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: this.username,
            email: this.email,
            password: this.password,
          }),
        });

        if (response.ok) {
          console.log('Registration successful!');
          // Optionally, redirect to login page or show success message
          this.$router.push('/LoginUser');
        } else {
          const data = await response.json();
          throw new Error(data.message); // Handle registration error
        }
      } catch (error) {
        console.error('An error occurred during registration:', error.message);
        // Handle registration error (e.g., show error message to the user)
      } finally {
        this.isRegistering = false; // Re-enable button after registration attempt
      }
    }
  }
};
</script>

<style scoped>
/* Add any scoped styles here */
</style>
