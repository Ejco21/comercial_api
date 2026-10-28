import os
import shutil
from fastapi import UploadFile


def guardar_imagen(file: UploadFile):
    # Carpeta donde se guardarán las fotos en el servidor
    directorio = "static/imagenes"

    # Si la carpeta no existe, le decimos a Python que la cree automáticamente
    if not os.path.exists(directorio):
        os.makedirs(directorio)

    # Generamos la ruta completa donde quedará el archivo
    ruta_archivo = f"{directorio}/{file.filename}"

    # Guardamos el archivo físicamente en el disco duro
    with open(ruta_archivo, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Retornamos la ruta para que la base de datos sepa dónde quedó guardada
    return ruta_archivo
