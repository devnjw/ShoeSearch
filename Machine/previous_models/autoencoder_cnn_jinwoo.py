# -*- coding: utf-8 -*-
"""autoencoder_cnn_jinwoo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dyUDv7GnOqwMFt8Sdc8Ic94VyfNDm1zP
"""

import keras
from keras import layers
import tensorflow as tf
import numpy as np
import pandas as pd
import cv2, os
import matplotlib.pyplot as plt

input_img = keras.Input(shape=(224, 224, 1))
x = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(input_img)
x = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(x)
x = layers.MaxPooling2D((2, 2), strides=(2,2))(x)

x = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(x)
x = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(x)
x = layers.MaxPooling2D((2, 2), strides=(2,2))(x)

x = layers.Conv2D(256, (3, 3), activation='relu', padding='same')(x)
x = layers.Conv2D(256, (3, 3), activation='relu', padding='same')(x)
x = layers.Conv2D(256, (3, 3), activation='relu', padding='same')(x)
x = layers.MaxPooling2D((2, 2), strides=(2,2))(x)

x = layers.Conv2D(512, (3, 3), activation='relu', padding='same')(x)
x = layers.Conv2D(512, (3, 3), activation='relu', padding='same')(x)
x = layers.Conv2D(512, (3, 3), activation='relu', padding='same')(x)
x = layers.MaxPooling2D((2, 2), strides=(2,2))(x)

x = layers.Conv2D(512, (3, 3), activation='relu', padding='same')(x)
x = layers.Conv2D(512, (3, 3), activation='relu', padding='same')(x)
x = layers.Conv2D(512, (3, 3), activation='relu', padding='same')(x)
encoded = layers.MaxPooling2D((2, 2), strides=(2,2))(x)
print(encoded.shape)

# (7, 7, 512)

x = layers.Conv2D(512, (3, 3), activation='relu', padding='same')(encoded)
x = layers.Conv2D(512, (3, 3), activation='relu', padding='same')(x)
x = layers.Conv2D(512, (3, 3), activation='relu', padding='same')(x)
x = layers.UpSampling2D((2, 2))(x)

x = layers.Conv2D(512, (3, 3), activation='relu', padding='same')(x)
x = layers.Conv2D(512, (3, 3), activation='relu', padding='same')(x)
x = layers.Conv2D(512, (3, 3), activation='relu', padding='same')(x)
x = layers.UpSampling2D((2, 2))(x)

x = layers.Conv2D(256, (3, 3), activation='relu', padding='same')(x)
x = layers.Conv2D(256, (3, 3), activation='relu', padding='same')(x)
x = layers.Conv2D(256, (3, 3), activation='relu', padding='same')(x)
x = layers.UpSampling2D((2, 2))(x)

x = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(x)
x = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(x)
x = layers.UpSampling2D((2, 2))(x)

x = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(x)
x = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(x)
x = layers.UpSampling2D((2, 2))(x)
print(x.shape)

decoded = layers.Conv2D(1, (3, 3), activation='sigmoid', padding='same')(x)
print(decoded.shape)

autoencoder = keras.Model(input_img, decoded)
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')

from google.colab import drive
drive.mount('/content/drive')

cd /content/drive/MyDrive/shoogle/

# images = os.listdir("./dataset/")
# len(images)

def split(data, train_ratio=0.8):
  train_size = int(len(data)*train_ratio)
  test_size = len(data) - train_size

  train_data = data[:train_size]
  test_data = data[train_size:]
  
  return train_data, test_data

data = []

for i in range(1, 1000):
  if i%100 == 0:
    print(str(i))
  try:
    image = cv2.imread("./dataset/m" + str(i) + ".jpg")
    image = cv2.resize(image, (224, 224))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    data.append(image)
  except:
    print("No file name: ", i)

data = tf.expand_dims(data, 3)
data = np.array(data)

x_train, x_test = split(data)

x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.

print(x_train.shape)
print(x_test.shape)

# data = np.load('./data.npy')

# x_train, x_test = split(data)

# x_train = x_train.astype('float32') / 255.
# x_test = x_test.astype('float32') / 255.

# print(x_train.shape)
# print(x_test.shape)

"""## MNIST Data"""

# from keras.datasets import mnist
# import numpy as np

# (x_train, _), (x_test, _) = mnist.load_data()

# x_train = x_train.astype('float32') / 255.
# x_test = x_test.astype('float32') / 255.
# x_train = np.reshape(x_train, (len(x_train), 28, 28, 1))
# x_test = np.reshape(x_test, (len(x_test), 28, 28, 1))

from keras.callbacks import TensorBoard

autoencoder.fit(x_train, x_train,
                epochs=50,
                batch_size=8,
                shuffle=True,
                validation_data=(x_test, x_test)
                )

decoded_imgs = autoencoder.predict(x_test)

n = 20
plt.figure(figsize=(20, 4))
for i in range(1, n + 1):
    # Display original
    ax = plt.subplot(2, n, i)
    plt.imshow(x_test[i].reshape(224, 224))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # Display reconstruction
    ax = plt.subplot(2, n, i + n)
    plt.imshow(decoded_imgs[i].reshape(224, 224))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
plt.show()

def cos_sim(A, B):
    return np.dot(A, B) / (np.linalg.norm(A) * np.linalg.norm(B))

def l2_sim(A, B):
    return np.linalg.norm(A-B)

encoder = keras.Model(input_img, encoded)
encoded_imgs = encoder.predict(x_test)

print(l2_sim(encoded_imgs[9].reshape(25088), encoded_imgs[18].reshape(25088)))

plt.imshow(x_test[4].reshape(224, 224))
plt.imshow(x_test[10].reshape(224, 224))
plt.show()

# n = 10
# plt.figure(figsize=(20, 8))
# for i in range(1, n + 1):
#     ax = plt.subplot(1, n, i)
#     plt.imshow(encoded_imgs[i].reshape((7, 7 * 512)).T)
#     plt.gray()
#     ax.get_xaxis().set_visible(False)
#     ax.get_yaxis().set_visible(False)
# plt.show()