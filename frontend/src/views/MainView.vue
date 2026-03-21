<template>
  <div class="app">
    <header class="header">
      <div class="header-left">
        <button v-if="currentPlano" class="btn-menu" @click="sidebarOpen = true">☰</button>
        <h1>{{ currentPlano ? currentPlano.nombre : 'Position View' }}</h1>
      </div>
      <div class="header-controls">
        <select v-model="selectedPlanoId" @change="onPlanoChange">
          <option value="">Seleccionar plano...</option>
          <option v-for="plano in planos" :key="plano.id" :value="plano.id">
            {{ plano.nombre }}
          </option>
        </select>
        <button 
          v-if="selectedPlanoId" 
          @click="confirmDeletePlano" 
          class="btn-delete-plano"
          title="Eliminar plano"
        >🗑</button>
        <button @click="showCreatePlano = true" class="btn-new">+</button>
      </div>
    </header>

    <div class="content">
      <Sidebar
        v-if="currentPlano"
        :puntos="puntos"
        :isOpen="sidebarOpen"
        :selectedPuntoId="selectedPuntoId"
        @close="sidebarOpen = false"
        @select-punto="onSelectPunto"
      />

      <main class="main">
        <PlanoViewer
          v-if="currentPlano"
          ref="planoViewerRef"
          :plano="currentPlano"
          :puntos="puntos"
          :uploading="uploading"
          :highlightedPuntoId="selectedPuntoId"
          @create-punto="onCreatePunto"
          @edit-punto="onEditPunto"
          @update-punto="onUpdatePunto"
          @upload-imagen="onUploadImagen"
        />
        <div v-else class="empty-state">
          <p>Selecciona o crea un plano para comenzar</p>
        </div>
      </main>
    </div>

    <div v-if="sidebarOpen" class="sidebar-overlay" @click="sidebarOpen = false"></div>

    <PuntoModal
      v-if="showPuntoModal"
      :punto="editingPunto"
      @save="onSavePunto"
      @close="showPuntoModal = false"
      @delete="onDeletePunto"
      @generate-qr="showQrModal = true"
    />

    <QrModal
      v-if="showQrModal && editingPunto"
      :punto="editingPunto"
      :baseUrl="appBaseUrl"
      @close="showQrModal = false"
    />

    <CreatePlanoModal
      v-if="showCreatePlano"
      @create="onCreatePlano"
      @close="showCreatePlano = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../api'
import PlanoViewer from '../components/PlanoViewer.vue'
import Sidebar from '../components/Sidebar.vue'
import PuntoModal from '../components/PuntoModal.vue'
import CreatePlanoModal from '../components/CreatePlanoModal.vue'
import QrModal from '../components/QrModal.vue'

const planos = ref([])
const selectedPlanoId = ref('')
const puntos = ref([])
const showPuntoModal = ref(false)
const showCreatePlano = ref(false)
const showQrModal = ref(false)
const editingPunto = ref(null)
const pendingCoords = ref(null)
const uploading = ref(false)
const sidebarOpen = ref(false)
const selectedPuntoId = ref(null)
const planoViewerRef = ref(null)
const appBaseUrl = ref(window.location.origin)

const currentPlano = computed(() => 
  planos.value.find(p => p.id === parseInt(selectedPlanoId.value))
)

onMounted(async () => {
  await loadPlanos()
})

async function loadPlanos() {
  const { data } = await api.getPlanos()
  planos.value = data
  if (data.length > 0 && !selectedPlanoId.value) {
    selectedPlanoId.value = data[0].id
    await loadPuntos(data[0].id)
  }
}

async function onPlanoChange() {
  selectedPuntoId.value = null
  if (selectedPlanoId.value) {
    await loadPuntos(selectedPlanoId.value)
  } else {
    puntos.value = []
  }
}

async function loadPuntos(planoId) {
  const { data } = await api.getPuntos(planoId)
  puntos.value = data
}

function onSelectPunto(punto) {
  selectedPuntoId.value = punto.id
  sidebarOpen.value = false
  planoViewerRef.value?.centerOnPunto(punto)
}

async function onCreatePunto(coords) {
  pendingCoords.value = coords
  editingPunto.value = { nombre: '', tipo: 'rack' }
  showPuntoModal.value = true
}

