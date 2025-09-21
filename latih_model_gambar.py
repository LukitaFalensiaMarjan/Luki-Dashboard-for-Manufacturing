import tensorflow as tf
import pathlib
import os

# Arahkan ke folder dataset lokal kita
data_dir = pathlib.Path('./dataset/')

# Hitung jumlah gambar untuk memastikan semuanya benar
image_count = len(list(data_dir.glob('*/*.jpg')))
print(f"Total gambar ditemukan: {image_count}")

# Siapkan parameter untuk memuat data
batch_size = 32
img_height = 180
img_width = 180

# Muat data pelatihan (80% dari total data)
train_ds = tf.keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2, # Sisihkan 20% untuk validasi
  subset="training",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

# Muat data validasi (20% yang disisihkan tadi)
val_ds = tf.keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="validation",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

class_names = train_ds.class_names
print("Kelas yang ditemukan:", class_names)

# Optimalkan performa pemuatan data
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# Bangun Model AI (Convolutional Neural Network)
model = tf.keras.Sequential([
  tf.keras.layers.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
  tf.keras.layers.Conv2D(16, 3, padding='same', activation='relu'),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Conv2D(32, 3, padding='same', activation='relu'),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Conv2D(64, 3, padding='same', activation='relu'),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Dropout(0.2), # Mencegah overfitting
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dense(len(class_names))
])

# Kompilasi Model
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# Tampilkan arsitektur model
model.summary()

# Latih Model
print("\nMemulai proses pelatihan model Computer Vision...")
epochs = 15
history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=epochs
)

# Simpan Model yang Sudah Dilatih
model.save('model_deteksi_cacat.h5')
print("\nModel Computer Vision berhasil dilatih dan disimpan sebagai 'model_deteksi_cacat.h5'")