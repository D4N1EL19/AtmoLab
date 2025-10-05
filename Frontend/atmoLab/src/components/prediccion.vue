<template>
    <div class="w-screen h-screen flex flex-col justify-center items-center font-lex">
        <p class="text-center text-4xl font-semibold text-white mb-4">
            Pronostico por hora 
        </p>
        <!-- Contenedor centrado con scroll -->
        <div 
        class=" p-4 rounded shadow w-[500px] max-h-[70vh] overflow-y-auto flex flex-col items-center"
        >
        <div class="w-full space-y-2 text-white">
            <div 
            v-for="item in datos?.prediccion" 
            :key="item.hora" 
            class=" p-2 flex justify-between"
            >
            <span class="font-medium text-center">{{ item.hora }}</span>
            <div class="text-right space-y-1 text-sm flex bg-[#112042] rounded-2xl p-4">
                <div class="px-4 text-center">
                    <p>Temperatura</p>
                    <p>{{ item.temperatura_c.toFixed(1) }}°C</p>
                </div>
                <div class="px-4 text-center">
                    <p>Humedad</p>
                    <p>{{ item.humedad_relativa_pct.toFixed(1) }}%</p>
                </div>
                <div class="px-4 text-center">
                    <p>Viento</p>
                    <p>{{ item.velocidad_viento_kmh.toFixed(1) }} km/h</p>
                </div>
            </div>
            </div>
        </div>

        <p v-if="error" class="text-red-500 mt-4">{{ error }}</p>
        <p v-else-if="!datos" class="mt-4">Cargando predicción...</p>
        </div>
    </div>
</template>





<script setup>
import { ref, watch } from 'vue'

const datos = ref(null)
const error = ref(null)

// Definir props
const props = defineProps({
    fecha: {
        type: String,
        required: true
    }
})

// Función que hace la petición a la API para una fecha específica
async function obtenerDatos(fecha) {
    try {
        const url = `http://127.0.0.1:8000/prediccion/${fecha}`
        const res = await fetch(url)
        if (!res.ok) throw new Error('Error en la petición')
        datos.value = await res.json()
    } catch (err) {
        error.value = err.message
        console.error(err)
    }
}

// Watch para la prop
watch(
    () => props.fecha,
    (nuevaFecha) => {
        if (nuevaFecha) {
            obtenerDatos(nuevaFecha)
        }
    },
    { immediate: true }
)
</script>

<style scoped>
/* Opcional: scrollbar personalizado */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-thumb {
  background-color: rgba(0,0,0,0.3);
  border-radius: 4px;
}

::-webkit-scrollbar-track {
  background-color: rgba(0,0,0,0.05);
}
</style>