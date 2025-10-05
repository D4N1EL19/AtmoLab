<template>
  <div class="min-h-screen bg-gradient-to-b from-slate-50 to-white flex items-center justify-center p-6">
    <div class="w-full max-w-4xl bg-white/80 backdrop-blur-md rounded-2xl shadow-xl border border-slate-100 overflow-hidden">

      <!-- Header -->
      <header class="flex items-center justify-between p-6 border-b border-slate-100">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 rounded-lg bg-gradient-to-tr from-indigo-500 to-pink-500 flex items-center justify-center text-white font-bold text-lg">MV</div>
          <div>
            <h1 class="text-lg font-semibold text-slate-800">Mi App Bonita</h1>
            <p class="text-sm text-slate-500">Interfaz simple con Vue 3 + Tailwind</p>
          </div>
        </div>
        <nav class="hidden md:flex items-center gap-4">
          <button class="text-sm px-3 py-2 rounded-md hover:bg-slate-100">Inicio</button>
          <button class="text-sm px-3 py-2 rounded-md hover:bg-slate-100">Proyectos</button>
          <button class="text-sm px-3 py-2 rounded-md bg-indigo-600 text-white hover:brightness-95">Conectar</button>
        </nav>
      </header>

      <!-- Main -->
      <main class="p-6 grid grid-cols-1 md:grid-cols-3 gap-6">

        <!-- Left: Lista de tareas -->
        <section class="md:col-span-2">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-xl font-semibold text-slate-800">Tareas</h2>
            <div class="text-sm text-slate-500">{ { items.length } } tareas</div>
          </div>

          <div class="space-y-3">
            <transition-group name="list" tag="div">
              <article v-for="item in items" :key="item.id" class="flex items-center justify-between gap-4 p-4 bg-slate-50 rounded-lg border">
                <div class="flex items-center gap-3">
                  <button @click="toggleDone(item)" class="w-8 h-8 rounded-full border flex items-center justify-center"
                          :class="item.done ? 'bg-indigo-600 text-white' : 'bg-white text-slate-400'">
                    <svg v-if="item.done" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <circle cx="12" cy="12" r="9" stroke-width="2" stroke="currentColor" />
                    </svg>
                  </button>

                  <div>
                    <h3 :class="['font-medium', item.done ? 'text-slate-400 line-through' : 'text-slate-800']">{{ item.title }}</h3>
                    <p class="text-sm text-slate-500">{{ item.description }}</p>
                  </div>
                </div>

                <div class="flex items-center gap-3">
                  <span class="text-xs px-2 py-1 rounded-full bg-slate-100 text-slate-600">{{ item.tag }}</span>
                  <button @click="editItem(item)" class="p-2 rounded-md hover:bg-slate-100">✏️</button>
                  <button @click="removeItem(item.id)" class="p-2 rounded-md hover:bg-rose-50 text-rose-600">🗑️</button>
                </div>
              </article>
            </transition-group>

            <div v-if="items.length === 0" class="p-6 text-center text-slate-500 border rounded-lg">
              No hay tareas — añade la primera a la derecha ✨
            </div>
          </div>
        </section>

        <!-- Right: Formulario + Estadísticas -->
        <aside class="space-y-4">
          <div class="p-4 rounded-lg border bg-white">
            <h3 class="font-semibold text-slate-800 mb-2">Nueva tarea</h3>
            <form @submit.prevent="submitForm" class="space-y-3">
              <input v-model="form.title" required placeholder="Título" class="w-full rounded-md border p-2" />
              <input v-model="form.tag" placeholder="Etiqueta (ej: Personal)" class="w-full rounded-md border p-2" />
              <textarea v-model="form.description" placeholder="Descripción" rows="3" class="w-full rounded-md border p-2"></textarea>

              <div class="flex items-center gap-2">
                <button type="submit" class="flex-1 py-2 rounded-md bg-indigo-600 text-white font-medium">Guardar</button>
                <button type="button" @click="resetForm" class="px-4 py-2 rounded-md border">Limpiar</button>
              </div>
            </form>
          </div>

          <div class="p-4 rounded-lg border bg-slate-50">
            <h4 class="font-medium text-slate-800">Estadísticas</h4>
            <div class="mt-3 grid grid-cols-2 gap-3">
              <div class="p-3 rounded-md bg-white text-center">
                <div class="text-sm text-slate-500">Totales</div>
                <div class="text-xl font-semibold">{{ items.length }}</div>
              </div>
              <div class="p-3 rounded-md bg-white text-center">
                <div class="text-sm text-slate-500">Completadas</div>
                <div class="text-xl font-semibold">{{ completedCount }}</div>
              </div>
            </div>
          </div>

          <div class="p-3 text-xs text-slate-500">Diseño responsive y listo para adaptar colores o comportamientos.</div>
        </aside>

      </main>

      <footer class="p-4 text-center text-sm text-slate-400 border-t">Hecho con ♥️ y Tailwind</footer>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'

// Datos demo
const items = reactive([
  { id: 1, title: 'Comprar regalo', description: 'Buscar opciones y comparar precios', tag: 'Personal', done: false },
  { id: 2, title: 'Enviar reporte', description: 'Enviar informe mensual al equipo', tag: 'Trabajo', done: true },
  { id: 3, title: 'Limpiar correo', description: 'Eliminar notificaciones viejas', tag: 'Personal', done: false }
])

const form = reactive({ id: null, title: '', description: '', tag: '' })

function resetForm() {
  form.id = null
  form.title = ''
  form.description = ''
  form.tag = ''
}

function submitForm() {
  if (!form.title.trim()) return

  if (form.id) {
    // editar
    const idx = items.findIndex(i => i.id === form.id)
    if (idx !== -1) {
      items[idx].title = form.title
      items[idx].description = form.description
      items[idx].tag = form.tag
    }
  } else {
    // crear
    const newItem = {
      id: Date.now(),
      title: form.title,
      description: form.description,
      tag: form.tag || 'General',
      done: false
    }
    items.unshift(newItem)
  }

  resetForm()
}

function removeItem(id) {
  const idx = items.findIndex(i => i.id === id)
  if (idx !== -1) items.splice(idx, 1)
}

function toggleDone(item) {
  item.done = !item.done
}

function editItem(item) {
  form.id = item.id
  form.title = item.title
  form.description = item.description
  form.tag = item.tag
  // opcional: hacer scroll o dar foco
}

const completedCount = computed(() => items.filter(i => i.done).length)
</script>

<style scoped>
/* Animación simple para el transition-group */
.list-enter-from, .list-leave-to { opacity: 0; transform: translateY(-6px); }
.list-enter-active, .list-leave-active { transition: all 180ms ease; }
</style>
