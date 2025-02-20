import os
import ee
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from .utils import download_image, save_image, generate_download_url

def get_satellite_collection(longitude, latitude, start_date, end_date, collection = 'COPERNICUS/S2_SR_HARMONIZED', buffer=0.02, bands=['B4', 'B3', 'B2']):
    """Fetches Sentinel-2 images for the given location and date range."""
    geometry = ee.Geometry.Rectangle([
        longitude - buffer,
        latitude - buffer,
        longitude + buffer,
        latitude + buffer
    ])

    filtered_collection = (ee.ImageCollection(collection)
                           .filterBounds(geometry)
                           .filterDate(start_date, end_date)
                           .filterMetadata('CLOUDY_PIXEL_PERCENTAGE', 'less_than', 10)
                           .map(lambda img: img.divide(10000)))  # Normalize
    if filtered_collection.size().getInfo() == 0:
        return None, None

    return filtered_collection.median().select(bands).clip(geometry), geometry

def process_single_event(row, output_dir):
    """Processes a single fire event and downloads the corresponding image."""
    try:
        longitude, latitude = row['longitude'], row['latitude']
        acq_date = pd.to_datetime(row['acq_date'])

        start_date = (acq_date - pd.DateOffset(days=1)).strftime('%Y-%m-%d')
        end_date = (acq_date + pd.DateOffset(days=1)).strftime('%Y-%m-%d')

        image, geometry = get_satellite_collection(
            longitude=longitude,
            latitude=latitude,
            start_date=start_date,
            end_date=end_date,
        )

        if not image:
            return None

        filename = f"{row['latitude']}_{row['longitude']}_{acq_date.date()}.png"
        output_path = os.path.join(output_dir, filename)

        url = generate_download_url(image, geometry)
        image_content = download_image(url) # bytes

        if image_content:
            save_image(image_content, output_dir, filename)
            return output_path

        return None

    except Exception as e:
        print(f"Error processing event: {str(e)}")
        return None

def process_event_batch(fire_df, output_dir, max_workers=5):
    """Processes fire events concurrently using a thread pool."""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(process_single_event, row, output_dir)
            for _, row in fire_df.iterrows()
        ]
        return [f.result() for f in as_completed(futures)]