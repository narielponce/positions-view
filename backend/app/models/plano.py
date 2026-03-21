from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base


class Plano(Base):
    __tablename__ = "planos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    imagen_url = Column(String, nullable=True)

    puntos = relationship("Punto", back_populates="plano", cascade="all, delete-orphan")
