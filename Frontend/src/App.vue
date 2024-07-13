<template>
  <div class="container">
    <div class="row">
      <div class="col-md-12">
        <v-app>
          <v-main>
            <router-view />
          </v-main>
        </v-app>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "App",

  data: () => ({
    //
  }),
};
</script>
