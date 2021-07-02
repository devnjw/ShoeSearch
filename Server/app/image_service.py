from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
import tensorflow as tf
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os

from app import fe

def init_tensor():
    config = tf.ConfigProto(
        device_count = {'GPU': 0}
    )
    sess = tf.Session(config=config)

# input: image
# output: similar image ids
def findSimilarImages(img):
    img = Image.open(img)
    
    features = fe.features
    print("Feature Map Shape: ")
    print(features.shape)

    # Extract its features
    query = fe.extract(img)

    # Calculate the similarity (distance) between images
    dists = np.linalg.norm(features - query, axis=1)

    # Extract 100 images that have lowest distance
    ids = np.argsort(dists)[:100] # Type: numpy.int64

    ids += 1

    print(ids)

    return ids