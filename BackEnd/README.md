# API Endpoint: /api/v1/classify

## Descripción
Esta ruta permite enviar una imagen al backend, donde se valida, se procesa a traves de un motor ML para extraer sus caracteristicas(features), se guarda físicamente en almacenamiento local, se crea un registro en la base de datos, y se busca una imagen existente en la base de datos con caracteristicas similares. Finalmente, devuelve al frontend la ruta de la imagen encontrada (si existe) y la lista de caracteristicas extraídas.

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
{
    "filename": "uploads/21-09-2025/3b1f4e2a5e6f4c1e9d7a.png",
    "features": ["feature1", "feature2", "feature3"]
}
- filename: ruta de la imagen con caracteristicas similares de la DB    (puede ser null)
- features: lista de caracteristicas extraídas por el ML Engine

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
