from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import PlanoCreate, PlanoResponse
from app.services import PlanoService

router = APIRouter(prefix="/planos", tags=["Planos"])


@router.post("", response_model=PlanoResponse, status_code=status.HTTP_201_CREATED)
def crear_plano(data: PlanoCreate, db: Session = Depends(get_db)):
    service = PlanoService(db)
    return service.crear(data)


@router.get("", response_model=list[PlanoResponse])
def listar_planos(db: Session = Depends(get_db)):
    service = PlanoService(db)
    return service.listar()


@router.get("/{plano_id}", response_model=PlanoResponse)
def obtener_plano(plano_id: int, db: Session = Depends(get_db)):
    service = PlanoService(db)
    plano = service.obtener(plano_id)
    if not plano:
        raise HTTPException(status_code=404, detail="Plano no encontrado")
    return plano


@router.delete("/{plano_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_plano(plano_id: int, db: Session = Depends(get_db)):
    service = PlanoService(db)
    if not service.eliminar(plano_id):
        raise HTTPException(status_code=404, detail="Plano no encontrado")
