import os
import ee
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from lib.utils import download_image, save_image, generate_download_url

def get_satellite_collection(longitude, latitude, start_date, end_date,
                             collection = 'COPERNICUS/S2_SR_HARMONIZED',
                             buffer=0.02, bands=['B4', 'B3', 'B2']):
    """
    Retrieves a median composite satellite image for a given location and time range.

    The function filters a satellite image collection based on geographic bounds,
    date range, and cloud coverage. It normalizes pixel values and clips the images to a
    rectangular region around the specified coordinates.

    Args:
        longitude (float): Longitude of the fire event.
        latitude (float): Latitude of the fire event.
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        collection (str, optional): Earth Engine image collection to use. Defaults to
                                    'COPERNICUS/S2_SR_HARMONIZED'.
        buffer (float, optional): Buffer in degrees to define the rectangular bounding box.
                                  Defaults to 0.02.
        bands (list, optional): List of bands to select for visualization. Defaults to
                                ['B4', 'B3', 'B2'].

    Returns:
        ee.Image or None: The median composite satellite image clipped to the geometry
                          if available, otherwise None.
        ee.Geometry: The rectangular bounding box used for clipping.

    """
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
    """
    Processes a single fire event by retrieving satellite imagery and saving it.

    Workflow:
        1. **Extracting Event Details**:
           - Extracts longitude, latitude, and acquisition date (`acq_date`) from the fire data row.
           - These parameters define the geographical area and time window.

        2. **Defining the Time Window**:
           - A temporal window is set from one day before to one day after `acq_date` to ensure a sufficient observation period.

        3. **Satellite Collection Retrieval**:
           - Calls `get_satellite_collection` with extracted parameters to retrieve the relevant satellite images.

        4. **Generating the Image URL**:
           - Uses `generate_download_url` to obtain a downloadable image URL.

        5. **Downloading the Image**:
           - Calls `download_image` to fetch the image as bytes.

        6. **Saving the Image**:
           - Saves the image locally with a filename based on event coordinates and date using `save_image`.


    Args:
        row (pd.Series): A pandas Series containing fire event data with at least
                         'longitude', 'latitude', and 'acq_date' fields.
        output_dir (str): The directory where the downloaded image should be saved.

    Returns:
        str or None: The file path of the saved image if successful, otherwise None.

    Raises:
        Exception: Logs an error message if any issue occurs during processing.
    """
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
    """
    Processes a batch of fire events concurrently. Uses a thread pool to process multiple fire events simultaneously.

    Workflow:
        1. **Thread Pool Execution**:
           - Uses `ThreadPoolExecutor` from `concurrent.futures` to process multiple fire events in parallel.
           - The `max_workers` parameter controls the number of concurrent threads.

        2. **Submitting Tasks**:
           - Iterates over the fire event dataset (`fire_df`) and submits each row to `process_single_event` for processing.

        3. **Collecting Results**:
           - Uses `as_completed` to retrieve results as soon as they are available.
           - Each task processes a single event, and `result()` is used to collect the output.

        4. **Returning Processed Results**:
           - Returns a list containing file paths of successfully processed images or `None` for failed events.

    Args:
        fire_df (pd.DataFrame): DataFrame containing fire event data with columns
                                'longitude', 'latitude', and 'acq_date'.
        output_dir (str): Directory where downloaded images will be saved.
        max_workers (int, optional): The maximum number of concurrent threads.
                                     Defaults to 5.

    Returns:
        list: A list of file paths of successfully saved images, or None for failed events.
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(process_single_event, row, output_dir)
            for _, row in fire_df.iterrows()
        ]
        return [f.result() for f in as_completed(futures)]