<template>
  <div class="plano-viewer">
    <div class="plano-header">
      <h2>{{ plano.nombre }}</h2>
      <label class="upload-btn" :class="{ loading: uploading }">
        <input type="file" accept="image/*" @change="onFileChange" ref="fileInput" :disabled="uploading" />
        <span v-if="uploading">Subiendo...</span>
        <span v-else>{{ plano.imagen_url ? 'Cambiar' : 'Subir' }}</span>
      </label>
    </div>

    <div
      class="zoom-container"
      ref="zoomContainerRef"
      @wheel.prevent="onWheel"
      @mousedown="onPanStart"
      @mousemove="onPanMove"
      @mouseup="onPanEnd"
      @mouseleave="onPanEnd"
      @touchstart="onTouchStart"
      @touchmove="onTouchMove"
      @touchend="onTouchEnd"
    >
      <div
        class="plano-container"
        ref="containerRef"
        :style="containerStyle"
        @click="onContainerClick"
      >
        <div v-if="uploading" class="upload-overlay">
          <div class="spinner"></div>
        </div>

        <img
          v-if="plano.imagen_url"
          :src="fullImageUrl"
          class="plano-imagen"
          alt="Plano"
          :class="{ loading: uploading }"
          draggable="false"
        />
        <div v-else class="plano-placeholder">
          <div class="placeholder-icon">📐</div>
          <p>Sin imagen</p>
          <p class="hint">Subí una imagen para comenzar</p>
        </div>

        <div
          v-for="punto in puntos"
          :key="punto.id"
          class="punto"
          :class="[punto.tipo, { 
            dragging: draggingId === punto.id,
            highlighted: highlightedPuntoId === punto.id
          }]"
          :style="{ left: `${punto.x * 100}%`, top: `${punto.y * 100}%` }"
          @mousedown="onMouseDown($event, punto)"
          @touchstart.prevent="onTouchStartPunto($event, punto)"
          :title="punto.nombre"
        >
          <div class="marker-inner">
            <div v-if="punto.tipo === 'rack'" class="rack-lines">
              <span></span><span></span><span></span>
            </div>
            <div v-else-if="punto.tipo === 'access_point'" class="wifi-waves"></div>
            <div v-else-if="punto.tipo === 'switch'" class="switch-ports">
              <span></span><span></span><span></span><span></span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="zoom-controls">
      <button @click="zoomOut" title="Zoom out">−</button>
      <span class="zoom-level">{{ Math.round(scale * 100) }}%</span>
      <button @click="zoomIn" title="Zoom in">+</button>
      <button @click="resetZoom" title="Reset">⟲</button>
    </div>

    <p v-if="plano.imagen_url && puntos.length > 0" class="hint-bottom">
      {{ puntos.length }} punto{{ puntos.length !== 1 ? 's' : '' }} · Arrastrá para mover · Tap para editar
    </p>
  </div>
</template>

<script setup>
import { computed, ref, defineProps, defineEmits, nextTick } from 'vue'

const props = defineProps({
  plano: Object,
  puntos: Array,
  uploading: Boolean,
  highlightedPuntoId: Number
})

const emit = defineEmits(['create-punto', 'edit-punto', 'upload-imagen', 'update-punto'])

const containerRef = ref(null)
const zoomContainerRef = ref(null)
const draggingId = ref(null)
const isDragging = ref(false)
const dragStartX = ref(0)
const dragStartY = ref(0)
const puntoClickHandled = ref(false)

const scale = ref(1)
const translateX = ref(0)
const translateY = ref(0)
const isPanning = ref(false)
const panStartX = ref(0)
const panStartY = ref(0)
const initialTranslateX = ref(0)
const initialTranslateY = ref(0)

let lastTouchDistance = 0

const containerStyle = computed(() => ({
  transform: `translate(${translateX.value}px, ${translateY.value}px) scale(${scale.value})`,
  transformOrigin: 'center center'
}))

const fullImageUrl = computed(() => {
  if (!props.plano.imagen_url) return ''
  const base = import.meta.env.VITE_API_URL || ''
  return base + props.plano.imagen_url
})

function zoomIn() {
  scale.value = Math.min(3, scale.value + 0.25)
}

