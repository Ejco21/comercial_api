from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from config.session_Dependencia import SessionDeDependencia
from config.segurity_Dependencia import Token_Dependencia
from models.tipo_pago import TipoPago, TipoPagoCreate, TipoPagoUpdate, TipoPagoUpdatePatch
from datetime import datetime

router = APIRouter()


@router.get("/tipo_pago", response_model=list[TipoPago], status_code=status.HTTP_200_OK)
async def get_tipos_pago(session: SessionDeDependencia, token: Token_Dependencia, offset: int = Query(0, ge=0), limit: int = Query(100, ge=1)):
    consulta = select(TipoPago).offset(offset).limit(limit)
    resultado_de_consulta = session.exec(consulta)
    return resultado_de_consulta.all()


@router.get("/tipo_pago/{id}", response_model=TipoPago, status_code=status.HTTP_200_OK)
async def get_tipo_pago(id: int, session: SessionDeDependencia, token: Token_Dependencia):
    consulta = select(TipoPago).where(TipoPago.id == id)
    resultado_de_consulta = session.exec(consulta).first()
    if not resultado_de_consulta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Tipo de pago no encontrado")
    return resultado_de_consulta


@router.post('/tipo_pago', response_model=TipoPago, status_code=status.HTTP_201_CREATED)
async def create_tipo_pago(datos_tipo_pago: TipoPagoCreate, session: SessionDeDependencia, token: Token_Dependencia):
    tipo_pago_nuevo = TipoPago(**datos_tipo_pago.model_dump())
    session.add(tipo_pago_nuevo)
    session.commit()
    session.refresh(tipo_pago_nuevo)
    return tipo_pago_nuevo


@router.put('/tipo_pago/{id}', response_model=TipoPago, status_code=status.HTTP_200_OK)
async def update_tipo_pago(id: int, datos_tipo_pago: TipoPagoUpdate, session: SessionDeDependencia, token: Token_Dependencia):
    consulta = select(TipoPago).where(TipoPago.id == id)
    tipo_pago = session.exec(consulta).first()
    if not tipo_pago:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Tipo de pago no encontrado')

    for key, value in datos_tipo_pago.model_dump().items():
        setattr(tipo_pago, key, value)

    tipo_pago.updated_at = datetime.utcnow()
    session.add(tipo_pago)
    session.commit()
    session.refresh(tipo_pago)
    return tipo_pago


@router.delete('/tipo_pago/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_tipo_pago(id: int, session: SessionDeDependencia, token: Token_Dependencia):
    consulta = select(TipoPago).where(TipoPago.id == id)
    resultado = session.exec(consulta).first()
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Tipo de pago no encontrado")
    session.delete(resultado)
    session.commit()
    return None


@router.patch('/tipo_pago/{id}', response_model=TipoPago, status_code=status.HTTP_200_OK)
async def patch_tipo_pago(id: int, datos_tipo_pago: TipoPagoUpdatePatch, session: SessionDeDependencia, token: Token_Dependencia):
    consulta = select(TipoPago).where(TipoPago.id == id)
    tipo_pago = session.exec(consulta).first()
    if not tipo_pago:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Tipo de pago no encontrado')

    tipo_pago.sqlmodel_update(datos_tipo_pago.model_dump(exclude_unset=True))
    tipo_pago.updated_at = datetime.utcnow()
    session.add(tipo_pago)
    session.commit()
    session.refresh(tipo_pago)
    return tipo_pago
