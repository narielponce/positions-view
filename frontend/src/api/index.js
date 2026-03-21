import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api'
})

export default {
  getPlanos() {
    return api.get('/planos')
  },
  getPlano(id) {
    return api.get(`/planos/${id}`)
  },
  createPlano(data) {
    return api.post('/planos', data)
  },
  deletePlano(id) {
    return api.delete(`/planos/${id}`)
  },
  uploadImagen(planoId, file) {
    const formData = new FormData()
    formData.append('file', file)
    return api.post(`/planos/${planoId}/imagen`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  getPuntos(planoId) {
    return api.get('/puntos', { params: { plano_id: planoId } })
  },
  createPunto(data) {
    return api.post('/puntos', data)
  },
  updatePunto(id, data) {
    return api.put(`/puntos/${id}`, data)
  },
  deletePunto(id) {
    return api.delete(`/puntos/${id}`)
  },
  getPunto(id) {
    return api.get(`/puntos/${id}`)
  }
}
