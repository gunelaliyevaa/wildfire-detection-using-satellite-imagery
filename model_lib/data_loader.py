wildfire_modeling/data_loader.py

# wildfire_modeling/data_loader.py

import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def count_images_in_directory(directory):
    """
    Count the number of images in a directory.
    
    Parameters:
        directory (str): The path to the directory.
        
    Returns:
        int: Number of files in the directory.
    """
    return len(os.listdir(directory))

def create_data_generators(base_dir, target_size=(350, 350), batch_size=32, validation_split=0.2):
    """
    Create training and validation data generators from a directory.
    
    Parameters:
        base_dir (str): Base directory containing the dataset.
        target_size (tuple): Desired image size.
        batch_size (int): Number of images per batch.
        validation_split (float): Fraction of data reserved for validation.
    
    Returns:
        tuple: (train_generator, validation_generator)
    """
    datagen = ImageDataGenerator(
        rescale=1.0/255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        validation_split=validation_split
    )
    
    train_generator = datagen.flow_from_directory(
        base_dir,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='binary',
        subset='training'
    )
    
    val_generator = datagen.flow_from_directory(
        base_dir,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='binary',
        subset='validation'
    )
    
    return train_generator, val_generator
