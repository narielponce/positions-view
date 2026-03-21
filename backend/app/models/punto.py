from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.base import Base


class Punto(Base):
    __tablename__ = "puntos"

    id = Column(Integer, primary_key=True, index=True)
    plano_id = Column(Integer, ForeignKey("planos.id"), nullable=False)
    nombre = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    descripcion = Column(String, nullable=True)
    extra_data = Column(JSON, nullable=True)

    plano = relationship("Plano", back_populates="puntos")
