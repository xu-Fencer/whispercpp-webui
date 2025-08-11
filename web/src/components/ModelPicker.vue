<template>
  <div>
    <label for="model-picker">Choose Model:</label>
    <input type="file" id="model-picker" @change="handleModelChange" />
  </div>
</template>

<script setup>
const handleModelChange = (event) => {
  const model = event.target.files[0];
  console.log(model);
};
</script>
