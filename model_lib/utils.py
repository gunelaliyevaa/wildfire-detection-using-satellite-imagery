import matplotlib.pyplot as plt

def plot_training_history(history):
    """
    Plot training and validation accuracy from the training history.
    
    Parameters:
        history: History object returned by model.fit.
    """
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.legend()
    plt.title('Training and Validation Accuracy')
    plt.show()

def plot_fine_tuning_history(history):
    """
    Plot fine-tuning training and validation accuracy.
    
    Parameters:
        history: History object from fine-tuning.
    """
    plt.plot(history.history['accuracy'], label='Training Accuracy (Fine-tune)')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy (Fine-tune)')
    plt.legend()
    plt.title('Fine-Tuning Accuracy')
    plt.show()

def save_model(model, filepath):
    """
    Save the Keras model to the given file path.
    
    Parameters:
        model: Trained Keras model.
        filepath (str): File path to save the model.
    """
    model.save(filepath)
