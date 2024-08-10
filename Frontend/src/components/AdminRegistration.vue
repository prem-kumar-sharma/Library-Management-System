<template>
  <div class="container">
    <h1 class="mt-5 mb-4">Admin Registration</h1>
    <form @submit.prevent="registerAdmin" class="mb-4">
      <div class="mb-3">
        <input type="text" v-model="username" class="form-control" placeholder="Username" required>
      </div>
      <div class="mb-3">
        <input type="email" v-model="email" class="form-control" placeholder="Email" required>
      </div>
      <div class="mb-3">
        <input type="password" v-model="password" class="form-control" placeholder="Password" required>
      </div>
      <button type="submit" class="btn btn-primary">Register</button>
    </form>
  </div>
</template>

  
  <script>
  export default {
    data() {
      return {
        username: '',
        email: '',
        password: ''
      };
    },
    methods: {
      async registerAdmin() {
        const response = await fetch('http://localhost:5000/admin/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: this.username,
            email: this.email,
            password: this.password
          })
        });
        const data = await response.json();
        alert(data.message); // Show registration message
        // Redirect or handle success as needed
      }
  }
};
</script>
