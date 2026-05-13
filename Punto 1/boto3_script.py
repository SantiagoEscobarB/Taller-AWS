import boto3
import os

s3 = boto3.client('s3')
nombre_bucket = 'user-1034991096-ueia-so'

#Cargar Archivo
#s3.upload_file('notas1.txt', nombre_bucket, 'notas1_en_s3.txt')

#descargar en una carpeta diferente
#carpeta_destino = 'descargas'
#os.makedirs(carpeta_destino, exist_ok=True) 

#ruta_descarga = os.path.join(carpeta_destino, 'notas1_descargado.txt')
#s3.download_file(nombre_bucket, 'notas1_en_s3.txt', ruta_descarga)

#Subir multiples archivos
#for archivo in os.listdir('multiplesArchivos'):
 #   ruta_archivo = os.path.join('multiplesArchivos', archivo)
  #  s3.upload_file(ruta_archivo, nombre_bucket, f'multiplesEnS3/{archivo}')

#Descargar multiples archivos
carpeta_descarga_multiple = 'multiples_descargas'
os.makedirs(carpeta_descarga_multiple, exist_ok=True)
prefijo_s3 = 'multiplesEnS3/'
archivos = ['multiples1.txt', 'multiples2.txt', 'multiples3.txt']
for archivo in archivos:
    ruta_descarga = os.path.join(carpeta_descarga_multiple, archivo)
    s3.download_file(nombre_bucket, prefijo_s3 + archivo, ruta_descarga)
