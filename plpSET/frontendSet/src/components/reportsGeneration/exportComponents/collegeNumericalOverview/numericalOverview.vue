<template>
  <div class="pt-16">
    <TablePrint :refreshChart="refreshChart"></TablePrint>
  </div>
</template>
<script setup lang="ts">
import TablePrint from "./collegenumericalTable.vue";

defineProps({
  college: String,
  professor: String,
  question: String,
  refreshChart: Boolean,
});
</script>
