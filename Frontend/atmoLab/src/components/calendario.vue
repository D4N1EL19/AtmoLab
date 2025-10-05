<template>
<div
    class="bg-gray-100 p-4 rounded-lg mb-6 mx-auto w-full max-w-[320px] sm:max-w-[320px] md:max-w-[300px]"
>

    <div class="flex justify-between items-center mb-4">
    <button
        @click="cambiarMes(-1)"
        class="text-[#002E6C] hover:text-blue-700 font-jom text-xl md:text-2xl "
    >
        ❮
    </button>
    <h3 class="text-3xl md:text-3xl font-jom text-[#002E6C]">{{ nombreMes }} {{ anio }}</h3>
    <button
        @click="cambiarMes(1)"
        class="text-[#002E6C] hover:text-blue-700 font-jom text-xl md:text-2xl"
    >
        ❯
    </button>
    </div>

    <div class="grid grid-cols-7 gap-1 text-center font-popins text-sm">
    <span class="text-gray-700">Lun</span>
    <span class="text-gray-700">Mar</span>
    <span class="text-gray-700">Mie</span>
    <span class="text-gray-700">Jue</span>
    <span class="text-gray-700">Vie</span>
    <span class="text-gray-700">Sab</span>
    <span class="text-gray-700">Dom</span>

    <!-- Días vacíos antes del primer día del mes -->
    <span v-for="n in primerDiaMes" :key="'empty-' + n"></span>

    <!-- Días del mes -->
    <span
        v-for="dia in diasDelMes"
        :key="dia"
        @click="seleccionarFecha(dia)"
        :class="[
        'p-2 rounded-full cursor-pointer',
        dia === diaActual && mesActual === mes && anioActual === anio
            ? 'bg-blue-300  font-bold'
            : 'text-gray-600 hover:bg-gray-300',
        dia === diaSeleccionado ? 'bg-[#FFFF]' : ''
        ]"
    >
        {{ dia }}
    </span>
    </div>
</div>
</template>

<script>
export default {
name: "calendario",
props: {
    rol: { type: String, required: false},
},
data() {
    return {
    diasDelMes: [],
    primerDiaMes: 0,
    diaSeleccionado: null,
    mes: new Date().getMonth(),
    anio: new Date().getFullYear(),
    diaActual: new Date().getDate(),
    mesActual: new Date().getMonth(),
    anioActual: new Date().getFullYear(),
    asesorias: [],
    };
},
computed: {
    nombreMes() {
    const nombresMeses = [
        "Enero",
        "Febrero",
        "Marzo",
        "Abril",
        "Mayo",
        "Junio",
        "Julio",
        "Agosto",
        "Septiembre",
        "Octubre",
        "Noviembre",
        "Diciembre",
    ];
    return nombresMeses[this.mes];
    },
},
methods: {
    generarCalendario() {
    const primerDia = new Date(this.anio, this.mes, 1).getDay();
    this.primerDiaMes = primerDia === 0 ? 6 : primerDia - 1;

    const ultimoDia = new Date(this.anio, this.mes + 1, 0).getDate();
    this.diasDelMes = Array.from({ length: ultimoDia }, (_, i) => i + 1);
    },
    cambiarMes(direccion) {
    this.mes += direccion;
    if (this.mes < 0) {
        this.mes = 11;
        this.anio--;
    } else if (this.mes > 11) {
        this.mes = 0;
        this.anio++;
    }
    this.generarCalendario();
    },
    seleccionarFecha(dia) {
    this.diaSeleccionado = dia;
    const fechaSeleccionada = `${this.anio}-${String(this.mes + 1).padStart(
        2,
        "0"
    )}-${String(dia).padStart(2, "0")}`;
    this.$emit("fecha-seleccionada", { fecha: fechaSeleccionada });
    },
},
mounted() {
    this.generarCalendario();
},
};
</script>

<style scoped>
div.grid {
aspect-ratio: 1 / 1.1;
max-width: 320px;
}
</style>
