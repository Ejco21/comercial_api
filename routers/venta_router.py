from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from config.session_Dependencia import SessionDeDependencia
from config.segurity_Dependencia import Token_Dependencia
from models.venta import Venta, VentaCreate, VentaUpdate, VentaUpdatePatch
from datetime import datetime

router = APIRouter()


@router.get("/ventas", response_model=list[Venta], status_code=status.HTTP_200_OK)
async def get_ventas(session: SessionDeDependencia, token: Token_Dependencia, offset: int = Query(0, ge=0), limit: int = Query(100, ge=1)):
    consulta = select(Venta).offset(offset).limit(limit)
    resultado_de_consulta = session.exec(consulta)
    return resultado_de_consulta.all()


@router.get("/ventas/{id}", response_model=Venta, status_code=status.HTTP_200_OK)
async def get_venta(id: int, session: SessionDeDependencia, token: Token_Dependencia):
    consulta = select(Venta).where(Venta.id == id)
    resultado_de_consulta = session.exec(consulta).first()
    if not resultado_de_consulta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada")
    return resultado_de_consulta


@router.post('/ventas', response_model=Venta, status_code=status.HTTP_201_CREATED)
async def create_venta(datos_venta: VentaCreate, session: SessionDeDependencia, token: Token_Dependencia):
    venta_nueva = Venta(**datos_venta.model_dump())
    session.add(venta_nueva)
    session.commit()
    session.refresh(venta_nueva)
    return venta_nueva


@router.put('/ventas/{id}', response_model=Venta, status_code=status.HTTP_200_OK)
async def update_venta(id: int, datos_venta: VentaUpdate, session: SessionDeDependencia, token: Token_Dependencia):
    consulta = select(Venta).where(Venta.id == id)
    venta = session.exec(consulta).first()
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Venta no encontrada')

    for key, value in datos_venta.model_dump().items():
        setattr(venta, key, value)

    venta.updated_at = datetime.utcnow()
    session.add(venta)
    session.commit()
    session.refresh(venta)
    return venta


@router.delete('/ventas/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_venta(id: int, session: SessionDeDependencia, token: Token_Dependencia):
    consulta = select(Venta).where(Venta.id == id)
    resultado = session.exec(consulta).first()
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada")
    session.delete(resultado)
    session.commit()
    return None


@router.patch('/ventas/{id}', response_model=Venta, status_code=status.HTTP_200_OK)
async def patch_venta(id: int, datos_venta: VentaUpdatePatch, session: SessionDeDependencia, token: Token_Dependencia):
    consulta = select(Venta).where(Venta.id == id)
    venta = session.exec(consulta).first()
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Venta no encontrada')

    venta.sqlmodel_update(datos_venta.model_dump(exclude_unset=True))
    venta.updated_at = datetime.utcnow()
    session.add(venta)
    session.commit()
    session.refresh(venta)
    return venta