function zoomOut() {
  scale.value = Math.max(0.5, scale.value - 0.25)
}

function resetZoom() {
  scale.value = 1
  translateX.value = 0
  translateY.value = 0
}

function onWheel(e) {
  const delta = e.deltaY > 0 ? -0.1 : 0.1
  scale.value = Math.max(0.5, Math.min(3, scale.value + delta))
}

function onPanStart(e) {
  if (e.target === containerRef.value || e.target.classList.contains('plano-imagen')) {
    isPanning.value = true
    panStartX.value = e.clientX
    panStartY.value = e.clientY
    initialTranslateX.value = translateX.value
    initialTranslateY.value = translateY.value
  }
}

function onPanMove(e) {
  if (!isPanning.value) return
  const dx = e.clientX - panStartX.value
  const dy = e.clientY - panStartY.value
  translateX.value = initialTranslateX.value + dx
  translateY.value = initialTranslateY.value + dy
}

function onPanEnd() {
  isPanning.value = false
}

function onTouchStart(e) {
  if (e.touches.length === 2) {
    lastTouchDistance = getTouchDistance(e.touches)
  } else if (e.touches.length === 1) {
    const touch = e.touches[0]
    if (touch.target === containerRef.value || touch.target.classList.contains('plano-imagen')) {
      isPanning.value = true
      panStartX.value = touch.clientX
      panStartY.value = touch.clientY
      initialTranslateX.value = translateX.value
      initialTranslateY.value = translateY.value
    }
  }
}

function onTouchMove(e) {
  if (e.touches.length === 2) {
    const distance = getTouchDistance(e.touches)
    if (lastTouchDistance > 0) {
      const delta = (distance - lastTouchDistance) * 0.005
      scale.value = Math.max(0.5, Math.min(3, scale.value + delta))
    }
    lastTouchDistance = distance
  } else if (isPanning.value && e.touches.length === 1) {
    const touch = e.touches[0]
    const dx = touch.clientX - panStartX.value
    const dy = touch.clientY - panStartY.value
    translateX.value = initialTranslateX.value + dx
    translateY.value = initialTranslateY.value + dy
  }
}

function onTouchEnd() {
  isPanning.value = false
  lastTouchDistance = 0
}

function getTouchDistance(touches) {
  const dx = touches[0].clientX - touches[1].clientX
  const dy = touches[0].clientY - touches[1].clientY
  return Math.sqrt(dx * dx + dy * dy)
}

function centerOnPunto(punto) {
  nextTick(() => {
    scale.value = 1.5
    const centerX = zoomContainerRef.value.clientWidth / 2
    const centerY = zoomContainerRef.value.clientHeight / 2
    translateX.value = centerX - (punto.x * containerRef.value.clientWidth)
    translateY.value = centerY - (punto.y * containerRef.value.clientHeight)
  })
}

let touchStartTime = 0
let touchMoved = false

function onMouseDown(e, punto) {
  if (props.uploading) return
  e.preventDefault()
  e.stopPropagation()
  
  draggingId.value = punto.id
  isDragging.value = false
  dragStartX.value = e.clientX
  dragStartY.value = e.clientY
  puntoClickHandled.value = true
  
  const rect = containerRef.value.getBoundingClientRect()
  
  const onMouseMove = (moveEvent) => {
    const dist = Math.sqrt(
      Math.pow(moveEvent.clientX - dragStartX.value, 2) + 
      Math.pow(moveEvent.clientY - dragStartY.value, 2)
    )
    if (dist > 5) {
      isDragging.value = true
    }
    
    if (isDragging.value) {
      let x = (moveEvent.clientX - rect.left) / rect.width
      let y = (moveEvent.clientY - rect.top) / rect.height
      x = Math.max(0.02, Math.min(0.98, x))
      y = Math.max(0.02, Math.min(0.98, y))
      punto.x = x
      punto.y = y
    }
  }
  
  const onMouseUp = () => {
    draggingId.value = null
    document.removeEventListener('mousemove', onMouseMove)
    document.removeEventListener('mouseup', onMouseUp)
    
    if (isDragging.value) {
      emit('update-punto', { id: punto.id, x: punto.x, y: punto.y })
    } else {
      emit('edit-punto', punto)
    }
    
    setTimeout(() => {
      puntoClickHandled.value = false
    }, 100)
  }
  
  document.addEventListener('mousemove', onMouseMove)
  document.addEventListener('mouseup', onMouseUp)
}

