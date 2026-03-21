<template>
  <div class="public-view">
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Cargando...</p>
    </div>

    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <a href="/" class="btn-home">Ir al inicio</a>
    </div>

    <template v-else-if="punto && plano">
      <header class="header">
        <div class="header-content">
          <span class="punto-tipo-mini" :class="punto.tipo"></span>
          <h1>{{ punto.nombre }}</h1>
          <span class="plano-nombre">{{ plano.nombre }}</span>
        </div>
      </header>

      <div class="plano-area">
        <div class="plano-container">
          <div
            class="punto-marker"
            :class="punto.tipo"
            :style="{ left: `${punto.x * 100}%`, top: `${punto.y * 100}%` }"
          ></div>
          <img
            v-if="plano.imagen_url"
            :src="fullImageUrl"
            class="plano-image"
            alt="Plano"
          />
          <div v-else class="no-image">
            <p>Sin imagen del plano</p>
          </div>
        </div>
      </div>

      <div class="info-section">
        <button class="info-toggle" @click="infoExpanded = !infoExpanded">
          <span class="info-toggle-icon">{{ infoExpanded ? '▼' : '▶' }}</span>
          <span>Información del punto</span>
        </button>
        
        <div v-if="infoExpanded" class="info-card">
          <div class="info-row" v-if="punto.descripcion">
            <div class="info-item">
              <span class="info-icon">📍</span>
              <div class="info-text">
                <span class="info-label">Ubicación</span>
                <span class="info-value">{{ punto.descripcion }}</span>
              </div>
            </div>
          </div>
          <div class="info-row">
            <div class="info-item">
              <span class="info-icon">🏷️</span>
              <div class="info-text">
                <span class="info-label">Tipo</span>
                <span class="info-value tipo-badge" :class="punto.tipo">{{ tipoLabel }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <footer class="footer">
        <a href="/" class="btn-open">Abrir en Position View</a>
      </footer>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api'

const route = useRoute()

const loading = ref(true)
const error = ref(null)
const infoExpanded = ref(true)
const punto = ref(null)
const plano = ref(null)

const tiposMap = {
  rack: 'Rack',
  access_point: 'Access Point',
  boca_red: 'Boca de red',
  switch: 'Switch',
  router: 'Router'
}

const tipoLabel = computed(() => tiposMap[punto.value?.tipo] || punto.value?.tipo || '')

const fullImageUrl = computed(() => {
  if (!plano.value?.imagen_url) return ''
  const base = import.meta.env.VITE_API_URL || ''
  return base + plano.value.imagen_url
})

onMounted(async () => {
  try {
    const puntoId = route.params.id
    const { data: puntoData } = await api.getPunto(puntoId)
    punto.value = puntoData

    const { data: planoData } = await api.getPlano(puntoData.plano_id)
    plano.value = planoData
  } catch (err) {
    error.value = err.response?.status === 404 
      ? 'Punto no encontrado' 
      : 'Error al cargar los datos'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.public-view {
  height: 100vh;
  height: 100dvh;
  display: flex;
  flex-direction: column;
  background: #121220;
  color: white;
  overflow: hidden;
}

.loading, .error {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid rgba(255,255,255,0.1);
  border-top-color: #2196F3;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error p {
  color: rgba(255,255,255,0.7);
  font-size: 1.1rem;
}

.btn-home {
  padding: 0.75rem 1.5rem;
  background: #2196F3;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 500;
}

.header {
  background: rgba(26, 26, 46, 0.95);
  backdrop-filter: blur(10px);
  padding: 0.5rem 1rem;
  flex-shrink: 0;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.header-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.punto-tipo-mini {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.punto-tipo-mini.rack { background: #37474F; border-radius: 2px; }
.punto-tipo-mini.access_point { background: #2196F3; }
.punto-tipo-mini.boca_red { background: #4CAF50; width: 8px; height: 8px; }
.punto-tipo-mini.switch { background: #7B1FA2; border-radius: 2px; width: 12px; height: 8px; }
.punto-tipo-mini.router { background: #1565C0; }

.header h1 {
  margin: 0;
  font-size: 0.9rem;
  font-weight: 600;
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.plano-nombre {
  font-size: 0.7rem;
  color: rgba(255,255,255,0.5);
  max-width: 80px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.plano-area {
  flex: 1;
  min-height: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.plano-container {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.plano-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.no-image {
  padding: 2rem;
  text-align: center;
  color: rgba(255,255,255,0.5);
}

.punto-marker {
  position: absolute;
  width: 56px;
  height: 56px;
  transform: translate(-50%, -50%);
  border: 4px solid white;
  box-shadow: 0 4px 16px rgba(0,0,0,0.6), 0 0 24px rgba(33, 150, 243, 0.5);
  z-index: 10;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { 
    box-shadow: 0 4px 16px rgba(0,0,0,0.6), 0 0 20px rgba(33, 150, 243, 0.4); 
    transform: translate(-50%, -50%) scale(1);
  }
  50% { 
    box-shadow: 0 4px 16px rgba(0,0,0,0.6), 0 0 40px rgba(33, 150, 243, 0.6); 
    transform: translate(-50%, -50%) scale(1.05);
  }
}

.punto-marker.rack {
  background: #37474F;
  border-radius: 8px;
}

.punto-marker.access_point {
  background: #2196F3;
  border-radius: 50%;
}

.punto-marker.boca_red {
  background: #4CAF50;
  border-radius: 4px;
  width: 36px;
  height: 36px;
}

.punto-marker.switch {
  background: #7B1FA2;
  border-radius: 4px;
  width: 60px;
  height: 36px;
}

.punto-marker.router {
  background: #1565C0;
  border-radius: 50%;
}

.info-section {
  background: rgba(26, 26, 46, 0.95);
  backdrop-filter: blur(10px);
  flex-shrink: 0;
}

.info-toggle {
  width: 100%;
  padding: 0.75rem 1rem;
  background: transparent;
  border: none;
  color: white;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  cursor: pointer;
  border-top: 1px solid rgba(255,255,255,0.1);
}

.info-toggle-icon {
  color: rgba(255,255,255,0.5);
  font-size: 0.6rem;
}

.info-card {
  padding: 0 1rem 0.75rem;
}

.info-row {
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.info-row:last-child {
  border-bottom: none;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.info-icon {
  font-size: 1rem;
  flex-shrink: 0;
}

.info-text {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.info-label {
  font-size: 0.75rem;
  color: rgba(255,255,255,0.5);
}

.info-value {
  font-size: 0.85rem;
  color: white;
}

.tipo-badge {
  display: inline-block;
  padding: 0.15rem 0.5rem;
  border-radius: 10px;
  font-size: 0.75rem;
}

.tipo-badge.rack { background: #37474F; }
.tipo-badge.access_point { background: #2196F3; }
.tipo-badge.boca_red { background: #4CAF50; }
.tipo-badge.switch { background: #7B1FA2; }
.tipo-badge.router { background: #1565C0; }

.footer {
  padding: 0.75rem 1rem;
  background: rgba(26, 26, 46, 0.95);
  flex-shrink: 0;
  border-top: 1px solid rgba(255,255,255,0.1);
}

.btn-open {
  display: block;
  width: 100%;
  padding: 0.875rem;
  background: #4CAF50;
  color: white;
  text-decoration: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.95rem;
  text-align: center;
}

@media (min-width: 768px) {
  .public-view {
    max-width: 600px;
    margin: 0 auto;
    border-radius: 16px;
    height: auto;
    min-height: 100vh;
    margin-top: 1rem;
    margin-bottom: 1rem;
  }
  
  .header {
    position: relative;
    background: #1a1a2e;
    border-radius: 16px 16px 0 0;
  }
  
  .header-content {
    justify-content: center;
  }
  
  .plano-nombre {
    max-width: none;
  }
  
  .info-section {
    border-radius: 0 0 16px 16px;
  }
  
  .plano-area {
    background: #1a1a2e;
  }
  
  .plano-container {
    background: #121220;
    border-radius: 0;
  }
  
  .plano-image {
    max-height: none;
    width: 100%;
  }
  
  .punto-marker {
    width: 48px;
    height: 48px;
  }
  
  .punto-marker.boca_red {
    width: 32px;
    height: 32px;
  }
  
  .punto-marker.switch {
    width: 52px;
    height: 32px;
  }
}
</style>
