# API Endpoint: /api/v1/classify

## Descripción
Esta ruta permite enviar una imagen al backend, donde se valida, se procesa a traves de un motor ML para extraer sus caracteristicas(features), se guarda físicamente en almacenamiento local y se crea un registro en la base de datos. Finalmente, devuelve al frontend la lista de caracteristicas extraídas.

## Método
POST

## URL
/api/v1/classify

## Headers
Content-Type: multipart/form-data

## Parámetros
Parámetro: image
Tipo: file
Requerido: si
Descripción: archivo de imagen a procesar. Debe ser JPG o PNG y máximo 5 MB

## Validaciones
- Extensiones permitidas: jpg, jpeg, png
- MIME type: image/jpg, image/png
- Tamaño máximo: 5 MB
- Debe ser una imagen valida (no corrupto)

## Ejemplo de request
curl -X POST http://localhost:5000/api/v1/classify \
   -F "image=@/ruta/a/mi/imagen.jpg"

## Respuesta exitosa (200 OK)

["feature1", "feature2", "feature3"]

- lista de caracteristicas extraídas por el ML Engine

## Posibles errores
- Código: 400, Mensaje: "no image provided" -> No se envió ningún archivo.
- Código: 400, Mensaje: "Formato no permitido" -> Extensión no valida.
- Código: 400, Mensaje: "Tipo de archivo no valido" -> MIME type incorrecto.
- Código: 400, Mensaje: "El archivo supera los 5mb" -> Archivo demasiado grande.
- Código: 400, Mensaje: "No es una imagen valida" -> Archivo corrupto o no procesable.
- Código: 500, Mensaje: "unexpected error" -> Error interno del backend

## Notas
Las imagenes se guardan en uploads/<dd-mm-yyyy>/ con nombres únicos generados por UUID.
Las features se almacenan en la DB como JSON.
Cada request guarda la imagen enviada y registra su predicción en la base de datos.


# API Endpoint: /api/v1/play

## Descripción
Esta ruta selecciona de manera aleatoria un registro existente en la base de datos de imagenes y devuelve al frontend el nombre del archivo (URL) y la lista de caracteristicas (features) asociadas a esa imagen. 

## Método
POST

## URL
/api/v1/play

## Headers
Content-Type: application/json

## Parámetros
No recibe parametros.
La selección es totalmente interna, el backend genera una semilla aleatoria basada en el tiempo actual y la utuliza para elegir un registro al azar entre los existentes en la base de datos.

## Validaciones
- Debe existir al menos un registro en la base de datos.
- El ID aleatorio debe corresponder a un registro valido.

## Ejemplo de request
curl -X POST http://localhost:5000/api/v1/play \
   -H "Content-Type: application/json"

## Respuesta exitosa (200 OK)
{
    "filename": "imagen_123.jpg",
    "features": ["spiral", "blue", "bright"]
}

- filename: dirección de almacenamiento de la imagen.
- features: lista de caracteristicas extraídas por el ML Engine.

## Posibles errores
- Código: 500, Mensaje: "unexpected error" -> Error interno del backend (no se pudo acceder a la DB o no hay registros disponibles).

## Notas
La semilla usada para generar el número aleatorio se basa en la hora actual(UTC timestamp).
La elección de la imagen es uniforme entre todas las que están registradas en la base de datos.
No se requiere enviar información adicional en el request, el backend se encarga de todo el proceso.

# API Endpoint: /api/v1/articles (Create)
# Descripción
   Esta ruta permite crear un nuevo artículo en la base de datos. El backend valida los campos recibidos, crea el registro y devuelve el artículo creado.
# Método
POST
# URL
/api/v1/articles
# Parámetros
title
Tipo: string
Requerido: sí
Descripción: título del artículo

# Validaciones
title no puede ser vacío
resumen no puede ser vacío
Cuerpo del articulo no puede ser vacío

# API Endpoint: /api/v1/articles (List)
# Descripción
Devuelve la lista completa de artículos almacenados en la base de datos.
# Método
GET
# URL
/api/v1/articles
# Parámetros
No recibe parámetros.
# Validaciones
Debe poder ejecutar correctamente la consulta en la base de datos

# API Endpoint: /api/v1/articles/<id> 
# Descripción
Devuelve un único artículo según su ID.
# Método
GET
# URL
/api/v1/articles/<id>
# Parámetros
id
Tipo: integer
Requerido: sí
Descripción: ID del artículo a consultar
# Validaciones
El ID debe ser un entero válido
El artículo debe existir

# API Endpoint: /api/v1/login
# Descripción
Permite iniciar sesión verificando email y contraseña. Si las credenciales son válidas, genera un token JWT y devuelve los datos del usuario.
# Método
POST
# URL
/api/v1/login
# Parámetros
email
Tipo: string
Requerido: sí
password
Tipo: string
Requerido: sí
# Validaciones
El email debe existir
La contraseña debe coincidir con el hash guardado
Ambos campos deben enviarse

# Servicio: Image Validation
# Descripción
Este servicio se encarga de validar archivos de imagen enviados al backend. Realiza múltiples verificaciones: extensión permitida, MIME type correcto, tamaño máximo y que el archivo sea efectivamente una imagen válida. Devuelve un resultado booleano junto a un mensaje explicando la validación.

# Archivo
app/services/validation_service.py

# Parámetros:
filename
Tipo: string
Descripción: nombre del archivo recibido

# Retorno:
True si la extensión es válida, False en caso contrario.

# Parámetros:
file
Tipo: FileStorage (archivo subido)
Descripción: archivo a validar

# Validaciones realizadas
La extensión debe ser png, jpg o jpeg
El MIME type debe ser image/jpeg o image/png
El tamaño del archivo no puede superar 5 MB
El archivo debe ser una imagen válida y decodificable por PIL
