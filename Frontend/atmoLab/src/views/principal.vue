<template>
  <div class="relative h-screen w-screen overflow-hidden">
    <!-- Capa del globo -->
    <MapaVue class="absolute inset-0 z-0" />

    <!-- Capa de UI encima -->
    <div class="relative z-10 h-full w-full
                grid grid-cols-1 gap-6
                md:grid-cols-[30%_40%_30%] md:grid-rows-[20%_60%_20%]">

      <!-- Arriba izquierda -->
      <div class="p-4 flex items-start">
        <div class="bg-white/20 rounded-lg p-4">fecha (placeholder)</div>
      </div>

      <!-- Arriba derecha -->
      <div class="p-4 flex items-start justify-end">
        <BuscadorLugar />
      </div>

      <!-- Centro izquierda -->
      <div class="p-4 flex items-center">
        <climaGral />
      </div>

      <!-- Centro derecha -->
      <div class="p-4 flex items-center justify-end">
        <Calendario />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import MapaVue from '../components/MapaVue.vue'
import calendario from '../components/Calendario.vue'
import BuscadorLugar from '../components/BuscadorLugar.vue'
import climaGral from '../components/climaGral.vue'
import fecha from '../components/fecha.vue'
</script>