async function onSavePunto(puntoData) {
  if (editingPunto.value && editingPunto.value.id) {
    const { data } = await api.updatePunto(editingPunto.value.id, puntoData)
    const idx = puntos.value.findIndex(p => p.id === data.id)
    if (idx !== -1) puntos.value[idx] = data
  } else {
    const { data } = await api.createPunto({
      plano_id: parseInt(selectedPlanoId.value),
      nombre: puntoData.nombre,
      tipo: puntoData.tipo,
      descripcion: puntoData.descripcion || null,
      x: pendingCoords.value.x,
      y: pendingCoords.value.y
    })
    puntos.value.push(data)
  }
  showPuntoModal.value = false
  editingPunto.value = null
  pendingCoords.value = null
}

function onEditPunto(punto) {
  editingPunto.value = { ...punto }
  selectedPuntoId.value = punto.id
  showPuntoModal.value = true
}

async function onUpdatePunto(puntoData) {
  try {
    const { data } = await api.updatePunto(puntoData.id, {
      nombre: puntoData.nombre,
      tipo: puntoData.tipo,
      x: puntoData.x,
      y: puntoData.y
    })
    const idx = puntos.value.findIndex(p => p.id === data.id)
    if (idx !== -1) puntos.value[idx] = data
  } catch (err) {
    console.error('Error updating punto:', err)
  }
}

async function onCreatePlano(nombre) {
  const { data } = await api.createPlano({ nombre })
  planos.value.push(data)
  selectedPlanoId.value = data.id
  puntos.value = []
  showCreatePlano.value = false
}

async function onUploadImagen(file) {
  uploading.value = true
  try {
    const { data } = await api.uploadImagen(parseInt(selectedPlanoId.value), file)
    const idx = planos.value.findIndex(p => p.id === parseInt(selectedPlanoId.value))
    if (idx !== -1) {
      planos.value[idx].imagen_url = data.imagen_url
    }
  } catch (err) {
    console.error('Error uploading image:', err)
  } finally {
    uploading.value = false
  }
}

async function onDeletePunto() {
  if (!editingPunto.value || !editingPunto.value.id) return
  try {
    await api.deletePunto(editingPunto.value.id)
    puntos.value = puntos.value.filter(p => p.id !== editingPunto.value.id)
    if (selectedPuntoId.value === editingPunto.value.id) {
      selectedPuntoId.value = null
    }
    showPuntoModal.value = false
    editingPunto.value = null
  } catch (err) {
    console.error('Error deleting punto:', err)
  }
}

function confirmDeletePlano() {
  if (!selectedPlanoId.value) return
  if (confirm('¿Eliminar este plano y todos sus puntos?')) {
    onDeletePlano()
  }
}

async function onDeletePlano() {
  try {
    await api.deletePlano(parseInt(selectedPlanoId.value))
    planos.value = planos.value.filter(p => p.id !== parseInt(selectedPlanoId.value))
    selectedPlanoId.value = planos.value.length > 0 ? planos.value[0].id : ''
    puntos.value = []
  } catch (err) {
    console.error('Error deleting plano:', err)
  }
}
</script>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background: #1a1a2e;
  color: white;
  padding: 0.75rem 1rem;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-width: 0;
}

.header h1 {
  font-size: 1rem;
  margin: 0;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.btn-menu {
  width: 40px;
  height: 40px;
  background: rgba(255,255,255,0.1);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  flex-shrink: 0;
}

.header-controls {
  display: flex;
  gap: 0.5rem;
  flex-shrink: 0;
}

.header-controls select {
  padding: 0.6rem;
  border-radius: 8px;
  border: none;
  background: #2d2d44;
  color: white;
  font-size: 0.9rem;
  max-width: 150px;
}

.btn-delete-plano {
  width: 40px;
  height: 40px;
  background: #f44336;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
}

.btn-new {
  width: 40px;
  height: 40px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.3rem;
  cursor: pointer;
}

.content {
  flex: 1;
  display: flex;
}

.main {
  flex: 1;
  padding: 1rem;
  min-width: 0;
}

.empty-state {
  text-align: center;
  color: #666;
  padding: 2rem;
}

.sidebar-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  z-index: 150;
}

@media (min-width: 768px) {
  .header {
    padding: 1rem 2rem;
  }

  .header h1 {
    font-size: 1.25rem;
  }

  .header-controls select {
    max-width: none;
    min-width: 200px;
  }

  .btn-menu {
    display: none;
  }

  .main {
    padding: 1.5rem;
  }
}

@media (min-width: 1024px) {
  .content {
    display: flex;
    flex-direction: row;
  }

  .main {
    overflow: auto;
  }
}
</style>
