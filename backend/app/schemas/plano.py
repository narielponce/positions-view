from typing import Optional
from pydantic import BaseModel


class PlanoBase(BaseModel):
    nombre: str


class PlanoCreate(PlanoBase):
    pass


class PlanoResponse(PlanoBase):
    id: int
    imagen_url: Optional[str] = None

    class Config:
        from_attributes = True
