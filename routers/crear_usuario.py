from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel


router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


class UsuarioRegistro(BaseModel):
    nombre: str
    correo: str
    password: str
    rol_id: int


class UsuarioLogin(BaseModel):
    correo: str
    password: str


@router.post("/registro", status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: UsuarioRegistro):

    return {"mensaje": "Usuario registrado exitosamente", "correo": usuario.correo}


@router.post("/login")
def login(usuario: UsuarioLogin):

    token = "tu_token_generado_aqui"
    return {"access_token": token, "token_type": "bearer"}
