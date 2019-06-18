from cloud_storage.__about__ import __version__
from cloud_storage.gcs_storage import GoogleCloudStorage

def create_storage_client(name):
    """
    Return new CloudStorage client

    Args:
        name
    """
    return GoogleCloudStorage()

def int_or_str(value):
    try:
        return int(value)
    except ValueError:
        return value

VERSION = tuple(map(int_or_str, __version__.split('.')))

__all__ = (
    '__version__',
    'VERSION',
    'create_storage_client',
    'GoogleCloudStorage',
)
