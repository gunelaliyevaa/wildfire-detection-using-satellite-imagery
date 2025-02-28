from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import tensorflow as tf

def train_model(model, train_generator, val_generator, epochs=20):
    """
    Train the model using early stopping and a learning rate scheduler.
    
    Parameters:
        model: Keras model to train.
        train_generator: Training data generator.
        val_generator: Validation data generator.
        epochs (int): Number of training epochs.
    
    Returns:
        History object from model.fit.
    """
    early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
    lr_scheduler = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2, min_lr=1e-6)
    
    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=epochs,
        callbacks=[early_stopping, lr_scheduler]
    )
    return history

def fine_tune_model(model, base_model, train_generator, val_generator, epochs=10, fine_tune_lr=1e-5):
    """
    Fine-tune the model by unfreezing the base model and training with a lower learning rate.
    
    Args:
        model: The previously trained Keras model.
        base_model: The base model whose layers will be unfrozen.
        train_generator: Training data generator.
        val_generator: Validation data generator.
        epochs (int): Number of fine-tuning epochs.
        fine_tune_lr (float): Learning rate for fine-tuning.
    
    Returns:
        History object from model.fit.
    """
    base_model.trainable = True
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=fine_tune_lr),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
    lr_scheduler = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2, min_lr=1e-6)
    
    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=epochs,
        callbacks=[early_stopping, lr_scheduler]
    )
    return history
