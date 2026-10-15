from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from models.categoria import Categoria, CategoriaCreate, CategoriaUpdate
from config.session_Dependencia import SessionDeDependencia

router = APIRouter()


@router.get("/categorias", response_model=list[Categoria], status_code=status.HTTP_200_OK)
async def obtener_categorias(
    session: SessionDeDependencia,
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1)
):
    consulta = select(Categoria).offset(offset).limit(limit)
    resultado_de_consulta = session.exec(consulta)
    return resultado_de_consulta.all()


@router.get("/categorias/{id}", response_model=Categoria, status_code=status.HTTP_200_OK)
async def get_categoria(id: int, session: SessionDeDependencia):
    consulta = select(Categoria).where(Categoria.id == id)
    resultado = session.exec(consulta).first()
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Categoria no encontrada")
    return resultado


@router.post("/categorias", response_model=Categoria, status_code=status.HTTP_201_CREATED)
async def create_categoria(datos_categoria: CategoriaCreate, session: SessionDeDependencia):
    categoria_nueva = Categoria(
        nombre=datos_categoria.nombre, descripcion=datos_categoria.descripcion)
    session.add(categoria_nueva)
    session.commit()
    session.refresh(categoria_nueva)
    return categoria_nueva


@router.delete("/categorias/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_categoria(id: int, session: SessionDeDependencia):
    consulta = select(Categoria).where(Categoria.id == id)
    resultado = session.exec(consulta).first()
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Categoria no encontrada")
    session.delete(resultado)
    session.commit()
    return None


@router.put("/categorias/{id}", response_model=Categoria, status_code=status.HTTP_200_OK)
async def update_categoria(id: int, datos_categoria: CategoriaUpdate, session: SessionDeDependencia):
    consulta = select(Categoria).where(Categoria.id == id)
    resultado = session.exec(consulta).first()
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Categoria no encontrada")

    resultado.nombre = datos_categoria.nombre

    if datos_categoria.descripcion is not None:
        resultado.descripcion = datos_categoria.descripcion

    resultado.updated_at = datetime.utcnow()
    session.add(resultado)

    session.commit()
    session.refresh(resultado)
    return resultado
