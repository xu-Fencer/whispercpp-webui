<template>
  <div>
    <label for="file-upload">Choose a file:</label>
    <input type="file" id="file-upload" @change="handleFileChange" />
  </div>
</template>

<script setup>
const handleFileChange = (event) => {
  const file = event.target.files[0];
  console.log(file);
};
</script>
