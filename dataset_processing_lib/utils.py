import os
import requests

def generate_download_url(image, rectangle):
    """Generates a download URL for the processed image."""
    return image.getThumbURL({
        'min': 0,
        'max': 0.5,
        'dimensions': 512,
        'format': 'png',
        'bands': ['B4', 'B3', 'B2'],
        'region': rectangle
    })

def download_image(url):
    """Downloads an image from the given URL and returns the content as bytes."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Failed to download image: {e}")
        return None

def save_image(image_content, output_dir, filename):
    """Saves the given image content to the specified directory with the given filename."""
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