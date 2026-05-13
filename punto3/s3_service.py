import boto3
import os

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
s3_client = boto3.client("s3")

def subir_imagen_s3(usuario: str, nombre_archivo: str, contenido: bytes, content_type: str) -> str:
    ruta_s3 = f"{usuario}/{nombre_archivo}"
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=ruta_s3,
        Body=contenido,
        ContentType=content_type
    )
    return ruta_s3

def generar_url_prefirmada(ruta_s3: str, expiracion: int = 3600) -> str:
    url = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET_NAME, "Key": ruta_s3},
        ExpiresIn=expiracion
    )
    return url