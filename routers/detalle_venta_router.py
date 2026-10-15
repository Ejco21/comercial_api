from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from config.session_Dependencia import SessionDeDependencia
from config.segurity_Dependencia import Token_Dependencia
from models.detalle_venta import DetalleVenta, DetalleVentaCreate, DetalleVentaUpdate, DetalleVentaUpdatePatch
from datetime import datetime

router = APIRouter()


@router.get("/detalle_ventas", response_model=list[DetalleVenta], status_code=status.HTTP_200_OK)
async def get_detalle_ventas(session: SessionDeDependencia, token: Token_Dependencia, offset: int = Query(0, ge=0), limit: int = Query(100, ge=1)):
    consulta = select(DetalleVenta).offset(offset).limit(limit)
    resultado_de_consulta = session.exec(consulta)
    return resultado_de_consulta.all()


@router.get("/detalle_ventas/{id}", response_model=DetalleVenta, status_code=status.HTTP_200_OK)
async def get_detalle_venta(id: int, session: SessionDeDependencia, token: Token_Dependencia):
    consulta = select(DetalleVenta).where(DetalleVenta.id == id)
    resultado_de_consulta = session.exec(consulta).first()
    if not resultado_de_consulta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Detalle de venta no encontrado")
    return resultado_de_consulta


@router.post('/detalle_ventas', response_model=DetalleVenta, status_code=status.HTTP_201_CREATED)
async def create_detalle_venta(datos_detalle_venta: DetalleVentaCreate, session: SessionDeDependencia, token: Token_Dependencia):
    detalle_venta_nuevo = DetalleVenta(**datos_detalle_venta.model_dump())
    session.add(detalle_venta_nuevo)
    session.commit()
    session.refresh(detalle_venta_nuevo)
    return detalle_venta_nuevo


@router.put('/detalle_ventas/{id}', response_model=DetalleVenta, status_code=status.HTTP_200_OK)
async def update_detalle_venta(id: int, datos_detalle_venta: DetalleVentaUpdate, session: SessionDeDependencia, token: Token_Dependencia):
    consulta = select(DetalleVenta).where(DetalleVenta.id == id)
    detalle_venta = session.exec(consulta).first()
    if not detalle_venta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Detalle de venta no encontrado')

    for key, value in datos_detalle_venta.model_dump().items():
        setattr(detalle_venta, key, value)

    detalle_venta.updated_at = datetime.utcnow()
    session.add(detalle_venta)
    session.commit()
    session.refresh(detalle_venta)
    return detalle_venta


@router.delete('/detalle_ventas/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_detalle_venta(id: int, session: SessionDeDependencia, token: Token_Dependencia):
    consulta = select(DetalleVenta).where(DetalleVenta.id == id)
    resultado = session.exec(consulta).first()
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Detalle de venta no encontrado")
    session.delete(resultado)
    session.commit()
    return None


@router.patch('/detalle_ventas/{id}', response_model=DetalleVenta, status_code=status.HTTP_200_OK)
async def patch_detalle_venta(id: int, datos_detalle_venta: DetalleVentaUpdatePatch, session: SessionDeDependencia, token: Token_Dependencia):
    consulta = select(DetalleVenta).where(DetalleVenta.id == id)
    detalle_venta = session.exec(consulta).first()
    if not detalle_venta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Detalle de venta no encontrado')

    detalle_venta.sqlmodel_update(
        datos_detalle_venta.model_dump(exclude_unset=True))
    detalle_venta.updated_at = datetime.utcnow()
    session.add(detalle_venta)
    session.commit()
    session.refresh(detalle_venta)
    return detalle_venta
