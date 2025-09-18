import tensorflow as tf
from tensorflow.keras.models import load_model


model = load_model("galaxy_model.h5")

IMG_SIZE = 64

# La imagen ya se debe recibir en formato 64x64
def preprocess_single_image(file_storage):
    img_bytes = file_storage.read()
    img = tf.image.decode_image(img_bytes, channels=3, expand_animations=False)
    img = tf.image.resize(img, [IMG_SIZE, IMG_SIZE])
    img = tf.cast(img, tf.float32) / 255.0
    img = tf.expand_dims(img, axis=0)  # batch de 1
    return img


def makePrediction(file_storage):
    img_tensor = preprocess_single_image(file_storage)
    prediction = model.predict(img_tensor)
    prediction = prediction[0]
    return prediction