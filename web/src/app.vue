<template>
  <div>
    <header>
      <h1>Whisper Web UI</h1>
      <nav>
        <router-link to="/">Tasks</router-link>
        <router-link to="/preview">Preview</router-link>
        <router-link to="/settings">Settings</router-link>
      </nav>
    </header>
    <main>
      <router-view></router-view>
    </main>
  </div>
</template>

<script setup>
</script>

<style scoped>
header {
  padding: 1rem;
  background-color: #6200ee;
  color: white;
  text-align: center;
}
nav a {
  margin: 0 1rem;
  color: white;
  text-decoration: none;
}
</style>
