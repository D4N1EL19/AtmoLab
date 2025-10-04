<template>
  <div class="globo-container">
    <!-- Globo 3D -->
    <div ref="globeEl" class="globo"></div>

    <!-- Panel lateral flotante -->
    <div class="panel-lugares">
      <h2>🗺️ Buscar Ubicación</h2>
      <input
        v-model="busqueda"
        type="text"
        placeholder="Ingresa ciudad o país"
      />
      <button @click="buscarLugar">Buscar</button>

      <div v-if="lugarEncontrado" class="info-lugar">
        <h3>{{ lugarEncontrado.name }}</h3>
        <p>Latitud: {{ lugarEncontrado.lat }}</p>
        <p>Longitud: {{ lugarEncontrado.lng }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import Globe from 'globe.gl'
import * as THREE from 'three'

export default {
  name: 'GloboTerraqueo',
  data() {
    return {
      world: null,
      busqueda: '',
      lugarEncontrado: null
    }
  },
  mounted() {
    const globeEl = this.$refs.globeEl

    this.world = new Globe(globeEl, { rendererConfig: { alpha: true, antialias: true } })
      .globeImageUrl('//cdn.jsdelivr.net/npm/three-globe/example/img/earth-blue-marble.jpg')
      .bumpImageUrl('//cdn.jsdelivr.net/npm/three-globe/example/img/earth-topology.png')
      .showAtmosphere(true)
      .atmosphereColor('#88ccff')
      .atmosphereAltitude(0.2)
      .pointOfView({ lat: 20, lng: -100, altitude: 3 })

    this.world.renderer().setClearColor(0x000000, 0)
    this.world.controls().autoRotate = true
    this.world.controls().autoRotateSpeed = 0.5

    const ambientLight = new THREE.AmbientLight(0xffffff, 1.5)
    this.world.scene().add(ambientLight)

    const directionalLight = new THREE.DirectionalLight(0xffffff, 1)
    directionalLight.position.set(5, 3, 5)
    this.world.scene().add(directionalLight)

    const CLOUDS_IMG_URL =
      'https://raw.githubusercontent.com/turban/webgl-earth/master/images/fair_clouds_4k.png'
    const CLOUDS_ALT = 0.004
    const CLOUDS_ROTATION_SPEED = -0.006

    new THREE.TextureLoader().load(CLOUDS_IMG_URL, cloudsTexture => {
      const clouds = new THREE.Mesh(
        new THREE.SphereGeometry(this.world.getGlobeRadius() * (1 + CLOUDS_ALT), 75, 75),
        new THREE.MeshPhongMaterial({ map: cloudsTexture, transparent: true, opacity: 0.4 })
      )
      this.world.scene().add(clouds)

      const rotateClouds = () => {
        clouds.rotation.y += (CLOUDS_ROTATION_SPEED * Math.PI) / 180
        requestAnimationFrame(rotateClouds)
      }
      rotateClouds()
    })
  },
  methods: {
    async buscarLugar() {
      if (!this.busqueda) return
      const url = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(this.busqueda)}&format=json&limit=1`
      try {
        const res = await fetch(url)
        const data = await res.json()
        if (data.length > 0) {
          const lugar = data[0]
          this.lugarEncontrado = {
            name: lugar.display_name,
            lat: parseFloat(lugar.lat),
            lng: parseFloat(lugar.lon)
          }

          // Zoom más cercano al lugar
          this.world.pointOfView(
            { lat: this.lugarEncontrado.lat, lng: this.lugarEncontrado.lng, altitude: 2 },
            1500
          )

          // Detener la rotación automática
          this.world.controls().autoRotate = false

          // Agregar marcador rojo en la ubicación
          this.world
            .pointsData([this.lugarEncontrado])
            .pointLat('lat')
            .pointLng('lng')
            .pointColor(() => 'red')
            .pointAltitude(0.01)
            .pointRadius(0.3)
        } else {
          alert('No se encontró la ubicación')
        }
      } catch (err) {
        console.error(err)
      }
    }
  }
}
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

.panel-lugares {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 280px;
  background-color: rgba(255, 255, 255, 0.95);
  padding: 15px 20px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.25);
  z-index: 10;
}

.panel-lugares h2 {
  margin-top: 0;
  font-size: 1.2rem;
}

.panel-lugares input {
  width: 100%;
  padding: 8px;
  margin: 10px 0;
  font-size: 1rem;
  border-radius: 6px;
  border: 1px solid #ccc;
}

.panel-lugares button {
  padding: 8px 16px;
  cursor: pointer;
  border-radius: 6px;
  border: none;
  background-color: #4a90e2;
  color: white;
}

.info-lugar {
  margin-top: 15px;
  background: #f0f0f0;
  padding: 10px;
  border-radius: 8px;
  font-size: 0.9rem;
}
</style>
