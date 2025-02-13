import ee

def auth_earth_engine(project_id):
    """
    Authenticate and initialize Earth Engine.

    Parameters:
        project_id (str): Google Cloud project ID for Earth Engine.
    """
    ee.Authenticate()
    ee.Initialize(project=project_id)

def fetch_image_collection(longitude, latitude, start_date, end_date, buffer=0.02):
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
    rectangle = ee.Geometry.Rectangle([
        longitude - buffer,
        latitude - buffer,
        longitude + buffer,
        latitude + buffer
    ])
    collection = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
                  .filterBounds(rectangle)
                  .filterDate(start_date, end_date)
                  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 15))
                  .map(lambda img: img.divide(10000))) # Normalize
    return collection, rectangle










