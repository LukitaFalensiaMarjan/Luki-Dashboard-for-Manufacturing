import tensorflow as tf
import pathlib

# 1. Data Preparation (unchanged)
print("Mempersiapkan dataset...")
data_dir = pathlib.Path('./dataset/')
batch_size = 32
img_height = 180
img_width = 180
train_ds = tf.keras.utils.image_dataset_from_directory(data_dir, validation_split=0.2, subset="training", seed=123, image_size=(img_height, img_width), batch_size=batch_size)
val_ds = tf.keras.utils.image_dataset_from_directory(data_dir, validation_split=0.2, subset="validation", seed=123, image_size=(img_height, img_width), batch_size=batch_size)
class_names = train_ds.class_names
print(f"Kelas yang ditemukan: {class_names}")

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# 2. Model Architecture
print("Membangun arsitektur model...")
data_augmentation = tf.keras.Sequential([tf.keras.layers.RandomFlip('horizontal'), tf.keras.layers.RandomRotation(0.1), tf.keras.layers.RandomZoom(0.1),])

# Download MobileNetV2 model
base_model = tf.keras.applications.MobileNetV2(input_shape=(img_height, img_width, 3), include_top=False, weights='imagenet')

# Freeze the base model
base_model.trainable = False

inputs = tf.keras.Input(shape=(img_height, img_width, 3))
x = data_augmentation(inputs)
x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
x = base_model(x, training=False)
x = tf.keras.layers.GlobalAveragePooling2D()(x)
x = tf.keras.layers.Dropout(0.2)(x)
outputs = tf.keras.layers.Dense(len(class_names))(x)
model = tf.keras.Model(inputs, outputs)

# 3. Compile and Train the Model (Initial Training)
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

initial_epochs = 10
print(f"\nMemulai Pelatihan Awal selama {initial_epochs} epoch...")
history = model.fit(train_ds, validation_data=val_ds, epochs=initial_epochs)

# --- FINE-TUNING ---

# 4. Unfreeze some layers in the base model
base_model.trainable = True
fine_tune_at = 100 
for layer in base_model.layers[:fine_tune_at]:
    layer.trainable = False

# 5. Recompile the model with a lower learning rate
model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              optimizer=tf.keras.optimizers.RMSprop(learning_rate=1e-5),
              metrics=['accuracy'])

model.summary() # Optional: Print model summary to see trainable layers

# 6. Continue Training (Fine-Tuning)
fine_tune_epochs = 10
total_epochs = initial_epochs + fine_tune_epochs

print(f"\nMemulai Proses Fine-Tuning selama {fine_tune_epochs} epoch...")
history_fine = model.fit(train_ds,
                         epochs=total_epochs,
                         initial_epoch=history.epoch[-1],
                         validation_data=val_ds)

# 7. Save the fine-tuned model
model.save('model_deteksi_cacat.h5')
print("\nThe Computer Vision model has been successfully trained and saved.")