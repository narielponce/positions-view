from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import PuntoCreate, PuntoUpdate, PuntoResponse
from app.services import PuntoService

router = APIRouter(prefix="/puntos", tags=["Puntos"])


@router.post("", response_model=PuntoResponse, status_code=status.HTTP_201_CREATED)
def crear_punto(data: PuntoCreate, db: Session = Depends(get_db)):
    service = PuntoService(db)
    return service.crear(data)


@router.get("", response_model=list[PuntoResponse])
def listar_puntos(plano_id: int, db: Session = Depends(get_db)):
    service = PuntoService(db)
    return service.listar_por_plano(plano_id)


@router.put("/{punto_id}", response_model=PuntoResponse)
def actualizar_punto(punto_id: int, data: PuntoUpdate, db: Session = Depends(get_db)):
    service = PuntoService(db)
    punto = service.actualizar(punto_id, data)
    if not punto:
        raise HTTPException(status_code=404, detail="Punto no encontrado")
    return punto


@router.get("/{punto_id}", response_model=PuntoResponse)
def obtener_punto(punto_id: int, db: Session = Depends(get_db)):
    service = PuntoService(db)
    punto = service.obtener(punto_id)
    if not punto:
        raise HTTPException(status_code=404, detail="Punto no encontrado")
    return punto


@router.delete("/{punto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_punto(punto_id: int, db: Session = Depends(get_db)):
    service = PuntoService(db)
    if not service.eliminar(punto_id):
        raise HTTPException(status_code=404, detail="Punto no encontrado")
