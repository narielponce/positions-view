<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal">
      <div class="modal-header">
        <h2>{{ punto && punto.id ? 'Editar' : 'Nuevo' }} Punto</h2>
        <button class="btn-close" @click="$emit('close')">×</button>
      </div>
      
      <form @submit.prevent="onSubmit">
        <div class="form-group">
          <label>Nombre</label>
          <input v-model="form.nombre" type="text" required placeholder="Ej: Switch Core" />
        </div>

        <div class="form-group">
          <label>Descripción</label>
          <input v-model="form.descripcion" type="text" placeholder="Ej: Cerca de columna J7" />
        </div>

        <div class="form-group">
          <label>Tipo</label>
          <div class="tipo-grid">
            <button
              v-for="t in tipos"
              :key="t.value"
              type="button"
              class="tipo-btn"
              :class="{ active: form.tipo === t.value, [t.value]: true }"
              @click="form.tipo = t.value"
            >
              <div class="tipo-icon"></div>
              <span class="tipo-label">{{ t.label }}</span>
            </button>
          </div>
        </div>

        <div class="actions">
          <button v-if="punto && punto.id" type="button" class="btn-qr" @click="$emit('generate-qr')">Generar QR</button>
          <button v-if="punto && punto.id" type="button" class="btn-delete" @click="$emit('delete')">Eliminar</button>
          <button type="button" class="btn-cancel" @click="$emit('close')">Cancelar</button>
          <button type="submit" class="btn-save">Guardar</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch } from 'vue'

const props = defineProps({
  punto: Object
})

const emit = defineEmits(['save', 'close', 'delete', 'generate-qr'])

const tipos = [
  { value: 'rack', label: 'Rack' },
  { value: 'access_point', label: 'AP' },
  { value: 'boca_red', label: 'Boca' },
  { value: 'switch', label: 'Switch' },
  { value: 'router', label: 'Router' }
]

const form = reactive({
  nombre: '',
  tipo: 'rack',
  descripcion: ''
})

watch(() => props.punto, (val) => {
  if (val) {
    form.nombre = val.nombre || ''
    form.tipo = val.tipo || 'rack'
    form.descripcion = val.descripcion || ''
  }
}, { immediate: true })

function onSubmit() {
  emit('save', { ...form })
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
  z-index: 100;
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
    max-width: 400px;
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

.form-group {
  margin-bottom: 0.75rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.35rem;
  font-weight: 500;
  color: #333;
  font-size: 0.9rem;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 0.9rem;
  transition: border-color 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: #2196F3;
}

.tipo-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.4rem;
}

.tipo-btn {
  padding: 0.6rem 0.4rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.2rem;
  transition: all 0.2s;
}

.tipo-btn.active {
  border-color: #2196F3;
  background: #E3F2FD;
}

.tipo-icon {
  width: 18px;
  height: 18px;
  background: #666;
  display: block;
}

.tipo-label {
  font-size: 0.75rem;
  color: #666;
}

.tipo-btn.active .tipo-label {
  color: #1976D2;
  font-weight: 500;
}

.tipo-btn.active .tipo-icon {
  background: #333;
}

/* Rack */
.tipo-btn.rack .tipo-icon {
  background: #37474F;
  border-radius: 3px;
}

/* Access Point */
.tipo-btn.access_point .tipo-icon {
  background: #2196F3;
  border-radius: 50%;
}

/* Boca de red */
.tipo-btn.boca_red .tipo-icon {
  background: #4CAF50;
  border-radius: 2px;
  width: 14px;
  height: 14px;
}

/* Switch */
.tipo-btn.switch .tipo-icon {
  background: #7B1FA2;
  border-radius: 2px;
  width: 26px;
  height: 16px;
}

/* Router */
.tipo-btn.router .tipo-icon {
  background: #1565C0;
  border-radius: 50%;
  position: relative;
}

.tipo-btn.router .tipo-icon::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 8px;
  height: 8px;
  background: rgba(255,255,255,0.3);
  border-radius: 50%;
}

.actions {
  display: flex;
  gap: 0.4rem;
  margin-top: 1rem;
}

.btn-qr {
  padding: 0.75rem;
  background: #7B1FA2;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  white-space: nowrap;
}

.btn-qr:hover {
  background: #6A1B9A;
}

.btn-delete {
  padding: 0.75rem;
  background: #f44336;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  white-space: nowrap;
}

.btn-delete:hover {
  background: #d32f2f;
}

.btn-cancel {
  flex: 1;
  padding: 0.75rem;
  background: #f0f0f0;
  border: none;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
}

.btn-save {
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

.btn-save:hover {
  background: #1976D2;
}
</style>