function onTouchStartPunto(e, punto) {
  if (props.uploading) return
  
  touchStartTime = Date.now()
  touchMoved = false
  draggingId.value = punto.id
  isDragging.value = false
  dragStartX.value = e.touches[0].clientX
  dragStartY.value = e.touches[0].clientY
  
  const rect = containerRef.value.getBoundingClientRect()
  const startX = dragStartX.value
  const startY = dragStartY.value
  
  const onTouchMove = (moveEvent) => {
    const dist = Math.sqrt(
      Math.pow(moveEvent.touches[0].clientX - startX, 2) + 
      Math.pow(moveEvent.touches[0].clientY - startY, 2)
    )
    if (dist > 10) {
      touchMoved = true
      isDragging.value = true
    }
    
    if (isDragging.value) {
      let x = (moveEvent.touches[0].clientX - rect.left) / rect.width
      let y = (moveEvent.touches[0].clientY - rect.top) / rect.height
      x = Math.max(0.02, Math.min(0.98, x))
      y = Math.max(0.02, Math.min(0.98, y))
      punto.x = x
      punto.y = y
    }
  }
  
  const onTouchEnd = () => {
    draggingId.value = null
    document.removeEventListener('touchmove', onTouchMove)
    document.removeEventListener('touchend', onTouchEnd)
    
    if (isDragging.value) {
      emit('update-punto', { id: punto.id, x: punto.x, y: punto.y })
    } else if (!touchMoved) {
      emit('edit-punto', punto)
    }
  }
  
  document.addEventListener('touchmove', onTouchMove, { passive: false })
  document.addEventListener('touchend', onTouchEnd)
}

function onContainerClick(e) {
  if (!props.plano.imagen_url || props.uploading || draggingId.value) return
  if (isPanning.value) return
  if (puntoClickHandled.value) return
  
  const container = containerRef.value
  const zoomContainer = zoomContainerRef.value
  const rect = zoomContainer.getBoundingClientRect()
  
  const centerX = rect.width / 2 + rect.left
  const centerY = rect.height / 2 + rect.top
  
  const relX = e.clientX - centerX - translateX.value
  const relY = e.clientY - centerY - translateY.value
  
  const x = (relX / scale.value / container.offsetWidth) + 0.5
  const y = (relY / scale.value / container.offsetHeight) + 0.5
  
  if (x >= 0.02 && x <= 0.98 && y >= 0.02 && y <= 0.98) {
    emit('create-punto', { x, y })
  }
}

function onPuntoClick(punto) {
  if (draggingId.value || isDragging.value) return
  emit('edit-punto', punto)
}

function onFileChange(e) {
  const file = e.target.files[0]
  if (file) {
    emit('upload-imagen', file)
    e.target.value = ''
  }
}

defineExpose({ centerOnPunto })
</script>

<style scoped>
.plano-viewer {
  width: 100%;
  display: flex;
  flex-direction: column;
}

.plano-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  gap: 0.5rem;
}

.plano-header h2 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.upload-btn {
  padding: 0.75rem 1rem;
  background: #4CAF50;
  color: white;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  min-height: 44px;
}

.upload-btn:hover {
  background: #43A047;
}

.upload-btn.loading {
  background: #9E9E9E;
  cursor: wait;
}

.upload-btn input {
  display: none;
}

.zoom-container {
  position: relative;
  width: 100%;
  min-height: 400px;
  max-height: 70vh;
  overflow: hidden;
  background: #1a1a2e;
  border-radius: 12px;
  cursor: grab;
  display: flex;
  align-items: center;
  justify-content: center;
}

.zoom-container:active {
  cursor: grabbing;
}

.plano-container {
  position: relative;
  width: 100%;
  transition: transform 0.1s ease-out;
  will-change: transform;
}

.plano-imagen {
  width: 100%;
  height: auto;
  display: block;
  pointer-events: none;
}

.plano-imagen.loading {
  opacity: 0.5;
}

