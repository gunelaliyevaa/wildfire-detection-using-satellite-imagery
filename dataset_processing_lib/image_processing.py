import os
import ee
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from .earth_engine import fetch_image_collection


def process_image(collection, rectangle):
    """
    Processes the image collection by selecting RGB bands and clipping.

    Parameters:
        collection (ee.ImageCollection): The image collection.
        rectangle (ee.Geometry.Rectangle): The region to clip.

    Returns:
        ee.Image or None: Processed image if available; otherwise, None.
    """
    if collection.size().getInfo() > 0:
        return collection.median().select(['B4', 'B3', 'B2']).clip(rectangle)
    return None

def generate_download_url(image, rectangle):
    """
    Generates a download URL for the processed image.

    Parameters:
        image (ee.Image): Processed image.
        rectangle (ee.Geometry.Rectangle): The region used for image generation.

    Returns:
        str: Download URL for the image.
    """
    return image.getThumbURL({
        'min': 0,
        'max': 0.5,
        'dimensions': 512,
        'region': rectangle,
        'format': 'png'
    })

def download_image(url, output_dir, filename):
    """
    Downloads an image from the given URL and saves it.

    Parameters:
        url (str): URL of the image.
        output_dir (str): Directory where the image will be saved.
        filename (str): Name of the file.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        file_path = os.path.join(output_dir, filename)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Downloaded: {file_path}")
    except Exception as e:
        print(f"Failed to download image {filename}: {e}")

def process_fire_event(row, output_dir):
    """
    Processes a single fire event and downloads the corresponding image.

    Parameters:
        row (pd.Series): A row from the fire event data.
        output_dir (str): Directory where the image will be saved.
    """
    latitude, longitude = row['latitude'], row['longitude']
    acq_date = pd.to_datetime(row['acq_date'])

    start_date = (acq_date - pd.DateOffset(days=1)).strftime('%Y-%m-%d')
    end_date = (acq_date + pd.DateOffset(days=1)).strftime('%Y-%m-%d')

    collection, rectangle = fetch_image_collection(longitude, latitude, start_date, end_date)
    image = process_image(collection, rectangle)
    if image:
        url = generate_download_url(image, rectangle)
        filename = f"{latitude}_{longitude}.png"
        download_image(url, output_dir, filename)

def process_fire_events_concurrently(fire_df, output_dir, max_workers=5):
    """
    Processes fire events concurrently using a thread pool.

    Parameters:
        fire_df (pd.DataFrame): DataFrame containing fire event data.
        output_dir (str): Directory to save downloaded images.
        max_workers (int): Maximum number of concurrent threads.
    """
    os.makedirs(output_dir, exist_ok=True)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_fire_event, row, output_dir)
                   for _, row in fire_df.iterrows()]
        for future in as_completed(futures):
            future.result()