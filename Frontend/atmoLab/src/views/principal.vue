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
        <BuscadorLugar />
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
import climaGral from "../components/climaGral.vue";

const globeEl = ref(null);

onMounted(() => {
  if (!globeEl.value) return;

  const world = new Globe(globeEl.value, {
    rendererConfig: { alpha: true, antialias: true },
  })
    .globeImageUrl("//cdn.jsdelivr.net/npm/three-globe/example/img/earth-blue-marble.jpg")
    .bumpImageUrl("//cdn.jsdelivr.net/npm/three-globe/example/img/earth-topology.png")
    .showAtmosphere(true)
    .atmosphereColor("#88ccff")
    .atmosphereAltitude(0.2)
    .pointOfView({ lat: 20, lng: -100, altitude: 3 });

  world.renderer().setClearColor(0x000000, 0);
  world.controls().autoRotate = true;
  world.controls().autoRotateSpeed = 0.5;

  const ambientLight = new THREE.AmbientLight(0xffffff, 1.5);
  world.scene().add(ambientLight);

  const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
  directionalLight.position.set(5, 3, 5);
  world.scene().add(directionalLight);

  const CLOUDS_IMG_URL =
    "https://raw.githubusercontent.com/turban/webgl-earth/master/images/fair_clouds_4k.png";
  const CLOUDS_ALT = 0.004;
  const CLOUDS_ROTATION_SPEED = -0.006;

  new THREE.TextureLoader().load(CLOUDS_IMG_URL, (cloudsTexture) => {
    const cloudsMaterial = new THREE.MeshPhongMaterial({
      map: cloudsTexture,
      transparent: true,
      opacity: 0, // <-- invisible desde el inicio
    });

    const clouds = new THREE.Mesh(
      new THREE.SphereGeometry(world.getGlobeRadius() * (1 + CLOUDS_ALT), 75, 75),
      cloudsMaterial
    );

    clouds.visible = true; // ya está en la escena, pero opacidad 0
    world.scene().add(clouds);

    const rotateClouds = () => {
      clouds.rotation.y += (CLOUDS_ROTATION_SPEED * Math.PI) / 180;
      requestAnimationFrame(rotateClouds);
    };
    rotateClouds();

    // Fade-in de opacidad
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
});
</script>
