import ee

def create_rectangle(longitude, latitude, buffer=0.02):
    """
    Create a rectangular geometry around the given coordinates.

    Parameters:
        longitude (float): Longitude of the center point.
        latitude (float): Latitude of the center point.
        buffer (float): Buffer size to extend the rectangle (default is 0.02).

    Returns:
        ee.Geometry.Rectangle: The generated rectangle geometry.
    """
    return ee.Geometry.Rectangle([longitude - buffer,
                                  latitude - buffer,
                                  longitude + buffer,
                                  latitude + buffer])

def mask_s2_clouds(image):
    """
    Mask clouds from Sentinel-2 images using the QA60 band.

    Parameters:
        image (ee.Image): The input Sentinel-2 image.

    Returns:
        ee.Image: Cloud-masked image, scaled appropriately.
    """
    qa = image.select('QA60')
    cloud_bit_mask = 1 << 10
    cirrus_bit_mask = 1 << 11
    mask = qa.bitwiseAnd(cloud_bit_mask).eq(0).And(qa.bitwiseAnd(cirrus_bit_mask).eq(0))
    return image.updateMask(mask).divide(10000)
