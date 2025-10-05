<template>
  <div class="p-4 text-white font-lex">
    <p class="text-5xl m-4">{{ diaSemana }}</p>
    <p class="text-4xl m-4">{{ fechaCompleta }}</p>
    <p class="text-2xl m-4">{{ ubicacion }}</p>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";

// Prop para la ubicación, con valor por defecto
const props = defineProps({
  ubicacion: {
    type: String,
    default: "Ensenada, Baja California, México"
  }
});

// Fecha actual
const ahora = ref(new Date());

// Array con nombres de días en español
const diasSemana = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"];

// Computed: nombre del día
const diaSemana = computed(() => {
  return diasSemana[ahora.value.getDay()];
});

// Computed: fecha completa en español
const fechaCompleta = computed(() => {
  const opciones = { year: "numeric", month: "long", day: "numeric" };
  return ahora.value.toLocaleDateString("es-ES", opciones);
});
</script>
