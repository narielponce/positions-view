<template>
  <aside class="sidebar" :class="{ open: isOpen }">
    <div class="sidebar-header">
      <h3>Puntos</h3>
      <button class="btn-close-sidebar" @click="$emit('close')">×</button>
    </div>

    <div class="search-box">
      <input 
        v-model="searchQuery" 
        type="text" 
        placeholder="Buscar..."
        class="search-input"
      />
    </div>

    <div class="filters">
      <span class="filters-label">Filtrar:</span>
      <label v-for="tipo in tipos" :key="tipo.value" class="filter-item">
        <input 
          type="checkbox" 
          v-model="selectedTipos" 
          :value="tipo.value"
        />
        <span class="filter-check" :class="tipo.value"></span>
        <span class="filter-label">{{ tipo.label }}</span>
      </label>
    </div>

    <div class="puntos-list">
      <button
        v-for="punto in filteredPuntos"
        :key="punto.id"
        class="punto-item"
        :class="[punto.tipo, { selected: selectedPuntoId === punto.id }]"
        @click="onSelectPunto(punto)"
      >
        <span class="punto-marker" :class="punto.tipo"></span>
        <span class="punto-info">
          <span class="punto-nombre">{{ punto.nombre }}</span>
          <span class="punto-tipo">{{ getTipoLabel(punto.tipo) }}</span>
        </span>
      </button>
      <p v-if="filteredPuntos.length === 0" class="no-results">
        Sin resultados
      </p>
    </div>
  </aside>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  puntos: Array,
  isOpen: Boolean,
  selectedPuntoId: Number
})

const emit = defineEmits(['close', 'select-punto'])

const searchQuery = ref('')
const selectedTipos = ref(['rack', 'access_point', 'boca_red', 'switch', 'router'])

const tipos = [
  { value: 'rack', label: 'Racks' },
  { value: 'access_point', label: 'APs' },
  { value: 'boca_red', label: 'Bocas' },
  { value: 'switch', label: 'Switches' },
  { value: 'router', label: 'Routers' }
]

const filteredPuntos = computed(() => {
  return props.puntos.filter(punto => {
    const matchesSearch = !searchQuery.value || 
      punto.nombre.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesTipo = selectedTipos.value.includes(punto.tipo)
    return matchesSearch && matchesTipo
  })
})

function getTipoLabel(tipo) {
  const t = tipos.find(t => t.value === tipo)
  return t ? t.label.slice(0, -1) : tipo
}

function onSelectPunto(punto) {
  emit('select-punto', punto)
}

watch(searchQuery, () => {
  // Reset selection when searching
})
</script>

<style scoped>
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: 280px;
  height: 100vh;
  background: white;
  box-shadow: 2px 0 8px rgba(0,0,0,0.1);
  z-index: 200;
  display: flex;
  flex-direction: column;
  transform: translateX(-100%);
  transition: transform 0.3s ease;
}

.sidebar.open {
  transform: translateX(0);
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #eee;
}

.sidebar-header h3 {
  margin: 0;
  font-size: 1.1rem;
}

.btn-close-sidebar {
  width: 32px;
  height: 32px;
  border: none;
  background: #f0f0f0;
  border-radius: 50%;
  font-size: 1.2rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.search-box {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #eee;
}

.search-input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 0.95rem;
}

.search-input:focus {
  outline: none;
  border-color: #2196F3;
}

.filters {
  padding: 0.75rem 1rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  border-bottom: 1px solid #eee;
}

.filters-label {
  width: 100%;
  font-size: 0.85rem;
  color: #666;
  margin-bottom: 0.25rem;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.35rem 0.6rem;
  background: #f5f5f5;
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.8rem;
}

.filter-item input {
  display: none;
}

.filter-check {
  width: 12px;
  height: 12px;
  border-radius: 3px;
  border: 2px solid #ddd;
}

.filter-check.rack { background: #37474F; border-color: #37474F; }
.filter-check.access_point { background: #2196F3; border-color: #2196F3; border-radius: 50%; }
.filter-check.boca_red { background: #4CAF50; border-color: #4CAF50; }
.filter-check.switch { background: #7B1FA2; border-color: #7B1FA2; }
.filter-check.router { background: #1565C0; border-color: #1565C0; border-radius: 50%; }

.filter-item input:not(:checked) + .filter-check {
  background: transparent;
  border-color: #999;
}

.puntos-list {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
}

.punto-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: none;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  text-align: left;
  transition: background 0.15s;
}

.punto-item:hover {
  background: #f5f5f5;
}

.punto-item.selected {
  background: #E3F2FD;
}

.punto-marker {
  width: 20px;
  height: 20px;
  border-radius: 4px;
  flex-shrink: 0;
}

.punto-marker.rack { background: #37474F; border-radius: 3px; }
.punto-marker.access_point { background: #2196F3; border-radius: 50%; }
.punto-marker.boca_red { background: #4CAF50; width: 14px; height: 14px; }
.punto-marker.switch { background: #7B1FA2; border-radius: 3px; }
.punto-marker.router { background: #1565C0; border-radius: 50%; }

.punto-info {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.punto-nombre {
  font-weight: 500;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.punto-tipo {
  font-size: 0.75rem;
  color: #888;
}

.no-results {
  text-align: center;
  color: #888;
  padding: 2rem;
  font-size: 0.9rem;
}

@media (min-width: 1024px) {
  .sidebar {
    position: static;
    transform: none;
    width: 260px;
    height: auto;
    box-shadow: none;
    border-right: 1px solid #eee;
    flex-shrink: 0;
  }

  .btn-close-sidebar {
    display: none;
  }

  .sidebar-header {
    padding: 0 1rem 1rem 0;
  }
}
</style>
