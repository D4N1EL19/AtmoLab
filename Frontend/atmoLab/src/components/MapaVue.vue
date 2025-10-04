<template>
  <div class="globo-container">
    <div ref="globeEl" class="globo"></div>

    <!-- Importamos el buscador -->
    <BuscadorLugar :world="world" />
  </div>
</template>

<script>
import Globe from "globe.gl";
import * as THREE from "three";
import BuscadorLugar from "./BuscadorLugar.vue";

export default {
  name: "MapaVue",
  components: { BuscadorLugar },
  data() {
    return {
      world: null
    };
  },
  mounted() {
    const globeEl = this.$refs.globeEl;

    this.world = new Globe(globeEl, { rendererConfig: { alpha: true, antialias: true } })
      .globeImageUrl("//cdn.jsdelivr.net/npm/three-globe/example/img/earth-blue-marble.jpg")
      .bumpImageUrl("//cdn.jsdelivr.net/npm/three-globe/example/img/earth-topology.png")
      .showAtmosphere(true)
      .atmosphereColor("#88ccff")
      .atmosphereAltitude(0.2)
      .pointOfView({ lat: 20, lng: -100, altitude: 3 });

    this.world.renderer().setClearColor(0x000000, 0);
    this.world.controls().autoRotate = true;
    this.world.controls().autoRotateSpeed = 0.5;

    const ambientLight = new THREE.AmbientLight(0xffffff, 1.5);
    this.world.scene().add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(5, 3, 5);
    this.world.scene().add(directionalLight);

    // Nubes
    const CLOUDS_IMG_URL = "https://raw.githubusercontent.com/turban/webgl-earth/master/images/fair_clouds_4k.png";
    const CLOUDS_ALT = 0.004;
    const CLOUDS_ROTATION_SPEED = -0.006;

    new THREE.TextureLoader().load(CLOUDS_IMG_URL, (cloudsTexture) => {
      const clouds = new THREE.Mesh(
        new THREE.SphereGeometry(this.world.getGlobeRadius() * (1 + CLOUDS_ALT), 75, 75),
        new THREE.MeshPhongMaterial({ map: cloudsTexture, transparent: true, opacity: 0.4 })
      );
      this.world.scene().add(clouds);

      const rotateClouds = () => {
        clouds.rotation.y += (CLOUDS_ROTATION_SPEED * Math.PI) / 180;
        requestAnimationFrame(rotateClouds);
      };
      rotateClouds();
    });
  }
};
</script>

<style scoped>
.globo-container {
  position: relative;
  width: 100vw;
  height: 100vh;
}

.globo {
  width: 50%;
  height: 50%;
  background: transparent;
}
</style>
