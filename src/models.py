from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class ReviewBase(SQLModel):
    producto_id: int
    usuario_id: int
    calificacion: int = Field(..., ge=1, le=5)
    comentario: Optional[str] = None


class Review(ReviewBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha: datetime = Field(default_factory=datetime.utcnow)


class ReviewCreate(ReviewBase):
    pass


class ReviewRead(ReviewBase):
    id: int
    fecha: datetime
