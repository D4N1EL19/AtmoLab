<template>
  <div class="relative h-screen w-screen overflow-hidden">
    <!-- 🌍 Capa del globo -->
    <div ref="globeEl" class="absolute inset-0 z-0"></div>

    <!-- 🌥️ Capa de UI encima -->
    <div
      class="relative z-10 h-full w-full
              grid grid-cols-1 gap-6
              md:grid-cols-[30%_40%_30%] md:grid-rows-[20%_60%_20%]"
    >
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
        <calendario />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import Globe from "globe.gl";
import * as THREE from "three";

import BuscadorLugar from "../components/BuscadorLugar.vue";
import calendario from "../components/calendario.vue";
import climaGral from "../components/climaGral.vue";
import fecha from "../components/fecha.vue";

export default {
  name: "VistaPrincipal",
  components: { BuscadorLugar, calendario, climaGral, fecha },

  setup() {
    // 🌍 Referencia al contenedor del globo
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

      // 🌤️ Luces
      const ambientLight = new THREE.AmbientLight(0xffffff, 1.5);
      world.scene().add(ambientLight);

      const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
      directionalLight.position.set(5, 3, 5);
      world.scene().add(directionalLight);

      // ☁️ Nubes
      const CLOUDS_IMG_URL =
        "https://raw.githubusercontent.com/turban/webgl-earth/master/images/fair_clouds_4k.png";
      const CLOUDS_ALT = 0.004;
      const CLOUDS_ROTATION_SPEED = -0.006;

      new THREE.TextureLoader().load(CLOUDS_IMG_URL, (cloudsTexture) => {
        const clouds = new THREE.Mesh(
          new THREE.SphereGeometry(world.getGlobeRadius() * (1 + CLOUDS_ALT), 75, 75),
          new THREE.MeshPhongMaterial({
            map: cloudsTexture,
            transparent: true,
            opacity: 0.4,
          })
        );
        world.scene().add(clouds);

        const rotateClouds = () => {
          clouds.rotation.y += (CLOUDS_ROTATION_SPEED * Math.PI) / 180;
          requestAnimationFrame(rotateClouds);
        };
        rotateClouds();
      });
    });

    // 👇 Lo que se retorna desde setup() se puede usar en el template
    return {
      globeEl,
    };
  },
};
</script>

<style scoped>
  .globo {
    width: 100%;
    height: 100%;
    background: transparent;
  }
</style>
