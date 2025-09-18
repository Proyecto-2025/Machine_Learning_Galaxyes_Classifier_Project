import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
import pandas as pd

from model.Response import Response

model = load_model("galaxy_model.h5")

IMG_SIZE = 64

# La imagen ya se debe recibir en formato 64x64
def preprocess_single_image(img_path):
    img = tf.io.read_file(img_path)
    img = tf.image.decode_jpeg(img, channels=3)
    img = tf.image.resize(img, [IMG_SIZE, IMG_SIZE])
    img = tf.cast(img, tf.float32) / 255.0
    img = tf.expand_dims(img, axis=0)  # batch de 1
    return img


img_path = "SpiralGalaxy.jpg"
img_tensor = preprocess_single_image(img_path)

img_array = img_tensor[0].numpy()  # quitamos el batch -> (64, 64, 3)

plt.imshow(img_array)
plt.axis("off")
plt.show()

prediction = model.predict(img_tensor)
prediction = prediction[0]

response = Response(prediction)
print(response)