import os
import sys
import random
from datetime import datetime

from BackEnd.app import db, create_app
from BackEnd.app.models import ImageModel
from MLmodel.model.PredictGalaxy import makePrediction
from MLmodel.model.Response import Response

project_root = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.join(project_root, "BackEnd")
mlmodel_path = os.path.join(project_root, "MLmodel")

sys.path.insert(0, backend_path)
sys.path.insert(0, mlmodel_path)


# Configuración
ruta_dataset = os.path.expanduser("~/Descargas/dataset/images_test_rev1")
cantidad_imagenes = 30


def procesar_imagen(ruta_img):
    try:
        # Simular FileStorage de Flask
        from werkzeug.datastructures import FileStorage

        with open(ruta_img, 'rb') as f:
            image_file = FileStorage(
                stream=f,
                filename=os.path.basename(ruta_img),
                content_type='image/jpeg'
            )

            # makePrediction del modelo ML
            raw_prediction = makePrediction(image_file)

            response_obj = Response(raw_prediction)

            prediction = [round(float(p), 3) for p in response_obj.prediction]
            features = response_obj.features
            hubble_sequence = response_obj.hubble_sequence

            return {
                "prediction": prediction,
                "features": features,
                "hubble_sequence": hubble_sequence
            }

    except Exception as e:
        print(f"   ✗ Error procesando: {e}")
        import traceback
        traceback.print_exc()
        return None


def seleccionar_y_procesar_imagenes(ruta, cantidad):
    """
    Selecciona imágenes al azar y las procesa para la BD
    """
    if not os.path.exists(ruta):
        print(f"❌ Error: La ruta {ruta} no existe")
        return 0

    # Obtener todas las imágenes .jpg
    imagenes = [f for f in os.listdir(ruta) if f.endswith('.jpg')]

    print(f"📁 Total de imágenes encontradas: {len(imagenes)}")

    if len(imagenes) == 0:
        print("❌ No se encontraron imágenes .jpg")
        return 0

    if cantidad > len(imagenes):
        print(f"⚠️  Solo hay {len(imagenes)} imágenes, procesando todas")
        cantidad = len(imagenes)

    # Seleccionar al azar
    imagenes_seleccionadas = random.sample(imagenes, cantidad)

    registros_insertados = 0
    registros_duplicados = 0
    registros_fallidos = 0

    print(f"\n{'=' * 70}")
    print(f"🚀 Procesando {cantidad} imágenes seleccionadas al azar")
    print(f"{'=' * 70}\n")

    for i, nombre_img in enumerate(imagenes_seleccionadas, 1):
        ruta_completa = os.path.join(ruta, nombre_img)

        print(f"[{i}/{cantidad}] 📷 {nombre_img}")

        try:
            # Verificar duplicados
            existe = db.session.query(ImageModel).filter_by(filename=nombre_img).first()
            if existe:
                print(f"         ⚠️  Ya existe en BD (ID: {existe.id})")
                registros_duplicados += 1
                continue

            # Procesar con el modelo ML
            print(f"         🔄 Ejecutando predicción...")
            resultado = procesar_imagen(ruta_completa)

            if resultado is None:
                print(f"         ❌ Falló el procesamiento")
                registros_fallidos += 1
                continue

            # Crear registro
            nuevo_registro = ImageModel(
                filename=nombre_img,
                prediction=resultado["prediction"],
                features=resultado["features"],
                hubble_sequence=resultado["hubble_sequence"],
                creation_date=datetime.utcnow()
            )

            # Guardar en BD
            db.session.add(nuevo_registro)
            db.session.commit()

            registros_insertados += 1
            print(f"         ✅ Insertado (ID: {nuevo_registro.id})")
            print(f"         📊 Features: {len(resultado['features'])}")
            print(f"         🌌 Hubble: {resultado['hubble_sequence']}")

        except Exception as e:
            print(f"         ❌ Error: {e}")
            registros_fallidos += 1
            db.session.rollback()

        print()  # Línea en blanco entre imágenes

    # Resumen final
    print(f"{'=' * 70}")
    print(f"📊 RESUMEN DEL PROCESAMIENTO")
    print(f"{'=' * 70}")
    print(f"✅ Insertadas:   {registros_insertados}")
    print(f"⚠️  Duplicadas:   {registros_duplicados}")
    print(f"❌ Fallidas:     {registros_fallidos}")
    print(f"📁 Total:        {cantidad}")
    print(f"{'=' * 70}\n")

    return registros_insertados


def main():
    print(f"\n{'=' * 70}")
    print(f"🌌 PROCESADOR DE IMÁGENES DE GALAXIAS")
    print(f"{'=' * 70}\n")

    # Crear app Flask
    app = create_app()

    with app.app_context():
        # Info de la BD
        db_path = app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "")
        print(f"💾 Base de datos: {db_path}")
        print(f"✓  Existe: {os.path.exists(db_path)}")

        # Registros actuales
        total_actual = db.session.query(ImageModel).count()
        print(f"📊 Registros actuales: {total_actual}\n")

        # Procesar
        nuevos = seleccionar_y_procesar_imagenes(ruta_dataset, cantidad_imagenes)

        # Total final
        if nuevos > 0:
            total_final = db.session.query(ImageModel).count()
            print(f"✨ Total de registros en BD: {total_final}")


if __name__ == "__main__":
    main()