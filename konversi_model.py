import tensorflow as tf

# 1. Muat model .h5 yang sudah Anda latih sebelumnya
model = tf.keras.models.load_model('model_deteksi_cacat.h5')

# 2. Buat objek konverter dari model Keras
converter = tf.lite.TFLiteConverter.from_keras_model(model)

# 3. Lakukan proses konversi
tflite_model = converter.convert()

# 4. Simpan model TFLite yang baru ke sebuah file
with open('model_deteksi_cacat.tflite', 'wb') as f:
    f.write(tflite_model)

print("Model berhasil dikonversi ke 'model_deteksi_cacat.tflite'")
print("Anda sekarang bisa mengunggah file .tflite ini ke server.")