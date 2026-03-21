from typing import Optional
from pydantic import BaseModel, Field


class PuntoBase(BaseModel):
    nombre: str
    tipo: str
    descripcion: Optional[str] = None


class PuntoCreate(PuntoBase):
    plano_id: int
    x: float = Field(..., ge=0, le=1)
    y: float = Field(..., ge=0, le=1)


class PuntoUpdate(BaseModel):
    nombre: Optional[str] = None
    tipo: Optional[str] = None
    descripcion: Optional[str] = None
    x: Optional[float] = Field(None, ge=0, le=1)
    y: Optional[float] = Field(None, ge=0, le=1)


class PuntoResponse(PuntoBase):
    id: int
    plano_id: int
    x: float
    y: float
    extra_data: Optional[dict] = None

    class Config:
        from_attributes = True
