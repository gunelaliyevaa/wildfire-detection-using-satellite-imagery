import os
import ee
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from .preprocessor import create_rectangle, mask_s2_clouds


def fetch_image_collection(longitude, latitude, start_date, end_date):
    """
    Fetch the Sentinel-2 image collection for a given fire event.

    Parameters:
        longitude (float): Longitude coordinate of the fire event.
        latitude (float): Latitude coordinate of the fire event.
        start_date (str): Start date (format 'YYYY-MM-DD').
        end_date (str): End date (format 'YYYY-MM-DD').

    Returns:
        tuple: (ee.ImageCollection, ee.Geometry.Rectangle)
    """
    rectangle = create_rectangle(longitude, latitude)
    collection = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
                  .filterBounds(rectangle)
                  .filterDate(start_date, end_date)
                  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
                  .map(mask_s2_clouds))
    return collection, rectangle


def download_image_from_event(row, output_dir):
    """
    Generate and download an image for a specific fire event.

    Parameters:
        row (pandas.Series): A row from the fire event DataFrame.
        output_dir (str): Directory where the image will be saved.
    """
    latitude, longitude = row['latitude'], row['longitude']
    start_date = pd.to_datetime(row['acq_date']).strftime('%Y-%m-%d')
    # Fetch one day after the acquisition date
    end_date = (pd.to_datetime(start_date) + pd.DateOffset(days=1)).strftime('%Y-%m-%d')

    collection, rectangle = fetch_image_collection(longitude, latitude, start_date, end_date)

    # Check if any images were found
    if collection.size().getInfo() > 0:
        # Generate an image by taking the median and selecting RGB bands, then clip it to the region
        image = collection.median().select(['B4', 'B3', 'B2']).clip(rectangle)

        # Generate a download URL for the image thumbnail
        url = image.getThumbURL({
            'min': 0,
            'max': 0.5,
            'dimensions': 512,
            'region': rectangle,
            'format': 'png'
        })

        # Download and save the image
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            filename = os.path.join(output_dir, f"{latitude}_{longitude}.png")
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Downloaded: {filename}")
        except Exception as e:
            print(f"Failed to download image for {latitude}, {longitude}: {e}")
    else:
        print(f"No images found for {latitude}, {longitude} between {start_date} and {end_date}")


def download_fire_images_concurrently(fire_df, output_dir, max_workers=5):
    """
    Process fire events concurrently and download images.

    Parameters:
        fire_df (pandas.DataFrame): DataFrame containing fire event data.
        output_dir (str): Directory where images will be saved.
        max_workers (int): Maximum number of concurrent threads.
    """
    os.makedirs(output_dir, exist_ok=True)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(download_image_from_event, row, output_dir)
                   for _, row in fire_df.iterrows()]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error processing a fire event: {e}")
