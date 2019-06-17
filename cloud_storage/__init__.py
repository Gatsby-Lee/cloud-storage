from cloud_storage.gcs_storage import GoogleCloudStorage

__version__ = '1.1.0'
VERSION = tuple(map(int_or_str, __version__.split('.')))

__all__ = (
    'GoogleCloudStorage',
)
