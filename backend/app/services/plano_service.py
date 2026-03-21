from sqlalchemy.orm import Session
from app.models import Plano
from app.schemas import PlanoCreate, PlanoResponse
from app.repositories import PlanoRepository


class PlanoService:
    def __init__(self, db: Session):
        self.repo = PlanoRepository(db)

    def crear(self, data: PlanoCreate) -> PlanoResponse:
        plano = Plano(nombre=data.nombre)
        return self.repo.create(plano)

    def listar(self) -> list[PlanoResponse]:
        return self.repo.get_all()

    def obtener(self, plano_id: int) -> PlanoResponse | None:
        return self.repo.get_by_id(plano_id)

    def eliminar(self, plano_id: int) -> bool:
        plano = self.repo.get_by_id(plano_id)
        if not plano:
            return False
        self.repo.delete(plano)
        return True
