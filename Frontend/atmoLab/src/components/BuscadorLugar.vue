<template>
  <div class="panel-lugares">
    <h2>Selecciona una ciudad de México</h2>

    <input
      v-model="busqueda"
      type="text"
      placeholder="Ingresa ciudad o país"
      @keyup.enter="buscarLugar"
    />

    <div v-if="lugarEncontrado" class="info-lugar">
      <h3>{{ lugarEncontrado.name }}</h3>
      <p>Latitud: {{ lugarEncontrado.lat }}</p>
      <p>Longitud: {{ lugarEncontrado.lng }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "BuscadorLugar",
  props: {
    world: Object // el globo 3D desde el componente padre
  },
  data() {
    return {
      busqueda: "",
      lugarEncontrado: null
    };
  },
  methods: {
    async buscarLugar() {
      if (!this.busqueda) return;

      const url = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(
        this.busqueda
      )}&format=json&limit=1`;

      try {
        const res = await fetch(url);
        const data = await res.json();

        if (data.length > 0) {
          const lugar = data[0];
          this.lugarEncontrado = {
            name: lugar.display_name,
            lat: parseFloat(lugar.lat),
            lng: parseFloat(lugar.lon)
          };

          // Zoom al lugar
          this.world.pointOfView(
            { lat: this.lugarEncontrado.lat, lng: this.lugarEncontrado.lng, altitude: 2 },
            1500
          );

          // Detener rotación
          this.world.controls().autoRotate = false;

          // Marcar en el globo
          this.world
            .pointsData([this.lugarEncontrado])
            .pointLat("lat")
            .pointLng("lng")
            .pointColor(() => "red")
            .pointAltitude(0.01)
            .pointRadius(0.3);
        } else {
          alert("No se encontró la ubicación");
        }
      } catch (err) {
        console.error(err);
      }
    }
  }
};
</script>

<style scoped>
.panel-lugares {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 280px;
  background-color: #1c3563;
  padding: 15px 20px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.25);
  z-index: 10;
}

.panel-lugares h2 {
  margin-top: 0;
  font-size: 1.2rem;
  color: #fbfbfb;
  text-align: center;
}

.panel-lugares input {
  width: 100%;
  padding: 8px;
  margin: 10px 0;
  font-size: 1rem;
  border-radius: 6px;
  border: 1px solid #ccc;
  background-color: #fbfbfb;
}

.info-lugar {
  margin-top: 15px;
  background: #1c3563;
  padding: 10px;
  border-radius: 8px;
  font-size: 0.9rem;
  color: #fbfbfb;
}
</style>
