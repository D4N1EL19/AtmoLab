<template>
  <div class="panel-lugares bg-[#07122B] p-4 rounded-xl shadow-md text-white w-72 h-[50%] flex flex-col justify-center"
  style="filter: drop-shadow(6px 6px 10px #1A2B53);
                    :drop-shadow(-2px -2px 4px #1A2B53)">
    
    <h2 class="text-center font-lex text-lg font-semibold">Ingresa tu destino</h2>

    <input
      v-model="busqueda"
      type="text"
      placeholder="Ingresa ciudad o país"
      @keyup.enter="buscarLugar"
      class="w-full p-2 mt-2 mb-3 rounded-4xl border border-gray-300 text-black bg-white focus:outline-none font-lex focus:ring-2 focus:ring-blue-400"
    />

  </div>
</template>

<script>
export default {
  name: "BuscadorLugar",
  props: {
    world: Object
  },
  data() {
    return {
      busqueda: "",
      lugarEncontrado: null
    };
  },
  methods: {
    async buscarLugar() {
      if (!this.busqueda || !this.world) return;

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

          // Emitimos evento al padre
          this.$emit("actualizar-ubicacion", {
            lat: this.lugarEncontrado.lat,
            lng: this.lugarEncontrado.lng,
            name: this.lugarEncontrado.name
          });

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
