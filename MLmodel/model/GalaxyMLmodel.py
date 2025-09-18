import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from PIL import Image
from tensorflow import keras
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
import seaborn as sns
import random
from epochCheckPoint import EpochCheckpoint

# Rutas
dataset_dir = Path("/home/david/Descargas/dataset/")
#dataset_dir = Path("./dataset")
path_training_solutions = dataset_dir / "training_solutions_rev1.csv"
path_training_images = dataset_dir / "images_training_rev1"
path_test_images = dataset_dir / "images_test_rev1"

# Cargar CSV
training_solutions = pd.read_csv(path_training_solutions)
print(f"Datos cargados: {training_solutions.shape[0]} galaxias, {training_solutions.shape[1]} columnas")
print(f"Formato: GalaxyID + {training_solutions.shape[1] - 1} probabilidades morfológicas")

prob_columns = [col for col in training_solutions.columns if col != 'GalaxyID']

# Verificar imágenes
print(f"\n  VERIFICANDO IMÁGENES:")
train_images = list(path_training_images.iterdir()) if path_training_images.exists() else []
test_images = list(path_test_images.iterdir()) if path_test_images.exists() else []

print(f"Imágenes de entrenamiento: {len(train_images)}")
print(f"Imágenes de test: {len(test_images)}")

# Top categorías
mean_probs = training_solutions[prob_columns].mean().sort_values(ascending=False)
print("Top 10 categorías más frecuentes:")
for i, (col, prob) in enumerate(mean_probs.head(10).items()):
    print(f"  {i+1:2d}. {col}: {prob:.4f}")

# Parámetros
IMG_SIZE = 64
BATCH_SIZE = 32
NUM_CLASSES = len(prob_columns)

# Función de preprocessing
def preprocess_image_tf(filename, label):
    img = tf.io.read_file(filename)
    img = tf.image.decode_jpeg(img, channels=3)
    img = tf.image.resize(img, [IMG_SIZE, IMG_SIZE])
    img = tf.cast(img, tf.float32) / 255.0
    return img, label

# Cargar dataset
image_paths = []
labels = []

for _, row in training_solutions.iterrows():
    galaxy_id = f"{int(row['GalaxyID'])}.jpg"
    img_path = path_training_images / galaxy_id

    if img_path.exists():
        image_paths.append(str(img_path))
        labels.append(row[prob_columns].values.astype(np.float32))

image_paths = np.array(image_paths)
labels = np.array(labels, dtype=np.float32)

# (scikit learn) Divide el dataset para evaluarse durante el entrenamiento
X_train, X_val, y_train, y_val = train_test_split(image_paths, labels, test_size=0.2, random_state=42)

# Dataset de entrenamiento
train_ds = tf.data.Dataset.from_tensor_slices((X_train, y_train))
train_ds = train_ds.map(preprocess_image_tf, num_parallel_calls=tf.data.AUTOTUNE)
train_ds = train_ds.shuffle(1000).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

# Dataset de validación
val_ds = tf.data.Dataset.from_tensor_slices((X_val, y_val))
val_ds = val_ds.map(preprocess_image_tf, num_parallel_calls=tf.data.AUTOTUNE)
val_ds = val_ds.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

# modelo CNN
model = models.Sequential([
    layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3)),

    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),

    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),

    layers.Conv2D(128, (3, 3), activation='relu'),

    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),

    layers.Flatten(),

    layers.Dense(512, activation='relu'),
    layers.Dense(512, activation='relu'),
    layers.Dense(NUM_CLASSES, activation='sigmoid')  # usamos sigmoid porque cada columna es una probabilidad
])

# -------------------------------
# Compilacion
model.compile(optimizer='adam',
              loss='binary_crossentropy',  # como son probabilidades multilabel
              metrics=['accuracy'])

# -------------------------------
# Resumen
model.summary()

# -------------------------------
# Entrenamiento

checkpoint_cb = EpochCheckpoint(save_interval=50, file_name="name")

history = model.fit(
    train_ds,
    validation_data=val_ds,
    batch_size=BATCH_SIZE,
    epochs=20,
    callbacks= [checkpoint_cb]
)

model.save("galaxy_model.h5")

plt.plot(history.history['loss'], label='train_loss')
plt.plot(history.history['val_loss'], label='val_loss')
plt.legend()
plt.savefig()
plt.show()

sample_idx = random.sample(range(len(X_val)), 5)

for idx in sample_idx:
    img_path = X_val[idx]
    true_label = y_val[idx]

    # Preprocesar la imagen (igual que en preprocess_image_tf)
    img = tf.io.read_file(img_path)
    img = tf.image.decode_jpeg(img, channels=3)
    img = tf.image.resize(img, [IMG_SIZE, IMG_SIZE])
    img = tf.cast(img, tf.float32) / 255.0
    img_exp = tf.expand_dims(img, axis=0)  # batch de 1

    # Predicción
    pred = model.predict(img_exp, verbose=0)[0]

    # Top 3 categorías
    top3_idx = np.argsort(pred)[-3:][::-1]
    top3_labels = [(prob_columns[i], pred[i]) for i in top3_idx]

    # Mostrar
    plt.figure(figsize=(3,3))
    plt.imshow(img.numpy())
    plt.axis("off")
    plt.title("\n".join([f"{name}: {p:.2f}" for name, p in top3_labels]))
    plt.show()
