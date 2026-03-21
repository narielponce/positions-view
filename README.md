# Position View

Aplicación web para gestionar la ubicación de activos (equipos de red) sobre un plano.

## Stack

- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **Frontend**: Vue 3 + Vite
- **Contenedores**: Docker + Docker Compose

## Desarrollo local

```bash
# 1. Crear DB
createdb position_view

# 2. Backend
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000

# 3. Frontend (en otra terminal)
cd frontend
npm install
npm run dev
```

## Docker (desarrollo)

```bash
docker-compose up --build
```

- Frontend: http://localhost:3000
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

## Producción (VPS con GHCR)

```bash
# Login a GHCR
docker login ghcr.io

# Pull y ejecutar
docker-compose -f docker-compose.prod.yml up -d
```

## API Endpoints

```bash
# Planos
POST   /planos           # Crear plano
GET    /planos           # Listar planos
GET    /planos/{id}      # Obtener plano

# Puntos
POST   /puntos           # Crear punto
GET    /puntos?plano_id= # Listar puntos por plano
PUT    /puntos/{id}      # Editar punto
```

## Ejemplos con curl

```bash
# Crear plano
curl -X POST http://localhost:8000/planos \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Galpón A"}'

# Crear punto (coordenadas relativas 0-1)
curl -X POST http://localhost:8000/puntos \
  -H "Content-Type: application/json" \
  -d '{"plano_id": 1, "nombre": "Switch Core", "tipo": "switch", "x": 0.5, "y": 0.3}'

# Editar punto
curl -X PUT http://localhost:8000/puntos/1 \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Switch Core v2", "tipo": "router"}'
```
