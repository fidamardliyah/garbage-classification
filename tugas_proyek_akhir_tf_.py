# -*- coding: utf-8 -*-
"""Tugas Proyek Akhir TF .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nG8vqfNFBFMJ2V1_RaJpLhFptA31t0k0

#Biodata

**Fida Mardliyah // fidamardliyah11@gmail.com**

Sumber Data : https://www.kaggle.com/mostafaabla/garbage-classification

# Import Data

## Install Kaggle & Ynzip Data
"""

!pip install -q kaggle

! mkdir ~/.kaggle

! cp kaggle.json ~/.kaggle/

! chmod 600 ~/.kaggle/kaggle.json

! kaggle datasets download -d mostafaabla/garbage-classification

! mkdir sampah

! unzip -qq garbage-classification.zip -d sampah
!ls sampah

!ls sampah/garbage_classification

import os
garbages =  os.path.join("/content/sampah/garbage_classification")

list_garbages = os.listdir(garbages)

print(list_garbages)

"""## Memilih variabel yang digunakan"""

import shutil

hapus = ['green-glass', 'brown-glass', 'shoes']

for x in hapus:
  path = os.path.join(garbages, x)
  shutil.rmtree(path)

list_garbages = os.listdir(garbages)
print(list_garbages)

"""## Image Understanding"""

from PIL import Image
jumlah = 0

for x in list_garbages:
  dc = os.path.join(garbages, x)
  y = len(os.listdir(dc))
  print(x + ':', y)
  jumlah = jumlah + y

  namagbr = os.listdir(dc)
  for z in range(4):
    gbr_dc = os.path.join(dc, namagbr[z])
    gbr = Image.open(gbr_dc)
    print('ukuran', gbr.size)  
  print('/////////////////')

print('\nTotal Gambar :', jumlah)

"""# Split Data

"""

!pip install split_folders

# data training : data validasi =  8:2

import splitfolders

splitfolders.ratio('/content/sampah/garbage_classification', '/content/sampah/data', seed=1, ratio=(.8, .2))

"""## Penamaan Direktori"""

base_dir = '/content/sampah/data'
train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'val')
os.listdir('/content/sampah/data/train')
os.listdir('/content/sampah/data/val')

"""#Direktori train and val"""

#train
train_plastic_dir = os.path.join(train_dir, 'plastic')
train_battery_dir = os.path.join(train_dir, 'battery')
train_cardboard_dir = os.path.join(train_dir, 'cardboard')
train_clothes_dir = os.path.join(train_dir, 'clothes')
train_biological_dir = os.path.join(train_dir, 'biological')
train_trash_dir = os.path.join(train_dir, 'trash')
train_whiteglass_dir = os.path.join(train_dir, 'white-glass')
train_paper_dir = os.path.join(train_dir, 'paper')
train_metal_dir = os.path.join(train_dir, 'metal')


# validation
validation_plastic_dir = os.path.join(validation_dir, 'plastic')
validation_battery_dir = os.path.join(validation_dir, 'battery')
validation_cardboard_dir = os.path.join(validation_dir, 'cardboard')
validation_clothes_dir = os.path.join(validation_dir, 'clothes')
validation_biological_dir = os.path.join(validation_dir, 'biological')
validation_trash_dir = os.path.join(validation_dir, 'trash')
validation_whiteglass_dir = os.path.join(validation_dir, 'white-glass')
validation_paper_dir = os.path.join(validation_dir, 'paper')
validation_metal_dir = os.path.join(validation_dir, 'metal')

"""# Augmentasi Image"""

import tensorflow as tf

from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_gen = ImageDataGenerator(
                    rescale=1./255,
                    rotation_range = 50,
                    horizontal_flip =True,
                    shear_range = 0.2,
                    zoom_range = 0.2,
                    fill_mode = 'nearest'
)

"""# Generator Image"""

train_generator = train_gen.flow_from_directory(
    train_dir,
    target_size = (150,150),
    class_mode = 'categorical',
    batch_size = 16,
    shuffle = True,
    seed=123
)

val_generator = train_gen.flow_from_directory(
    validation_dir,
    target_size = (150,150),
    class_mode = "categorical",
    batch_size = 16,
    shuffle = True,
    seed=123
)

"""# Modelling"""

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Activation, Dense, Flatten
from tensorflow.keras.layers import Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

"""## Sequential"""

model = Sequential([
    Conv2D(16, (3,3), activation='relu', input_shape=(150, 150, 3)),
    MaxPooling2D(3,3),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(3,3),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(3,3),
    Flatten(),
    Dense(512, activation='relu'),
    Dense(512, activation='relu'),
    Dense(512, activation='relu'),
    Dense(9, activation='softmax')
])

"""## Compile Optimizer"""

model.compile(
    loss='categorical_crossentropy',
    optimizer=Adam(),
    metrics=['accuracy']
)

"""## Callbacks"""

class callback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('accuracy') >= 0.92 and logs.get('val_accuracy') >= 0.92):  # berhenti training ketika accuracy diatas 92%
      print('\nFor Epoch', epoch, '\nAccuracy has reach = %2.2f%%' %(logs['accuracy']*100), 'finish training'),
      self.model.stop_training = False

callbacks = callback()

model.summary()

"""# Training"""

fitmodel = model.fit(
      train_generator,
      steps_per_epoch = 20,  
      epochs = 50, 
      validation_data = val_generator,  
      validation_steps= 25,  
      verbose=1,   
      callbacks = [callbacks]
)

"""# Plot Perbandingan"""

import matplotlib.pyplot as plt

"""## Accuracy"""

epochs = range(len(fitmodel.history['accuracy']))

plt.plot(epochs, fitmodel.history['accuracy'], label='Training Accuracy', color='blue')
plt.plot(fitmodel.history['val_accuracy'], label='Validation Accuracy', color='green')
plt.title('Perbandingan Ukuran Akurasi')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(loc=0)
plt.figure()

plt.show()

"""## Loss"""

plt.plot(epochs, fitmodel.history['loss'], label='Training Loss', color='blue')
plt.plot(epochs, fitmodel.history['val_loss'], label='Validation Loss', color = 'green')
plt.title('Loss Training & Validation')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(loc=0)
plt.figure()

plt.show()

"""# Deployment format TF-Lite"""

# Convert Model.
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the model.
with open('RPS_model.tflite', 'wb') as f:
  f.write(tflite_model)

