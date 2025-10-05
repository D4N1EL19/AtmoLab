<template>
  <div class="relative h-screen w-screen overflow-hidden">
    <!-- 🌍 Capa del globo -->
    <div ref="globeEl" class="absolute inset-0 z-0"></div>

    <!-- 🌥️ Capa de UI encima -->
    <div
      class="relative z-10 h-full w-full
              grid gap-6
              grid-cols-[40%_30%_30%] grid-rows-[40%_60%]"
    >
      <!-- 🔹 Celda 1: Arriba izquierda -->
      <div class="p-4 flex items-start justify-start">
        <div class="bg-white/20 rounded-lg p-4">fecha (placeholder)</div>
      </div>

      <!-- 🔹 Celda 2: Arriba centro -->
      <div class="p-4 flex">
        <!-- Espacio en blanco-->
      </div>

      <!-- 🔹 Celda 3: Arriba derecha -->
      <div class="p-4 flex justify-center">
        <BuscadorLugar :world="world" />
      </div>

      <!-- 🔹 Celda 4: Abajo izquierda -->
      <div class="p-4 flex items-end justify-start">
        <calendario />
      </div>

      <!-- 🔹 Celda 5: Abajo centro -->
      <div class="p-4 flex items-end justify-center">
        <div class="bg-white/20 rounded-lg p-4">Otra sección (placeholder)</div>
      </div>

      <!-- 🔹 Celda 6: Abajo derecha -->
      <div class="p-4 flex items-end justify-end">
        <div class="bg-white/20 rounded-lg p-4">Otra sección (placeholder)</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Globe from "globe.gl";
import * as THREE from "three";

import BuscadorLugar from "../components/BuscadorLugar.vue";
import calendario from "../components/calendario.vue";

const globeEl = ref(null);
const world = ref(null);

onMounted(() => {
  if (!globeEl.value) return;

  // 🔹 Inicializar globo en África
  world.value = new Globe(globeEl.value, {
    rendererConfig: { alpha: true, antialias: true },
  })
    .globeImageUrl("//cdn.jsdelivr.net/npm/three-globe/example/img/earth-blue-marble.jpg")
    .bumpImageUrl("//cdn.jsdelivr.net/npm/three-globe/example/img/earth-topology.png")
    .showAtmosphere(true)
    .atmosphereColor("#88ccff")
    .atmosphereAltitude(0.2)
    .pointOfView({ lat: 0, lng: 20, altitude: 3 }); // África

  world.value.renderer().setClearColor(0x000000, 0);
  world.value.controls().autoRotate = true;
  world.value.controls().autoRotateSpeed = 0.5;

  // Luces
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

  // 🔹 Geolocalización con marcador rojo usando pointsData
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude;
        const lng = position.coords.longitude;

        // Rotar suavemente hasta la ubicación
        world.value.pointOfView({ lat, lng, altitude: 2 }, 1500);

        // Detener auto-rotación al centrar
        world.value.controls().autoRotate = false;

        // Agregar marcador rojo
        world.value
          .pointsData([{ lat, lng, name: "Tu ubicación" }])
          .pointLat("lat")
          .pointLng("lng")
          .pointColor(() => "red")
          .pointAltitude(0.01)
          .pointRadius(0.3);
      },
      (err) => console.warn("No se pudo obtener la ubicación:", err),
      { enableHighAccuracy: true }
    );
  }
});
</script>


