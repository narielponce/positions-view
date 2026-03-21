from sqlalchemy.orm import Session
from app.models import Punto
from app.schemas import PuntoCreate, PuntoUpdate, PuntoResponse
from app.repositories import PuntoRepository


class PuntoService:
    def __init__(self, db: Session):
        self.repo = PuntoRepository(db)

    def crear(self, data: PuntoCreate) -> PuntoResponse:
        punto = Punto(
            plano_id=data.plano_id,
            nombre=data.nombre,
            tipo=data.tipo,
            descripcion=data.descripcion,
            x=data.x,
            y=data.y,
        )
        return self.repo.create(punto)

    def obtener(self, punto_id: int) -> PuntoResponse | None:
        return self.repo.get_by_id(punto_id)

    def listar_por_plano(self, plano_id: int) -> list[PuntoResponse]:
        return self.repo.get_by_plano(plano_id)

    def actualizar(self, punto_id: int, data: PuntoUpdate) -> PuntoResponse | None:
        punto = self.repo.get_by_id(punto_id)
        if not punto:
            return None
        if data.nombre is not None:
            punto.nombre = data.nombre
        if data.tipo is not None:
            punto.tipo = data.tipo
        if data.descripcion is not None:
            punto.descripcion = data.descripcion
        if data.x is not None:
            punto.x = data.x
        if data.y is not None:
            punto.y = data.y
        return self.repo.update(punto)

    def eliminar(self, punto_id: int) -> bool:
        punto = self.repo.get_by_id(punto_id)
        if not punto:
            return False
        self.repo.delete(punto)
        return True
