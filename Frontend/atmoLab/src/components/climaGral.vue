<template>
  <div
    class="p-4 h-full w-full rounded-lg text-white font-lex
            flex flex-col justify-start"
    style="filter: drop-shadow(6px 6px 10px #324679);
                    :drop-shadow(-2px -2px 4px #324679)"
  >
    <h2 class="text-xl font-semibold mb-4">Condiciones Climáticas</h2>

    <div
      class="flex flex-col items-center bg-[#07122B] rounded-lg p-6 w-[50%] gap-3"
    >
      <template v-if="clima">
        <p class="text-sm text-gray-300">Temperatura</p>
        <p class="text-2xl font-semibold">{{ clima.temperatura }}°C</p>

        <p class="text-sm text-gray-300">Sensación térmica</p>
        <p class="text-2xl font-semibold">{{ clima.sensacion }}°C</p>

        <p class="text-sm text-gray-300">Humedad</p>
        <p class="text-2xl font-semibold">{{ clima.humedad }}%</p>

        <p class="text-sm text-gray-300">Viento</p>
        <p class="text-2xl font-semibold">{{ clima.viento }} km/h</p>

        <p class="text-sm text-gray-300">Precipitación</p>
        <p class="text-2xl font-semibold">{{ clima.precipitacion }} mm</p>
      </template>

      <template v-else>
        <p class="text-gray-400 animate-pulse">Cargando datos del clima...</p>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue";

// Props
const props = defineProps({
  lat: { type: [Number, null], required: true },
  lng: { type: [Number, null], required: true }
});

const clima = ref(null);
const API_KEY = "20edc629cae6e88e953a64586fb2cfce";

async function obtenerClima(lat, lng) {
  try {
    const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lng}&units=metric&lang=es&appid=${API_KEY}`;
    const res = await fetch(url);
    const data = await res.json();

    clima.value = {
      temperatura: data.main.temp,
      sensacion: data.main.feels_like,
      humedad: data.main.humidity,
      viento: data.wind.speed,
      precipitacion: data.rain?.["1h"] || 0
    };
  } catch (error) {
    console.error("Error al obtener el clima:", error);
  }
}

onMounted(() => {
  if (props.lat && props.lng) obtenerClima(props.lat, props.lng);
});

watch(() => [props.lat, props.lng], ([lat, lng]) => {
  if (lat && lng) obtenerClima(lat, lng);
});
</script>
