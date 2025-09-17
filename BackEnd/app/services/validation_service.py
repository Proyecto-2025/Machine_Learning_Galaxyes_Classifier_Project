from PIL import image

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png"}
MAX_SIZE_MB = 5

#chequea extension
def allowed_file(filename):
  return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS

#Chequea que el archivo subido sea una imagen valida"""
def validate_image(file):
  
  if not allowed_file(file.filename):
    return False, "Formato no permitido. Solo JPG y PNG"
  

  #validar mime type
  if file.mimetype not in ALLOWED_MIME_TYPES:
    return False, "El tipo de archivo no es valido"

  #validar tamaño
  file.seek(0,2)
  size_mb = file.tell() / (1024 * 1024)
  if size_mb > MAX_SIZE_MB:
    return False, "El arhivo supera los 5MB"

  #check procesar imagen
  try:
    img = image.open(file)
    img.verify() 
  except Exception:
    return False, "El archivo no es una imagen válida."

  return True, "Imagen válida."
