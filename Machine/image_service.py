from PIL import Image
from app import fe

def findSimilarImages(img):
    img = Image.open(img)
    
    # Pre-extracted features of Database Images
    features = fe.features

    # Extract features of Input Image
    feature = fe.extract(img)