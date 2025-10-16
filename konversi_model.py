import tensorflow as tf

# 1. Separate Features (4 inputs) and Target (1 output)
# compile=False ditambahkan untuk menghindari error kompatibilitas
model = tf.keras.models.load_model('model_deteksi_cacat.h5', compile=False)

# 2. Create a TFLite converter
converter = tf.lite.TFLiteConverter.from_keras_model(model)

# 3. Convert the model to TFLite format
tflite_model = converter.convert()

# 4. Save the TFLite model to a file
with open('model_deteksi_cacat.tflite', 'wb') as f:
    f.write(tflite_model)

print("Model fine-tuned (.h5) berhasil dikonversi ke 'model_deteksi_cacat.tflite'")