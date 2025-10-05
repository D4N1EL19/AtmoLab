<template>
  <div class="relative h-screen w-screen overflow-hidden">
    <!-- 🌍 Capa del globo -->
    <div class="globo-wrapper" style="overflow:hidden; width:100%; height:100%;">
      <div ref="globeEl" class="globo-canvas"></div>
    </div>

    <!-- 🌥️ Capa de UI encima -->
    <div
      class="relative z-10 h-full w-full
              grid gap-6
              grid-cols-[40%_30%_30%] grid-rows-[40%_60%]"
    >
      <!-- 🔹 Celda 1: Arriba izquierda -->
      <div class="p-4 flex items-start justify-start">
        <div
          v-if="!fechaEnOtroLado"
          class="fecha-container"
          :class="{
            'fecha-desplazandose': fechaDesplazandose
          }"
        >
          <fecha :ubicacion="nameLocation" />
        </div>
      </div>

      <!-- 🔹 Celda 2: Arriba centro -->
      <div class="p-4 flex"></div>

      <!-- 🔹 Celda 3: Arriba derecha -->
      <div class="p-4 flex justify-center items-start">
        <!-- 🔸 El texto aparece aquí después de la animación -->
        <div
          v-if="fechaEnOtroLado"
          class="fecha-container fecha-en-otro-lado"
        >
          <fecha :ubicacion="nameLocation" />
        </div>

        <!-- Buscador solo visible antes de seleccionar fecha -->
        <BuscadorLugar
          v-if="!fechaSeleccionada"
          :world="world"
          @actualizar-ubicacion="actualizarUbicacion"
        />
      </div>

      <!-- 🔹 Celda 4: Abajo izquierda -->
      <div class="p-4 flex items-end justify-start">
        <climaGral
          v-if="!fechaSeleccionada"
          :lat="userLocation.lat"
          :lng="userLocation.lng"
        />
      </div>

      <!-- 🔹 Celda 5: Abajo centro -->
      <div class="p-4 flex items-end justify-center"></div>

      <!-- 🔹 Celda 6: Abajo derecha -->
      <div class="p-4 flex items-center justify-center">
        <calendario
          v-if="!fechaSeleccionada"
          @fecha-seleccionada="handleFechaSeleccionada"
        />
      </div>
    </div>
  </div>

  <prediccion
    v-if="fechaSeleccionada"
    :fecha="fechaSeleccionada"
    class="absolute inset-0 z-50 flex justify-center items-center"
  />
</template>


<script setup>
import { ref, onMounted } from "vue";
import Globe from "globe.gl";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import * as THREE from "three";

import BuscadorLugar from "../components/BuscadorLugar.vue";
import calendario from "../components/calendario.vue";
import fecha from "../components/fecha.vue";
import climaGral from "../components/climaGral.vue";
import prediccion from "../components/prediccion.vue";

const globeEl = ref(null);
const world = ref(null);
const nameLocation = ref("Ensenada, Baja California, México");
const userLocation = ref({ lat: null, lng: null });
const fechaSeleccionada = ref(null);

// 🔹 NUEVAS VARIABLES PARA ANIMAR TEXTO
const fechaDesplazandose = ref(false);
const fechaEnOtroLado = ref(false);

function actualizarUbicacion({ lat, lng, name }) {
  nameLocation.value = name;
  userLocation.value.lat = lat;
  userLocation.value.lng = lng;
}

function animarGlobo(targetX, lat = userLocation.value.lat, lng = userLocation.value.lng) {
  let x = 0;
  const velocidad = 15;
  const canvas = globeEl.value;

  // Empieza animación de la fecha
  fechaDesplazandose.value = true;
  fechaEnOtroLado.value = false;

  // Activar rotación del globo
  world.value.controls().autoRotate = true;
  world.value.controls().autoRotateSpeed = 15;

  function animar() {
    if (x < targetX) {
      x += velocidad;
      canvas.style.transform = `translateX(-${x}px)`;
      requestAnimationFrame(animar);
    } else {
      canvas.style.transform = `translateX(-${targetX}px)`;
      world.value.controls().autoRotate = false;

      if (lat && lng)
        world.value.pointOfView({ lat, lng, altitude: 2 }, 1000);

      // Espera breve antes de mostrar texto nuevamente
      setTimeout(() => {
        fechaDesplazandose.value = false;
        fechaEnOtroLado.value = true;
      }, 300);
    }
  }

  animar();
}

function handleFechaSeleccionada({ fecha }) {
  fechaSeleccionada.value = fecha;
  animarGlobo(900);
}

