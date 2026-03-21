from sqlalchemy.orm import Session
from app.models import Punto


class PuntoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, punto: Punto) -> Punto:
        self.db.add(punto)
        self.db.commit()
        self.db.refresh(punto)
        return punto

    def get_by_plano(self, plano_id: int) -> list[Punto]:
        return self.db.query(Punto).filter(Punto.plano_id == plano_id).all()

    def get_by_id(self, punto_id: int) -> Punto | None:
        return self.db.query(Punto).filter(Punto.id == punto_id).first()

    def update(self, punto: Punto) -> Punto:
        self.db.commit()
        self.db.refresh(punto)
        return punto

    def delete(self, punto: Punto) -> None:
        self.db.delete(punto)
        self.db.commit()
