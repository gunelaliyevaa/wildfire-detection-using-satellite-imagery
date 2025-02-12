from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.models import Sequential

def build_model(input_shape=(350, 350, 3), dense_units=256, freeze_base=True):
    """
    Build and compile a model based on InceptionV3.
    
    Parameters:
        input_shape (tuple): Shape of the input images.
        dense_units (int): Number of neurons in the dense layer.
        freeze_base (bool): Whether to freeze the base model.
    
    Returns:
        tuple: (compiled model, base_model) where base_model is returned to enable later fine-tuning.
    """
    base_model = InceptionV3(weights='imagenet', include_top=False, input_shape=input_shape)
    base_model.trainable = not freeze_base
    
    model = Sequential([
        base_model,
        Flatten(),
        Dense(dense_units, activation='relu'),
        Dense(1, activation='sigmoid')  # For binary classification
    ])
    
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    return model, base_model
