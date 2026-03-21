# Position View - AGENTS.md

Agent guidance for the Position View codebase.

## Project Overview

MVP for managing asset locations (network equipment) on floor plan images.

- **Backend**: FastAPI + SQLAlchemy + Alembic + PostgreSQL
- **Frontend**: Vue 3 + Vite + Axios
- **Infrastructure**: Docker + Docker Compose
- **Ports**: Frontend 3000, API 8000, PostgreSQL 5432

## Quick Start

```bash
# Development with Docker
docker compose up --build -d

# Direct backend (requires pip + PostgreSQL)
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload

# Direct frontend
cd frontend
npm install
npm run dev
```

## Build/Lint/Test Commands

### Backend
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head
alembic revision --autogenerate -m "description"

# Run server
uvicorn app.main:app --reload --port 8000

# Test API
curl http://localhost:8000/health
curl http://localhost:8000/docs  # Swagger UI
```

### Frontend
```bash
cd frontend

# Install dependencies
npm install

# Development server
npm run dev

# Production build
npm run build

# Preview production build
npm run preview
```

### Docker
```bash
# Full stack
docker compose up --build -d

# Rebuild specific service
docker compose up --build [backend|frontend|db] -d

# Logs
docker compose logs -f [backend|frontend|db]

# Clean rebuild (removes volumes!)
docker compose down -v && docker compose up --build -d

# Shell into container
docker exec -it position-view-backend-1 /bin/sh
```

## Code Style Guidelines

### Python (Backend)

**Imports**:
- Standard library first, then third-party, then local
- Use absolute imports from `app.` package
- Never use `*` imports

```python
# Correct
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from app.models import Plano
from app.schemas import PlanoCreate

# Avoid
from app.models.plano import Plano as P
```

**Naming**:
- Classes: `PascalCase` (e.g., `PlanoService`)
- Functions/variables: `snake_case` (e.g., `get_plano`)
- Constants: `UPPER_SNAKE_CASE`
- Private methods: prefix with `_`

**Pydantic Schemas**:
```python
from pydantic import BaseModel, Field

class PlanoCreate(BaseModel):
    nombre: str

class PuntoCreate(BaseModel):
    plano_id: int
    x: float = Field(..., ge=0, le=1)
    y: float = Field(..., ge=0, le=1)

class PuntoUpdate(BaseModel):
    nombre: Optional[str] = None
    tipo: Optional[str] = None
    x: Optional[float] = Field(None, ge=0, le=1)  # For drag repositioning
    y: Optional[float] = Field(None, ge=0, le=1)
```

**SQLAlchemy Models**:
- Use `declarative_base()` pattern
- Never use `metadata` as column name (reserved by SQLAlchemy)
- Use `extra_data` for JSON metadata fields

**Error Handling**:
```python
from fastapi import HTTPException, status

# In routers
if not plano:
    raise HTTPException(status_code=404, detail="Plano no encontrado")
```

**Layer Separation**:
```
api/          → Routers, HTTP handling
services/     → Business logic
repositories/ → Data access (DB queries)
models/       → SQLAlchemy entities
schemas/      → Pydantic DTOs
```

### Vue 3 (Frontend)

**Structure**:
```
frontend/src/
├── App.vue              → Main app component
├── main.js              → Entry point
├── api/index.js         → Axios API client
└── components/
    ├── PlanoViewer.vue       → Floor plan display + interactive canvas
    ├── PuntoModal.vue       → Create/edit punto modal
    └── CreatePlanoModal.vue → Create plano modal
```

**Script Setup**:
```vue
<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/api'

const props = defineProps({ plano: Object })
const emit = defineEmits(['create-punto', 'edit-punto', 'update-punto', 'upload-imagen'])
</script>
```

**PlanoViewer Events**:
- `@create-punto` - Emitted with `{x, y}` when clicking on empty area
- `@edit-punto` - Emitted with full punto object when tapping a punto
- `@update-punto` - Emitted with `{id, x, y}` after drag ends
- `@upload-imagen` - Emitted with File object when image is selected

**Naming**:
- Components: `PascalCase.vue`
- Files: `kebab-case.js`
- Props: `camelCase` (HTML: `kebab-case`)

**Mobile-First Responsive Design**:
- Use CSS media queries with breakpoint at `768px`
- Modals: slide-up from bottom on mobile (`align-items: flex-end`)
- Touch targets: minimum `44px` height
- Puntos (markers): `36px` on mobile, `28px` on desktop
- Header: stacked layout on mobile, inline on desktop

**API Calls**:
```javascript
// In api/index.js
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api'
})

export default {
  getPlanos() {
    return api.get('/planos')
  },
  uploadImagen(planoId, file) {
    const formData = new FormData()
    formData.append('file', file)
    return api.post(`/planos/${planoId}/imagen`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  updatePunto(id, data) {
    return api.put(`/puntos/${id}`, data)
  }
}
```

**No Comments**: Do not add comments unless explicitly requested.

### General

- Use 2 spaces for indentation (no tabs)
- Remove trailing whitespace
- No TODO comments in production code
- Keep functions small and focused
- Handle errors gracefully (no bare `except:`)

## Database

### Coordinate System

- All coordinates are relative (0.0 to 1.0)
- x: horizontal position (0 = left, 1 = right)
- y: vertical position (0 = top, 1 = bottom)
- Render with: `left: ${x * 100}%, top: ${y * 100}%`
- Bounds check: `x >= 0.02 && x <= 0.98 && y >= 0.02 && y <= 0.98`

### Migrations

```bash
# Create migration
alembic revision --autogenerate -m "add column"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## API Endpoints

```
POST   /planos              → Create plano
GET    /planos              → List all planos
GET    /planos/{id}         → Get single plano
POST   /planos/{id}/imagen  → Upload floor plan image (multipart/form-data)

POST   /puntos              → Create punto
GET    /puntos?plano_id=X   → List puntos for plano
PUT    /puntos/{id}          → Update punto (name, type, x, y)

GET    /health              → Health check
```

## Known Constraints

- Coordinates must always be 0-1 (validated by Pydantic)
- Image uploads stored in `/app/uploads/` (container path)
- Volume mounts required for persistence across rebuilds
- No authentication in MVP scope
- Plano imagen_url stored as `/uploads/{filename}`

## Features

### Drag and Drop Puntos
- Drag puntos to reposition on the floor plan
- Position saved automatically on drag end
- Tap to open edit modal (only if no significant drag movement)
- Minimum 5px movement threshold to detect drag vs tap

### Image Upload
- Click "Subir" button to select image
- Spinner shown during upload
- Images stored in backend `/app/uploads/` directory
- Proxy configured in nginx for `/uploads/` path

## Troubleshooting

**Image not displaying**: Check nginx proxy config and ensure trailing slash in `proxy_pass`

**CORS issues**: Backend CORS configured for all origins in development

**DB connection**: Wait for `db` healthcheck before starting `backend`

**Migration errors**: May need fresh DB (`docker compose down -v`)

**Mobile UI issues**: Ensure viewport meta tag is set in index.html

**Drag not working**: Check that `touch-action: none` is set on container and `pointer-events` are handled correctly
