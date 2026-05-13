from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ImagenUsuario(Base):
    __tablename__ = "imagenes_usuarios"

    id             = Column(Integer, primary_key=True, index=True)
    usuario        = Column(String, nullable=False, index=True)
    nombre_img     = Column(String, nullable=False)
    ruta_s3        = Column(String, nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())