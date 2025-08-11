<template>
  <div class="row">
    <div class="col">
      <label class="label">线程数 (--threads)</label>
      <md-outlined-text-field type="number" :value="threads" @input="(e:any)=> $emit('update:threads', parseInt(e.target.value||'0'))"/>
    </div>
    <div class="col">
      <label class="label">Beam Size (--beam-size)</label>
      <md-outlined-text-field type="number" :value="beamSize" @input="(e:any)=> $emit('update:beamSize', parseInt(e.target.value||'0'))"/>
    </div>
    <div class="col">
      <label class="label">Best Of (--best-of)</label>
      <md-outlined-text-field type="number" :value="bestOf" @input="(e:any)=> $emit('update:bestOf', parseInt(e.target.value||'0'))"/>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ threads: number; beamSize: number; bestOf: number }>();
defineEmits(['update:threads','update:beamSize','update:bestOf']);
</script>

<style scoped>
.row { display: flex; gap: 16px; margin: 12px 0; }
.col { display: flex; flex-direction: column; gap: 6px; width: 180px; }
.label { font-size: 12px; color: var(--md-sys-color-on-surface-variant); }
</style>

