wildfire_modeling/preprocessing.py


# wildfire_modeling/preprocessing.py

import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array

def preprocess_image(image_path, target_size=(350, 350)):
    """
    Load and preprocess an image.
    
    Parameters:
        image_path (str): Path to the image file.
        target_size (tuple): Desired image size.
    
    Returns:
        numpy.ndarray: Preprocessed image ready for model prediction.
    """
    img = load_img(image_path, target_size=target_size)
    img_array = img_to_array(img) / 255.0  # Normalize pixel values
    return np.expand_dims(img_array, axis=0)
