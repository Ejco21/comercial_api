from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from config.session_Dependencia import SessionDeDependencia
from config.segurity_Dependencia import Token_Dependencia
from models.cliente import Cliente, ClienteCreate, ClienteUpdate, ClienteUpdatePatch
from datetime import datetime

router = APIRouter()


@router.get("/clientes", response_model=list[Cliente], status_code=status.HTTP_200_OK)
async def get_clientes(session: SessionDeDependencia, token: Token_Dependencia, offset: int = Query(0, ge=0), limit: int = Query(100, ge=1)):
    consulta = select(Cliente).offset(offset).limit(limit)
    resultado_de_consulta = session.exec(consulta)
    return resultado_de_consulta.all()


@router.get("/clientes/{id}", response_model=Cliente, status_code=status.HTTP_200_OK)
async def get_cliente(id: int, session: SessionDeDependencia, token: Token_Dependencia):
    consulta = select(Cliente).where(Cliente.id == id)
    resultado_de_consulta = session.exec(consulta).first()
    if not resultado_de_consulta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return resultado_de_consulta


@router.post('/clientes', response_model=Cliente, status_code=status.HTTP_201_CREATED)
async def create_cliente(datos_cliente: ClienteCreate, session: SessionDeDependencia, token: Token_Dependencia):
    cliente_nuevo = Cliente(**datos_cliente.model_dump())
    session.add(cliente_nuevo)
    session.commit()
    session.refresh(cliente_nuevo)
    return cliente_nuevo


@router.put('/clientes/{id}', response_model=Cliente, status_code=status.HTTP_200_OK)
async def update_cliente(id: int, datos_cliente: ClienteUpdate, session: SessionDeDependencia, token: Token_Dependencia):
    consulta = select(Cliente).where(Cliente.id == id)
    cliente = session.exec(consulta).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Cliente no encontrado')

    for key, value in datos_cliente.model_dump().items():
        setattr(cliente, key, value)

    cliente.updated_at = datetime.utcnow()
    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return cliente


@router.delete('/clientes/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_cliente(id: int, session: SessionDeDependencia, token: Token_Dependencia):
    consulta = select(Cliente).where(Cliente.id == id)
    resultado = session.exec(consulta).first()
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    session.delete(resultado)
    session.commit()
    return None


@router.patch('/clientes/{id}', response_model=Cliente, status_code=status.HTTP_200_OK)
async def patch_cliente(id: int, datos_cliente: ClienteUpdatePatch, session: SessionDeDependencia, token: Token_Dependencia):
    consulta = select(Cliente).where(Cliente.id == id)
    cliente = session.exec(consulta).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Cliente no encontrado')

    cliente.sqlmodel_update(datos_cliente.model_dump(exclude_unset=True))
    cliente.updated_at = datetime.utcnow()
    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return cliente