.upload-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 20;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.plano-placeholder {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #666;
  padding: 2rem;
  text-align: center;
}

.placeholder-icon {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

.plano-placeholder p {
  margin: 0;
  color: #888;
}

.plano-placeholder .hint {
  margin-top: 0.5rem;
  font-size: 0.85rem;
  color: #666;
}

.zoom-controls {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  display: flex;
  gap: 0.25rem;
  background: white;
  padding: 0.25rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
  z-index: 10;
}

.zoom-controls button {
  width: 36px;
  height: 36px;
  border: none;
  background: #f5f5f5;
  border-radius: 6px;
  font-size: 1.2rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.zoom-controls button:hover {
  background: #e0e0e0;
}

.zoom-level {
  min-width: 50px;
  text-align: center;
  font-size: 0.85rem;
  color: #666;
  line-height: 36px;
}

.hint-bottom {
  text-align: center;
  color: #888;
  margin-top: 0.75rem;
  font-size: 0.85rem;
}

.punto {
  position: absolute;
  width: 40px;
  height: 40px;
  border: 3px solid white;
  transform: translate(-50%, -50%);
  cursor: grab;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 3px 8px rgba(0,0,0,0.4);
  transition: transform 0.15s, box-shadow 0.15s, border-width 0.15s;
  z-index: 10;
}

.punto:active {
  cursor: grabbing;
}

.punto.dragging {
  transform: translate(-50%, -50%) scale(1.15);
  box-shadow: 0 6px 16px rgba(0,0,0,0.5);
  z-index: 100;
  transition: none;
}

.punto.highlighted {
  border-width: 4px;
  box-shadow: 0 0 0 4px rgba(33, 150, 243, 0.4), 0 3px 8px rgba(0,0,0,0.4);
}

.marker-inner {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* RACK - Cuadrado gris con líneas */
.punto.rack {
  background: #37474F;
  border-radius: 6px;
}

.punto.rack .rack-lines {
  display: flex;
  flex-direction: column;
  gap: 2px;
  width: 50%;
  height: 60%;
}

.punto.rack .rack-lines span {
  background: rgba(255,255,255,0.3);
  height: 3px;
  border-radius: 1px;
}

/* ACCESS POINT - Círculo azul */
.punto.access_point {
  background: #2196F3;
  border-radius: 50%;
}

.punto.access_point .wifi-waves {
  width: 60%;
  height: 60%;
  position: relative;
}

.punto.access_point .wifi-waves::before,
.punto.access_point .wifi-waves::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border: 2px solid white;
  border-radius: 50%;
  opacity: 0.7;
}

.punto.access_point .wifi-waves::before {
  width: 100%;
  height: 100%;
}

.punto.access_point .wifi-waves::after {
  width: 50%;
  height: 50%;
}

/* BOCA DE RED - Cuadrado chico verde */
.punto.boca_red {
  background: #4CAF50;
  border-radius: 4px;
  width: 24px;
  height: 24px;
}

/* SWITCH - Rectángulo violeta */
.punto.switch {
  background: #7B1FA2;
  border-radius: 4px;
  width: 44px;
  height: 28px;
}

.punto.switch .switch-ports {
  display: flex;
  gap: 3px;
  padding: 0 4px;
}

.punto.switch .switch-ports span {
  width: 4px;
  height: 4px;
  background: rgba(255,255,255,0.6);
  border-radius: 50%;
  align-self: center;
}

/* ROUTER - Círculo azul oscuro */
.punto.router {
  background: #1565C0;
  border-radius: 50%;
}

.punto.router::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 40%;
  height: 40%;
  background: white;
  border-radius: 50%;
  opacity: 0.3;
  pointer-events: none;
}

@media (min-width: 768px) {
  .plano-header h2 {
    font-size: 1.25rem;
  }

  .zoom-container {
    min-height: auto;
    max-height: none;
  }

  .punto {
    width: 32px;
    height: 32px;
  }

  .punto.boca_red {
    width: 20px;
    height: 20px;
  }

  .punto.switch {
    width: 36px;
    height: 22px;
  }

  .punto.switch .switch-ports span {
    width: 3px;
    height: 3px;
  }

  .punto.rack .rack-lines span {
    height: 2px;
  }
}
</style>
