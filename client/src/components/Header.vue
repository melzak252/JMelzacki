<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">MyApp</a>
     
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link class="nav-link active" aria-current="page" to="/">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/countrydle">Countrydle</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/guess-country">Contact</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Header'
}
</script>

<style scoped>
/* Basic styling; customize as needed */
.navbar {
  box-shadow: 0 2px 4px rgba(0,0,0,.1);
}
</style>