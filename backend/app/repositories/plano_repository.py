from sqlalchemy.orm import Session
from app.models import Plano


class PlanoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, plano: Plano) -> Plano:
        self.db.add(plano)
        self.db.commit()
        self.db.refresh(plano)
        return plano

    def get_all(self) -> list[Plano]:
        return self.db.query(Plano).all()

    def get_by_id(self, plano_id: int) -> Plano | None:
        return self.db.query(Plano).filter(Plano.id == plano_id).first()

    def delete(self, plano: Plano) -> None:
        self.db.delete(plano)
        self.db.commit()
