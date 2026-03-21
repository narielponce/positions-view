<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal">
      <div class="modal-header">
        <h2>Nuevo Plano</h2>
        <button class="btn-close" @click="$emit('close')">×</button>
      </div>
      
      <form @submit.prevent="onSubmit">
        <div class="form-group">
          <label>Nombre del plano</label>
          <input 
            v-model="nombre" 
            type="text" 
            required 
            placeholder="Ej: Planta Baja"
            ref="inputRef"
          />
        </div>

        <div class="actions">
          <button type="button" class="btn-cancel" @click="$emit('close')">Cancelar</button>
          <button type="submit" class="btn-save">Crear</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const emit = defineEmits(['create', 'close'])
const nombre = ref('')
const inputRef = ref(null)

onMounted(() => {
  inputRef.value?.focus()
})

function onSubmit() {
  if (nombre.value.trim()) {
    emit('create', nombre.value.trim())
  }
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
  padding: 1.5rem;
}

@media (min-width: 480px) {
  .modal {
    border-radius: 16px;
    max-width: 400px;
    padding: 2rem;
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.25rem;
}

.btn-close {
  width: 40px;
  height: 40px;
  border: none;
  background: #f0f0f0;
  border-radius: 50%;
  font-size: 1.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.form-group input {
  width: 100%;
  padding: 0.875rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: #2196F3;
}

.actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.btn-cancel {
  flex: 1;
  padding: 0.875rem;
  background: #f0f0f0;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
}

.btn-save {
  flex: 1;
  padding: 0.875rem;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
}

.btn-save:hover {
  background: #43A047;
}
</style>
