from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Query, File, UploadFile
from sqlmodel import select
from datetime import datetime

from config.session_Dependencia import SessionDeDependencia
from config.segurity_Dependencia import Token_Dependencia
from models.categoria import Categoria
from models.producto import Producto, ProductoCreate, ProductoUpdate, ProductoUpdatePatch
from services.guardar_imagen import guardar_imagen

router = APIRouter()


@router.get("/productos", response_model=list[Producto], status_code=status.HTTP_200_OK)
async def get_productos(session: SessionDeDependencia, token: Token_Dependencia, offset: int = Query(0, ge=0), limit: int = Query(100, ge=1)):
    consulta = select(Producto).offset(offset).limit(limit)
    resultado_de_consulta = session.exec(consulta)
    return resultado_de_consulta.all()


@router.get("/productos/{id}", response_model=Producto, status_code=status.HTTP_200_OK)
async def get_producto(id: int, session: SessionDeDependencia, token: Token_Dependencia):
    consulta = select(Producto).where(Producto.id == id)
    resultado_de_consulta = session.exec(consulta).first()
    if not resultado_de_consulta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Producto no encontrado")
    return resultado_de_consulta


@router.post('/productos', response_model=Producto, status_code=status.HTTP_201_CREATED)
async def create_producto(datos_producto: ProductoCreate, session: SessionDeDependencia, token: Token_Dependencia):
    if token['id_rol'] != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Solo el administrador puede crear productos")

    consulta = select(Categoria).where(
        Categoria.id == datos_producto.id_categoria)
    categoria = session.exec(consulta).first()

    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Categoria con id {datos_producto.id_categoria} no encontrada")

    producto_nuevo = Producto(**datos_producto.model_dump())
    session.add(producto_nuevo)
    session.commit()
    session.refresh(producto_nuevo)
    return producto_nuevo


@router.put('/productos/{id}', response_model=Producto, status_code=status.HTTP_200_OK)
async def update_producto(id: int, datos_producto: ProductoUpdate, session: SessionDeDependencia, token: Token_Dependencia):
    if token['id_rol'] != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Solo el administrador puede actualizar productos")

    consulta = select(Producto).where(Producto.id == id)
    producto = session.exec(consulta).first()

    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Producto no encontrado')

    categoria = session.exec(select(Categoria).where(
        Categoria.id == datos_producto.id_categoria)).first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Categoria con id: {datos_producto.id_categoria} no encontrada")

    for key, value in datos_producto.model_dump().items():
        setattr(producto, key, value)

    producto.updated_at = datetime.utcnow()
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


@router.patch('/productos/{id}', response_model=Producto, status_code=status.HTTP_200_OK)
async def patch_producto(id: int, datos_producto: ProductoUpdatePatch, session: SessionDeDependencia, token: Token_Dependencia):
    if token['id_rol'] != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Solo el administrador puede actualizar productos")

    consulta = select(Producto).where(Producto.id == id)
    producto = session.exec(consulta).first()

    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Producto no encontrado')

    if datos_producto.id_categoria:
        categoria = session.exec(select(Categoria).where(
            Categoria.id == datos_producto.id_categoria)).first()
        if not categoria:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Categoria con id: {datos_producto.id_categoria} no encontrada")
        producto.id_categoria = datos_producto.id_categoria

    producto.sqlmodel_update(datos_producto.model_dump(exclude_unset=True))
    producto.updated_at = datetime.utcnow()
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


@router.delete('/productos/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_producto(id: int, session: SessionDeDependencia, token: Token_Dependencia):
    if token['id_rol'] != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Solo el administrador puede eliminar productos")

    consulta = select(Producto).where(Producto.id == id)
    resultado_de_consulta = session.exec(consulta).first()

    if not resultado_de_consulta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Producto no encontrado")

    session.delete(resultado_de_consulta)
    session.commit()
    return None


@router.post("/productos/{id}/imagen", response_model=Producto, status_code=status.HTTP_200_OK)
async def upload_imagen_producto(
    id: int,
    session: SessionDeDependencia,
    token: Token_Dependencia,
    imagen: Annotated[UploadFile, File(...)]
):
    if token['id_rol'] != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Solo el administrador puede subir imágenes")

    consulta = select(Producto).where(Producto.id == id)
    producto = session.exec(consulta).first()

    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Producto no encontrado")

    datos_archivo = guardar_imagen(imagen)

    producto.imagen = datos_archivo['nombre']
    producto.updated_at = datetime.utcnow()

    session.add(producto)
    session.commit()
    session.refresh(producto)

    return producto
