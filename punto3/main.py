import os
from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from mangum import Mangum

import models, schemas, s3_service
from database import get_db, get_engine

app = FastAPI(title="Taller AWS - FastAPI + S3 + RDS")

# Crear tablas al iniciar
@app.on_event("startup")
def startup():
    engine = get_engine()
    models.Base.metadata.create_all(bind=engine)

FORMATOS_PERMITIDOS = {"image/png", "image/jpeg", "image/jpg"}
EXTENSIONES_PERMITIDAS = {".png", ".jpg", ".jpeg"}


# POST /upload — Subir imagen

@app.post("/upload", response_model=schemas.ImagenResponse, status_code=201)
async def subir_imagen(
    usuario: str = Form(...),
    imagen: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    extension = os.path.splitext(imagen.filename)[1].lower()

    if imagen.content_type not in FORMATOS_PERMITIDOS or extension not in EXTENSIONES_PERMITIDAS:
        raise HTTPException(
            status_code=415,
            detail=f"Formato no permitido: '{imagen.content_type}'. "
                   f"Solo se aceptan PNG, JPG o JPEG."
        )

    contenido = await imagen.read()

    # Subir a S3
    ruta_s3 = s3_service.subir_imagen_s3(
        usuario=usuario,
        nombre_archivo=imagen.filename,
        contenido=contenido,
        content_type=imagen.content_type
    )

    # Guardar registro en RDS
    registro = models.ImagenUsuario(
        usuario=usuario,
        nombre_img=imagen.filename,
        ruta_s3=ruta_s3
    )
    db.add(registro)
    db.commit()
    db.refresh(registro)

    return registro


# GET /imagen — Obtener URL prefirmada
@app.get("/imagen")
def obtener_imagen(usuario: str, nombre_img: str, db: Session = Depends(get_db)):

    registro = db.query(models.ImagenUsuario).filter(
        models.ImagenUsuario.usuario == usuario,
        models.ImagenUsuario.nombre_img == nombre_img
    ).first()

    if not registro:
        existe_usuario = db.query(models.ImagenUsuario).filter(
            models.ImagenUsuario.usuario == usuario
        ).first()

        if not existe_usuario:
            raise HTTPException(status_code=404, detail=f"El usuario '{usuario}' no existe.")
        else:
            raise HTTPException(status_code=404, detail=f"La imagen '{nombre_img}' no existe para el usuario '{usuario}'.")

    url = s3_service.generar_url_prefirmada(registro.ruta_s3)

    return {
        "usuario": registro.usuario,
        "nombre_img": registro.nombre_img,
        "url_acceso": url,
        "fecha_almacenamiento": registro.fecha_creacion,
        "ruta_s3": registro.ruta_s3
    }


handler = Mangum(app)