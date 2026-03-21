<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal">
      <div class="modal-header">
        <h2>QR del Punto</h2>
        <button class="btn-close" @click="$emit('close')">×</button>
      </div>
      
      <div class="qr-container">
        <canvas ref="qrCanvas"></canvas>
        <p class="punto-name">{{ punto.nombre }}</p>
        <p class="punto-info">{{ tipoLabel }} · {{ punto.descripcion || 'Sin descripción' }}</p>
      </div>

      <div class="actions">
        <button class="btn-copy" @click="copyUrl">
          {{ copied ? '✓ Copiado' : 'Copiar URL' }}
        </button>
        <button class="btn-download" @click="downloadQr">
          Descargar PNG
        </button>
      </div>
      
      <p class="hint">Escanea este código para ver la ubicación del punto en el plano.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import QRCode from 'qrcode'

const props = defineProps({
  punto: Object,
  baseUrl: {
    type: String,
    default: window.location.origin
  }
})

const emit = defineEmits(['close'])

const qrCanvas = ref(null)
const copied = ref(false)

const tiposMap = {
  rack: 'Rack',
  access_point: 'AP',
  boca_red: 'Boca de red',
  switch: 'Switch',
  router: 'Router'
}

const tipoLabel = ref('')

onMounted(() => {
  tipoLabel.value = tiposMap[props.punto.tipo] || props.punto.tipo
  const url = `${props.baseUrl}/view/${props.punto.id}`
  
  QRCode.toCanvas(qrCanvas.value, url, {
    width: 200,
    margin: 2,
    color: {
      dark: '#1a1a2e',
      light: '#ffffff'
    }
  })
})

function copyUrl() {
  const url = `${props.baseUrl}/view/${props.punto.id}`
  navigator.clipboard.writeText(url)
  copied.value = true
  setTimeout(() => { copied.value = false }, 2000)
}

function downloadQr() {
  const link = document.createElement('a')
  link.download = `qr-${props.punto.nombre.replace(/\s+/g, '-').toLowerCase()}.png`
  link.href = qrCanvas.value.toDataURL('image/png')
  link.click()
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  align-items: flex-end;
  justify-content: center;
  z-index: 200;
  padding: 0;
}

@media (min-width: 480px) {
  .modal-overlay {
    align-items: center;
    padding: 1rem;
  }
}

.modal {
  background: white;
  border-radius: 16px 16px 0 0;
  width: 100%;
  max-width: 100%;
  padding: 1rem;
  max-height: 85vh;
  overflow-y: auto;
}

@media (min-width: 480px) {
  .modal {
    border-radius: 16px;
    max-width: 340px;
    padding: 1.5rem;
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.1rem;
}

.btn-close {
  width: 32px;
  height: 32px;
  border: none;
  background: #f0f0f0;
  border-radius: 50%;
  font-size: 1.25rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

.qr-container {
  text-align: center;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 12px;
  margin-bottom: 0.75rem;
}

.qr-container canvas {
  border-radius: 8px;
}

.punto-name {
  margin: 0.75rem 0 0.2rem;
  font-size: 1rem;
  font-weight: 600;
  color: #1a1a2e;
}

.punto-info {
  margin: 0;
  font-size: 0.8rem;
  color: #666;
}

.actions {
  display: flex;
  gap: 0.4rem;
}

.btn-copy {
  flex: 1;
  padding: 0.75rem;
  background: #7B1FA2;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
}

.btn-copy:hover {
  background: #6A1B9A;
}

.btn-download {
  flex: 1;
  padding: 0.75rem;
  background: #2196F3;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
}

.btn-download:hover {
  background: #1976D2;
}

.hint {
  margin: 0.75rem 0 0;
  font-size: 0.75rem;
  color: #999;
  text-align: center;
}
</style>
