from fastapi import FastAPI, status
from contextlib import asynccontextmanager
from config.db import crear_db_y_tablas
from routers.categoria_router import router as categoria_router
from routers.producto_router import router as productos_router
import models
from routers.cliente_router import router as clientes_router
from routers.tipo_pago_router import router as tipo_pago_router
from routers.venta_router import router as ventas_router
from routers.detalle_venta_router import router as detalle_ventas_router
from routers.usuario_router import router as usuarios_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_db_y_tablas()
    yield

app = FastAPI(lifespan=lifespan)
app.title = "API Tienda la Cachaca"
app.version = "0.0.1"
app.include_router(categoria_router, tags=["Categorias"])
app.include_router(productos_router, tags=["productos"])
app.include_router(usuarios_router, tags=["Usuarios"])


@app.get("/", summary="Comprobndo estado de api", status_code=status.HTTP_200_OK)
async def home():
    return {"message": "API funcionando correctamente"}

app.include_router(clientes_router, tags=["clientes"])
app.include_router(tipo_pago_router, tags=["tipo pago"])
app.include_router(ventas_router, tags=["ventas"])
app.include_router(detalle_ventas_router, tags=["detalle ventas"])
