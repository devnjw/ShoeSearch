from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
from pathlib import Path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

class FeatureExtractor:
    def __init__(self):
        # Use VGG-16 as the architecture and ImageNet for the weight
        base_model = VGG16(weights='imagenet')
        # Customize the model to return features from fully-connected layer
        self.model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)

    def extract(self, img):
        # Resize the image
        img = img.resize((224, 224))
        # Convert the image color space
        img = img.convert('RGB')
        # Reformat the image
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        # Extract Features
        feature = self.model.predict(x)[0]
        return feature / np.linalg.norm(feature)

fe = FeatureExtractor()

# import os
# images = os.listdir("./dataset/")
# len(images)

# features = []
# img_paths = []

# # Save Image Feature Vector with Database Images
# for i in range(1, len(images)+1):
#   if i%500 == 0:
#     print(i)
#   try:
#     image_path = "./dataset/m" + str(i) + ".jpg"
#     img_paths.append(image_path)

#     # Extract Features
#     feature = fe.extract(img=Image.open(image_path))

#     features.append(feature)

#     # Save the Numpy array (.npy) on designated path
#     feature_path = "./features/m" + str(i) + ".npy"
#     np.save(feature_path, feature)
#   except Exception as e:
#     print('예외가 발생했습니다.', e)

# features = []
# img_paths = []

# # Save Image Feature Vector with Database Images
# for i in range(1, 3000):
#   if i%500 == 0:
#     print(i)
#   try:
#     image_path = "./dataset/m" + str(i) + ".jpg"
#     img_paths.append(image_path)

#     # Load Features
#     feature_path = "./features/m" + str(i) + ".npy"
#     feature = np.load(feature_path)
#     features.append(feature)
#   except Exception as e:
#     print('예외가 발생했습니다.', e)

features2 = np.load("./mFeatures.npy")
features2 = np.array(features2)
features2.shape

# feature_path = "./mFeatures.npy"
# np.save(feature_path, features)

# Insert the image query
# img = Image.open("./test_dataset/t1.jpeg")
img = Image.open("./dataset/m12.jpg")

# Extract its features
query = fe.extract(img)

# Calculate the similarity (distance) between images
dists = np.linalg.norm(features2 - query, axis=1)

# Extract 30 images that have lowest distance
ids = np.argsort(dists)[:30]

scores = [(dists[id], img_paths[id], id) for id in ids]
# Visualize the result
axes=[]
fig=plt.figure(figsize=(8,8))
for a in range(5*6):
    score = scores[a]
    axes.append(fig.add_subplot(5, 6, a+1))
    subplot_title=str(round(score[0],2)) + "/m" + str(score[2]+1)
    axes[-1].set_title(subplot_title)
    plt.axis('off')
    plt.imshow(Image.open(score[1]))
fig.tight_layout()
plt.show()
