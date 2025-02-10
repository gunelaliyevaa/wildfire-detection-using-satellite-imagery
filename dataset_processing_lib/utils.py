import ee

def earth_engine_init(project_id):
    """
    Authenticate and initialize Earth Engine.

    Parameters:
        project_id (str): Google Cloud project ID for Earth Engine.
    """
    ee.Authenticate()
    ee.Initialize(project=project_id)
