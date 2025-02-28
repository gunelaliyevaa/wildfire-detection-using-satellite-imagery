import os
import requests
import matplotlib.pyplot as plt

# Dataset Processing Utility Functions
def generate_download_url(image, rectangle):
    """
    Generates a thumbnail download URL for a satellite image.

    Creates a true-color RGB visualization (bands B4, B3, B2) using Earth Engine's
    rendering system. The generated URL provides temporary access to a 512px PNG
    preview of the specified geographic area.

    Args:
        image: An object representing the satellite image, which must have a
               `getThumbURL` method to produce a download URL.
        rectangle: A geographic region of interest, defined as a polygon or
                   bounding box, specifying the area to include in the thumbnail.

    Returns:
        str: A URL to download the generated thumbnail image (expires after ~2 hours).
    """
    return image.getThumbURL({
        'min': 0,
        'max': 0.5,
        'dimensions': 512,
        'format': 'png',
        'bands': ['B4', 'B3', 'B2'],
        'region': rectangle
    })

def download_image(url):
    """
    Downloads an image from a given URL.

    Sends an HTTP GET request to the specified URL to download
    image data. If the request is successful, the image content is returned.
    In cases of network or HTTP errors, an error message is logged and None
    is returned.
    
    Args:
        url (str): The URL of the image to be downloaded.
    
    Returns:
        bytes | None: The binary content of the image if the download is successful, or 
                      None if the download fails due to an exception or HTTP error.
                       
    Raises:
        RequestException: If there is a network-related or HTTP protocol error.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Failed to download image: {e}")
        return None

def save_image(image_content, output_dir, filename):
    """
    Save an image file to the specified directory with the provided filename.

    This function handles the creation of the output directory if it does not
    exist and writes the binary content of the image to disk. If the image content
    is None, the function skips processing. Any errors encountered during saving
    are logged.

    Args:
        image_content (bytes): The binary content of the image to be saved.
                               If None, the function skips processing.
        output_dir (str): The path to the directory where the image file should be saved. 
        filename (str): The desired name of the file (including extension) for the saved image.

    Raises:
        OSError:
            If there is a failure in writing the file or creating directories,
            an OSError exception is raised and logged.
    """
    if image_content is None:
        print(f"Skipping save: No content for {filename}")
        return

    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, filename)

    try:
        with open(file_path, 'wb') as f:
            f.write(image_content)
        print(f"Saved: {file_path}")
    except OSError as e:
        print(f"Failed to save {filename}: {e}")

# Model Training Utility Functions

def plot_training_history(history):
    """
    Plot training and validation accuracy from the training history.

    Args:
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

    Args:
        history: History object from fine-tuning.
    """
    plt.plot(history.history['accuracy'], label='Training Accuracy (Fine-tune)')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy (Fine-tune)')
    plt.legend()
    plt.title('Fine-Tuning Accuracy')
    plt.show()