onMounted(() => {
  if (!globeEl.value) return;

  world.value = new Globe(globeEl.value, {
    rendererConfig: { alpha: true, antialias: true },
  })
    .globeImageUrl("//cdn.jsdelivr.net/npm/three-globe/example/img/earth-blue-marble.jpg")
    .bumpImageUrl("//cdn.jsdelivr.net/npm/three-globe/example/img/earth-topology.png")
    .showAtmosphere(true)
    .atmosphereColor("#88ccff")
    .atmosphereAltitude(0.2)
    .pointOfView({ lat: 0, lng: 20, altitude: 3 });

  world.value.renderer().setClearColor(0x000000, 0);
  world.value.controls().autoRotate = true;
  world.value.controls().autoRotateSpeed = 0.5;

  const ambientLight = new THREE.AmbientLight(0xffffff, 1.5);
  world.value.scene().add(ambientLight);

  const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
  directionalLight.position.set(5, 3, 5);
  world.value.scene().add(directionalLight);

  // Nubes
  const CLOUDS_IMG_URL =
    "https://raw.githubusercontent.com/turban/webgl-earth/master/images/fair_clouds_4k.png";
  const CLOUDS_ALT = 0.004;
  const CLOUDS_ROTATION_SPEED = -0.006;

  new THREE.TextureLoader().load(CLOUDS_IMG_URL, (cloudsTexture) => {
    const cloudsMaterial = new THREE.MeshPhongMaterial({
      map: cloudsTexture,
      transparent: true,
      opacity: 0,
    });

    const clouds = new THREE.Mesh(
      new THREE.SphereGeometry(world.value.getGlobeRadius() * (1 + CLOUDS_ALT), 75, 75),
      cloudsMaterial
    );

    clouds.visible = true;
    world.value.scene().add(clouds);

    const rotateClouds = () => {
      clouds.rotation.y += (CLOUDS_ROTATION_SPEED * Math.PI) / 180;
      requestAnimationFrame(rotateClouds);
    };
    rotateClouds();

    setTimeout(() => {
      let opacity = 0;
      const fadeIn = () => {
        opacity += 0.01;
        if (opacity > 0.4) opacity = 0.4;
        clouds.material.opacity = opacity;
        if (opacity < 0.4) requestAnimationFrame(fadeIn);
      };
      fadeIn();
    }, 1000);
  });

  // Satélite
  const loader = new GLTFLoader();
  const radius = world.value.getGlobeRadius() * 1.4;

  loader.load(
    new URL("../assets/modelos/satellite.glb", import.meta.url).href,
    (gltf) => {
      const satellite = gltf.scene;
      satellite.scale.set(0.2, 0.2, 0.2);
      satellite.position.set(radius, 0, 0);
      world.value.scene().add(satellite);

      const orbitSpeed = 0.3;
      const orbitRadius = radius;

      const animateSatellite = () => {
        const time = Date.now() * 0.001 * orbitSpeed;
        satellite.position.x = Math.cos(time) * orbitRadius;
        satellite.position.z = Math.sin(time) * orbitRadius;
        satellite.rotation.y += 0.02;
        requestAnimationFrame(animateSatellite);
      };
      animateSatellite();
    },
    undefined,
    (error) => console.error("❌ Error cargando el satélite:", error)
  );

  // Geolocalización
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const lat = position.coords.latitude;
        const lng = position.coords.longitude;

        userLocation.value.lat = lat;
        userLocation.value.lng = lng;

        const res = await fetch(
          `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lng}&format=json&accept-language=es`
        );
        const data = await res.json();
        nameLocation.value = data.display_name;

        world.value.pointOfView({ lat, lng, altitude: 2 }, 1500);
        world.value.controls().autoRotate = false;

        world.value
          .pointsData([{ lat, lng, name: "Tu ubicación" }])
          .pointLat("lat")
          .pointLng("lng")
          .pointColor(() => "red")
          .pointAltitude(0.01)
          .pointRadius(0.3);
      },
      (err) => console.warn("No se pudo obtener la ubicación:", err),
      { enableHighAccuracy: false }
    );
  }
});
</script>

<style scoped>
.globo-wrapper {
  position: absolute;
  inset: 0;
  overflow: hidden;
  background-color: #000011;
}

.globo-canvas {
  width: 200%;
  height: 100%;
  background-color: #000011;
}

/* Estado base del contenedor de fecha */
.fecha-container {
  transition: all 0.8s ease-in-out;
  transform: translateX(0);
  opacity: 1;
}

/* 🔹 Cuando se está desplazando (salida) */
.fecha-desplazandose {
  transform: translateX(-100%);
  opacity: 0;
}

/* 🔹 Cuando aparece en el otro lado (entrada suave) */
.fecha-en-otro-lado {
  opacity: 0;
  transform: translateX(20%);
  animation: aparecer 0.8s ease-out forwards;
}

/* 🔸 Animación personalizada para entrada */
@keyframes aparecer {
  from {
    opacity: 0;
    transform: translateX(20%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
</style>
