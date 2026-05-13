# Actividad-AWS-Sistemas-Operativos
Santiago Escobar Baena

Es una API tipo REST con un metodo GET y un metodo POST. Sirve para subir registros de usuario, imagen y fecha de creacion a una base de datos usando los servicios de nube de AWS. 

Arquitectura:
1. El cliente hace una peticion al servidor usando curl con la interfaz de Swagger.
2. La petición se hace a una URL de una funcion lambda de AWS, que esta construida con la imagen de docker de este repositorio. Esta imagen fue previamente subida a ECR.
3. Se usa S3 para guardar las rutas de la imagenes y RDS con Postgres para el registro completo (id, usuario, ruta de la imagen, fecha de creacion). También se hace validación. 

ENDPOINTS:
1. POST: recibe el nombre de usuario y una imagen en formato .png, -jpeg o .jpg. Sube la imagen a S3 y crea el registro en RDS. Si se usa un formato no permitido hay error del servidor 415 con un mensaje de "formato de imagen no permitido"
2. GET:  recibe el nombre de usuario y el nombre de una imagen. Retorn una URL prefirmada que es válida por una hora y contiene la imagen pedida, mientras exista. Si no existe, sale error del servidor 404 con los mensajes "El usuario no existe" o "La imagen no existe para este usuario", dependiendo del caso.

Variables de Entorno: 
1. DATABASE_URL: cadena de conexion a Postgres en RDS.
2. S3_BUCKET_NAME: nombre del bucket para las imagenes. 
