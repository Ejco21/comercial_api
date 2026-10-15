from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from decimal import Decimal


class VentaBase(SQLModel):
    fecha: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    total: Decimal = Field(nullable=False, ge=0)
    id_cliente: int = Field(nullable=False, foreign_key="clientes.id")
    id_usuario: int = Field(nullable=False, foreign_key="usuarios.id")
    id_tipo_pago: int = Field(nullable=False, foreign_key="tipo_pago.id")


class Venta(VentaBase, table=True):
    __tablename__ = "ventas"
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(default_factory=datetime.utcnow)


class VentaCreate(VentaBase):
    pass


class VentaUpdate(VentaBase):
    pass


class VentaUpdatePatch(SQLModel):
    fecha: Optional[datetime] = Field(default=None)
    total: Optional[Decimal] = Field(default=None, ge=0)
    id_cliente: Optional[int] = Field(default=None)
    id_usuario: Optional[int] = Field(default=None)
    id_tipo_pago: Optional[int] = Field(default=None)
